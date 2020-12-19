import numpy as np
import pandas as pd
from pandas_datareader import data as wb
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
import requests

def main():
    intro = introduction()
    index_ticker = index()
    stock_list = get_stocks()
    date = get_date()
    #sector_ticker = sector(stock_list)
    new_stock_list = add_index(index_ticker,stock_list)
    graph = create_graph(new_stock_list,date)
    returns = show_returns(new_stock_list,date)
def introduction():
    print("This tool will compare stocks to a selected index over a specified time period")

def index():
    print()
    print("Indexes")
    print("-------")
    indexes = ['S&P 500','Nasdaq','Dow Jones']
    numbers = ['1','2','3']
    count = 1
    for i in indexes:
        print(i,"(",count,")",sep="")
        count +=1
    print()
    index = input("Index(enter number): ")
    while index not in numbers:
        print("Please enter number that corresponds with desired index.")
        index = input("Index(enter number): ")
    if index == '1':
        ticker = '^GSPC'
    elif index == '2':
        ticker = '^IXIC'
    elif index == '3':
        ticker = '^DJI'
    return ticker

def get_stocks():
    stocks = []
    stock = input("Stock ticker: ")
    count = 2
    while stock != 'done':
        stock = stock.upper()
        stocks.append(stock)
        stock = input("Stock ticker(if no more enter 'done'): ")
    return stocks

def sector(stock_list):
    if len(stock_list) == 1:
        for i in stock_list:
            page = requests.get("https://finance.yahoo.com/quote/"+ i +"/profile?p"+i)

        soup = BeautifulSoup(page.content, "html.parser")

        sector = soup.find(class_="Fw(600)").get_text()

        if sector == "Basic Materials":
            ticker = "^DJUSBM"
        elif sector == "Communication Services":
            ticker = "S5TELS"

        return ticker



def get_date():
    date = input("Start date(year-month-day): ")
    return date

def add_index(index_ticker,stock_list):
    stock_list.append(index_ticker)

    return stock_list



def create_graph(new_stock_list, date):
    mydata = pd.DataFrame()
    for i in new_stock_list:
        mydata[i] = wb.DataReader(i, data_source='yahoo', start=date)['Adj Close']
    (mydata / mydata.iloc[0] * 100).plot(figsize=(15, 6))
    plt.show()

def show_returns(new_stock_list,date):
    for ticker in new_stock_list:
        stock = wb.DataReader(ticker,data_source='yahoo',start=date)
        stock['Simple Return'] = (stock['Adj Close']/stock['Adj Close'].shift(1))-1
        avg_annual_return = stock['Simple Return'].mean()*250
        print("Average annual return of ",ticker," since ",date," is equal to ",str(format(avg_annual_return*100,'.2f')),' %')

main()


