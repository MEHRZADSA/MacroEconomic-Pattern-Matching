from dtaidistance import dtw
from dtaidistance import dtw_visualisation as dtwvis
import numpy as np


class PlotingofDTW ():
    def __init__(self,x,y,Variable = False):
        
        self.x = x
        self.y = y
        self.Variable = Variable
    
    def compute_euclidean_distance_matrix(self,x,y) -> np.array:
        """Calculate distance matrix
        This method calcualtes the pairwise Euclidean distance between two sequences.
        The sequences can have different lengths.
    
        """
        dist = np.zeros((len(y), len(x)))
        for i in range(len(y)):
            for j in range(len(x)):
                dist[i,j] = (x[j]-y[i])**2
        return (dist)


    def compute_accumulated_cost_matrix(self,x, y):
        
        distances = self.compute_euclidean_distance_matrix(x,y)

        # Initialization
        cost = np.zeros((len(y), len(x)))
        cost[0,0] = distances[0,0]
    
        for i in range(1, len(y)):
            cost[i, 0] = distances[i, 0] + cost[i-1, 0]  
        
        for j in range(1, len(x)):
            cost[0, j] = distances[0, j] + cost[0, j-1]  

        # Accumulated warp path cost
        for i in range(1, len(y)):
            for j in range(1, len(x)):
                cost[i, j] = min(
                cost[i-1, j],    # insertion
                cost[i, j-1],    # deletion
                cost[i-1, j-1]   # match
                ) + distances[i, j] 
            
        return (cost)


    def Plotting (self):
        
   
        cost_matrix = self.compute_accumulated_cost_matrix(self.x , self.y)
        d, paths = dtw.warping_paths(self.x, self.y, window=20, use_pruning=True )
        best_path = dtw.best_path(paths)
        if self.Variable:
            return (best_path,d)
        else:
            return dtwvis.plot_warpingpaths(self.x, self.y, paths, best_path,shownumbers=False,showlegend=True)
        
