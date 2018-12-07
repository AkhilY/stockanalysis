import sys
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication, QDialog, QMainWindow
from PyQt5.uic import loadUi
import quandl
import pandas
import math
import dash_core_components as dcc
import dash_html_components as html
import dash
import threading
from sklearn.svm import SVR
import matplotlib.pyplot as plt 
import numpy as np
quandl.ApiConfig.api_key = "x7hUv-ccTXF9Uz2CFT4w"

class stocks:
	def __init__(self):
		self.stocks = {

			'Fiyta Holdings Ltd':200026,
			'Dongxu Optoelectronic Technology Co Ltd':200413,
			'Changhong Meiling Co Ltd':200521,
			'CSG Holding Co Ltd':200012,
			'Dalian Refrigeration Co Ltd':200530,
			'Shenzhen Wongtee International Enterprise Co Ltd':200056,
			'Guangdong Electriv Power Development':200539,
			'Shandong Chenming Paper Holding Ltd':200488,
			'Foshan Electrical And Lighting Co Ltd':200011,




		}
		
		combine = []

		for i in self.stocks:
			combine.append("XSHE/"+str(self.stocks[i]))
		self.combine = combine
class MainWindow(QMainWindow):
    def __init__(self):

                super(MainWindow, self).__init__()
                loadUi('chinesestock (1).ui', self)
                self.averagestockpricecalculate.clicked.connect(self.average)
                self.pushButton_2.clicked.connect(self.calcCoCo)
                stock = stocks()
                self.graphdatagraphdata.clicked.connect(self.graphdata)
                self.stocks = stock.stocks
                self.pushButton_3.clicked.connect(self.visual2)
                self.pushButton_4.clicked.connect(self.visual3)
                self.predictcalculate.clicked.connect(self.futureAverageStock)
                self.predictgraph.clicked.connect(self.visual4)
    
    def average(self):
                bstock=self.averagestockstock1.currentText()
                starty=self.averagestockyear1.currentText()
                endy=self.averagestockyear2.currentText()
                itis = True
                for key in self.stocks:
                        try:
                                if self.stocks[bstock] == self.stocks[key]:
                                        self.stocks[key]
                        except:
                                itis = False
                                pass
                        if itis == True:
                                stock = self.stocks[bstock]
                aaverage = []
                dump1 = 0
                for i in range(int(starty), int(endy) + 1, 1):
                        sdate = str(i)+"-01-01"
                        mdate = str(i)+"-06-15"
                        edate = str(i)+"-12-31"
                        data1_1 = quandl.get("XSHE/"+str(stock), start_date = str(sdate), end_date = str(mdate))
                        data1_2 = quandl.get("XSHE/"+str(stock), start_date = str(mdate), end_date = str(edate))
                        aaverage.append(data1_1["High"].mean())
                        aaverage.append(data1_2["High"].mean())
                for i in aaverage:
                        dump1 += i
                average = dump1/len(aaverage)
                self.averagestockvalue.setText(str(average))
    def stocknum(self, bstock):
                itis = True
                for key in self.stocks:
                        itis = True
                        try:
                                if self.stocks[bstock] == self.stocks[key]:
                                        self.stocks[key]
                        except:
                                itis = False
                                pass
                        if itis == True:
                                stock = self.stocks[bstock]
                return stock
    def calcCoCo(self):
                binputCompany=self.corralationstock1.currentText()
                bcompany=self.corralationstock2.currentText()
                inputCompany = str(self.stocknum(binputCompany))
                company = str(self.stocknum(bcompany))
                year_start=int(self.corralationyear1.currentText())
                year_end=int(self.corralationyear2.currentText())
                listInput = []
                totalInput = 0
                listComp = []
                totalComp = 0 
                for i in range(year_start, year_end+1):
                        df = quandl.get("XSHE/"+inputCompany, start_date = str(i)+"-01-01", end_date = str(i)+"-12-31")
                        df2 = quandl.get("XSHE/"+company, start_date = str(i)+"-01-01", end_date = str(i)+"-12-31")


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
                self.corralationvalue.setText(str(CoCo))
    def visual2(self):
                threading.Thread(target=self.grapha, daemon=True).start()
    def grapha(self):
                inputCompany=self.stocknum(self.corralationstock1.currentText())
                company=self.stocknum(self.corralationstock2.currentText())
                year_start=int(self.corralationyear1.currentText())
                year_end=int(self.corralationyear2.currentText())
                listInput = []
                totalInput = 0
                listComp = []
                totalComp = 0 
                for i in range(year_start, year_end+1):
                        df = quandl.get("XSHE/"+str(inputCompany), start_date = str(i)+"-01-01", end_date = str(i)+"-12-31")
                        df2 = quandl.get("XSHE/"+str(company), start_date = str(i)+"-01-01", end_date = str(i)+"-12-31")


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
                        html.H1(children='Corralation Coefficients'),
                        html.Div(children=''' 
                                Graphs each company with each other 
                        '''),

                        dcc.Graph(
                                id='example-graph-5',
                                figure={
                                        'data': [
                                                {'x': years, 'y': listInput, 'type': 'line', 'name': inputCompany},
                                                {'x': years, 'y': listComp, 'type': 'line', 'name': company},
                                        ],
                                        'layout': {
                                                'title': 'corralation= '+str(CoCo)
                                        }
                                }
                        ),
                ])
                app.run_server(port=2222)
    def visual3(self):
                threading.Thread(target=self.graphb, daemon=True).start()
    def graphb(self):
                inputCompany=self.corralationstock1.currentText()
                year_start=int(self.corralationyear1.currentText())
                year_end=int(self.corralationyear2.currentText())
                #list of companies to loop through
                stock = stocks()
                companies = stock.combine
                #dictionary with each company and its corralation coefficient
                stockList=[]
                absstock=[]
                absstockDiction={}
                randstockDiction={}
                stockList=[]
                absstock=[]
                absstockDiction={}
                randstockDiction={}
                avgValuesDiction={}
                #calculate corralation for each company and append the values to a dictionary
                for company in companies:
                        listInput = []
                        totalInput = 0
                        listComp = []
                        totalComp = 0 
                        for i in range(year_start, year_end+1):
                                df = quandl.get('XSHE/'+str(self.stocknum(inputCompany)), start_date = str(i)+"-01-01", end_date = str(i)+"-12-31")
                                df2 = quandl.get(str(company), start_date = str(i)+"-01-01", end_date = str(i)+"-12-31")
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
                i=8
                while i>=0:
                        try:
                                comp=absstockDiction[absstock[i]]
                                stockList.append([comp,randstockDiction[comp]])
                                i=i-1
                        except KeyError:
                                pass
                #graph the related data
                years=[]
                for i in range(year_start, year_end+1):
                        years.append(i)
                app = dash.Dash()
                app.layout = html.Div(children=[
                        html.H1(children='Corralation Coefficients: Related Data'),
                        html.Div(children=''' 
                                Graphs each company with eachother and finds the corralation coefficient. 
                        '''),

                        dcc.Graph(
                                id='example-graph-6',
                                figure={
                                        'data': [
                                                {'x': years, 'y': avgValuesDiction[inputCompany], 'type': 'line', 'name': inputCompany},
                                                {'x': years, 'y': avgValuesDiction[stockList[0][0]], 'type': 'line', 'name': stockList[0][0]},
                                        ],
                                        'layout': {
                                                                'title': 'corralation between ' +str(inputCompany) + ' and ' + str(stockList[0][0]) +'= '+str(stockList[0][1])
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
                                                                'title': 'corralation between ' +str(inputCompany) + ' and ' + str(stockList[1][0]) +'= '+str(stockList[1][1])
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
                                                                'title': 'corralation between ' +str(inputCompany) + ' and ' + str(stockList[2][0]) +'= '+str(stockList[2][1])
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
                                                                'title': 'corralation between ' +str(inputCompany) + ' and ' + str(stockList[3][0]) +'= '+str(stockList[3][1])
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
                                                                'title': 'corralation between ' +str(inputCompany) + ' and ' + str(stockList[4][0]) +'= '+str(stockList[4][1])
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
                                                                'title': 'corralation between ' +str(inputCompany) + ' and ' + str(stockList[5][0]) +'= '+str(stockList[5][1])
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
                                                                'title': 'corralation between ' +str(inputCompany) + ' and ' + str(stockList[6][0]) +'= '+str(stockList[6][1])
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
                                                                'title': 'corralation between ' +str(inputCompany) + ' and ' + str(stockList[7][0]) +'= '+str(stockList[7][1])
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
                                                                'title': 'corralation between ' +str(inputCompany) + ' and ' + str(stockList[8][0]) +'= '+str(stockList[8][1])
                                        }
                                }
                        )
                ])
                app.run_server(port=3333)
    def graphdata(self):
                bstock=self.graphdatastock1.currentText()
                starty=self.graphdatayear1.currentText()
                endy=self.graphdatayear2.currentText()
                years = []
                itis = True
                for key in self.stocks:
                        try:
                                if self.stocks[bstock] == self.stocks[key]:
                                        self.stocks[key]
                        except:
                                itis = False
                                pass
                        if itis == True:
                                stock = self.stocks[bstock]
                average = []
                dump1 = 0
                for i in range(int(starty), int(endy) + 1, 1):
                        sdate = str(i)+"-01-01"
                        mdate = str(i)+"-06-15"
                        edate = str(i)+"-12-31"
                        data1_1 = quandl.get("XSHE/"+str(stock), start_date = str(sdate), end_date = str(mdate))
                        data1_2 = quandl.get("XSHE/"+str(stock), start_date = str(mdate), end_date = str(edate))
                        average.append(data1_1["High"].mean())
                        average.append(data1_2["High"].mean())
                for i in range(int(starty), int(endy) + 1, 1):
                        years.append(i)
                    
                app = dash.Dash()
                app.layout = html.Div(children=[
                        html.H1(children='Graphing Data'),
                        html.Div(children=''' 
                                Graphs average stock prices for each year 
                        '''),

                        dcc.Graph(
                                id='example-graph-6',
                                figure={
                                        'data': [
                                                {'x': years, 'y': average, 'type': 'line', 'name': bstock},
                                        ],
                                        'layout': {
                                                'title': 'Average Stock Prices Of ' +str(bstock) + 'between years '+str(starty)+' and '+ str(endy)
                                        }
                                }
                        )
                ])
                app.run_server(port=3123)
     #function to calculate future average stock price
    def futureAverageStock(self):
        ccompany=self.predictstock1.currentText()
        company = 'XSHE/'+str(self.stocknum(ccompany))
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
        futureYear=int(self.predictyear2.currentText())
        x=(futureYear-2018)*365
        def predict_stock_prices(years, prices, x):
            years = np.reshape(years,  (len(years),1 ))
            #prices = np.reshape(prices, (len(prices),1))

            svr_rbf = SVR(kernel = 'rbf', C=1e3, gamma=0.1)
            svr_rbf.fit(years, prices)
    

            print('Printing results')
            return svr_rbf.predict(x)[0]
        predicted_prices = predict_stock_prices(years, prices, [[x]])
        self.predictvalue.setText(str(predicted_prices))
    def visual4(self):
        threading.Thread(target=self.graph4, daemon=True).start()
    def graph4(self):
        quandl.ApiConfig.api_key = "x7hUv-ccTXF9Uz2CFT4w"


        ccompany=self.predictstock1.currentText()
        company = 'XSHE/'+str(self.stocknum(ccompany))

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

        app.run_server(port=9216)
		
	


	

app = QApplication(sys.argv)
widget = MainWindow()
widget.show()
sys.exit(app.exec_())
