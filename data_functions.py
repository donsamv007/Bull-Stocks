#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 27 20:33:29 2020

NAME:
    data_functions - This module contains functions that are used for data related operations.

FILE:
    data_functions.py

FUNCTIONS:
    get_company_list
    get_ticker_data
    get_statistical_description
    write_to_excel

@author: donsam
"""
#pre-defined modules
import yfinance as yf
import pandas as pd
import tkinter as tk

#Function to get company list from a csv file and convert it to a list
def get_company_list():
    #Reading company data from a csv file 
    try:
        company_data = pd.read_csv('companylist.csv')
        #Reading only the ticker symbol and company name and seperating them by double pipe symbol
        ticker_symbols = company_data['Symbol'] + ' || ' + company_data['Name']
        ticker_symbols = ticker_symbols.sort_values(ascending=True)
        #Returning the list of ticker symbols 
    except:
        print('Failed to fetch company list')
    return ticker_symbols


#Function to get data associated with ticker symbols     
def get_ticker_data(start_date, end_date, ticker_symbol_e):
    #Ticker symbol is taken from the entry field and assigned to variable symbol
    symbol= ticker_symbol_e.get()

    try:
        #Ticker data is obtained passing the ticker symbol to yf.Ticker
        ticker_data = yf.Ticker(symbol)
    except:
        status_msg = tk.messagebox.showerror(title='Error Message', 
                                        message= 'Msg: Unable to contact yahoo finance')     
    #Ticker history data is obtained based on the date range specified
    ticker_hist = ticker_data.history(start= start_date, end= end_date)
    #if the dataframe ticker_history is empty then variable empty is set to False otherwise True  
    empty = ticker_hist.empty
    
    #Boolean value of the variable empty is checked
    if empty == True:
        #error message is printed 
        status_msg = tk.messagebox.showerror(title='Error Message',
                                             message= 'No data found, symbol may be delisted')
        return ticker_data, ticker_hist, symbol, False
       
    else:
        return ticker_data, ticker_hist, symbol, True 
    
    
#Function to compute statistical descriptions
def get_statistical_description(ticker_hist): 
    """describe_data stores the statistical description values obtained running
    the describe function on the ticker_hist dataframe""" 
    describe_data = ticker_hist.describe()
    #the dataframe is transposed ie rows -> column conversion to perform column subtraction
    describe_data = describe_data.transpose()
    #Inter Quartile Range is obtaned by subtracting Q3-Q1 which is 75% - 25%
    describe_data['IQR'] = describe_data['75%'] - describe_data['25%']
    # Range is obtained by performing max - min 
    describe_data['range'] = describe_data['max'] - describe_data['min']
    #standard deviation is obtained by squaring standard variation
    describe_data['standard variation'] = describe_data['std']*describe_data['std']
    #coefficient of variation is obtained by multipling stanndard deviation by mean and 100
    describe_data['coefficient of variation'] = (describe_data['std']*describe_data['mean'])*100
    #dataframe describe_data is transposed back
    describe_data = describe_data.transpose() 
    #index of the dataframe is reset
    describe_data.reset_index(inplace = True)
    #the index column is renamed to staistic
    describe_data = describe_data.rename({'index': 'Statistic'},axis=1)
    #Returning the dataframe containing the statistical descriptions, describe_data
    return describe_data    


def write_to_excel(filename_e, symbol, comp_info, ticker_hist, describe_data):    
    try:
        filepath = filename_e.get() 
        # Create a Pandas Excel writer using XlsxWriter as the engine.
        writer = pd.ExcelWriter(filepath, engine='xlsxwriter')
        #creating an empty dataframe to store company info
        cf = pd.DataFrame()
        cf.to_excel(writer,sheet_name= symbol)
                    
        worksheet = writer.sheets[symbol]
        #Sheet1 stores the company info
        worksheet.write(0, 0,comp_info )
        #sorting ticker history by date
        ticker_hist = ticker_hist.sort_values(by='Date', ascending=False)
        #Sheet2 stores all history data from ticker_hist 
        ticker_hist.to_excel(writer,sheet_name='All Data')
    
        #Sheet3 stores all statistical descriptions from ticker_hist 
        describe_data.to_excel(writer,sheet_name='Statistical Description')
        # Close the Pandas Excel writer and output the Excel file.
        writer.save()
        msg = 'File downloaded to' + filepath
        status_msg = tk.messagebox.showerror(title='Success', message= msg)     
    except:
        status_msg = tk.messagebox.showerror(title='Success', message= 'File Download Failed')
       
            