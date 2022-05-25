import csv
import kivy
kivy.require('2.1.0')

from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.lang.builder import Builder
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty

from subprocess import Popen, PIPE
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn import linear_model
from sklearn import tree
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import roc_curve
import glob
import time

# Data Grabbing

all_files = glob.glob("CleanedData/" + "/*.csv")

li = []

for filename in all_files:
    df = pd.read_csv(filename, index_col=None, header=0)
    li.append(df)

new_li = []

#Wanted_Dates = ['2017q1','2017q2','2017q3','2017q4','2018q1','2018q2','2018q3','2018q4','2019q1','2019q2','2019q3','2019q4','2020q1','2020q2','2020q3','2020q4','2021q1','2021q2','2021q3']
#li[0].drop("Liabilities", inplace=True, axis=1)
li[10].rename(columns = {"DebtCurrent":"LongTermDebt"},inplace=True)

#No offset

for df in li:
    new_li.append(df)

frame = pd.concat(new_li, axis=0, ignore_index=True)

frame.drop("date", inplace=True, axis=1)

frame = frame.dropna()

# Data Processing
numpy_2015_start = np.array(frame.to_numpy(dtype="float64"))

#print(numpy_2015_start)
#X = numpy_2015_start[:, 0:13]
#y = numpy_2015_start[:, -1]

#model_r = linear_model.Ridge(normalize= True, alpha= 35)
#model_r.fit(X,y)
#print('coef= ' , model_r.coef_)
#print('intercept= ' , model_r.intercept_)

#Decision Tree

#Test with 1 var
new_frame = np.array(frame.to_numpy(dtype="float64"))
var_test_y = new_frame[:, -1]
new_frame = np.delete(new_frame, 3, axis=1)
var_test_x = new_frame[:, 0:5]

test_row = new_frame[10, 0:5]

#test_rows = new_frame[:, 0:5]

clf = tree.DecisionTreeRegressor(max_depth=15)
clf = clf.fit(var_test_x, var_test_y)
tree.plot_tree(clf)

values = ['DayRec', 'DTA', 'StR', 'ROE', 'DTE']

arr = []

results = 0

class inputScreen(GridLayout):

    def __init__(self):
        super(inputScreen, self).__init__()
        self.cols = int(len(values)/2)

        self.inputs = values

        for i in range(0, len(values)):
            self.add_widget(Label(text=values[i]))
            self.inputs[i] = TextInput(multiline=False)
            self.add_widget(self.inputs[i])

        self.result = '\u0394'+"ROA"

        self.add_widget(Label(text='\u0394'+"ROA"))
        self.result = TextInput(multiline=False)
        self.result.text = str(results)
        
        self.add_widget(self.result)

        clear = Button(text="Clear")
        clear.bind(on_press=self.ClearText)
        analyze = Button(text="Analyze")
        analyze.bind(on_press=self.Analyze)
        """
        importCSV = Button(text="Import")
        importCSV.bind(on_press=self.importCSVFile)
        exitProg = Button(text="Exit")
        exitProg.bind(on_press=exit)
        """

        self.add_widget(clear)
        self.add_widget(analyze)
        """
        self.add_widget(importCSV)
        self.add_widget(exitProg)
        """

    def ClearText(self, *args):
        for i in self.inputs:
            i.text = '0'

    def Analyze(self, *args):
        arr = []
        for i in self.inputs:
            if(i.text == ""):
                i.text = '0'
                arr.append(i.text)
            else:
                arr.append(i.text)
        nparr = np.array(arr)
    
        results = clf.predict(nparr.reshape(1,-1))
        self.result.text = str(results)

    """    
    def importCSVFile(self, *args):
        arr = []
        
        process = Popen(['python3', 'openFile.py'], stdout=PIPE)
        stdout, stderr = process.communicate()

        with open(stdout[:-1], 'r') as file:
            reader = csv.reader(file)
            
            for row in reader:
                arr = row
        
        nparr = np.array(arr)
        
        results = clf.predict(nparr.reshape(1,-1))
        self.result.text = str(results)
    """

class MyApp(App):

    def build(self):
        self.title = 'UI'
        return inputScreen()

if __name__ == '__main__':
    MyApp().run()
