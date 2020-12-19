from pandas_datareader import data as wb
import numpy as np
import matplotlib.pyplot as plt


def main():
    ticker = get_ticker()
    date = get_date()
    table = show_table(ticker, date)


def get_ticker():
    ticker = input("Enter ticker symbol: ")
    ticker = ticker.upper()
    return ticker


def get_date():
    date = input("Enter date(year-month-day): ")
    return date


def show_table(ticker, date):
    stock = wb.DataReader(ticker, data_source='yahoo', start=date)
    stock['Simple Return'] = (stock['Adj Close'] / stock['Adj Close'].shift(1)) - 1
    stock['Simple Return'].plot()
    plt.show()
    avg_annual_return = stock['Simple Return'].mean() * 250
    print("Average annual return rate since ", date, " is equal to ", str(format(avg_annual_return*100,".2f")), ' %')

main()