import numpy as np






class Propose ():
    
    def __init__(self, DictofClustered, DictofAdj, DictofOptimalW, DictofRet) -> None:
        
        self.DictofClustered = DictofClustered #a Dict which hase 1 layer ande the keys of it is Clusret0 to Cluster n 
        # and value of each cluster is the stockes which are grouped in that cluster
        self.DictofAdj = DictofAdj             # a Dict that keys is name of each stocks and values is Adj Close of that stock
        
        self.DictofOptimalW = DictofOptimalW   # a Dict that has to layers the first one is Clusret and second one is name of stocks
        # the value of stocks is optimal lenght of window 
        
        self.DictofRet = DictofRet # a dict that the keys is name of stocks and its value is series of return
        
    
    
    
    def FindinFuturePatter (self,PriceSeries ,Window, ReturenSeries, k=1 ):
        """"
        This function act for calculationg decision measure for choosing which pattern is more sutable for prediction tommorow
        """
        BachforPredicting =PriceSeries[-Window:] #seprate a bach of data for finding the most resemble pattern with it 
        #RestofData = PriceSeries[:-Window]
        TomorrowP = list()
        TomorrowR = list()
        Measure = list ()
        for i in range(len(PriceSeries)-2*Window):#searching through pervious data for fining best batter 
            Tomorrow = PriceSeries[i+Window+1] #seperate tommorow price as an feature for rest of code
            SeperatedofWhol = PriceSeries[i:i+Window]#seperate a bach for calculiting resemblance between BachforPredicting and it
            Temp = BachforPredicting - SeperatedofWhol
            Distance =np.linalg.norm(Temp)#calculate distance
            ReturnofTommorow =ReturenSeries[i+Window+1]
            TomorrowP.append(Tomorrow)#save Price of tommorow 
            TomorrowR.append(ReturnofTommorow)#save Returnof tommorow 
            Measure.append (Distance)#save measure
        
        x = np.argsort(Measure)[::-1][:k]
        Index = x[k-1]
        Best_pettern = [TomorrowP[Index],TomorrowR[Index],Measure[Index]]
        # the return is return and price of tommoraw and Distance as a measure
    
        return(Best_pettern)
    
    
    
    def fit (self):
        DictofProposed = dict()
        for i in self.DictofClustered.keys ():
            listOfMeasures = list()
            ListOfStocks = list ()
            for j in self.DictofClustered[i]: # it the name of Stocks such as AAPL that are in a same cluster 
                _,TommorowR, Meas = self.FindinFuturePatter(self.DictofAdj[j] ,self.DictofOptimalW[i][j], self.DictofRet[j])
                listOfMeasures.append(TommorowR/Meas)
                ListOfStocks.append(j)
            Index = np.argmax(listOfMeasures)
            Proposed = ListOfStocks[Index]
            DictofProposed[i]= Proposed
        return(DictofProposed)
    