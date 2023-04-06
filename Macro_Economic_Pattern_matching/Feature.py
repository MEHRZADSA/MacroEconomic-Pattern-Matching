import numpy as np
import pandas as pd
import talib as ta





class CreatingFeatures ():
    def __init__(self,  DictofStocks, Lag = 7):
        """
        the inpute is Dict of Variables which can be obtained from Downloding data
        
        """
        
        self.Lag = Lag
        self.DictofStocks = DictofStocks
        
    def Features(self):
        
        DictofAdj = dict()
        DictofVol = dict()
        DictofSha = dict()
        DictofRsi = dict()
        DictofRet = dict()
        
        
        for i in list(self.DictofStocks.keys()):
            """  
            seprating Adj close then truning to weekly based on mean 
            and get value as a numpy
            
            
            Calculating features for importing as a variable 
            
            Returning : first variable is Dict of Adj close of stocks
            
                        second is Dict of Volume
                        
                        third is Dict of Sharp Ratio
                        
                        Fourth is Dict of Rsi
                        
                        Fifth is Dict of Ret
                        
                        last one is Time 
                        
                        Due to lag of rsi we eliminate a part of data
                
            """
                
            DictofAdj[i] = self.DictofStocks[i].resample("W").\
            mean()['Adj Close'].values[self.Lag:]
                
                
            DictofVol[i] = self.DictofStocks[i].resample("W").\
            mean()['Volume'].values[self.Lag:]
            
            ListofR = self.DictofStocks[i].resample("W").mean().\
            pct_change()['Adj Close'].values[self.Lag:]
            
            
            ListofS = self.DictofStocks[i].pct_change()
            ListofS = ListofS.resample("W").std()['Adj Close'].values[self.Lag:]
            ListofS = np.divide(ListofR, ListofS)
            DictofSha[i] = ListofS
            
            ListofP = self.DictofStocks[i].resample("W").mean()['Adj Close'].values
            DictofRsi[i] = ta.RSI(ListofP, self.Lag)[self.Lag:]
            
            
            DictofRet[i] =self.DictofStocks[i].resample("W").\
            mean().pct_change()['Adj Close'].values[self.Lag:]
        name= list(self.DictofStocks.keys())
        Time = self.DictofStocks[name[0]].resample("W").mean().index[self.Lag:]
        
            
        return (DictofAdj,
                     DictofVol,
                      DictofSha,
                       DictofRsi,
                        DictofRet,
                         Time)
    
    
    
    def Capm(self, Index, Start, End):
        
        
        IndexP = yf.download(Index, start = Start, end = End)
        
        DictofCap = dict()
        
        for i in list(self.DictofStocks.keys()):
            
            X = IndexP.resample("W").\
            mean().pct_change()['Adj Close'].values[self.Lag:].reshape((-1,1))
            
            Y = self. DictofStocks[i].resample("W").\
            mean().pct_change()['Adj Close'].values[self.Lag:]
            
            model = LinearRegression().fit(X, Y)
            
            model = model.fit(X, Y)
            
            RS = model.score(X, Y)
            
            DictofCap[i] = (model.coef_[0], model.intercept_, RS) 
            
            
        return(DictofCap)
