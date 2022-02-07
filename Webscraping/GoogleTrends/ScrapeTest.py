#import the libraries
import pandas as pd                        

import matplotlib.pyplot as plt
import time
from os.path import exists
from pytrends.request import TrendReq
pytrend = TrendReq()

#provide your search terms
MyKw=[
#['Apple', 'AAPL', 'Information technology'],
#['Boeing', 'BA', 'Aerospace and defense'],
#['Amgen', 'AMGN']#, 'Biopharmaceutical'],
['Chevron', 'CVX'],# 'Petroleum industry'],
['Cisco Systems', 'CSCO'],# 'Information technology'],
['Coca-Cola', 'KO'],# 'Soft Drink'],
['Disney', 'DIS'],# 'Broadcasting and entertainment'],
['Dow', 'DOW'],# 'Chemical industry'],
['Home Depot', 'HD'],# 'Home Improvement'],
['Honeywell', 'HON'],# 'Conglomerate'],
['IBM', 'IBM'],# 'Information technology'],
['Intel', 'INTC'],# 'Semiconductor industry'],
['Johnson & Johnson', 'JNJ'],# 'Pharmaceutical industry'],
['McDonald\'s', 'MCD'],# 'Food industry'],
['Merck', 'MRK'],# 'Pharmaceutical industry'],
['Microsoft', 'MSFT'],# 'Information technology'],
['Nike', 'NKE'],# 'Apparel'],
['Procter & Gamble', 'PG'],# 'Fast-moving consumer goods'],
['Salesforce', 'CRM'],# 'Information technology'],
['Walgreens Boots Alliance', 'WBA'],# 'Retailing'],
['Walmart', 'WMT'],# 'Retailing'],
['Caterpillar', 'CAT'],# 'Construction and Mining'],
['3M', 'MMM'],# 'Conglomerate']
    ]
testdf = pytrend.get_historical_interest(["stuff"], year_start=2018, month_start=1, day_start=1, hour_start=0, year_end=2018, month_end=2, day_end=1, hour_end=0, cat=0, geo='', gprop='', sleep=0)
print(testdf)
name = "DataCollection" + "_" + "test" + ".txt"
if exists(name):
    print("Already exists")
else:
    f = open(name, "a")
    means = testdf.mean(axis=0, skipna=True, level=None, numeric_only=None)
    print(means)
    f.write("Timestamp q1," + str(means[0]))
    f.write('\n')
    f.write("Finish")
    f.close()
for i in range(0, len(MyKw)):
    print("On i=" + str(i))
#historical interest
    for s in MyKw[i]:
        print("On s=" + s)

        ToPrint = []
        for y in range(2010, 2021):
            print("On y=" + str(y))

            if True:
                means = 0;
                histdf = []
                histdf = pytrend.get_historical_interest([s], year_start=y, month_start=1, day_start=1, hour_start=0, year_end=y, month_end=3, day_end=31, hour_end=0, cat=0, geo='', gprop='', sleep=1)
                means = histdf.mean(axis=0, skipna=True, level=None, numeric_only=None)
                print(histdf)               
                if(len(means) >= 1):
                    ToPrint.append(str(y) + "Q1," + str(means[0]))
                else:
                    ToPrint.append(str(y) + "Q1," + "No Data")
                means = 0;
                histdf = []
                time.sleep(30)
                histdf = pytrend.get_historical_interest([s], year_start=y, month_start=4, day_start=1, hour_start=0, year_end=y, month_end=6, day_end=30, hour_end=0, cat=0, geo='', gprop='', sleep=1)
                means = histdf.mean(axis=0, skipna=True, level=None, numeric_only=None)
                print(histdf)               
                if(len(means) >= 1):
                    ToPrint.append(str(y) + "Q2," + str(means[0]))
                else:
                    ToPrint.append(str(y) + "Q2," + "No Data")
                means = 0;
                histdf = []
                time.sleep(30)
                histdf = pytrend.get_historical_interest([s], year_start=y, month_start=7, day_start=1, hour_start=0, year_end=y, month_end=9, day_end=30, hour_end=0, cat=0, geo='', gprop='', sleep=1)
                means = histdf.mean(axis=0, skipna=True, level=None, numeric_only=None)
                print(histdf)               
                if(len(means) >= 1):
                    ToPrint.append(str(y) + "Q3," + str(means[0]))
                else:
                    ToPrint.append(str(y) + "Q3," + "No Data")
                means = 0;
                histdf = []
                time.sleep(30)
                histdf = pytrend.get_historical_interest([s], year_start=y, month_start=10, day_start=1, hour_start=0, year_end=y, month_end=12, day_end=31, hour_end=0, cat=0, geo='', gprop='', sleep=1)
                means = histdf.mean(axis=0, skipna=True, level=None, numeric_only=None)
                print(histdf)
                if(len(means) >= 1):
                    ToPrint.append(str(y) + "Q4," + str(means[0]))
                else:
                    ToPrint.append(str(y) + "Q4," + "No Data")
                time.sleep(1)

            print("Got 1 year Data\n")
            print(ToPrint)
            name = "DataCollection" + "_" + s + ".txt"
            f = open(name, "a")
            for l in range(0, len(ToPrint)):
                f.write(ToPrint[l])
                f.write('\n')
            f.close()
            ToPrint = []
        print("GotData")
print("Done\n")
