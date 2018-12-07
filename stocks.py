#APPL = first ticker
#TSLA = second ticker
import quandl
import sys
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication, QDialog
from PyQt5.uic import loadUi
import dash
import dash_core_components as dcc
import dash_html_components as html
import threading
import webbrowser
import operator
import math
import numpy as np
from sklearn.svm import SVR
import matplotlib.pyplot as plt 

class AppWindow2(QDialog):
    def __init__(self):
        quandl.ApiConfig.api_key = "zmEJw-5s6WZrEmH4pJ7U"
        super(AppWindow2, self).__init__()
        loadUi('stock.ui',self)
        self.comboBoxes()
        self.pushButton.clicked.connect(self.AvgPrice)
        self.pushButton_4.clicked.connect(self.corrCoff)
        self.pushButton_7.clicked.connect(self.choose2)
        self.pushButton_3.clicked.connect(self.choose3)
        self.pushButton_2.clicked.connect(self.choose4)
        self.pushButton_5.clicked.connect(self.choose5)
        self.pushButton_6.clicked.connect(self.futureAverageStock)

    def comboBoxes(self):
        #quandl.ApiConfig.api_key = "zmEJw-5s6WZrEmH4pJ7U"

        stocks = ["AAPL", "TSLA", "GOOG", "MSFT", "INTC", "AMZN", "FB", "JNJ", "JPM", "XOM", "BAC", "WMT", "WFC"]
        for i in range(0, len(stocks), 1):
            self.comboBox.addItem(stocks[i])
        year = 1997
        for n in range(1996, 2019):
            self.comboBox_2.addItem(str(n))
        for m in range(1996, 2019):
            self.comboBox_15.addItem(str(m))
        for b in range(0, len(stocks), 1):
            self.comboBox_3.addItem(stocks[b])
        for v in range(1996, 2019):
            self.comboBox_5.addItem(str(v))
        for c in range(1996, 2019):
            self.comboBox_6.addItem(str(c))
        for x in range(0, len(stocks), 1):
            self.comboBox_7.addItem(stocks[x])
        for s in range(2019, 2040):
            self.comboBox_10.addItem(str(s))
        for d in range(0, len(stocks), 1):
            self.comboBox_11.addItem(stocks[d])
        for g in range(0, len(stocks), 1):
            self.comboBox_12.addItem(stocks[g])
        for h in range(1996, 2019):
            self.comboBox_13.addItem(str(h))
        for j in range(1996, 2019):
            self.comboBox_14.addItem(str(j))
        columns = ["Open", "Close", "High", "Low"]
        for f in range(0, len(columns), 1):
            self.comboBox_4.addItem(columns[f])
        
    def AvgPrice(self):
        stock = self.comboBox.currentText()
        startdate = self.comboBox_2.currentText()
        enddate = self.comboBox_15.currentText()
        column = self.comboBox_4.currentText()
        avgs = []
        for i in range(int(startdate), int(enddate)+1, 1):
            df = quandl.get("WIKI/" + str(stock), start_date=str(i)+"-01-01", end_date=str(i)+"-12-31")
            avg = df[column].mean()
            avgs.append(avg)
        ans = 0
        for e in range(len(avgs)):
            ans += float(avgs[e])
        w = ans / len(avgs)
        self.textEdit.setText(str(w))

    def corrCoff(self):
        stock = self.comboBox_11.currentText()
        stock2 = self.comboBox_12.currentText()
        startdate = self.comboBox_13.currentText()
        enddate = self.comboBox_14.currentText()
        avgs = []
        avgs2 = []
        for i in range(int(startdate), int(enddate)+1):
            df = quandl.get("WIKI/"+ str(stock), start_date=str(i)+"-01-01", end_date=str(i)+"-12-31")
            df2 = quandl.get("WIKI/"+ str(stock2), start_date=str(i)+"-01-01", end_date=str(i)+"-12-31")
            avg = df["Close"].mean() #Average colsing price for AAPL eah day
            avg2 = df2["Close"].mean() #Average closing price for TSLA each day
            avgs.append(avg)
            avgs2.append(avg2)
        #print(avgs)
        #print(avgs2)
        cls = df["Close"].var() #variance of both tickers
        cls2 = df2["Close"].var()
        
        #print(cls)
        #print(cls2)
        times = []
        for n in range(0, len(avgs), 1):
            time = avgs[n]*avgs2[n] #AAPL * TSLA
            times.append(time)
        #print(times)
        avgss = sum(avgs)/len(avgs) #Average Value of whole AAPL column
        avgss2 = sum(avgs2)/len(avgs2) #average Value of whole TSLA column
        sqrs = []
        sqrs2 = []
        for u in range(0, len(avgs), 1):
            sqr = avgs[u]**2 #Square root of each day in AAPL
            sqr2 = avgs2[u]**2 #Square root of each day in TSLA
            sqrs.append(sqr)
            sqrs2.append(sqr2)
        sqrss = sum(sqrs)/ len(sqrs)#Average of square root colums
        sqrss2 = sum(sqrs2)/len(sqrs2)
        timess = sum(times)/ len(times) #Average of AAPL*TSLA column
        var1 = sqrss - (avgss**2)
        var2 = sqrss2 - (avgss2**2)
        cov = timess - (avgss*avgss2)
        cc = cov / sqrt(var1*var2)
        #print(sqrs)
        #print(sqrs2)
        #print(sqrss)
        #print(sqrss2)
        #print(timess)
        #print("Covariance")
        #print(cov)
        #print("Correlation Coefficient")
        #print(cc)
        self.textEdit_2.setText(str(cc))

    def choose5(self):
        thread = threading.Thread(target=self.futurePrice, daemon=True).start()

    def futurePrice(self):
        company = self.comboBox_7.currentText()
        years=[]
        prices=[]
        for i in range(2007,2019):
            #make a list of years from 2007 to 2018
            years.append(i)
            #make a list of averages for each year
            df=quandl.get("WIKI/"+str(company), start_date=str(i)+"-01-01", end_date=str(i)+"-12-31")
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
            df = quandl.get("WIKI/"+str(company), start_date = str(i)+"-01-01", end_date = str(i)+"-12-31")
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

        if __name__ == '__main__':
            app.run_server(debug=False)
            
    def futureAverageStock(self):
        company=self.comboBox_7.currentText()
        years=[]
        prices=[]
        for i in range(2007,2019):
            #make a list of years from 2007 to 2018
            years.append(i)
            #make a list of averages for each year
            df=quandl.get("WIKI/"+str(company), start_date=str(i)+"-01-01", end_date=str(i)+"-12-31")
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
        
    def choose4(self):
        thread = threading.Thread(target=self.graph2, daemon=True).start()

    def graph2(self):
        stock = self.comboBox_3.currentText()
        startdate = self.comboBox_5.currentText()
        enddate = self.comboBox_6.currentText()
        avgs = []
        dates = []
        avgs2 = []
        avgs3 = []
        avgs4 = []
        for i in range(int(startdate), int(enddate)+1, 1):
            df = quandl.get("WIKI/"+str(stock), start_date=str(i)+"-01-01", end_date=str(i+1)+"-12-31")
            avg = df["Open"].mean()        
            avgs.append(avg)            
            dates.append(i)
            avg2 = df["High"].mean()            
            avgs2.append(avg2)          
            avg3 = df["Low"].mean()
            avgs3.append(avg3)
            avg4 = df["Close"].mean()
            avgs4.append(avg4)
        app = dash.Dash()
        app.layout = html.Div(children=[
            html.H1(children='HelloMain'),
            html.Div(children='''
                Dash: A web application framework for Python.
            '''),
            dcc.Graph(
                id='example-graph',
                figure={
                    'data': [
                    {'x': dates, 'y': avgs, 'type': 'line', 'name': stock},
    
                    ],
                    'layout': {
                    'title': 'Opening Prices'
                    }
                }
          ),
            dcc.Graph(
                id='example-graph2',
                figure={
                    'data': [
                    {'x': dates, 'y': avgs2, 'type': 'line', 'name': stock},
                    ],
                    'layout': {
                    'title': 'Highest Prices'
                    }
                }
          ),
            dcc.Graph(
                id='example-graph3',
                figure={
                    'data': [
                    {'x': dates, 'y': avgs3, 'type': 'line', 'name': stock},
                    ],
                    'layout': {
                    'title': 'Lowest Prices'
                    }
                }
          ),
            dcc.Graph(
                id='example-graph4',
                figure={
                    'data': [
                    {'x': dates, 'y': avgs4, 'type': 'line', 'name': stock},
                    ],
                    'layout': {
                    'title': 'Closing Prices'
                    }
                }
          )
        ])
        app.run_server(port=3003)

    def choose3(self):
        thread = threading.Thread(target=self.relGraph, daemon=True).start()

    def relGraph(self):
        inputCompany=self.comboBox_11.currentText()
        year_start=int(self.comboBox_13.currentText())
        year_end=int(self.comboBox_14.currentText())
        #list of companies to loop through
        companies=["AAPL", "TSLA", "GOOG", "MSFT", "INTC", "AMZN", "FB", "JNJ", "JPM", "XOM", "BAC", "WMT", "WFC"]
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
                df = quandl.get("WIKI/"+str(inputCompany), start_date = str(i)+"-01-01", end_date = str(i)+"-12-31")
                df2 = quandl.get("WIKI/"+str(company), start_date = str(i)+"-01-01", end_date = str(i)+"-12-31")
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

    def contents(self, Startstock, stock2):
        avgs = []
        averages = []
        dates = []
        avgs2 = []
        averages2 = []
        avgs3 = []
        averages3 = []
        avgs4 = []
        averages4 = []
        for i in range(int(startdate), int(enddate)+1, 1):
            df = quandl.get("WIKI/"+str(stock), start_date=str(i)+"-01-01", end_date=str(i+1)+"-12-31")
            df2 = quandl.get("WIKI/"+str(stock2), start_date=str(i)+"-01-01", end_date=str(i+1)+"-12-31")
            avg = df["Open"].mean()
            average = df2["Open"].mean()
            avgs.append(avg)
            averages.append(average)
            dates.append(i)
            avg2 = df["High"].mean()
            average2 = df2["High"].mean()
            avgs2.append(avg2)
            averages2.append(average2)
            avg3 = df["Low"].mean()
            average3 = df2["Low"].mean()
            avgs3.append(avg3)
            averages3.append(average3)
            avg4 = df["Close"].mean()
            average4 = df2["Close"].mean()
            avgs4.append(avg4)
            averages4.append(average4)
        app = dash.Dash()
        print("debug")

        app.layout = html.Div(children=[
            html.H1(children='HelloMain'),
            html.Div(children='''
                Dash: A web application framework for Python.
            '''),
            dcc.Graph(
                id='example-graph',
                figure={
                    'data': [
                    {'x': dates, 'y': avgs, 'type': 'line', 'name': stock},
                    {'x': dates, 'y': averages, 'type': 'line', 'name': stock2},
                    ],
                    'layout': {
                    'title': 'Comparision of Opening prices'
                    }
                }
          )
        ])
        app.run_server(port=3003)
       
    def correlation(self, startStock, endStock):
        stock = self.comboBox_11.currentText()
        stock2 = self.comboBox_12.currentText()
        startdate = self.comboBox_13.currentText()
        enddate = self.comboBox_14.currentText()
        avgs = []
        avgs2 = []
        for i in range(int(startdate), int(enddate)+1):
            df = quandl.get("WIKI/"+ str(startStock), start_date=str(i)+"-01-01", end_date=str(i)+"-12-31")
            df2 = quandl.get("WIKI/"+ str(endStock), start_date=str(i)+"-01-01", end_date=str(i)+"-12-31")
            avg = df["Close"].mean() #Average colsing price for AAPL eah day
            avg2 = df2["Close"].mean() #Average closing price for TSLA each day
            avgs.append(avg)
            avgs2.append(avg2)
        
        #print(avgs)
        #print(avgs2)
        cls = df["Close"].var() #variance of both tickers
        cls2 = df2["Close"].var()
        
        #print(cls)
        #print(cls2)
        times = []
        for n in range(0, len(avgs), 1):
            time = avgs[n]*avgs2[n] #AAPL * TSLA
            times.append(time)
        #print(times)
        avgss = sum(avgs)/len(avgs) #Average Value of whole AAPL column
        avgss2 = sum(avgs2)/len(avgs2) #average Value of whole TSLA column
        sqrs = []
        sqrs2 = []
        for u in range(0, len(avgs), 1):
            sqr = avgs[u]**2 #Square root of each day in AAPL
            sqr2 = avgs2[u]**2 #Square root of each day in TSLA
            sqrs.append(sqr)
            sqrs2.append(sqr2)
        sqrss = sum(sqrs)/ len(sqrs)#Average of square root colums
        sqrss2 = sum(sqrs2)/len(sqrs2)
        timess = sum(times)/ len(times) #Average of AAPL*TSLA column
        var1 = sqrss - (avgss**2)
        var2 = sqrss2 - (avgss2**2)
        cov = timess - (avgss*avgss2)
        cc = cov / sqrt(var1*var2)
        #print(sqrs)
        #print(sqrs2)
        #print(sqrss)
        #print(sqrss2)
        #print(timess)
        #print("Covariance")
        #print(cov)
        #print("Correlation Coefficient")
        #print(cc)

        return cc

    def choose2(self):
        thread = threading.Thread(target=self.graph1, daemon=True).start()

    def graph1(self):
        stock = self.comboBox_11.currentText()
        stock2 = self.comboBox_12.currentText()
        startdate = self.comboBox_13.currentText()
        enddate = self.comboBox_14.currentText()
        avgs = []
        averages = []
        dates = []
        avgs2 = []
        averages2 = []
        avgs3 = []
        averages3 = []
        avgs4 = []
        averages4 = []
        print("hello")
        for i in range(int(startdate), int(enddate)+1, 1):
            df = quandl.get("WIKI/"+str(stock), start_date=str(i)+"-01-01", end_date=str(i+1)+"-12-31")
            df2 = quandl.get("WIKI/"+str(stock2), start_date=str(i)+"-01-01", end_date=str(i+1)+"-12-31")
            avg = df["Open"].mean()
            average = df2["Open"].mean()
            avgs.append(avg)
            averages.append(average)
            dates.append(i)
            avg2 = df["High"].mean()
            average2 = df2["High"].mean()
            avgs2.append(avg2)
            averages2.append(average2)
            avg3 = df["Low"].mean()
            average3 = df2["Low"].mean()
            avgs3.append(avg3)
            averages3.append(average3)
            avg4 = df["Close"].mean()
            average4 = df2["Close"].mean()
            avgs4.append(avg4)
            averages4.append(average4)
        print("hello")

        app = dash.Dash()
        print("debug")

        app.layout = html.Div(children=[
            html.H1(children='HelloMain'),
            html.Div(children='''
                Dash: A web application framework for Python.
            '''),
            dcc.Graph(
                id='example-graph',
                figure={
                    'data': [
                    {'x': dates, 'y': avgs, 'type': 'line', 'name': stock},
                    {'x': dates, 'y': averages, 'type': 'line', 'name': stock2},
                    ],
                    'layout': {
                    'title': 'Comparision of Opening prices'
                    }
                }
          ),
            dcc.Graph(
                id='example-graph2',
                figure={
                    'data': [
                    {'x': dates, 'y': avgs2, 'type': 'line', 'name': stock},
                    {'x': dates, 'y': averages2, 'type': 'line', 'name': stock2},
                    ],
                    'layout': {
                    'title': 'Comparision of Highest prices'
                    }
                }
          ),
            dcc.Graph(
                id='example-graph3',
                figure={
                    'data': [
                    {'x': dates, 'y': avgs3, 'type': 'line', 'name': stock},
                    {'x': dates, 'y': averages3, 'type': 'line', 'name': stock2},
                    ],
                    'layout': {
                    'title': 'Comparision of Lowest prices'
                    }
                }
          ),
            dcc.Graph(
                id='example-graph4',
                figure={
                    'data': [
                    {'x': dates, 'y': avgs4, 'type': 'line', 'name': stock},
                    {'x': dates, 'y': averages4, 'type': 'line', 'name': stock2},
                    ],
                    'layout': {
                    'title': 'Comparision of Closing prices'
                    }
                }
          )
        ])
        print("debug")
        app.run_server(port=3003)
