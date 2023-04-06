
import numpy as np
import pandas as pd
import datetime


class FindingMacroPattren:
    def __init__ (self,DataFramofVaribles, Window = 12):
        self.DataFramofVaribles = DataFramofVaribles
        self.Window = Window
    
    
    
    def PatternMatchingofMicro (self,SeriesofVarible,Window = 12):
        #SeriesofVarible is macro variable for example 'CPI'
        BachforPredicting = SeriesofVarible.iloc[-Window:] # seperate the end of date, since findding pattern is on this batch
        RestofData = SeriesofVarible.iloc[:-Window] #keep rest of data separate from bachforpredicting to eliminate overlap
        Measure = list ()# Creat a list for saving Measures
        Date =list()# create the list for saving the date
        for i in range(len(RestofData)-Window):#searching through pervious data for fining best batter 
            Bachforcal = RestofData [i:i+Window] # Separate a bach for calculating measure with BachforPredict
            Measu = np.corrcoef(Bachforcal,BachforPredicting)[0][1]
            SDate = Bachforcal.index[0]# Get start batch index to refer to it when the best masure is finded
            EDate = Bachforcal.index[-1]#Get end batch index to refer to it when the best masure is finded
            Date.append((SDate,EDate)) # save start and end of index
            Measure.append(Measu) # save measures to find wich one is the best
    
        ArgM = np.argmax(Measure)# find arge max
        return(Date[ArgM])
    


    def FIndDateOFMacro (self, TimeV : list)-> dict :
    
    
        Starttimey = TimeV[0].year
        Starttimem = TimeV[0].month
        
        Endtimey = TimeV[-1].year
        Endtimem = TimeV[-1].month
        Start= datetime.datetime(Starttimey, Starttimem, 1)# Since the downloaded macro variables are from 1971 
        End =  datetime.datetime(Endtimey, Endtimem, 1)
        self.DataFramofVaribles = self.DataFramofVaribles.loc[Start:End]  
        # in order to match Time of sStocks with Time of Macrovaraibles we do that
        DictofBestDateofMacro = dict()
        for i in self.DataFramofVaribles.columns:
            DictofBestDateofMacro[i] = self.PatternMatchingofMicro (self.DataFramofVaribles[i])
        return(DictofBestDateofMacro)
