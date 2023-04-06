import pandas as pd
import yfinance as yf
import numpy as np



class ReadData ():
    def __init__(self,NameofFile):
        """
        Name of Excel which is saved in directory should be inserted as 
        a char variable + .text
        
        """
        self.NameofFile = NameofFile
        
    def NameofStocks(self):
        """

        the name of stocks read by pandas and the col whose name is 'Name' 
        should be chosen
        
        """
        dataframe = pd.read_excel(self.NameofFile+'.xlsx')
        
        "read the excel file which has a col, named 'Name'"
        
        ticker_names = list(dataframe['Name'].values)
         
            
        
        return (ticker_names)


class DownloadData ():
    
    def __init__(self):
        pass
        
    def Download (self,NameStocks,Start,End):
        """
        The in put contain tree variables 
        NameStocks : is a list whom emlements are name of each stock as char
        Start : is related to Start Day for implementing model
        End :is the date of last set of data
        
        """
        DictofStocks = dict()
        ListofLengh = list()
        for i in NameStocks:
            Stock = yf.download(i, start=Start, end=End)
            DictofStocks[i] = Stock
            ListofLengh.append(len(DictofStocks[i]))

        counts = np.bincount(ListofLengh)

        MaxIndex = np.argmax(counts)

        
        for i in NameStocks:
            if len(DictofStocks[i]) != MaxIndex:
                del DictofStocks[i]



        return (DictofStocks)
    

    
 



