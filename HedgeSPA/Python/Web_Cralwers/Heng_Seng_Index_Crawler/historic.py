# User-defined exception
class inputDateError(Exception):
    """Raised when the input date is not of the form YYYY-MM-DD"""
    pass

class historic():
    """"""
    
    def __init__(self,stockscodes,startdate=None,enddate=None):
        """The input stockscodes and either be a single string standing for the code of a stocks or a tuple of list of stocks codes
        
        If it is a single string, the methods prices and returns would return a pd.Series. If it is a tuple of list, the methods prices and returns would return a pd.DataFrame.
        
        self._price: the adjusted close price of the stocks within the specified period
        
        startdate and enddate must be of the form "YYYY-MM-DD"
        
        if enddate is not provided, it is set to be today, if startdate is not provided, it is set to be one year before the enddate
        """
        try:
           import pandas_datareader
        except ImportError:
            print('Error, the module "pandas_datareader" is required.')
        try:
           import datetime
        except ImportError:
            print('Error, the module "datetime" is required.')
        try:
           import seaborn
        except ImportError:
            print('Error, the module "seaborn" is required.')
        try:
           import re
        except ImportError:
            print('Error, the module "re" is required.')
        
        
        if enddate==None:
            enddate=str(datetime.date.today())
        else:
            pass
        if startdate==None:
            temp=list(str(enddate).partition("-"))
            temp[0]=str(int(temp[0])-1)
            startdate="".join(temp)
        else:
            pass
        
        gex=re.compile(r"[\d]{4}-[\d]{2}-[\d]{2}")
        try:
            if gex.match(startdate):
                pass
            else:
                raise inputDateError()
        except inputDateError:
            print("startdate must be of the format YYYY-MM-DD")
        try:
            if gex.match(enddate):
                pass
            else:
                raise inputDateError()
        except inputDateError:
            print("enddate must be of the format YYYY-MM-DD")
            
        from pandas_datareader import data
        import numpy as np
        import pandas as pd
        
        self._stockscodes=stockscodes
        if type(stockscodes)==str:
            temp=data.DataReader(stockscodes,start=startdate,end=enddate,data_source='yahoo')['Adj Close']
            temp.name=stockscodes
            self._prices=temp
            self._returns=pd.Series((np.array(temp)[1:]-np.array(temp)[:-1])/np.array(temp)[:-1],index=np.array(temp.index)[1:])
            self._logreturns=pd.Series(np.log(np.array(temp)[1:]/np.array(temp)[:-1]),index=np.array(temp.index)[1:])
        else:
            temp=[data.DataReader(i,start=startdate,end=enddate,data_source='yahoo')['Adj Close'] for i in stockscodes]
            dum=pd.DataFrame({key:value for (key,value) in zip(stockscodes,temp)})
            self._prices=dum
            self._returns=pd.DataFrame((np.array(dum)[1:,:]-np.array(dum)[:-1,:])/np.array(dum)[:-1,:],index=np.array(dum.index)[1:],columns=stockscodes)
            self._logreturns=pd.DataFrame(np.log(np.array(dum)[1:,:]/np.array(dum)[:-1,:]),index=np.array(dum.index)[1:],columns=stockscodes)
    
    def getprices(self):
        """Get the prices"""
        return(self._prices)
 
    def plotprices(self):
        """provide a timeseries plot of the data
        """
        import matplotlib
        self.getprices().plot(title='Adj. Closing Price',grid=True)
        
    def getreturns(self):
        """Get the standard daily returns"""
        return(self._returns)
        
    def getlogreturns(self):
        """Get the log daily returns"""
        return(self._logreturns)
        
    def plotreturns(self,log=False):
        """provide a histogram of the return
        
        if log=False, plot the standard returns
        
        if log=Ture, plot the log returns
        """
        #seaborn.distplot() cant handel a dataframe directly
        #import seaborn as sns
        #sns.set_style('darkgrid')
        #if log==True:
        #    sns.distplot(self.getlogreturns())
        #else:
        #    sns.distplot(self.getreturns())
        import matplotlib
        if log==True:
            self.getlogreturns().hist(bins=20)
        else:
            self.getreturns().hist(bins=20)
            
            
        
        
        
        
        
        
        


if __name__=="__main__":
    
    historic("0001.HK").getprices()
    historic("0001.HK").plotprices()
    historic("0001.HK").getreturns()
    historic("0001.HK").getlogreturns()
    historic("0001.HK").plotreturns()
    historic("0001.HK").plotreturns(log=True)
    
    historic("0001.HK",startdate="2018-01-01",enddate="2018-12-31")
    historic("0001.HK",startdate="2018-01-01")
    historic("0001.HK",enddate="2018-12-31")
    historic("0001.HK")    

    
    historic(["0001.HK","0005.HK"]).getprices()
    historic(["0001.HK","0005.HK"]).plotprices()
    historic(["0001.HK","0005.HK"]).getreturns()
    historic(["0001.HK","0005.HK"]).getlogreturns()
    historic(["0001.HK","0005.HK"]).plotreturns()
    historic(["0001.HK","0005.HK"]).plotreturns(log=True)
    
    historic(["0001.HK","0005.HK"],startdate="2018-01-01",enddate="2018-12-31")
    historic(["0001.HK","0005.HK"],startdate="2018-01-01")
    historic(["0001.HK","0005.HK"],enddate="2018-12-31")
    historic(["0001.HK","0005.HK"])


