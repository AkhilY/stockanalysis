import sys
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication, QDialog
from PyQt5.uic import loadUi
import quandl
import math
import dash
import dash_core_components as dcc
import dash_html_components as html
import threading
import numpy as np
from sklearn.svm import SVR
import matplotlib.pyplot as plt 

quandl.ApiConfig.api_key = "Ui3JT8HDDV3vnADUsD2k"

class LondonStocks(QDialog):
    #link the UI
    def __init__(self):
        super(LondonStocks,self).__init__()
        loadUi('LondonStocks.ui', self)
        #call the fill combobox function
        x=self.fillCombobox()
        #call the function to take the text from the combobox
        self.pushButton.clicked.connect(self.averageStock)
        #call the function to graph a stock
        self.pushButton_2.clicked.connect(self.visual)
        #call the function to calculate calculate correlation
        self.pushButton_3.clicked.connect(self.calcCoCo)
        #call the function to graph correlation data
        self.pushButton_4.clicked.connect(self.visual2)
        #call the function to graph related data
        self.pushButton_5.clicked.connect(self.visual3)
        #call the function to calculate future average stock price
        self.pushButton_6.clicked.connect(self.futureAverageStock)
        #call the function to graph the future stock prices
        self.pushButton_7.clicked.connect(self.visual4)
        
        
    #function for filling the comboboxes
    def fillCombobox(self):
        companies=['XLON/AEO', 'XLON/ABBY', 'XLON/ADIG', 'XLON/ABF', 'XLON/AEP', 'XLON/AAL', 'XLON/AGK', 'XLON/AFN', 'XLON/AAS', 'XLON/AEFS']
        #fill the stock comboboxes
        for company in companies:
            self.comboBox.addItem(company)
            self.comboBox_5.addItem(company)
            self.comboBox_8.addItem(company)
            self.comboBox_10.addItem(company)
            self.comboBox_12.addItem(company)
        #fill the year comboboxes    
        for i in range(2007, 2019):
            self.comboBox_2.addItem(str(i))
            self.comboBox_3.addItem(str(i))
            self.comboBox_4.addItem(str(i))
            self.comboBox_6.addItem(str(i))
            self.comboBox_7.addItem(str(i))
            self.comboBox_9.addItem(str(i))
        #fill the future year comboBox
        for i in range(2019, 2025):
            self.comboBox_14.addItem(str(i))
            
    #function for taking the text from the comboboxes
    def averageStock(self):
        company=self.comboBox.currentText()
        year_start=int(self.comboBox_2.currentText())
        year_end=int(self.comboBox_3.currentText())
        listC = []
        totalC = 0
        for i in range(year_start, year_end+1):
            df = quandl.get(company, start_date = str(i)+"-01-01", end_date = str(i)+"-12-31")
            y = df["High"].mean()
            listC.append(y)
            totalC += y
        avgC = totalC / len(listC)
        self.textEdit.setText(str(avgC))
        
    #functions to graph a stock
    def visual(self):
        threading.Thread(target=self.graph, daemon=True).start()
    def graph(self):
        #make the list for the y values
        company=self.comboBox_5.currentText()
        year_start=int(self.comboBox_4.currentText())
        year_end=int(self.comboBox_6.currentText())
        listC = []
        totalC = 0
        for i in range(year_start, year_end+1):
            print(i)
            df = quandl.get(company, start_date = str(i)+"-01-01", end_date = str(i)+"-12-31")
            y = df["High"].mean()
            listC.append(y)
            print(y,listC)
        #make the list for the x values
        years=[]
        for i in range(year_start, year_end+1):
            years.append(i)
        
        #make the graph
        app = dash.Dash()

        app.layout = html.Div(children=[
            html.H1(children=str(company)+' Graph'),
            html.Div(children='Graph of '+str(company)+' In The Years '+str(year_start)+' through '+str(year_end)
            ),

            dcc.Graph(
                id='ui-graphicvisualization',
                figure={
                    'data': [
                        {'x': years, 'y': listC, 'type': 'line', 'name': company},
                    ],
                    'layout': {
                        'title': str(company)
                    }
                }
            )
    
        ])

        app.run_server(port=1111)
        
    #function to calculate correlation
    def calcCoCo(self):
        inputCompany=self.comboBox_8.currentText()
        company=self.comboBox_10.currentText()
        year_start=int(self.comboBox_7.currentText())
        year_end=int(self.comboBox_9.currentText())
        listInput = []
        totalInput = 0
        listComp = []
        totalComp = 0 
        for i in range(year_start, year_end+1):
            df = quandl.get(inputCompany, start_date = str(i)+"-01-01", end_date = str(i)+"-12-31")
            df2 = quandl.get(company, start_date = str(i)+"-01-01", end_date = str(i)+"-12-31")


            y = df["High"].mean()
            x= df2["High"].mean()


            listInput.append(y)
            totalInput += y


            listComp.append(x)
            totalComp += x
    

        avgInput = totalInput / len(listInput)
        avgComp = totalComp / len(listComp)

        listCompSquared = []
        listInputSquared = []
        mult = []
        #to find the standard devations, u nee to find bot lists squared
        for i in listInput:
            listInputSquared.append(i**2)

        for i in listComp:
            listCompSquared.append(i**2)
        #to print out the multiplication of both the values in both lists, set a varaibe for both equal to the i'th number in each list. When i is 2 in the for loop, the variable will be list[i]
        for i in range(0, len(listInput)):
            itemInput = listInput[i]
            itemComp = listComp[i]
            mult.append(itemComp * itemInput)
        #find the average of he squared list

        sumPowInput = sum(listInputSquared)
        avgSquareInput = sumPowInput / len(listInputSquared)
        sumPowComp = sum(listCompSquared)
        avgSquareComp = sumPowComp / len(listCompSquared)
        sumMult = sum(mult)
        avgMult = sum(mult)/len(mult)
        varInput = avgSquareInput - (avgInput **2 )
        varComp = avgSquareComp - (avgComp **2 )
        coVar = (avgMult) - (avgInput * avgComp)
        CoCo = coVar / (math.sqrt(varInput * varComp))
        self.textEdit_2.setText(str(CoCo))
    #functions for graphing correlation between two stocks
    def visual2(self):
        threading.Thread(target=self.graph2, daemon=True).start()
    def graph2(self):
        inputCompany=self.comboBox_8.currentText()
        company=self.comboBox_10.currentText()
        year_start=int(self.comboBox_7.currentText())
        year_end=int(self.comboBox_9.currentText())
        listInput = []
        totalInput = 0
        listComp = []
        totalComp = 0 
        for i in range(year_start, year_end+1):
            df = quandl.get(inputCompany, start_date = str(i)+"-01-01", end_date = str(i)+"-12-31")
            df2 = quandl.get(company, start_date = str(i)+"-01-01", end_date = str(i)+"-12-31")


            y = df["High"].mean()
            x= df2["High"].mean()


            listInput.append(y)
            totalInput += y


            listComp.append(x)
            totalComp += x
    

        avgInput = totalInput / len(listInput)
        avgComp = totalComp / len(listComp)

        listCompSquared = []
        listInputSquared = []
        mult = []
        #to find the standard devations, u nee to find bot lists squared
        for i in listInput:
            listInputSquared.append(i**2)

        for i in listComp:
            listCompSquared.append(i**2)
        #to print out the multiplication of both the values in both lists, set a varaibe for both equal to the i'th number in each list. When i is 2 in the for loop, the variable will be list[i]
        for i in range(0, len(listInput)):
            itemInput = listInput[i]
            itemComp = listComp[i]
            mult.append(itemComp * itemInput)
        #find the average of he squared list

        sumPowInput = sum(listInputSquared)
        avgSquareInput = sumPowInput / len(listInputSquared)
        sumPowComp = sum(listCompSquared)
        avgSquareComp = sumPowComp / len(listCompSquared)
        sumMult = sum(mult)
        avgMult = sum(mult)/len(mult)
        varInput = avgSquareInput - (avgInput **2 )
        varComp = avgSquareComp - (avgComp **2 )
        coVar = (avgMult) - (avgInput * avgComp)
        CoCo = coVar / (math.sqrt(varInput * varComp))
        #make the x list consisting of the years
        years=[]
        for i in range(year_start, year_end+1):
            years.append(i)
        app = dash.Dash()
        app.layout = html.Div(children=[
            html.H1(children='Correlation Coefficients'),
            html.Div(children=''' 
                Graphs each company with eachother 
            '''),

            dcc.Graph(
                id='example-graph-5',
                figure={
                    'data': [
                        {'x': years, 'y': listInput, 'type': 'line', 'name': inputCompany},
                        {'x': years, 'y': listComp, 'type': 'line', 'name': company},
                    ],
                    'layout': {
                        'title': 'Correlation= '+str(CoCo)
                    }
                }
            ),
        ])
        app.run_server(port=2222)
    #functions for graphing correlation between first stock and list of other stocks
    def visual3(self):
        threading.Thread(target=self.graph3, daemon=True).start()
    def graph3(self):
        inputCompany=self.comboBox_8.currentText()
        year_start=int(self.comboBox_7.currentText())
        year_end=int(self.comboBox_9.currentText())
        #list of companies to loop through
        companies=['XLON/AEO', 'XLON/ABBY', 'XLON/ADIG', 'XLON/ABF', 'XLON/AEP', 'XLON/AAL', 'XLON/AGK',
                   'XLON/AFN', 'XLON/AAS', 'XLON/AEFS']
        #dictionary with each company and its correlation coefficient
        stockList=[]
        absstock=[]
        absstockDiction={}
        randstockDiction={}
        stockList=[]
        absstock=[]
        absstockDiction={}
        randstockDiction={}
        avgValuesDiction={}
        #calculate correlation for each company and append the values to a dictionary
        for company in companies:
            listInput = []
            totalInput = 0
            listComp = []
            totalComp = 0 
            for i in range(year_start, year_end+1):
                df = quandl.get(inputCompany, start_date = str(i)+"-01-01", end_date = str(i)+"-12-31")
                df2 = quandl.get(company, start_date = str(i)+"-01-01", end_date = str(i)+"-12-31")
                y = df["High"].mean()
                x= df2["High"].mean()
                listInput.append(y)
                totalInput += y
                listComp.append(x)
                totalComp += x
            avgInput = totalInput / len(listInput)
            avgComp = totalComp / len(listComp)
            listCompSquared = []
            listInputSquared = []
            mult = []
            for i in listInput:
                listInputSquared.append(i**2)
            for i in listComp:
                listCompSquared.append(i**2)
            for i in range(0, len(listInput)):
                itemInput = listInput[i]
                itemComp = listComp[i]
                mult.append(itemComp * itemInput)
            sumPowInput = sum(listInputSquared)
            avgSquareInput = sumPowInput / len(listInputSquared)
            sumPowComp = sum(listCompSquared)
            avgSquareComp = sumPowComp / len(listCompSquared)
            sumMult = sum(mult)
            avgMult = sum(mult)/len(mult)
            varInput = avgSquareInput - (avgInput **2 )
            varComp = avgSquareComp - (avgComp **2 )
            coVar = (avgMult) - (avgInput * avgComp)
            CoCo = coVar / (math.sqrt(varInput * varComp))
            #append values to dictionaries/lists
            randstockDiction[company]=CoCo
            absstockDiction[abs(CoCo)]=company
            absstock.append(abs(CoCo))
            avgValuesDiction[inputCompany]=listInput
            avgValuesDiction[company]=listComp
        #make final sorted dictionary
        absstock=sorted(absstock)
        i=9
        while i>=0:
            comp=absstockDiction[absstock[i]]
            stockList.append([comp,randstockDiction[comp]])
            i=i-1
        #graph the related data
        years=[]
        for i in range(year_start, year_end+1):
            years.append(i)
        app = dash.Dash()
        app.layout = html.Div(children=[
            html.H1(children='Correlation Coefficients: Related Data'),
            html.Div(children=''' 
                Graphs each company with eachother and finds the correlation coefficient. 
            '''),

            dcc.Graph(
                id='example-graph-6',
                figure={
                    'data': [
                        {'x': years, 'y': avgValuesDiction[inputCompany], 'type': 'line', 'name': inputCompany},
                        {'x': years, 'y': avgValuesDiction[stockList[0][0]], 'type': 'line', 'name': stockList[0][0]},
                    ],
                    'layout': {
                                'title': 'Correlation between ' +str(inputCompany) + ' and ' + str(stockList[0][0]) +'= '+str(stockList[0][1])
                    }
                }
            ),
            dcc.Graph(
                id='example-graph-7',
                figure={
                    'data': [
                        {'x': years, 'y': avgValuesDiction[inputCompany], 'type': 'line', 'name': inputCompany},
                        {'x': years, 'y': avgValuesDiction[stockList[1][0]], 'type': 'line', 'name': stockList[1][0]},
                    ],
                    'layout': {
                                'title': 'Correlation between ' +str(inputCompany) + ' and ' + str(stockList[1][0]) +'= '+str(stockList[1][1])
                    }
                }
            ),
            dcc.Graph(
                id='example-graph-8',
                figure={
                    'data': [
                        {'x': years, 'y': avgValuesDiction[inputCompany], 'type': 'line', 'name': inputCompany},
                        {'x': years, 'y': avgValuesDiction[stockList[2][0]], 'type': 'line', 'name': stockList[2][0]},
                    ],
                    'layout': {
                                'title': 'Correlation between ' +str(inputCompany) + ' and ' + str(stockList[2][0]) +'= '+str(stockList[2][1])
                    }
                }
            ),
            dcc.Graph(
                id='example-graph-9',
                figure={
                    'data': [
                        {'x': years, 'y': avgValuesDiction[inputCompany], 'type': 'line', 'name': inputCompany},
                        {'x': years, 'y': avgValuesDiction[stockList[3][0]], 'type': 'line', 'name': stockList[3][0]},
                    ],
                    'layout': {
                                'title': 'Correlation between ' +str(inputCompany) + ' and ' + str(stockList[3][0]) +'= '+str(stockList[3][1])
                    }
                }
            ),
            dcc.Graph(
                id='example-graph-10',
                figure={
                    'data': [
                        {'x': years, 'y': avgValuesDiction[inputCompany], 'type': 'line', 'name': inputCompany},
                        {'x': years, 'y': avgValuesDiction[stockList[4][0]], 'type': 'line', 'name': stockList[4][0]},
                    ],
                    'layout': {
                                'title': 'Correlation between ' +str(inputCompany) + ' and ' + str(stockList[4][0]) +'= '+str(stockList[4][1])
                    }
                }
            ),
            dcc.Graph(
                id='example-graph-11',
                figure={
                    'data': [
                        {'x': years, 'y': avgValuesDiction[inputCompany], 'type': 'line', 'name': inputCompany},
                        {'x': years, 'y': avgValuesDiction[stockList[5][0]], 'type': 'line', 'name': stockList[5][0]},
                    ],
                    'layout': {
                                'title': 'Correlation between ' +str(inputCompany) + ' and ' + str(stockList[5][0]) +'= '+str(stockList[5][1])
                    }
                }
            ),
            dcc.Graph(
                id='example-graph-12',
                figure={
                    'data': [
                        {'x': years, 'y': avgValuesDiction[inputCompany], 'type': 'line', 'name': inputCompany},
                        {'x': years, 'y': avgValuesDiction[stockList[6][0]], 'type': 'line', 'name': stockList[6][0]},
                    ],
                    'layout': {
                                'title': 'Correlation between ' +str(inputCompany) + ' and ' + str(stockList[6][0]) +'= '+str(stockList[6][1])
                    }
                }
            ),
            dcc.Graph(
                id='example-graph-13',
                figure={
                    'data': [
                        {'x': years, 'y': avgValuesDiction[inputCompany], 'type': 'line', 'name': inputCompany},
                        {'x': years, 'y': avgValuesDiction[stockList[7][0]], 'type': 'line', 'name': stockList[7][0]},
                    ],
                    'layout': {
                                'title': 'Correlation between ' +str(inputCompany) + ' and ' + str(stockList[7][0]) +'= '+str(stockList[7][1])
                    }
                }
            ),
            dcc.Graph(
                id='example-graph-14',
                figure={
                    'data': [
                        {'x': years, 'y': avgValuesDiction[inputCompany], 'type': 'line', 'name': inputCompany},
                        {'x': years, 'y': avgValuesDiction[stockList[8][0]], 'type': 'line', 'name': stockList[8][0]},
                    ],
                    'layout': {
                                'title': 'Correlation between ' +str(inputCompany) + ' and ' + str(stockList[8][0]) +'= '+str(stockList[8][1])
                    }
                }
            ),
            dcc.Graph(
                id='example-graph-15',
                figure={
                    'data': [
                        {'x': years, 'y': avgValuesDiction[inputCompany], 'type': 'line', 'name': inputCompany},
                        {'x': years, 'y': avgValuesDiction[stockList[9][0]], 'type': 'line', 'name': stockList[9][0]},
                    ],
                    'layout': {
                                'title': 'Correlation between ' +str(inputCompany) + ' and ' + str(stockList[9][0]) +'= '+str(stockList[9][1])
                    }
                }
            )
        ])
        app.run_server(port=3333)
    #function to calculate future average stock price
    def futureAverageStock(self):
        company=self.comboBox_12.currentText()
        years=[]
        prices=[]
        for i in range(2007,2019):
            #make a list of years from 2007 to 2018
            years.append(i)
            #make a list of averages for each year
            df=quandl.get(company, start_date=str(i)+"-01-01", end_date=str(i)+"-12-31")
            y=df["High"].mean()
            prices.append(y)
        #create variable for third parameter of predict_stock_prices function  
        futureYear=int(self.comboBox_14.currentText())
        x=(futureYear-2018)*365
        def predict_stock_prices(years, prices, x):
            years = np.reshape(years,  (len(years),1 ))
            #prices = np.reshape(prices, (len(prices),1))

            svr_rbf = SVR(kernel = 'rbf', C=1e3, gamma=0.1)
            svr_rbf.fit(years, prices)
    

            print('Printing results')
            return svr_rbf.predict(x)[0]
        predicted_prices = predict_stock_prices(years, prices, [[x]])
        self.textEdit_3.setText(str(predicted_prices))
    def visual4(self):
        threading.Thread(target=self.graph4, daemon=True).start()
    def graph4(self):
        quandl.ApiConfig.api_key = "Ui3JT8HDDV3vnADUsD2k"

        company=self.comboBox_12.currentText()

        years=[]
        prices=[]
        for i in range(2007,2019):
            #make a list of years from 2007 to 2018
            years.append(i)
            #make a list of averages for each year
            df=quandl.get(company, start_date=str(i)+"-01-01", end_date=str(i)+"-12-31")
            y=df["High"].mean()
            prices.append(y)
        #function for calculating the future stock price
        def predict_stock_prices(years, prices, x):
            years = np.reshape(years,  (len(years),1 ))

            svr_rbf = SVR(kernel = 'rbf', C=1e3, gamma=0.1)
            svr_rbf.fit(years, prices)
    

            print('Printing results')
            return svr_rbf.predict(x)[0]



        #make the average list for the graph and append the future values
        year_start=2015
        year_end=2018
        listC = []
        totalC = 0
        for i in range(year_start, year_end+1):
            df = quandl.get(company, start_date = str(i)+"-01-01", end_date = str(i)+"-12-31")
            y = df["High"].mean()
            listC.append(y)
        #append the future values
            #create variable for third parameter of predict_stock_prices function  
            futureYear=i
            x=(futureYear-2018)*365
            listC.append(predict_stock_prices(years, prices, [[x]]))

        #make the list for the x values
        years=[]
        for i in range(2015, 2026):

            years.append(i)

    
        #make the graph
        app = dash.Dash()

        app.layout = html.Div(children=[
            html.H1(children=str(company)+' Graph'),
            html.Div(children='Graph of '+str(company)+' In The Years '+str(year_start)+' through 2020'
            ),

            dcc.Graph(
                id='ui-graphicvisualization',
                figure={
                    'data': [
                        {'x': years, 'y': listC, 'type': 'line', 'name': company},
                    ],
                    'layout': {
                        'title': str(company)
                    }
                }
            )
    
        ])

        app.run_server(port=5555)
        
