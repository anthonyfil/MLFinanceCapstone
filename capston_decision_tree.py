# imports
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn import linear_model
from sklearn import tree
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import roc_curve
import glob

# Grabbing Data

all_files = glob.glob(r"C:\Users\cheri\OneDrive\Documents\Computer Science\CleanedDataF42722\CleanedData" + "/*.csv")

li = []

for filename in all_files:
    df = pd.read_csv(filename, index_col=None, header=0)
    li.append(df)

new_li = []

# Cleaning data/data processing

li[10].rename(columns = {"DebtCurrent":"LongTermDebt"},inplace=True)


for df in li:
    new_li.append(df)

frame = pd.concat(new_li, axis=0, ignore_index=True)

frame.drop("date", inplace=True, axis=1)

frame = frame.dropna()

# convert frame to numpy
#numpy_2015_start = np.array(frame.to_numpy(dtype="float64"))

#Decision Tree

#Test with 1 var
new_frame = np.array(frame.to_numpy(dtype="float64"))
var_test_y = new_frame[:, -1]
new_frame = np.delete(new_frame, 3, axis=1)
var_test_x = new_frame[:, 0:5]

test_rows = new_frame[:, 0:5]

clf = tree.DecisionTreeRegressor(max_depth=15)
clf = clf.fit(var_test_x, var_test_y)
print(clf.get_depth())
results = clf.predict(test_rows)
tree.plot_tree(clf)

#Analysis - Find incorrect/correct predictions from test
ten_test = []
for i in range(56):
    ten_test.append(i)
ten = frame['deltaROA'].nlargest(n=56)
result_ten = pd.DataFrame(results)
result_ten = result_ten[0].nlargest(n=56)

ten_idx = ten.index
result_ten_idx = result_ten.index

print(ten_idx)

correct = 0
missed = 0
incorrect = 0
correct_flipped = 0

for i in range(564):
    if (i in result_ten_idx and i in ten_idx):
        print(i)
        correct += 1
    elif (i in ten_idx):
        missed += 1
    elif (i in result_ten_idx):
        incorrect += 1
    else:
        correct_flipped += 1

#Graph
frame['Rank'] = frame['deltaROA'].rank(method='dense', ascending=False)
        
        
#Output graph based on analyzed results  
y = []
x = []
reverse = frame.sort_values('deltaROA', ascending=False)
new_test = frame['deltaROA'].argsort(order='descending')
print(new_test)
test = []
for i in range(564):
    test.append(i)
reverse['newidx'] = test
frame['newidx'] = new_test
print(reverse['deltaROA'].iloc[1])
for i in range(564):
    #We correctly predicted top 10%
    if (i in result_ten_idx and i in ten_idx):
        print(i)
        plt.scatter(frame['deltaROA'].iloc[i], (frame['Rank'].iloc[i]*100/564),color='green')
        #plt.scatter(reverse['deltaROA'].iloc[i], (i * 100/564),color='green')
    #We predicted top 10% but it actually wasn't
    elif (i in result_ten_idx):
        plt.scatter(frame['deltaROA'].iloc[i], (frame['Rank'].iloc[i]*100/564),color='blue')
        #plt.scatter(reverse['deltaROA'].iloc[i], (i * 100/564), color='blue')
    #We didn't predict top 10% but it actually was
    elif (i in ten_idx):
        plt.scatter(frame['deltaROA'].iloc[i], (frame['Rank'].iloc[i]*100/564),color='red')
        #plt.scatter(reverse['deltaROA'].iloc[i], (i * 100/564), color='red')
    #elif (i not in result_ten_idx and i not in ten_idx):
    #    plt.scatter(x[i], y[i],color='green')
    #else:
    #    plt.scatter(x[i], y[i], color='clear')
plt.show()




#Offset - 1 Q Ridge test
#offset_1qr_li = []
#for df in new_li:
#    df = df.map(lambda x: df[x + 1, -1]/df[x, -1])

#frame = pd.concat(new_li, axis=0, ignore_index=True)

#frame.drop("date", inplace=True, axis=1)

# Data Processing
#numpy_2015_start = np.array(frame.to_numpy(dtype="float64"))

#print(numpy_2015_start)
#X = numpy_2015_start[:, 0:13]
#y = numpy_2015_start[:, -1]

#model_r = linear_model.Ridge(normalize= True, alpha= 35)
#model_r.fit(X,y)
#print('coef= ' , model_r.coef_)
#print('intercept= ' , model_r.intercept_)