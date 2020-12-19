import numpy as np
import pandas as pd
from pandas_datareader import data as wb
import matplotlib.pyplot as plt


def main():

    try:
        portfolio = create_portfolio()
        weights = get_weights(portfolio)
        initial_investment = investment()
        date = get_date()
        total_returns_list = total_returns(portfolio, date)
        annual_returns_list = annual_returns(portfolio, date)
        ROI = return_on_investment(initial_investment, weights, total_returns_list)
        portfolio_annual_return = portfolio_return(ROI, initial_investment, date)
        display_results = show_results(portfolio_annual_return, ROI, total_returns_list, annual_returns_list, portfolio,
                                       initial_investment)
        show_graph = create_graph(portfolio, date, weights)

    except:
        print("One or more ticker symbols do not exist on yahoo finance")


def create_portfolio():
    portfolio = []

    stock = input('Enter stock ticker: ')
    while stock != "n":
        stock = stock.upper()
        portfolio.append(stock)
        stock = input('Enter stock ticker(if no more enter "n"): ')
    return portfolio

def investment():
    money = input("Original money invested:  $")
    return money

def get_weights(portfolio):
    print()
    print("Next you will enter the weight of each stock in your portfolio in decimal form.")
    print("Please make sure each entry is a decimal between 0 and 1, and the sum of all weights equals 1.")
    print()
    weight_list = []
    count = 0
    while sum(weight_list) != 1:
        weight_list = []
        if count >= 1:
            print("Sum of all weights must equal exactly 1. Please try again.")
            print()

        for stock in portfolio:

            try:
                weight = float(input(stock + "'s weight in portfolio(decimal form): "))

            except:
                print("Please only enter a decimal between 0 and 1")
                break
            else:
                while weight > 1 or weight <= 0:
                    print("Please enter a decimal between 0 and 1 (i.e. 0.25, 0.5645)")

                    try:
                        weight = float(input(stock + "'s weight in portfolio(decimal form): "))

                    except:

                        print("Please only enter a decimal between 0 and 1")
                        break
            count += 1

            weight_list.append(weight)



    return weight_list

def get_date():
    date = input("Start date(year-month-day): ")
    return date


def total_returns(portfolio, date):
    tr_list = []
    for ticker in portfolio:
        adj_close = wb.DataReader(ticker, data_source='yahoo', start=date)['Adj Close']
        start_price = adj_close[0]
        total_days = len(adj_close)
        current_price = adj_close[total_days - 1]
        total_return = (current_price / start_price - 1) * 100
        tr_list.append(total_return)
    return tr_list


def annual_returns(portfolio, date):
    ar_list = []
    for ticker in portfolio:
        stock = wb.DataReader(ticker, data_source='yahoo', start=date)
        stock['Simple Return'] = (stock['Adj Close'] / stock['Adj Close'].shift(1)) - 1
        avg_annual_return = stock['Simple Return'].mean() * 250
        ar_list.append(avg_annual_return * 100)
    return ar_list


def return_on_investment(initial_investment, weights, total_returns_list):
    ROI = 0
    count = 0
    for i in weights:
        cash_in_stock = float(initial_investment) * i

        value_added = cash_in_stock * (total_returns_list[count] / 100)
        count += 1
        ROI += value_added
    return ROI


def portfolio_return(ROI, initial_investment, date):
    percent_change = (ROI + float(initial_investment)) / float(initial_investment) - 1
    adj_close = wb.DataReader('KO', data_source='yahoo', start=date)['Adj Close']
    total_days = len(adj_close)

    average_annual_return = percent_change / (total_days / 250)
    return percent_change, average_annual_return


def show_results(portfolio_annual_return, ROI, total_returns_list, annual_returns_list, portfolio, initial_investment):
    print()
    print("Portfolio Performance(since start date)")
    print("---------------------------------------")
    print('Total percentage change:', format(portfolio_annual_return[0] * 100, ".2f"), "%")
    print('Current Portfolio Value: $', format(ROI + float(initial_investment), ".2f"), sep="")
    print('Average annual rate of return: ', format(portfolio_annual_return[1] * 100, ".2f"), "%")
    print()
    print("Individual Stock Performance")
    print("----------------------------")
    count = 0
    for stock in portfolio:
        print(stock)

        print("Percent Change: ", format(total_returns_list[count], ".2f"), "%")
        print("Average annual rate of return: ", format(annual_returns_list[count], ".2f"), "%")
        print()
        count += 1


def create_graph(portfolio, date, weights):
    mydata = pd.DataFrame()
    for i in portfolio:
        mydata[i] = wb.DataReader(i, data_source='yahoo', start=date)['Adj Close']
    (mydata / mydata.iloc[0] * 100).plot(figsize=(15, 6))
    plt.show()


main()