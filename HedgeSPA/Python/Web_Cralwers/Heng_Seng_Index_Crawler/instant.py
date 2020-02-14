class instant():
    """This is a module of subpackage hsi of package fed """
    
    def __init__(self):
        """"""
        try:
            import bs4
        except ImportError:
            print("Error, the module 'bs4' is required.")
        try:
            import urllib
        except ImportError:
            print("Error, the module 'urllib' is required.")
            
        self._names=("Hang_Seng_Index"
               ,"Finance_Sub-index"
               ,"Utilities_Sub-index"
               ,"Properties_Sub-index"
               ,"Commerce_and_Industry_Sub-index")
        self._sites=("http://www.aastocks.com/tc/stocks/market/index/hk-index-con.aspx?index=HSI&t=1&s=&o=1&p="
               ,"http://www.aastocks.com/tc/stocks/market/index/hk-index-con.aspx?index=HSF&t=1&s=&o=1&p="
               ,"http://www.aastocks.com/tc/stocks/market/index/hk-index-con.aspx?index=HSU&t=1&s=&o=1&p="
               ,"http://www.aastocks.com/tc/stocks/market/index/hk-index-con.aspx?index=HSP&t=1&s=&o=1&p="
               ,"http://www.aastocks.com/tc/stocks/market/index/hk-index-con.aspx?index=HSC&t=1&s=&o=1&p=")
        self._ZipDict=dict(zip(self._names,self._sites))
        


    def indices(self):
        """return Hang Seng Index and Sub-index
        
        Sub-index by 4 sector: Finance, Utilities, Properties, Commerce and Industry
        """
        import numpy as np
        import pandas as pd   
        try:
            from bs4 import BeautifulSoup
        except ImportError:
            print("Error, the module 'bs4' is required.")
        try:
            from urllib.request import urlopen
        except ImportError:
            print("Error, the module 'urllib' is required.")
     
        indicesInfo=dict()
        for i in self._names:
            doc=urlopen(self._ZipDict[i])
            soup=BeautifulSoup(doc,"html.parser")
            #dest="C:/Users/longh/Desktop/Python_working directory/"+i+".txt"
            #with open(dest,"w",encoding="utf8") as fucd:
            #    fucd.write(soup.prettify())
            temp1=list()
            for tag in soup.find_all("div",attrs={"class":{"hkidx-last txt_r"}}): 
                temp1.append(tag.string) 
            temp2=list()
            for tag in soup.find_all("span",attrs={"class":{"range"}}):
                temp2.append(tag.string)
            indicesInfo[i]=temp2+temp1
        
        try:
            indicesInfo=pd.DataFrame([indicesInfo[i] for i in self._names],columns=np.array(["Previous","Open","Instant"]),index=self._names)
        except:
            print("Something's wrong, an Data Frame is expected to be returned, check the code.")
        return(indicesInfo)
        
    
    def stocks(self):
        """Return the information 50 constituent stocks of the Hang Seng Index
        
        Information include 'Code', 'Name', 'Last_price', 'Market_Cap', 'P/E', 'P/B', 'Yield', and 'Sector'
        """
        import numpy as np
        import pandas as pd   
        try:
            from bs4 import BeautifulSoup
        except ImportError:
            print("Error, the module 'bs4' is required.")
        try:
            from urllib.request import urlopen
        except ImportError:
            print("Error, the module 'urllib' is required.")
        
        stocksInfo=dict()
        for i in self._names[1:]: # the first website is not of interest
            doc=urlopen(self._ZipDict[i]).read().decode("utf-8") 
            soup=BeautifulSoup(doc,"html.parser")
            temp1=list()
            for tag in soup.find_all("a",attrs={"class":{"a14 cls"}}): 
                temp1.append(tag.string) 
            temp2=list()
            for tag in soup.find_all("span",attrs={"class":{"float_l"},"style":{"line-height:17px"}}):
                temp2.append(tag.string)
            temp3=list() 
            for tag in soup.find_all("td",attrs={"class":{"cls txt_r font-b pad3"}}):
                temp3.append(tag.string)
            temp4=list()
            for tag in soup.find_all("td",attrs={"class":{"cls txt_r pad3 nowrap"}}):
                temp4.append(tag.string)
            temp5=list()
            for tag in soup.find_all("td",attrs={"class":{"cls txt_r pad3"}}):
                temp5.append(tag.string)
            temp5=np.array(temp5).reshape(len(temp5)//8,8).T[5:,:] # mind that reshape take integer, use // insteat of /
            #[len(i) for i in [temp1,temp2,temp3,temp4,temp5[0],temp5[1],temp5[2]]]
            stocksInfo[i]=pd.DataFrame({key:value for (key,value) in zip(("Code","Name","Last_price","Market_Cap","P/E","P/B","Yield","Sector"),(temp1,temp2,temp3,temp4,temp5[0],temp5[1],temp5[2],np.repeat(i.partition("_Sub")[0],len(temp1))))})
        #[len(stocksInfo[i]) for i in names[1:]]
               
        try:
            stocksInfo=pd.concat([stocksInfo[i] for i in self._names[1:]])
            stocksInfo.index=np.arange(1,50+1,1) 
        except:
            print("Something's wrong, an Data Frame is expected to be returned, check the code.")
        return(stocksInfo)
    

# Inheritance    
class useless(instant):
    """Demonstration of Inheritence"""
    def __init__(self,sector):
        """sector can take 4 values
        
        "F": Finance
        "U": Utilities
        "P": Properties
        "CI": Commerce and Industry
        """
        super().__init__()
        self._sector=sector
    
    # Two specializtions, no extension
    def indices(self):
        ZipDict=dict(zip(["F","U","P","CI"],self._names[1:]))
        return(super().indices().loc[ZipDict[self._sector],]) 
    def stocks(self):
        ZipDict=dict(zip(["F","U","P","CI"],["Finance","Utilities","Properties","Commerce_and_Industry"]))
        temp=super().stocks()
        return(temp[temp["Sector"]==ZipDict[self._sector]])
        
    








 
# Testing
if __name__=="__main__":
    
    print(instant().indices())
    useless("F").indices()
    #useless("U").indices()
    useless("P").indices()
    #useless("CI").indices()
    
    print(instant().stocks())
    #useless("F").stocks()
    useless("U").stocks()
    #useless("P").stocks()
    useless("CI").stocks()
