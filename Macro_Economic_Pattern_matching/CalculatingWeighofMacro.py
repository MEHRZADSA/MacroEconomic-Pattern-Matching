import yfinance as yf
import datetime
import pandas as pd
import numpy as np
from sklearn.feature_selection import mutual_info_regression
from dateutil.relativedelta import relativedelta





class WeightCalculator :
    def __init__(self, NumofStock : str, Time : list,  DataFrameofFred: pd.DataFrame) -> None:
        
        self.NumofStock = NumofStock
        self.Time = Time
        self.DataFrameofFred = DataFrameofFred
        """
        the Numofstock is name of index or variable that is supposed to calculate its mutual information with other 
        macro variables
        
        Time is a list that elements of its list is a time of downloaded data like AAPLE 
        getting time is for matching time of Macrovriables with other lenth of stock or index
        """
    
    def DownloadIndex (self)-> pd.DataFrame:
        Index =  self.NumofStock
        
        """
        The index is Name of Stock

        """
        Starttimey = self.Time[0].year
        Starttimem = self.Time[0].month
        
        Endtimey = self.Time[-1].year
        Endtimem = self.Time[-1].month
        
        self.Start = datetime.datetime(Starttimey, Starttimem, 1)# Since the downloaded macro variables are from 1971 
        self.End =  datetime.datetime(Endtimey, Endtimem, 1)# Since the end of macro variable is this date. 
    
        Stock =yf.download(Index, self.Start, self.End) #Downloading data
    
        """
        In order to match dates of market index to data which downloaded from FRED , many steps is needed to take.
        Firstly, make data in to mean of month.
        Secondly, since those data index become last day of month, it is necessery to bering data to first day of each month.
        thridly, the index should be shifted , becuase each first day of month in represent of previous month.
    
        """
    
        MonthlyStock = Stock.resample('M').agg({'Open':'first', 'High':'max', 'Low':'min', 'Close':'last', 'Volume':'sum'})
        MonthlyStock.index = MonthlyStock.index.to_period('M').astype(str) + '-01'
        Indexs = MonthlyStock.index #sprating indexs to eliminate the first index.
        Indexs = Indexs[1:] # Eliminating first index.
        MonthlyStock = MonthlyStock.iloc[:-1] # Deleting last row of data frame.
        MonthlyStock.index = Indexs # Match data with index of them
    
        return(MonthlyStock)
    
    
    
    def CalculatingWight (self)->dict:
        
        """
        It takes Dataframe whose elements are Macroeconomic variables 
        """
        
        DataFramofIndex = self.DownloadIndex()# Download Data or index from yahoo finance
        
        DataFrameofFred = self.DataFrameofFred.loc[self.Start+relativedelta(months=1): self.End-relativedelta(months=1)] 
        #Slicing the batch is needed to caclulate Mutual inf
        # because the shifting was used we have to add and subtract a month to fit the lenth
        
        #return (DataFrameofFred,DataFramofIndex, self.Start,self.End)
        
        
        Values = DataFramofIndex["Close"].values# Get the close price of downlodade data
     
        listofWight = list()
        for i in DataFrameofFred.columns: # calculating mutual information between index and each economic variable
            x = DataFrameofFred[i]
            MutualNum =  mutual_info_regression(X=np.array([x]).T, y=Values, n_neighbors=3) #calculating mutual inf value
            listofWight.append(MutualNum)
    
        listofWight = np.array(listofWight)/sum(listofWight) #Normalizing the calculated weights
    
        DictofWeight = {i:j[0]  for i,j in zip(DataFrameofFred,listofWight)} 
        #Creating a dictionary in which each key is name of econimic variable and its value is weight of that
    
        return(DictofWeight)