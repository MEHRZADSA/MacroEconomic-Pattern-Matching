import numpy as np





class FindingOptimal ():
    def __init__(self, DictofClustered,  DictofAdj, DictofRet) -> None:
        self.DictofClustered = DictofClustered 
        """
        it is a dictionery with 2 layers the first layer detrmines name of cluster and second layer
        determing wich stock is in that clastur
        """
        self.DictofAdj = DictofAdj
        """"
        the Dictionary which hase 1 layer and the keys of that is Name of stocks and its values is Adj close of each stocks
        """
        self.DictofRet = DictofRet
        
    
    def Predict(self, Train,Window, RetunrSeries):
        
        "This function is coded to predict tommorow with a set of data based on patter matching an best distance"
        BachforPredicting =Train[-Window:] #seperate a batch for predicting tommorow of that batch based on historical pattern
        TomorrowR = list()
        distance = list()
        for i in range(len(Train)-2*Window):# go through data and checking the distance between all pattern
            SeperatedofWhol = Train [i:i+Window]# seperate a bach for calculiting resemblance between BachforPredicting and it
            Temp = BachforPredicting - SeperatedofWhol
            Distance =np.linalg.norm(Temp)#calculate distance
            ReturnofTommorow =RetunrSeries[i+Window+1] # keep the tommorow return for proposing tommorow based on best distance 
            TomorrowR.append(ReturnofTommorow)
            distance.append(Distance)# keeping best distance to figure out which distance is min
        Index = np.argmin(distance) #finding best distance 
     
        return(TomorrowR[Index]) #retuning tommorow return based on the best distance 
    
    
    def MESE_Loss (self, actual_returns, predicted_returns):
        # calculate the MESE loss
        squared_errors = [(actual - predicted) ** 2 for actual, predicted in zip(actual_returns, predicted_returns)]
        mese_loss = sum(squared_errors) / len(squared_errors)
        return (mese_loss)
    
    
    def FindingOptimalWindow (self, SereiesofPrice, SeriesofReturn , Listof_windows = [4 , 12 , 16 ],k = 24):
        """
        The SeriesofPrice : 
        The Seriesof Return :
        ListofWindws : is a list that based on each elements the best windowlenght choose th
        Default values IS  [5 ,25 , 75 ,100] on the grounds of weekly, monthly, seasonally ,and quadrimester
        """
        # the k is representative of how many of data is considered as cross validation fro example you have 100
        # - data you seperate 24 of them in order to predict that 24 datas and calculate lenth of windows
        MSELIST = list()
        for j in Listof_windows:
            predicted= list() # creating list in order to save predicted to calculate Mse
            actual = list() #  creating list in order to save Actual to calculate Mse
            for i in range(len(SereiesofPrice)-k,len(SereiesofPrice)-1): # going throgh like a rolling window and calculating predicted
                actual.append(SeriesofReturn[i+1]) #saving actual Return for MSE function 
                predicted.append(self.Predict (SeriesofReturn[:i],j,SeriesofReturn[:i])) #saving and calculation predict
            
            
            MSELIST.append(self.MESE_Loss(actual , predicted)) # saving Mse as a list ot find which on is the lowest
        
        Proposed = np.argmin(MSELIST)
    
        Proposed = Listof_windows[Proposed]
    
        return (Proposed)
    
    
    def implementing (self):
        NameofClusters = list(self.DictofClustered.keys())
        WindowsofWhol = dict()
        for i in NameofClusters: # going through classes one by one
            globals()[i+"windows"] = dict()
            for j in self.DictofClustered[i]: # go inside of each classes and detrmine each lenght for each stocks
                globals()[i+"windows"][j] = self.FindingOptimalWindow(self.DictofAdj[j],self.DictofRet[j])
            WindowsofWhol[i] = globals()[i+"windows"] #add dictonary which is created to Whole dictionary
            
        return(WindowsofWhol)
        
