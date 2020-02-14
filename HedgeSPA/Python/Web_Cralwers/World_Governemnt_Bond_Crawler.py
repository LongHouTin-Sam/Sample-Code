
# REFERENCE: https://www.geeksforgeeks.org/implementing-web-scraping-python-beautiful-soup/

class WorldGovernmentBond():
    """This is a abstract data type defined to crawl all the world government bond data (country, identifier, title, href) 
 
    from https://www.investing.com/rates-bonds/world-government-bonds
    
    One of the instance variable would refernce to the data scrpaed in organized format (e.g., data frame)
    """
    
    def __init__(self):
        """The data of interest is scraped when the class is instanciated
        
        and stored into the instance variable "self._investing_ticker"
        """
        try:
            from bs4 import BeautifulSoup
        except ImportError:
            print("Error, the module 'bs4' is required.")
        try:
            from urllib.request import urlopen, Request
        except ImportError:
            print("Error, the module 'urllib' is required.")
        import numpy as np, pandas as pd
        
        investingURL="https://www.investing.com/rates-bonds/world-government-bonds"
        req=Request(investingURL, headers={"User-Agent": "Mozilla/5.0"})
        
        doc=urlopen(req)
        soup=BeautifulSoup(doc,"html.parser")
        dest=r"C:\Users\longh\Desktop\HedgeSPA\Crawling_investing.com\Python\investingSoup_html.txt"
        with open(dest,"w",encoding="utf8") as fucd:
            fucd.write(soup.prettify())
        
        tempsoup=pd.DataFrame(columns=["country","identifier","title","href"])
        looper=list(map(lambda x: x["id"], soup.find_all("table", attrs={"class":{"genTbl closedTbl crossRatesTbl"}})))
        # extracting only numbers from a string # [int(s) for s in str.split() if s.isdigit()]
        looper=sorted(looper, key=lambda x: int(x.split("_")[-1]))
        
        for i in looper:
            dumsoup=soup.find("table", attrs={"id":{i}})
            # country=list(map(lambda x: x[4]["title"], dumsoup.find_all("span")))
            identifier=list(map(lambda x: x.text, dumsoup.find_all("a")))
            title=list(map(lambda x: x["title"], dumsoup.find_all("a")))
            href=list(map(lambda x: x["href"], dumsoup.find_all("a")))
            if all(np.equal(len(identifier),[len(title),len(href)])):
                country=[dumsoup.find_all("span")[4]["title"]]*len(href)
                tempsoup=pd.concat([tempsoup,pd.DataFrame({"country":country,"identifier":identifier,"title":title,"href":href}, index=range(1,1+len(href)))], axis=0)
            else:
                print("Something's wrong with "+i+"!, Inspect the correponding html.",sep="")
        
        # assign the data frame to a instance variable
        self._investing_ticker=tempsoup
      
    
    def get_investing_ticker(self):
        """fetch the data frame refernced by the instance variable self._investing_ticker
        """
        return(self._investing_ticker)
        

 
# Testing
if __name__=="__main__":
    # Python naming convension: https://visualgit.readthedocs.io/en/latest/pages/naming_convention.html
    WorldGovernmentBond().get_investing_ticker().to_csv(r'C:\Users\longh\Desktop\HedgeSPA\Crawling_investing.com\Python\WGB_investing_ticker.csv', index=False)
    #######################################
    ### remember to specify index=False ###
    #######################################