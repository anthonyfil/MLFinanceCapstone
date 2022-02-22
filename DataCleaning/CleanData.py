import pandas
import os
from random import randint
from datetime import datetime


class sheet:
    def __init__(self, t):
        self.headers = ["date"]
        self.rows = []
        self.data = []
        self.ticker = t
    def addData(self, row, column, dat):
        c = 0;
        r = 0;
        if column in self.headers:
            c = self.headers.index(str(column))-1   
        else:
            self.headers.append(str(column))
            l = []
            for i in range(0,len(self.rows)):
                l.append("nil")
            self.data.append(l)
            c = self.headers.index(str(column))-1
        #print(self.headers, self.rows, self.data)
        if str(row) in self.rows:
            r = self.rows.index(str(row))   
        else:
            self.rows.append(str(row))
            for i in range(0,len(self.headers) - 1):
                self.data[i].append("0")
            r = self.rows.index(str(row))
        #print(self.headers, self.rows, self.data)
        self.data[c][r] = str(dat)
    def ToFile(self):
        os.remove(self.ticker + ".csv")
        f = open(self.ticker + ".csv", 'a')
        l1 = ""
        for h in self.headers:
            l1 = l1 + h + ","
        l1 = l1[:-1]
        l1 = l1 + "\n"
        f.write(l1)
        for i in range(0, len(self.rows)):
            l =  str(self.rows[i]) + ","
            for j in range(0, len(self.headers)-1):
                l = l + str(self.data[j][i]) + ","
            l = l[:-1]
            l = l + "\n"
            f.write(l )
        f.close()
    def FromFile(self, bit):
        t = ".txt"
        if bit == 1:
            t = ".csv"
        with open(self.ticker + t, 'r') as f:
            lines = f.readlines()
            if(len(lines) >= 2):
                hs = lines[0].replace('\n', '').split(',')
                for i in range(1, len(lines)):
                    thisl = lines[i].replace('\n', '').split(',')
                    date = thisl[0]
                    for j in range(1, len(thisl)):
                        self.addData(date,hs[j], thisl[j])
            else:
                self.headers = ["date"]
                self.rows = []
                self.data = []
            f.close()       

    def PrintStruct(self):
        l1 = ""
        for h in self.headers:
            l1 = l1 + h + ","
        print(l1 + "\n")
        for i in range(0, len(self.rows)):
            l =  str(self.rows[i]) + ","
            for j in range(0, len(self.headers)-1):
                l = l + str(self.data[j][i]) + ","
            print(l + "\n")


tickers = ["SALESFORCE.COM, INC.",
           "HOME DEPOT, INC.",
           "MICROSOFT CORP",
           "MCDONALDS CORP",
           "AMGEN INC",
           "BOEING CO",
           "CATERPILLAR INC",
           "HONEYWELL INTERNATIONAL INC",
           "TRAVELERS COMPANIES, INC.",
           "APPLE INC",
           "JOHNSON & JOHNSON",
           "WALT DISNEY CO",
           "3M CO",
           "PROCTER & GAMBLE CO",
           "NIKE, INC.",
           "CHEVRON CORP",
           "WALMART INC.",
           "INTERNATIONAL BUSINESS MACHINES CORP",
           "MERCK & CO., INC.",
           "DOW INC.",
           "COCA COLA CO",
           "CISCO SYSTEMS, INC.",
           "WALGREENS BOOTS ALLIANCE, INC.",
           "INTEL CORP",
           ]
def PrintToLog(log):
    f = open("statusLog" + ".txt", 'a')
    f.write(str(datetime.now()) + "|" +  str(log) + "\n")
    f.close()


for t in range(0, len(tickers)):
    f = open("CleanedData\\" + tickers[t] + ".csv", 'a')
    f.write("date,R&D,ROE,DPO,DTE,Trends,Assets,AssetsCurrent,NoncurrentAssets,AccountsPayable,AccountsPayableCurrent,AccountsReceivableNetCurrent,InventoryNet,Liabilities,LiabilitiesCurrent,PreconfirmationCurrentAssets,OtherAssetsNonCurrent,AssetsFairValueDisclosure,SellingGeneralAndAdministrativeExpense,RepaymentsOfNotesPayable,ResearchDevelopmentAndRelatedExpenses,ResearchAndDevelopmentExpense,SalesRevenueNet,DeferredRevenueCurrent,DebtCurrent,LongTermDebt,LongTermDebtCurrent,LongTermDebtNoneCurrent,OtherLongTermDebt,RepaymentsOfLongTermDebt,InterestExpenseDebt,LiabilitiesAndStockholdersEquity,StockholdersEquity,StockholdersEquityOther\n")
    f.write("0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,00,0,0,0,0\n")
    f.close()
    clean = sheet("CleanedData\\" + tickers[t])
    clean.FromFile(1)
    unclean = sheet(tickers[t])
    unclean.FromFile(0)
    ds = []
    for d in range(2011,2021):
        for m in range(1,4):
            q = str(d)
            m = "q" + str(m)
            ds.append(q)
    ds.sort()
    fil = open("Trend\\" + tickers[t] + ".csv", 'r')
    lins = fil.readlines()
    q1 = []
    q2 = []
    q3 = []
    q4 = []
    for l in range(3, len(lins)):

        parts = lins[l].split(',')
        date = parts[0].split('-')
        if int(date[0]) >= 2011:
            
            q = date[0]
            m = date[1]
            if m == "01" or m == "02" or m == "03":
                q = q + "q1"
                q1.append(parts[1])
                if len(q1) >= 3:
                    avg = 0;
                    for i in q1:
                        avg = avg + int(i.replace('\n',''))
                    avg = avg/3
                    clean.addData(q, "Trends", str(avg));
                    q1 = []
            if m == "04" or m == "05" or m == "06":
                q = q + "q2"
                q2.append(parts[1])
                if len(q2) >= 3:
                    avg = 0;
                    for i in q2:
                        avg = avg + int(i.replace('\n',''))
                    avg = avg/3
                    clean.addData(q, "Trends", str(avg));
                    q2 = []
            if m == "07" or m == "08" or m == "09":
                q = q + "q3"
                q3.append(parts[1])
                if len(q3) >= 3:
                    avg = 0;
                    for i in q3:
                        avg = avg + int(i.replace('\n',''))
                    avg = avg/3
                    clean.addData(q, "Trends", str(avg));
                    q3 = []
            if m == "10" or m == "11" or m == "12":
                q = q + "q4"
                q4.append(parts[1])
                if len(q4) >= 3:
                    avg = 0;
                    for i in q4:
                        avg = avg + int(i.replace('\n',''))
                    avg = avg/3
                    print(avg)
                    clean.addData(q, "Trends", str(avg));
                    q4 = []
            
    fil.close()
    clean.ToFile()
    for d in unclean.rows:
        q = d[:-4]
        m = d[:-2][4:]
        if m == "01" or m == "02" or m == "03":
            q = q + "q1"
        if m == "04" or m == "05" or m == "06":
            q = q + "q2"
        if m == "07" or m == "08" or m == "09":
            q = q + "q3"
        if m == "10" or m == "11" or m == "12":
            q = q + "q4"
        for h in unclean.headers:
            if h in clean.headers:
                j = unclean.headers.index(h)
                k = unclean.rows.index(d)
                PrintToLog(str(q) +  h + unclean.data[j - 1][k])
                if unclean.data[j-1][k] != "nil":
                    clean.addData(q, h, unclean.data[j - 1][k])
    clean.ToFile()
    rdexpindex = clean.headers.index("ResearchAndDevelopmentExpense")
    netsaleindex = clean.headers.index("SalesRevenueNet")
    dltindex = clean.headers.index("LongTermDebt")
    dcurrindex = clean.headers.index("DebtCurrent")
    apindex = clean.headers.index("AccountsPayableCurrent")
    dcurrindex = clean.headers.index("DebtCurrent")
    for d in clean.rows:
        Dindex = clean.rows.index(d)
        if clean.data[netsaleindex - 1][Dindex] == "0":
            clean.addData(d, "R&D", 0);
        else:
            rdexpRatio = float(clean.data[rdexpindex - 1][Dindex])/float(clean.data[netsaleindex - 1][Dindex])
            clean.addData(d, "R&D", str(rdexpRatio));

        dteRatio = float(clean.data[dltindex - 1][Dindex]) + float(clean.data[dcurrindex - 1][Dindex])
        clean.addData(d, "DTE", str(dteRatio));

    clean.ToFile()

            
    PrintToLog("Finished " + tickers[t])
    #s.addData(valuesDF["ddate"][i], valuesDF["tag"][i],valuesDF["value"][i])


'''               
for i in range(0, len(valuesDF["adsh"])):
    for a in range(0, len(adshs)):
        if valuesDF["adsh"][i] in adshs[a]:
            print(tickers[a],str(valuesDF["ddate"][i]), str(valuesDF["tag"][i]),str(valuesDF["value"][i]))
            index = adshs[a].index(valuesDF["adsh"][i])
            s = sheet(tickers[a], adshs[a][index])
            s.FromFile()
            s.addData(valuesDF["ddate"][i], valuesDF["tag"][i],valuesDF["value"][i])
            #print("Pre-Save")
            #s.PrintStruct()
            s.ToFile()
            s.FromFile()
            #print("Post-Save")
            #s.PrintStruct()
'''


               

