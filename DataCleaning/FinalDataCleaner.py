import pandas
import os
from random import randint
from datetime import datetime
from os.path import exists


#Custom Data Structure For Storing CSV information
class sheet:
    def __init__(self, t):
        self.headers = ["date"]
        self.rows = []
        self.data = []
        self.ticker = t
    #Remove a row from the sheet
    def rmRow(self, row):
        self.rows.pop(row)
        for c in range(0,len(self.data)):
            self.data[c].pop(row)
    #remove a column from the sheet
    def rmCol(self, col):
        self.headers.pop(col)
        self.data.pop(col - 1)
    #add data to the sheet, places dat at column,row
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
        if str(row) in self.rows:
            r = self.rows.index(str(row))   
        else:
            self.rows.append(str(row))
            for i in range(0,len(self.headers) - 1):
                self.data[i].append("0")
            r = self.rows.index(str(row))
        self.data[c][r] = str(dat)

    #saves the current sheet to the file. adds '.csv' to the file
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

    #Loads info from the file
    def FromFile(self):
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

    #Prints the current sheet to the screen.
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

tickers = []
ciks = []
folders = []
requirements = []
seen = []
def PrintToLog(log):
    f = open("statusLog" + ".txt", 'a')
    f.write(str(datetime.now()) + "|" +  str(log) + "\n")
    f.close()




print("Data Extracter and Cleaner.\nDrawing CIK numbers from Settings\\TickerCIK.csv\nEnter (E)xtract to extract data from SEC data folders\nEnter (C)lean to clean extracted data\nEnter (B)oth to do both.\n")
answer = input();
doExtract = False;
doClean = False;
if(answer == "B" or answer == "Both"):
    doExtract = True;
    doClean = True;
if(answer == "C" or answer == "Clean"):
    doClean = True;
if(answer == "E" or answer == "Extract"):
    doExtract = True;


#Extracting Data
if(doExtract):
    for i in range(2009,2022):
        for j in range(1,5):
            folders.append("SECData\\" + str(i) + "q" + str(j) + "\\")





#Cleaning and Extracting
if(doExtract or doClean):
    #reading the ticker/cik list
    f = open("Settings\\TickerCIK.csv",'r')
    t_c = f.readlines()
    for l in range(0, len(t_c)):
        a = t_c[l].replace('\n','').split(',')
        if len(a) >= 2:
            tickers.append(a[0])
            ciks.append(a[1])
    f.close()
    #Opening the settings files
    #required stats means that in the cleaned files
    #we will only include quarters which have data for this stat
    #seen stats means it will show the data in the cleaned folder,
    #but will not cut a line if the data is absent.


    #this controls stats that are required for cleaned files
    f = open("Settings\\RequiredStats.csv",'r')
    t_c = f.readlines()
    for l in range(0, len(t_c)):
        a = t_c[l].replace('\n','').split(',')
        for s in a:
            requirements.append(s)
    f.close()


    #this controls stats that are seen in cleaned files
    f = open("Settings\\SeenStats.csv",'r')
    t_c = f.readlines()
    for l in range(0, len(t_c)):
        a = t_c[l].replace('\n','').split(',')
        for s in a:
            seen.append(s)
    f.close()



#Extracting Data
if(doExtract):
    for s in tickers:
        f = open("OutputData\\ExtractedData\\" + s + ".csv", 'a')
        f.close()

    print("Extracting Company Data From SECData");



    adshs = []
    #go through each folder for each quarter
    for fold in folders:
        #open the data(num.txt) and filings(sub.txt) files
        adshs = []
        for i in range(0,len(tickers)):
            adshs.append([])
        print("On Folder " + fold)
        valuesDF = pandas.read_csv(fold + "num.txt", sep='\t', lineterminator='\n', low_memory=False)
        compDF = pandas.read_csv(fold + "sub.txt", sep='\t', lineterminator='\n', low_memory=False)

        #Find all the adsh numbers associated with a companies cik
        for i in range(0, len(compDF["cik"])):
            if str(compDF["cik"][i]) in ciks:
                t = ciks.index(str(compDF["cik"][i]))
                adshs[t].append(compDF["adsh"][i])
        
        #for all the adsh numbers in the list find the data from it and add it to that companies sheet
        for i in range(0, len(valuesDF["adsh"])):
            for a in range(0, len(adshs)):
                if valuesDF["adsh"][i] in adshs[a]:
                    index = adshs[a].index(valuesDF["adsh"][i])
                    s = sheet("OutputData\\ExtractedData\\" + tickers[a])
                    s.FromFile()
                    s.addData(valuesDF["ddate"][i], valuesDF["tag"][i],valuesDF["value"][i])
                    s.ToFile()
        
    print("Done Extracting Data");







#print("Done Extracting Company Data, Now Cleaning Data");



def isfloat(num):
    try:
        float(num)
        return True
    except ValueError:
        return False


#Cleaning data
#here we take the files for each company and cut it down to the data we care about
#we also calculate a few of the indicators
if(doClean):

    for t in range(0, len(tickers)):
        #open file for the cleaned data and clear it
        file = open("OutputData\\CleanedData\\" + tickers[t] + ".csv","w")
        file.close()
        
        #set up the file to write into
        f = open("OutputData\\CleanedData\\" + tickers[t] + ".csv", 'a')
        
        f.write("date,DayRec,DTA,StR,ROA,NetProfitability,R&D,ROE,ROA,DPO,DTE,Trends,deltaROA,Assets,AccountsReceivableNetCurrent,AccountsReceivableNet,CostOfRevenue,Liabilities,StockholdersEquity,AccountsPayableCurrent,DebtCurrent,LongTermDebt,NetIncomeLoss,SalesRevenueNet,ResearchAndDevelopmentExpense")
        for s in seen:
            f.write("," + s)
        f.write("\n")

        f.write("0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0")
        for s in seen:
            f.write("," + "0")
        f.write("\n")
        f.close()

        #open in and out files
        clean = sheet("OutputData\\CleanedData\\" + tickers[t])
        clean.FromFile()
        unclean = sheet("OutputData\\ExtractedData\\" + tickers[t])
        unclean.FromFile()

        #create rows for all the quarters and sort them
        ds = []
        for d in range(2004,2022):
            for m in range(1,5):
                q = str(d)
                q = q + "q" + str(m)
                #print(q)
                ds.append(q)
        ds.sort()
        for d in ds:
            clean.addData(d, "deltaROA", "0")
        for d in unclean.rows:
            q = d[:(4 - len(d))]
        
            m = d[4:][:2]
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



        #go through the clean folder and average out any small gaps in the data
        for k in range(0, len(clean.data[0])):
            for j in range(0, len(clean.data)):
                if k > 0 and k < len(clean.data[0]) -1 and (clean.data[j][k] == 0 or clean.data[j][k] == "0" or clean.data[j][k] == "0.0"):
                    
                    behind = -1
                    ahead = -1
                    for l in range(1,5):
                        if behind == -1 and k-l > 0 and (clean.data[j][k-l] != 0 and clean.data[j][k-l] != "0" and clean.data[j][k-l] != "0.0"):
                            behind = l
                        if ahead == -1 and k+l < len(clean.data[0]) and (clean.data[j][k+l] != 0 and clean.data[j][k+l] != "0" and clean.data[j][k+l] != "0.0"):
                            ahead = l
                    if behind != -1 and ahead != -1:
                        clean.data[j][k] = str(((float(clean.data[j][k-behind])*(behind/(ahead+behind))) + (float(clean.data[j][k+ahead])*(ahead/(ahead+behind)))))
        
        #get indexes of items we will use to make calculations
        rdexpindex = clean.headers.index("ResearchAndDevelopmentExpense")
        netsaleindex = clean.headers.index("SalesRevenueNet")
        netIncomeIndex = clean.headers.index("NetIncomeLoss")
        dltindex = clean.headers.index("LongTermDebt")
        dcurrindex = clean.headers.index("DebtCurrent")
        apindex = clean.headers.index("AccountsPayableCurrent")
        dcurrindex = clean.headers.index("DebtCurrent")
        Equityindex = clean.headers.index("StockholdersEquity")
        Liabilityindex = clean.headers.index("Liabilities")
        cogsindex = clean.headers.index("CostOfRevenue")
        ARNindex = clean.headers.index("AccountsReceivableNet")
        ARNCindex = clean.headers.index("AccountsReceivableNetCurrent")
        Assetsindex = clean.headers.index("Assets")

        #calculate ROA, DTE, ROE etc
        for d in clean.rows:
            Dindex = clean.rows.index(d)
            if isfloat(clean.data[rdexpindex - 1][Dindex]) and isfloat(clean.data[netsaleindex - 1][Dindex]):
                if float(clean.data[netsaleindex - 1][Dindex]) == 0:
                    clean.addData(d, "R&D", 0);
                else:
                    rdexpRatio = float(clean.data[rdexpindex - 1][Dindex])/float(clean.data[netsaleindex - 1][Dindex])
                    clean.addData(d, "R&D", str(rdexpRatio));
            if isfloat(clean.data[dltindex - 1][Dindex]) and isfloat(clean.data[Equityindex - 1][Dindex]):
                if float(clean.data[Equityindex - 1][Dindex]) == 0:
                    clean.addData(d, "DTE", 0);
                    clean.addData(d, "ROE", 0);
                else:
                    dteRatio = (float(clean.data[dcurrindex - 1][Dindex])+float(clean.data[dltindex - 1][Dindex]))/float(clean.data[Equityindex - 1][Dindex])
                    clean.addData(d, "DTE", str(dteRatio));

                    roeRatio = (float(clean.data[netIncomeIndex - 1][Dindex]))/(float(clean.data[Equityindex - 1][Dindex]))
                    clean.addData(d, "ROE", str(roeRatio));
            if isfloat(clean.data[apindex - 1][Dindex]) and isfloat(clean.data[cogsindex - 1][Dindex]):

                if float(clean.data[cogsindex - 1][Dindex]) == 0:
                    clean.addData(d, "DPO", 0);
                else:
                    dpoRatio = 90*(float(clean.data[apindex - 1][Dindex]))/float(clean.data[cogsindex - 1][Dindex])
                    clean.addData(d, "DPO", str(dpoRatio));
            if isfloat(clean.data[netsaleindex - 1][Dindex]) and isfloat(clean.data[netIncomeIndex - 1][Dindex]):

                if float(clean.data[netsaleindex - 1][Dindex]) == 0:
                    clean.addData(d, "NetProfitability", 0);
                else:
                    netprofRatio = (float(clean.data[netIncomeIndex - 1][Dindex]))/float(clean.data[netsaleindex - 1][Dindex])
                    clean.addData(d, "NetProfitability", str(netprofRatio));

            if isfloat(clean.data[Assetsindex - 1][Dindex]) and isfloat(clean.data[netIncomeIndex - 1][Dindex]):

                if float(clean.data[Assetsindex - 1][Dindex]) == 0:
                    clean.addData(d, "ROA", 0);
                else:
                    ROARatio = (float(clean.data[netIncomeIndex - 1][Dindex]))/float(clean.data[Assetsindex - 1][Dindex])
                    clean.addData(d, "ROA", str(ROARatio));
                    if Dindex > 1 and float(clean.data[Assetsindex - 1][Dindex - 1]) != 0 and (float(clean.data[netIncomeIndex - 1][Dindex - 1]))/float(clean.data[Assetsindex - 1][Dindex - 1]) != 0:
                        deltROA = (ROARatio) - ((float(clean.data[netIncomeIndex - 1][Dindex - 1]))/float(clean.data[Assetsindex - 1][Dindex - 1]))
                        if abs(deltROA) >= 10:
                            clean.addData(d, "deltaROA", str(0));
                            #print("In Ticker = " + tickers[t] + " delta ROA=" + str(deltROA) + " Current ROA=" + str(ROARatio) + "Last ROA= " + str(((float(clean.data[netIncomeIndex - 1][Dindex - 1]))/float(clean.data[Assetsindex - 1][Dindex - 1]))))
                        else:
                            clean.addData(d, "deltaROA", str(deltROA))
                    else:
                        clean.addData(d, "deltaROA", str(0));

            strRatio = 0;
            if isfloat(clean.data[ARNCindex - 1][Dindex]) and isfloat(clean.data[ARNindex - 1][Dindex]) and isfloat(clean.data[netsaleindex - 1][Dindex]):

                if float(clean.data[ARNindex - 1][Dindex]) + float(clean.data[ARNCindex - 1][Dindex]) == 0:
                    clean.addData(d, "StR", 0);
                else:
                    strRatio = (float(clean.data[netsaleindex - 1][Dindex]))/(float(clean.data[ARNindex - 1][Dindex]) + float(clean.data[ARNCindex - 1][Dindex]))
                    clean.addData(d, "StR", str(strRatio));
            if isfloat(clean.data[Assetsindex - 1][Dindex]) and isfloat(clean.data[dcurrindex - 1][Dindex]) and isfloat(clean.data[dltindex - 1][Dindex]):

                if float(clean.data[Assetsindex - 1][Dindex]) == 0:
                    clean.addData(d, "DTA", 0);
                else:
                    dtaRatio = (float(clean.data[dcurrindex - 1][Dindex])+float(clean.data[dltindex - 1][Dindex]))/float(clean.data[Assetsindex - 1][Dindex])
                    clean.addData(d, "DTA", str(dtaRatio));
            if True:

                if strRatio == 0:
                    clean.addData(d, "DayRec", 0);
                else:
                    clean.addData(d, "DayRec", str(90/strRatio));
                
        #Average out any small gaps in the data
        for k in range(0, len(clean.data[0])):
            for j in range(0, len(clean.data)):
                if k > 0 and k < len(clean.data[0]) -1 and (clean.data[j][k] == 0 or clean.data[j][k] == "0" or clean.data[j][k] == "0.0"):
                    
                    behind = -1
                    ahead = -1
                    for l in range(1,5):
                        if behind == -1 and k-l > 0 and (clean.data[j][k-l] != 0 and clean.data[j][k-l] != "0" and clean.data[j][k-l] != "0.0"):
                            behind = l
                        if ahead == -1 and k+l < len(clean.data[0]) and (clean.data[j][k+l] != 0 and clean.data[j][k+l] != "0" and clean.data[j][k+l] != "0.0"):
                            ahead = l
                    if behind != -1 and ahead != -1:
                        clean.data[j][k] = str(((float(clean.data[j][k-behind])*(behind/(ahead+behind))) + (float(clean.data[j][k+ahead])*(ahead/(ahead+behind)))))
        clean.ToFile()
        ROEIN = clean.headers.index("ROE")
        ROAIN = clean.headers.index("ROA")
        DRIN = clean.headers.index("DayRec")
        STRIN = clean.headers.index("StR")
        DTAIN = clean.headers.index("DTA")
        DPOIN = clean.headers.index("DPO")
        DTEIN = clean.headers.index("DTE")
        nProfIN = clean.headers.index("NetProfitability")
        dROAIN = clean.headers.index("deltaROA")

        #cleaning to just the data we care about
        interestingIndexes = []
        for s in requirements:
            interestingIndexes.append(clean.headers.index(s))
        l = []
        i = 0
        for ind in interestingIndexes:
            
            if (i >= len(clean.data[0])):
                break
            while clean.data[ind - 1][i] == 0 or clean.data[ind - 1][i] == "0" or clean.data[ind - 1][i] == "0.0" or clean.data[ind - 1][i] == "nan" and clean.data[ind - 1][i] == "NaN":
                clean.rmRow(i)
                if i >= len(clean.data[0]):
                    break
            end = len(clean.data[ind - 1]) - 1
            while end > 0 and (clean.data[ind - 1][end] == 0 or clean.data[ind - 1][end] == "0" or clean.data[ind - 1][end] == "0.0" or clean.data[ind - 1][end] == "nan" and clean.data[ind - 1][end] == "NaN"):
                clean.rmRow(end)
                if i >= len(clean.data[ind - 1]):
                    break
                end = len(clean.data[ind - 1]) - 1
        clean.ToFile()

        #clean out any data columns we don't want
        i = 1
        
        variables = ["date"] 
        
        for s in seen:
            variables.append(s)
        while i < len(clean.headers):
            if not clean.headers[i] in variables:
                clean.rmCol(i)
            else:
                i = i + 1
        
        clean.ToFile()
        if len(clean.data) <= 1 or len(clean.data[0]) <= 1:
            os.remove("OutputData\\CleanedData\\" + tickers[t] + ".csv")
        print("Finished Cleaning " + tickers[t])
        PrintToLog("Finished " + tickers[t])

print("Finished")

