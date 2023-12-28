import subprocess
from .gcn_utilis import  setup_graph
from .CPO_utils import get_neighbors, auto_resolution
from .utils import saveRep,get_all_adj_adata,mergeAdata,updateAttributes,get_data_file_path
from .buildGraph import getandUpadateEdges
import gc
import scanpy as sc
import numpy as np
import os
from .processIDREM import getClusterPaths, getClusterIdrem, runIdrem
from .processTFs import getTFs, getTargetGenes, matchTFandTGWithFoldChange, updataGeneTablesWithDecay
from sklearn.neighbors import kneighbors_graph
from scipy.sparse import csr_matrix
class UNAGI_runner():
    def __init__(self,data_path,total_stage,iteration,trainer,idrem_dir):
        super(UNAGI_runner, self).__init__()
        self.data_path = data_path
        self.total_stage = total_stage
        self.iteration = iteration
        self.trainer = trainer
        self.resolutions = None
        self.idrem_dir = idrem_dir
        self.neighbor_parameters = None
        self.setup_CPO = False
        self.species = None
        self.setup_IDREM = False
    def load_stage_data(self):
        stageadata = []
        for i in range(self.total_stage):
            if self.iteration != 0:
                adata = sc.read(os.path.join(self.data_path, '%d/stagedata/%d.h5ad'%(self.iteration-1,i)))
            elif self.iteration == 0:
                adata = sc.read(os.path.join(self.data_path, '%d.h5ad'%(i)))
            if 'leiden_colors' in adata.uns:
                del adata.uns['leiden_colors']
            stageadata.append(adata)
        self.all_in_one = get_all_adj_adata(stageadata)
        self.adata_stages = stageadata
        
    def annotate_stage_data(self, adata,stage):
        z_locs, z_scales, cell_embeddings = self.trainer.get_latent_representation(adata,self.iteration,self.data_path)
        adata.obsm['z'] = cell_embeddings
        if self.neighbor_parameters is None:
            sc.pp.neighbors(adata, use_rep="z",n_neighbors=50,method='umap')
            return adata
        if 'connectivities' in adata.obsp.keys():
            del adata.obsp['connectivities']
            del adata.obsp['distances']
        z_adj = kneighbors_graph(adata.obsm['z'], self.neighbor_parameters[stage], mode='connectivity', include_self=True,n_jobs=20)
        adata.obsp['connectivities'] = z_adj
        adata.obsp['distances'] = kneighbors_graph(adata.obsm['z'], self.neighbor_parameters[stage], mode='distance', include_self=True,n_jobs=20)
        sc.tl.leiden(adata,resolution = self.resolutions[stage])
        sc.tl.paga(adata)
        sc.pl.paga(adata,show=False)
        # sc.tl.umap(adata, min_dist=0.25/self.resolution_coefficient*len(adata),init_pos='paga')
        sc.tl.umap(adata, min_dist=0.05,init_pos='paga')
        rep=[z_locs, z_scales]
        adata.obs['ident'] = 'None'
        adata.obs['leiden'] = adata.obs['leiden'].astype(str)
        sc.pl.umap(adata,color='leiden',show=False)
        adata,averageValue,reps = updateAttributes(adata,rep)#add top genes, cell types attributes and get average cluster value
  
        adata.obs['leiden']=adata.obs['leiden'].astype(str)
        if self.iteration == 0:
            allzeros = np.zeros_like(adata.X)
            allzeros = csr_matrix(allzeros)
            adata.layers['geneWeight'] = allzeros
        sc.pl.umap(adata,color='ident',show=False)
        adata.write(os.path.join(self.data_path,str(self.iteration)+'/stagedata/%d.h5ad'%stage),compression='gzip',compression_opts=9)
        return adata,averageValue,reps
    
    def set_up_CPO(self, anchor_neighbors, max_neighbors, min_neighbors, resolution_min, resolution_max):
        self.setup_CPO = True
        self.anchor_neighbors = anchor_neighbors
        self.max_neighbors = max_neighbors
        self.min_neighbors = min_neighbors
        self.resolution_min = resolution_min
        self.resolution_max = resolution_max

    def run_CPO(self):
        max_adata_cells = 0
        num_cells = []
        for each in self.adata_stages:
            num_cells.append(each.shape[0])
            if len(each) > max_adata_cells:
                max_adata_cells = len(each)
        self.resolution_coefficient = max_adata_cells
        for i in range(0,len(self.adata_stages)):
            self.adata_stages[i] = self.annotate_stage_data(self.adata_stages[i], i)
        if not self.setup_CPO:
            print('CPO parameters are not set up, using default parameters')
            print('anchor_neighbors: 15, max_neighbors: 35, min_neighbors: 10, resolution_min: 0.8, resolution_max: 1.5')
            self.neighbor_parameters, anchor_index = get_neighbors(self.adata_stages, num_cells,anchor_neighbors=15,max_neighbors=35,min_neighbors=10)
            self.resolutions,_ = auto_resolution(self.adata_stages, anchor_index, self.neighbor_parameters, 0.8, 1.5)
        else:
            self.neighbor_parameters, anchor_index = get_neighbors(self.adata_stages, num_cells,anchor_neighbors=self.anchor_neighbors,max_neighbors=self.max_neighbors,min_neighbors=self.min_neighbors)
            self.resolutions,_ = auto_resolution(self.adata_stages, anchor_index, self.neighbor_parameters, self.resolution_min, self.resolution_max)
    
    def update_cell_attributes(self):
        self.averageValues = []
        reps = []
        for i in range(0,len(self.adata_stages)):
            adata = self.adata_stages[i]
            # print(adata.X.shape)
            adata.uns['topGene']={}
            adata.uns['clusterType']={}
            adata.uns['rep']={}
            adata,averageValue,rep = self.annotate_stage_data(adata,i)
            gc.collect()
            reps.append(rep)
            averageValue = np.array(averageValue)
            self.averageValues.append(averageValue)
        self.averageValues = np.array(self.averageValues,dtype=object)
        np.save(os.path.join(self.data_path, '%d/averageValues.npy'%self.iteration),self.averageValues)
        saveRep(reps,self.data_path,self.iteration)
    def build_temporal_dynamics_graph(self):
        self.edges = getandUpadateEdges(self.total_stage,self.data_path,self.iteration)
    def set_up_IDREM(self,Minimum_Absolute_Log_Ratio_Expression, Convergence_Likelihood, Minimum_Standard_Deviation):
        self.setup_IDREM = True
        self.Minimum_Absolute_Log_Ratio_Expression = Minimum_Absolute_Log_Ratio_Expression
        self.Convergence_Likelihood = Convergence_Likelihood
        self.Minimum_Standard_Deviation = Minimum_Standard_Deviation
    def register_species(self, species):
        print('Species is registered as %s'%species)
        self.species = species
    def run_IDREM(self):
        averageValues = np.load(os.path.join(self.data_path, '%d/averageValues.npy'%self.iteration),allow_pickle=True)
        paths = getClusterPaths(self.edges,self.total_stage)
        idrem= getClusterIdrem(paths,averageValues,self.total_stage)
        paths = [each for each in paths.values() if len(each) == self.total_stage]
        # print(paths) 
        idrem = np.array(idrem)
        self.genenames =np.array(list(self.adata_stages[0].var.index.values))
        if not self.setup_IDREM:
            print('IDREM parameters are not set up, using default parameters')
            print('Minimum_Absolute_Log_Ratio_Expression: 0.5, Convergence_Likelihood: 0.001, Minimum_Standard_Deviation: 0.5')
            if self.species is None:
                print('Human species is used as default')
                runIdrem(paths,self.data_path,idrem,self.genenames,self.iteration,self.idrem_dir)
            else:
                runIdrem(paths,self.data_path,idrem,self.genenames,self.iteration,self.idrem_dir,species=self.species)
        else:
            if self.species is None:
                print('Human species is used as default')
                runIdrem(paths,self.data_path,idrem,self.genenames,self.iteration,self.idrem_dir,Minimum_Absolute_Log_Ratio_Expression=self.Minimum_Absolute_Log_Ratio_Expression, Convergence_Likelihood=self.Convergence_Likelihood, Minimum_Standard_Deviation=self.Minimum_Standard_Deviation)
            else:
                runIdrem(paths,self.data_path,idrem,self.genenames,self.iteration,self.idrem_dir,species=self.species,Minimum_Absolute_Log_Ratio_Expression=self.Minimum_Absolute_Log_Ratio_Expression, Convergence_Likelihood=self.Convergence_Likelihood, Minimum_Standard_Deviation=self.Minimum_Standard_Deviation)
            
    def update_gene_weights_table(self,topN=100):
        TFs = getTFs(os.path.join(self.data_path,str(self.iteration)+'/'+'idremResults'+'/'))
        scope = getTargetGenes(os.path.join(self.data_path,str(self.iteration)+'/'+'idremResults'+'/'),topN)
        p = matchTFandTGWithFoldChange(TFs,scope,self.averageValues,get_data_file_path('human_encode.txt'),self.genenames)
        #np.save('../data/mes/'+str(iteration)+'/tfinfo.npy',np.array(p))
        updateLoss = updataGeneTablesWithDecay(self.data_path,str(self.iteration),p,self.total_stage)
    def build_iteration_dataset(self):
        mergeAdata(os.path.join(self.data_path,str(self.iteration)))
       
    def run(self):
        self.load_stage_data()
        if self.iteration == 0:
            is_iterative = False
        else:
            is_iterative = True
        self.trainer.train(self.all_in_one,self.iteration,target_dir=self.data_path,is_iterative=is_iterative)
        self.run_CPO()
        self.update_cell_attributes()
        self.build_temporal_dynamics_graph()
        self.run_IDREM()
        self.update_gene_weights_table()
        self.build_iteration_dataset()


