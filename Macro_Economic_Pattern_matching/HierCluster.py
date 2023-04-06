import numpy as np
from yellowbrick.cluster import KElbowVisualizer
from sklearn.cluster import AgglomerativeClustering
from scipy.cluster.hierarchy import dendrogram, linkage
import matplotlib.pyplot as plt





class HierClustering ():
    def __init__(self, Data, Variable=False , Ploting=False):
        
        self.Variable = Variable
        self.Data = Data
        self.Ploting = Ploting
        
    #def (self,)
        
        
    def FindingOptimalNum (self):
        """"
        it helps to find the optimal number of cluster by using GAP METHOD
        It uses a statistical test based on the difference between the within-cluster dispersion 
        and a reference distribution to select the optimal number of clusters
        """
        
        visualizer = KElbowVisualizer(AgglomerativeClustering(affinity = 'euclidean', linkage = 'ward'), k=(1, 10))
        visualizer.fit(self.Data)
        return (visualizer)
    
    def Hier (self):
        
        visualizer = self.FindingOptimalNum()
        NumbofClass = visualizer.elbow_value_
        plt.show()
        
        if self.Variable:
            plt.figure(figsize=(10, 5), dpi=300)
            linkage_data = linkage(self.Data, method='ward',)
            dendrogram(linkage_data, leaf_rotation=90, leaf_font_size=1, labels=self.Data.columns)
            plt.axhline(y=0.65, c='grey', lw=2, linestyle='dashed')
            plt.ylabel('Euclidean distances')
            plt.title('Dendrogram')
            plt.xlabel("Name of Stocks")
            plt.legend()
            plt.savefig('Dendrogram.png')
            plt.show()
        
        Agg_hc = AgglomerativeClustering(n_clusters = NumbofClass+1, affinity = 'euclidean', linkage = 'ward')
        y_hc = Agg_hc.fit_predict(self.Data)
        
        
        if self.Ploting:
            Range = np.arange(1 ,10)
            plt.plot(Range,visualizer.k_scores_,marker="D")
            plt.axvline(visualizer.elbow_value_+1, color = 'black', linestyle = '-.',label = "GAP Method at k {}, Score = {}".format(NumbofClass+1,visualizer.k_scores_[NumbofClass]))
            plt.plot(Range[visualizer.elbow_value_],visualizer.k_scores_[visualizer.elbow_value_] ,marker="o", markersize=10, markeredgecolor="black", markerfacecolor="green")
            plt.ylabel('Distortion Scores')
            plt.title ('Distortion Score for Hierarchical Clustering')
            plt.grid(True)
            plt.legend()
            plt.savefig('Elbo.png')
            plt.show()
            
            
        NameofStocks = list(self.Data.columns)
        for i in range(NumbofClass+1):
            globals()['Cluster'+str(i)]=list()
            
        for i,j in enumerate(y_hc):
            globals()['Cluster'+str(j)].append(NameofStocks[i])
            
        DictofClustered = dict()
        for i in range(NumbofClass+1):
            DictofClustered['Cluster'+str(i)] = globals()['Cluster'+str(i)]
        
            
        
        return (DictofClustered, y_hc, NumbofClass+1)