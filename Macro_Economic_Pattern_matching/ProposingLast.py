import yfinance as yf
import datetime
import numpy as np






class FinalPro :
    def __init__(self,DictofBestDateofMacro: dict ,OptimalWindowsofStocks,Time: list,NameofStock: str,
                 DictofMacroweight: dict,DictofClustered:dict) -> None:
        
        
        self.DictofBestDateofMacro =DictofBestDateofMacro # is a dic that each key is name of macro economic variables
        #and each values is best Pattern matched of that values
        self.OptimalWindowsofStocks = OptimalWindowsofStocks # is a dict that has 2 layer fist is name of cluster and second is name of its stock
        # the value of third layer is bets matched time window
        
        self.Time = Time # is the time that we are looking for pattern matching
        
        
        
        self.DictofMacroweight = DictofMacroweight # is the weight of each macro variable based on it each stock
        
        self.DictofClustered = DictofClustered
    
    
    
    
    def MeasuringStockParam (self,OtimalWindow,NameofStock):
        StartDate = self.Time[-OtimalWindow] 
        LastDAte = StartDate +datetime.timedelta(weeks=OtimalWindow)
        df = yf.download(NameofStock, start=StartDate, end=LastDAte)
        Dataforsearching = df.resample('W').mean()
        Dataforsearching= Dataforsearching['Adj Close'].values
        signals = []
        for i in self.DictofBestDateofMacro.keys():
            DateforMatching = self.DictofBestDateofMacro[i]# for pattern matching we choose set of data based on Macro variables
            data = yf.download(NameofStock, start=DateforMatching[0], end=DateforMatching[1])
            Data = data.resample('W').mean() # make it weekly
            Data = Data['Adj Close'].values # get the values of that series
            Measure = []
            tomorrowR = []
            SriesofReturn =data.resample('W').mean().pct_change()['Adj Close']
            for j in range(len(Data)-OtimalWindow-1):
                SeperatedofWhol = Data[j:j+OtimalWindow]#seperate a bach for calculiting resemblance between BachforPredicting and it
                Temp = Dataforsearching - SeperatedofWhol
                Distance =np.linalg.norm(Temp)#calculate distance
                ReturnofTommorow =SriesofReturn[j+OtimalWindow+1]
                tomorrowR.append(ReturnofTommorow)#save Returnof tommorow 
                Measure.append (Distance)#save measure
            
            argmin = np.argmin(Measure)
            Mainreturn = tomorrowR[argmin]
            signals.append(self.DictofMacroweight[NameofStock][i]*Mainreturn)
        
        return(sum(signals))
    
    
    
    
    def Implement (self):
        dictofproposed = dict()
        for i in self.DictofClustered.keys():
            dictNews = dict()
            for j in self.DictofClustered[i]:
        
                Params = self.MeasuringStockParam(self.OptimalWindowsofStocks[i][j],j)
                dictNews[j] = Params
    
            dictofproposed[i] = dictNews 
            
        FinalDecision = dict ()
        for i in dictofproposed.keys():
            values =list(dictofproposed[i].values())
            names =list(dictofproposed[i].keys())
            arg= np.argmax(values)
            FinalDecision[names[arg]] = values[arg]
            
        return(FinalDecision)
            