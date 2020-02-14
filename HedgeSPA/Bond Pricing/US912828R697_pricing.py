## Consider US912828R697
# Bond Data: https://markets.businessinsider.com/bonds/united_states_of_americadl-notes_201623-bond-2023-us912828r697
# Historical Price Data Source: https://www.treasurydirect.gov/GA-FI/FedInvest/selectSecurityPriceDate.htm
# Historial Zero-Coupon Yield Data: https://www.quandl.com/data/FED/SVENY-US-Treasury-Zero-Coupon-Yield-Curve
# Historical Treasury Bill Rate Data: https://www.quandl.com/data/USTREASURY/BILLRATES-Treasury-Bill-Rates

## Bond Data: 
#     Issue Date: 5/31/2016 (Tuesday)
#     Maturity Date: 5/31/2023
#     Coupon: 1.625%
#     Denomination: 100

## Consider the Price of US912828R697 on the settlemetn date of 3/18/2019:
#     clean price = dirty price - AI
#     Next coupon date: 5/31/2019 
#     9 certain future cash flows in total

# Historical Price Data:
#     Date       CUSIP	     SECURITY TYPE	    RATE	  MATURITY DATE 	CALL DATE   BUY	        SELL        END OF DAY
#     3/18/2019  912828R69	 MARKET BASED NOTE	1.625%	  05/31/2023		            96.859375	96.843750	96.812500

# Historial Zero-Coupon Yield Data: SVENYxx refers to the xx year continuously compunded US Treasury zero-coupon yield 
#    quandl.get("FED/SVENY", api_key="DJsNViiWw63DhNuAsDxM", start_date="2019-3-18", end_date="2019-3-18").iloc[0,:]
#    SVENY01    2.4953
#    SVENY02    2.4398
#    SVENY03    2.4173
#    SVENY04    2.4177
#    SVENY05    2.4336
#    SVENY06    2.4597
#    SVENY07    2.4919
#    SVENY08    2.5275
#    SVENY09    2.5646
#    SVENY10    2.6020
#    SVENY11    2.6386
#    SVENY12    2.6742
#    SVENY13    2.7083
#    SVENY14    2.7409
#    SVENY15    2.7720
#    SVENY16    2.8017
#    SVENY17    2.8302
#    SVENY18    2.8575
#    SVENY19    2.8839
#    SVENY20    2.9095
#    SVENY21    2.9345
#    SVENY22    2.9590
#    SVENY23    2.9832
#    SVENY24    3.0071
#    SVENY25    3.0310
#    SVENY26    3.0548
#    SVENY27    3.0786
#    SVENY28    3.1025
#    SVENY29    3.1266
#    SVENY30    3.1509

# Historical Treasury Bill Rate Data: 
#    quandl.get("USTREASURY/BILLRATES", authtoken="DJsNViiWw63DhNuAsDxM", start_date="2019-3-18", end_date="2019-3-18").iloc[0,:][np.array([i%2==0 for i in range(10)])]
#    4 Wk Bank Discount Rate     2.43
#    8 Wk Bank Discount Rate     2.41
#    13 Wk Bank Discount Rate    2.39
#    26 Wk Bank Discount Rate    2.44
#    52 Wk Bank Discount Rate    2.44

import numpy as np, pandas as pd
import quandl
from scipy.interpolate import PchipInterpolator
import matplotlib.pyplot as plt
from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta


## Step 1: Basic information of the Bond
issue=date(2016,5,31)
maturity=date(2023,5,31)
settlement=date(2019,3,18)
face=100
cRate=(1.625/100)
N=(maturity.year-issue.year)*2
rawDate=[issue+relativedelta(months=i*6) for i in range(1,1+N,1)] # layout all the cash date of the US Treasury from issue to maturity


## Step 2: Taking care of business day convention
# For US Treasury, we use modified following business day convention
# CAUTION: this step is not complete, it only take cares of weekends, but not holidays !!!
indi=[x.weekday() for x in rawDate]
for i in range(len(indi)):
    if indi[i]==5:
        temp=rawDate[i]+relativedelta(days=2)
        if (temp).month==rawDate[i].month:
            rawDate[i]=temp
        else:
            rawDate[i]=rawDate[i]-relativedelta(days=1)
    if indi[i]==6:
        temp=rawDate[i]+relativedelta(days=1)
        if (temp).month==rawDate[i].month:
            rawDate[i]=temp
        else:
            rawDate[i]=rawDate[i]-relativedelta(days=2)


## Step 3: Take care of day count convention, calculating accried interest and cash flows
# For US Treasury Note/Bond, we use ACT/ACT (ICMA) day count conventions,
# That is, the 1.625% 7 year US Treasury Note in a M day (could be 181, 182, 183, or 184 
#     depending on the start date and end date of the coupon period) accrues interest 
#     at a daily rate of (1.625%)*(1/(M*2))
# Under this day coupon convention, the coupon of a whole coupon period is garenteed to be face*(cRate/2), 
#     caution need to be taken only on the Accrued interest.
cashDate=[i for i in rawDate if settlement<i]
cashFlow=(np.repeat(face*cRate/2,len(cashDate))+np.repeat([0,100],[len(cashDate)-1,1])).tolist()
DFS=[(i-settlement).days for i in cashDate]
M=(cashDate[0]-(cashDate[0]-relativedelta(months=6))).days
AI=(face*cRate/(2*M))*(M-DFS[0]) 


## Step 4: Build a data frame to store the information of the future cash flows
cashDF=pd.DataFrame({"Cash_Date":cashDate,"Days_From_Settlement":DFS,"Cash_Flow":cashFlow})


## Step 5: Decide how to discount the cash flow:
# Pt0=np.dot(C,D), where C is the cash flow vector, D is the discounted rate vector
#     Always use continous compounding to discount the cash flow if the continously compunded US Treaury Zero-Coupon Yields is avaliable 
# We have direct access to the following rates from quandl: 
#     i-year continuously compounded  US Treasury Zero-Coupon Yield (annual) for i=1,2,...,30
#     j-week US Treasury Bill Rates (bank discount rate) for k=4,8,13,26,52
# Since extrapolation is not encouraged, we use the following discounting scheme:
# Denoted by ti the time from settlement to the cash event date:
#     if ti > 1 year: Di=exp(-ri*ti), where ri is the corresponding continuouly compounded US Treasuty Zero-Coupon Yield (annual), ti is time in year  
#     if 4 week<=ti<=56 week, Di=1-ri*(ti/360), where ri is the corresponding bank discount rate, ti is time in days
#     if ti<4 week, use fed fund overnight rate...

bdr=quandl.get("USTREASURY/BILLRATES", authtoken="DJsNViiWw63DhNuAsDxM", start_date="2019-3-18", end_date="2019-3-18").iloc[0,:][np.array([i%2==0 for i in range(10)])]
bdr_x=[4*7,8*7,13*7,26*7,52*7]
plt.figure(figsize=(6.5, 4))
plt.plot(bdr_x,bdr) # visualization
def BD(jk):
    # jk some array
    return(PchipInterpolator(bdr_x,bdr,extrapolate=False)(jk))
    
zr=quandl.get("FED/SVENY", api_key="DJsNViiWw63DhNuAsDxM", start_date="2019-3-18", end_date="2019-3-18").iloc[0,:]
zr_x=[((settlement+relativedelta(years=i))-settlement).days for i in range(1,30+1,1)]
plt.figure(figsize=(6.5, 4))
plt.plot(zr_x,zr) # visualization
def ZR(jk):
    # jk some array
    return(PchipInterpolator(zr_x,zr,extrapolate=False)(jk))

YFS=[DFS[0]/zr_x[0]+0.5*i for i in range(len(cashDate))]
if(settlement==cashDate[0]-relativedelta(months=6)):
    rate=["bank discount rate"]+["zero rate"]*(len(cashDate)-1)
    bd_t=np.array(DFS[0])
    bd=BD(bd_t)
    zr_t=YFS[1:]
    zr=ZR(np.array(DFS[1:]))
else:
    rate=["bank discount rate"]*2+["zero rate"]*(len(cashDate)-2)
    bd_t=np.array(DFS[:2])
    bd=BD(bd_t)
    zr_t=YFS[2:]
    zr=ZR(np.array(DFS[2:]))
discountFactor=(1-(bd/100)*(bd_t/360)).tolist()+(np.exp(-(zr/100)*np.array(zr_t))).tolist()
rate=list(map(lambda x: ": ".join(x), zip(rate,map(str,bd.tolist()+zr.tolist()))))
         

## Step 6: Integrate the information into the data frame and calculate discounted cash flows
cashDF["Years_From_Settlement"]=YFS
cashDF["Rate"]=rate
cashDF["Discount_Factor"]=discountFactor
cashDF["Discount_Cash_Flow"]=np.array(cashDF["Cash_Flow"])*np.array(cashDF["Discount_Factor"])
cashDF=cashDF.reindex(columns=["Cash_Date",
                               "Days_From_Settlement",
                               "Years_From_Settlement",
                               "Cash_Flow", 
                               "Rate", 
                               "Discount_Factor", 
                               "Discount_Cash_Flow"])
Pt0_dirty=sum(cashDF["Discount_Cash_Flow"])
Pt0_clean=Pt0_dirty-AI # Notice that it is a market practice in US to quote the clean price  

buy=96.859375
sell=96.843750
benchmark=(buy+sell)/2

np.abs(Pt0_clean-benchmark)