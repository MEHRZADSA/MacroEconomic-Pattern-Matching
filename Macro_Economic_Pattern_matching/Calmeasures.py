import numpy as np
import pandas as pd
from tqdm import tnrange
import math
import scipy.stats as ss 
from sklearn.metrics import mutual_info_score
from sklearn.feature_selection import mutual_info_regression




class Measures:
    def __init__(self, Dict, Metric, Saving=False):
        """"
        the Measure should be COR or MUTUAL

        """

        self.Dict = Dict
        self.Metric = Metric
        self.Saving = Saving
    
    def Corcal (self,Dict): 
        '''
        calculation corrolation for a Dictionary whom keys is Name of stocks and values of keys is Adj Close

        '''

        NameofStocks = list(Dict.keys()) #creating for name of stocks
        #LenofData = len(Dict[NameofStocks[0]])
        CorMatrix = np.zeros((len(NameofStocks),len(NameofStocks))) #creating a matrix whom values is zero with equal dimention
        CorDataframe = pd.DataFrame(CorMatrix, columns=NameofStocks, index=NameofStocks) # turning oue zero matiox to a dataframe
        for i in tnrange(len(NameofStocks),desc='1st loop'):# going through the col 
            for j in range(len(NameofStocks)):# going through the rows 
                a1=NameofStocks[i]
                a2=NameofStocks[j]
                if CorDataframe[a2][a1] != 0: #since our matrix is symmetric, symmetrical value is checked and if >0 the value would replace
                    CorDataframe[a1][a2] =CorDataframe[a2][a1]
                else:
                    CorNum =np.corrcoef(Dict[a1],Dict[a2])[0][1]
                    CorDataframe[a1][a2] = CorNum
        return(CorDataframe)
    
    def MutualInfFormula(self, X, Y, bins):
        
        
        cXY=np.histogram2d(np.reshape(np.array(X), (len(X))),
                  np.reshape(np.array(Y), (len(X)))
                  ,round(bins))[0]
        Hx=ss.entropy(np.histogram(np.reshape(np.array(X), (len(X))), round(bins))[0])
        Hy=ss.entropy(np.histogram(np.reshape(np.array(Y), (len(X))), round(bins))[0])
        iXY=mutual_info_score(None,None,contingency=cXY)
        iXYn=iXY/min(Hx,Hy)
        
        return(iXYn)
    
    def CalMutualInf (self, DictofAdj):
        '''
        to calculate mutual information number of bins is need
        '''
        NameofStocks = list(DictofAdj.keys()) #creating for name of stocks

        LenofWeeks = len(DictofAdj[NameofStocks[0]])

        Bin=(8+(32*LenofWeeks)+(12*math.sqrt(36*LenofWeeks+(12*LenofWeeks**2))))**1/3
        MutualMatrix = np.zeros((len(NameofStocks),len(NameofStocks)))
        MutualDataframe = pd.DataFrame(MutualMatrix, columns=NameofStocks, index=NameofStocks)
        for i in tnrange(len(NameofStocks),desc='1st loop'):
            for j in range(len(NameofStocks)):
                a1=NameofStocks[i]
                a2=NameofStocks[j]
                if MutualDataframe[a2][a1] != 0:
                    MutualDataframe[a1][a2] = MutualDataframe[a2][a1]
                else:
                    MutualNum = self.MutualInfFormula(DictofAdj[a1],DictofAdj[a2],Bin)
                    MutualDataframe[a1][a2] = MutualNum
        return(MutualDataframe)
    
    def entropy(self, x, base):
        """Calculates the entropy of a series."""
        _, counts = np.unique(x, return_counts=True)
        probs = counts / len(x)
        return -np.sum(probs * np.log(probs) / np.log(base))
    
       
    
    
    def CalGPUMutualInf (self, DictofAdj):
        '''
        to calculate mutual information number of bins is need
        '''
        NameofStocks = list(DictofAdj.keys()) #creating for name of stocks


        MutualMatrix = np.zeros((len(NameofStocks),len(NameofStocks)))
        MutualDataframe = pd.DataFrame(MutualMatrix, columns=NameofStocks, index=NameofStocks)
        for i in tnrange(len(NameofStocks),desc='1st loop'):
            for j in range(len(NameofStocks)):
                a1=NameofStocks[i]
                a2=NameofStocks[j]
                if MutualDataframe[a2][a1] != 0:
                    MutualDataframe[a1][a2] = MutualDataframe[a2][a1]
                else:
                    x= DictofAdj[a1]
                    y = DictofAdj[a2]
                    MutualNum =  mutual_info_regression(X=np.array([x]).T, y=y, n_neighbors=3)
                    normalized_mi = MutualNum / min(self.entropy(x, base=2) ,self.entropy(y, base=2))
                    MutualDataframe[a1][a2] = normalized_mi
                    
        return(MutualDataframe)
    
    
    
    

    def CalCulate(self):

        if self.Metric == 'COR':# detrmining which metric must use and deciding wheater save it or otherwise
            if self.Saving:
                Cor = self.Corcal(self.Dict)
                Cor.to_csv("Cor.CSV")
                return(Cor)
                
            else:
                return(self.Corcal(self.Dict))
            
        
        
        
        if self.Metric == 'MUTUAl' :
            if self.Saving:
                MutualInf = self.CalMutualInf(self.Dict)
                MutualInf.to_csv("MutualInf.CSV")
                return (MutualInf)
            
            else:
                return (self.CalMutualInf(self.Dict))
            
            
            
            
        if self.Metric == 'MUTUAlGPU' :
            if self.Saving:
                MutualInf = self.CalGPUMutualInf(self.Dict)
                MutualInf.to_csv("MutualInf.CSV")
                return (MutualInf)
            
            else:
                return (self.CalGPUMutualInf(self.Dict))
        
        else:
            print(" the input variable as measure is not supported, it must be 'MUTUAL', 'COR', or 'MUTUAlGPU")
