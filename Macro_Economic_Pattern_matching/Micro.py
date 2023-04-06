
import pandas_datareader.data as web
import pandas as pd

class DownloadMicroEconomic ():
    def __init__(self, ListOfVariables: list, ListforSaving: list ,Start='1971-01-01' , End='2022-10-01')  -> None:
        # is a list whose each elements is Microeconimic variable name based on  FED
        self.ListOistOfVariables = ListOfVariables
        # is a list of name for saving downloaded Variables
        self. ListforSaving =  ListforSaving
        
        self.Start = Start # The day on which the varible starts  
        self.End = End # The day on which the varible ends
    
    
    def Downlod (self):
        
        def CheckLen(numbers: list): # A function for checking the if there is a diffrent variable in a list or not
            return len(set(numbers)) == 1
        
        
        
        def find_diff_index(numbers):
            # Iterate over the list, comparing each element to the first element
            for i, number in enumerate(numbers):
                if number != numbers[0]:
                    # Return the index of the different element
                    return i
            # All elements are the same
            return None

        
        MicroData = pd.DataFrame()
        DictofMicro = dict()
        lenlist = list()
        for i,j in zip (self.ListOistOfVariables,self.ListforSaving): # Downloading variables based on inputed list 'ListOfVariables'
            globals()[j] = web.DataReader(i, 'fred', self.Start, self.End)
            if globals()[j].index.inferred_freq != 'MS': # This condition assess if the frequency of data is monthly of not 
                globals()[j] = globals()[j].resample('MS').interpolate() # if is not monthly it turn in into monthly by intepolation
            lenlist.append(len(globals()[j]))
            DictofMicro[j] = globals()[j]
            MicroData[j] = globals()[j]
        if CheckLen(lenlist) == False:
            Index = find_diff_index(lenlist)
            
            
            print("Not all elements in the list are the same and {} differs".format(self.ListforSaving[Index])) # this code is runed for checking that len of all variables are same or not

        return (DictofMicro, MicroData)