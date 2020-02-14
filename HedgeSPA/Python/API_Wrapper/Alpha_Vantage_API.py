# Refernce: https://www.alphavantage.co/documentation/#fx

class AVAPI(): 
    
    def __init__(self):
        try:
            import sys
            import requests
            import pandas as pd
        except:
            print("packages 'sys', 'request' and 'pandas' are required!")

    
    def Get_TimeSeries(self,symbol,interval):
        """
        A wrapper function to obtain the the time series of a the desired stock from the Alpha Vantage API.
        
        Parameters:
        -----------
        stock: the desired stock symbol (e.g., "GOOG", "AMD", "FB", "INTC").
        period: "daily", "weekly", "monthly"
        
        Returns:
        --------
        A pandas dataframe with the columns `open`, `high`, `low`, `close`, and `volume`.
        """
        import sys, requests, pandas as pd            
        API_URL="https://www.alphavantage.co/query" 
        
        funDict={"daily":"TIME_SERIES_DAILY_ADJUSTED", 
                 "weekly":"TIME_SERIES_WEEKLY_ADJUSTED", 
                 "monthly":"TIME_SERIES_MONTHLY_ADJUSTED"}
        jsonDict={"daily":"Time Series (Daily)", 
                  "weekly":"Weekly Adjusted Time Series", 
                  "monthly":"Monthly Adjusted Time Series"}
        renameDict={"daily":{"1. open":"Open", 
                             "2. high":"High", 
                             "3. low":"Low", 
                             "4. close":"Close", 
                             "5. adjusted close":"Adjusted_Close", 
                             "6. volume":"Volume", 
                             "7. dividend amount":"Dividend Amount", 
                             "8. split coefficient":"Split Coefficient"},
                    "weekly":{"1. open":"Open", 
                              "2. high":"High", 
                              "3. low":"Low", 
                              "4. close":"Close", 
                              "5. adjusted close":"Adjusted_Close", 
                              "6. volume":"Volume", 
                              "7. dividend amount":"Dividend Amount"},
                    "monthly":{"1. open":"Open", 
                               "2. high":"High", 
                               "3. low":"Low", 
                               "4. close":"Close", 
                               "5. adjusted close":"Adjusted_Close", 
                               "6. volume":"Volume", 
                               "7. dividend amount":"Dividend Amount"}}
        reindexDict={"daily":["Volume","Dividend Amount","Split Coefficient","Open","High","Low","Close","Adjusted_Close"],
                     "weekly":["Volume","Dividend Amount","Open","High","Low","Close","Adjusted_Close"],
                     "monthly":["Volume","Dividend Amount","Open","High","Low","Close","Adjusted_Close"]}
        
        try:
            data={"function": funDict[interval],
                  "symbol": symbol,
                  "outputsize": "full",
                  "datatype": "json",
                  "apikey": "WRFTGZ5VX5H962D3" }    
            response=requests.get(API_URL, data)
        except:
            print("Check the input parameter!")
            sys.exit()
        
        response_json=response.json()
        data=pd.DataFrame.from_dict(response_json[jsonDict[interval]], 
                                    orient="index").sort_index(axis=1, ascending=False)
        data=data.rename(columns=renameDict[interval])
        data=data.reindex(columns=reindexDict[interval])
        return data


    def FX_TimeSeries(self,fromSymbol,toSymbol,interval):
        """
        A wrapper function to obtain the the time series of a the desired stock from the Alpha Vantage API.
        
        Parameters:
        -----------
        fromSymbol: A three-letter symbol from the forex currency list. For example: from_symbol=USD.
        toSymbol: A three-letter symbol from the forex currency list. For example: to_symbol=CAD.
        period: "daily", "weekly", "monthly"
        
        Returns:
        --------
        A pandas dataframe with the columns `open`, `high`, `low`, `close`.
        """
        import sys, requests, pandas as pd
        API_URL="https://www.alphavantage.co/query" 
        #from_symbol='USD'
        #to_symbol='CAD'    
    
        funDict={"daily":"FX_DAILY", 
                 "weekly":"FX_WEEKLY", 
                 "monthly":"FX_MONTHLY"}
        jsonDict={"daily":"Time Series FX (Daily)", 
                  "weekly":"Time Series FX (Weekly)", 
                  "monthly":"Time Series FX (Monthly)"}
        
        try:
            data={"function": funDict[interval],
                  "from_symbol": fromSymbol,
                  "to_symbol": toSymbol,
                  "outputsize": "full",
                  "datatype": "json",
                  "apikey": "WRFTGZ5VX5H962D3" }  
            data=pd.DataFrame.from_dict(requests.get(API_URL, data).json()[jsonDict[interval]], 
                                        orient="index").sort_index(axis=1, ascending=False)
        except:
            print("Check the input!")
            sys.exit()
        
        data=data.rename(columns={"1. open":"Open", 
                                  "2. high":"High", 
                                  "3. low":"Low", 
                                  "4. close":"Close"})
        data=data.reindex(columns=["Open","High","Low","Close"])
        return(data)


    def technical_TimeSeries(self,fun,symbol,interval,time_period,series_type):
        """
        A wrapper function to obtain the the time series of a the desired technical indicator of the desired stock from the Alpha Vantage API.
        
        Parameters:
        -----------
        function: The technical indicator of your choice, e.g., function=SMA.
        symbol: The name of the security of your choice. For example: symbol=MSFT.
        interval: Time interval between two consecutive data points in the time series. The following values are supported: 1min, 5min, 15min, 30min, 60min, daily, weekly, monthly.
        time_period: Number of data points used to calculate each moving average value. Positive integers are accepted (e.g., time_period=60, time_period=200).
        series_type: The desired price type in the time series. Four types are supported: close, open, high, low.
        
        Returns:
        --------
        A pandas dataframe with the columns `open`, `high`, `low`, `close`.
        """
        import sys, requests, pandas as pd
        API_URL="https://www.alphavantage.co/query" 
        
        try:
            data={"function": fun,
                  "symbol": symbol,
                  "interval": interval,
                  "time_period": time_period, 
                  "series_type": series_type,
                  "datatype": "json",
                  "apikey": "WRFTGZ5VX5H962D3" } 
            data=pd.DataFrame.from_dict(requests.get(API_URL, data).json()["Technical Analysis: "+fun], 
                                        orient="index").sort_index(axis=0, ascending=False)
        except:
            print("Check the input!")
            sys.exit()        
        
        return(data)


if __name__=="__main__":
    
    testingAPI=AVAPI()
    print(testingAPI.Get_TimeSeries("MSFT", "daily").head(5))
    print(testingAPI.FX_TimeSeries("USD","CAD","monthly").head(5))
    
    from datetime import datetime
    import matplotlib.pyplot as plt
    sma=testingAPI.technical_TimeSeries("SMA","MSFT","weekly","7","close")
    ema=testingAPI.technical_TimeSeries("EMA","MSFT","weekly","7","close")
    smax=list(map(lambda x: datetime.strptime(x, "%Y-%m-%d").date(), sma.index))
    smay=list(map(lambda x: float(x), sma.values))
    plt.plot(smax,smay)
