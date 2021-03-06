import sys
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication, QDialog
from PyQt5.uic import loadUi
from forex_python.converter import CurrencyRates
from datetime import datetime
import dash
import dash_core_components as dcc 
import dash_html_components as html
import threading
import statistics


class AppWindow(QDialog):
    def __init__(self):
        super(AppWindow, self).__init__()
        loadUi('exchange1.ui',self)
        self.inputYears()
        self.inputCurrency()
        self.pushButton.clicked.connect(self.findRate)
        self.pushButton_2.clicked.connect(self.choose2)
        self.pushButton_5.clicked.connect(self.findVolatility)

    def choose2(self):
        
        threading.Thread(target = self.graphRate).start()
    
    def inputYears(self):
        for x in range(2004,2018):
            self.comboBox_5.addItem(str(x))
            self.comboBox_6.addItem(str(x))
            self.comboBox_9.addItem(str(x))
            self.comboBox_10.addItem(str(x))
            self.comboBox_15.addItem(str(x))
            self.comboBox_16.addItem(str(x))
            
    def inputCurrency(self):
        c = CurrencyRates()
        x = c.get_rates('USD')
        for key in x:
            self.comboBox.addItem(str(key))
            self.comboBox_2.addItem(str(key))
            self.comboBox_3.addItem(str(key))
            self.comboBox_4.addItem(str(key))
            self.comboBox_7.addItem(str(key))
            self.comboBox_8.addItem(str(key))
            self.comboBox_11.addItem(str(key))
            self.comboBox_12.addItem(str(key))
            self.comboBox_13.addItem(str(key))
            self.comboBox_14.addItem(str(key))
        
        self.comboBox.addItem(str('USD'))
        self.comboBox_2.addItem(str('USD'))
        self.comboBox_3.addItem(str('USD'))
        self.comboBox_4.addItem(str('USD'))
        self.comboBox_7.addItem(str('USD'))
        self.comboBox_8.addItem(str('USD'))
        self.comboBox_11.addItem(str('USD'))
        self.comboBox_12.addItem(str('USD'))
        self.comboBox_13.addItem(str('USD'))
        self.comboBox_14.addItem(str('USD'))
        
    def findRate(self):
        c = CurrencyRates()
        print('hi')
        currency = str(self.comboBox.currentText())
        currency2 = str(self.comboBox_2.currentText())
        currentDay = datetime.now().day
        currentMonth = datetime.now().month
        currentYear = datetime.now().year
        print('hello')
        new2 = float(self.plainTextEdit.toPlainText())
        print(new2)
        timing = datetime(2016, 1 , 1 , 18, 36, 28, 151012)
        print(timing)
        exchange = c.convert(currency,currency2, new2 , timing)
        self.textEdit.setText(str(exchange))
        
    def graphRate(self):
        c = CurrencyRates()
        print('hello')
        currency_1 = str(self.comboBox_3.currentText())
        currency_2 = str(self.comboBox_4.currentText())
        list1 = []
        list2 = []
        print('hello')
        for i in range(2004,2018):
            self.comboBox_5.addItem(str(i))
            self.comboBox_6.addItem(str(i))
            new2 = 1
            list1.append(i)
        print('hello')
        year1 = str(self.comboBox_5.currentText())
        year2 = str(self.comboBox_6.currentText())
        print('hello')
        for z in range(int(year1),int(year2)):
            timing = datetime(z, 1 , 1 , 18, 36, 28, 151012)
            exchange = c.convert(currency_1 , currency_2 , 1 , timing)
            list2.append(exchange)
      
        app = dash.Dash()
        print('hello')
        app.layout = html.Div(children=[
            html.H1(children= 'Currency Exchange'),
    
            html.Div(children = '''
                ok!.
                '''),
                dcc.Graph(
                    id ='example-graph',
                    figure = {
                        'data':[
                            {'x':list1, 'y' : list2, 'type': 'line', 'name': "Graph"},
                        ],
                        'layout': {
                            'title' : "Graph"
                        }
                    }
                )
            ]
        )
        print("end")
        app.run_server()
    def findVolatility(self):
        currency1 = str(self.comboBox_7.currentText())
        currency2 = str(self.comboBox_8.currentText())
        startYear = str(self.comboBox_9.currentText())
        endYear = str(self.comboBox_10.currentText())
        c = CurrencyRates()
        listX = []
        for x in range(int(startYear), int(endYear)+1):
            for y in range(1,13):
                timing = datetime(x, y , 1 , 18, 36, 28, 151012)
                exchange = c.convert(currency1,currency2, 1 , timing)
                listX.append(exchange)
        print(listX)
        v = statistics.stdev(listX)
        self.textEdit_3.setText(str(v))
      
