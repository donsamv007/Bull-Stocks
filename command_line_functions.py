#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 27 17:32:21 2020

NAME:
    command_line_functions - This module contains functions that support the command line output.

FILE:
    command_line_functions.py

FUNCTIONS:
    get_ticker_symbol
    get_date
    get_date_range
    get_ticker_data
    average_plot_choice
    number_of_days
    days_average
    output
    command_line_operations

@author: donsam
"""

#pre-defined modules
import yfinance as yf
import pandas as pd

#user-defined modules
import data_functions as df
import checks_and_validations as cv
import plots_and_averages as pa
import sys

#Function to get the ticker symbol from user
def get_ticker_symbol():
    print('Please press Q if you want to exit at any point...')
   #ticker symbol is gotten from user and stored in variable symbol     
    symbol = input('Enter the ticker symbol ')
    #Quit
    if symbol == 'Q' or symbol == 'q':
        sys.exit('Quitting') 
    nw_chk, msg = cv.nw_check("http://www.google.com")    
    if nw_chk == 0:    
        #ticker symbol is passed to yf.Ticker to get ticker data
        try:
            ticker_data = yf.Ticker(symbol)           
        except:
            #Error message is displayed if ticker symbol passed is not validticker symbol 
            print('No data found, symbol may be delisted')    
            get_ticker_symbol() 
    else:
        print(msg) 
        sys.exit('Quitting')   
    return symbol, ticker_data   
 
    
#Function to get the date from user
def get_date(date_text):
    #date_text specifies what date has to be obtained from user start date or end date
    date = input(date_text)
    #checks if the date is in yyyy-mm-dd format sets d_flag to 1 if not in format
    d_flag, msg = cv.date_format_validation(date)
    if d_flag == 1:
        #prints the error message
        print(msg)
    return date, d_flag


#Function to get the date range from user    
def get_date_range(): 
    #the date format is specified    
    print('Enter the date range in YYYY-MM-DD format ')
    #d_flag is set to 1 by default for asking the user input for start date once
    d_flag = 1
    #until the user inputs the start date in yyyy-mm-dd format d_flag is set to 1
    while d_flag == 1:
        #user input for start date is taken, dflag is set to 1 if the date isnt in proper format
        start_date, d_flag = get_date('Start Date: ')
        #Quit
        if start_date == 'Q' or start_date == 'q':
            sys.exit('Quitting')   
    #d_flag is set to 1 by default for asking the user input for end date once    
    d_flag = 1
    #until the user inputs the end date in yyyy-mm-dd format d_flag is set to 1
    while d_flag == 1:
        #user input for end date is taken, dflag is set to 1 if the date isnt in proper format
        end_date, d_flag = get_date('End Date: ')
        #Quit
        if end_date == 'Q' or end_date == 'q':
            sys.exit('Quitting') 
    #returning start date and end date    
    return start_date, end_date

        
#Function to get the ticker symbol from user and ticker data from yahoo finance based on date range
def get_ticker_data(ticker_data, start_date, end_date):
    try:
        #ticker history data is gotten for the date range
        ticker_hist = ticker_data.history(start= start_date, end= end_date)
        #The index of dataframe ticker_hist is changed from date     
        ticker_hist.index.name = 'Date'
        #Reindexing to count value
        ticker_hist.reset_index(inplace = True)
        #Date is treated as a regular column 
        ticker_hist['Date'] = pd.to_datetime(ticker_hist['Date']).dt.date
    except:
        #Error message is displayed if there is no data for the date range
        print('No data found for the date range')
        #user is asked to input ticker symbol again
        get_ticker_symbol()
        #user is asked to input date range again
        get_date_range()

    #Returning the dataframe ticker_hist   
    return ticker_hist 

#Function to get the choice from user for average plots   
def average_plot_choice():
    #The choice from user is obtained for the type of average plot
    print('Which Average do you want to compute and plot?')        
    choice = input('1. Simple Moving Average\n2. Weighted Moving Average\n3. Exponential Moving Average\n4. Cummulative Moving Average\n5. MACD\n6. Quit\n')
    #if choice is 1 ie. Simple Moving Average 
    if choice == '1':
        option = 'Simple Moving Average'
    #if choice is 2 ie. Weighted Moving Average    
    elif choice == '2':    
        option = 'Weighted Moving Average'
    #if choice is 3 ie. Exponential Moving Average     
    elif choice == '3':            
        option = 'Exponential Moving Average'
    #if choice is 4 ie. Cummulative Moving Average     
    elif choice == '4':            
        option = 'Cummulative Moving Average'
    #if choice is 5 ie. MACD     
    elif choice == '5':            
        option = 'MACD'
    #if choice is 6 ie. Quit     
    elif choice == '6' or choice == 'Q' or choice == 'q':
        sys.exit('Quitting')
    #in case of invalid choice                       
    else:
        print('Invalid Choice, Please Try again!!! ')
        #user is asked to input choice again
        average_plot_choice()
    return choice, option

#Function to validate number of days
def number_of_days():
    #The number of days is obtained from user
    no_of_days = input('Enter the number of days\n')
    #Number of days is converted to integer
    no_of_days = int(no_of_days)
    #Number of days is validated    
    if no_of_days == '' or no_of_days <= 0:
        #Error message is displayed for invalid number of days
        print('Invalid number of days')
        #flag is set to 1 in case of invalid input
        dflag = 1
    else:
        #flag is set to 0 in case of valid input
        dflag = 0
    return  no_of_days, dflag   
        

#Function to plot average based on number of days input by user
def days_average(choice, option,ticker_hist, symbol):
      #if choice is not MACD
        if choice != 5:
            dflag = 1
            while dflag == 1:
                no_of_days, dflag = number_of_days()
            #average function is called from the plots and averages module 
            pa.average(no_of_days, option, ticker_hist, symbol, 2, 1)
        #If choice is 5 ie. MACD
        elif choice == '5':
            #average function is called from the plots and averages module
            pa.average(0, option, ticker_hist, symbol, 2)
   
#Function to display the output menu options    
def output(ticker_hist, symbol):
    #The choice from user is obtained for Plots, Statistical Description, or Average Price
    print('Enter your choice')
    choice = input('1. Show Plots\n2. Show Statistical Description\n3. Average Prices\n4. Quit\n')
    #if choice is 1 ie. Show Plots
    if choice == '1':
       #plot_prices function is called from the plots and averages module  
       pa.plot_prices(ticker_hist, symbol, 0,2)
       output(ticker_hist, symbol)
    #if choice is 2 ie. Show Statistical Description
    elif choice == '2':
        #get_statistical_description function is called from the data functions module 
        describe_data = df.get_statistical_description(ticker_hist)
        #Statisttical Descriptions are printed
        print(describe_data)
        output(ticker_hist, symbol)
    #if choice is 3 ie. Average Prices   
    elif choice == '3':
        #average plot choice function for type of average is called
        choice, option = average_plot_choice()
        #number of days of average is obtained
        days_average(choice, option, ticker_hist, symbol)
        #user is redirected to output choice menu again
        output(ticker_hist, symbol)
    #if choice is 4 ie. Quit      
    elif choice == '4' or choice == 'Q' or choice == 'q':
        sys.exit('Quitting') 
    #if choice is invalid    
    else:
        print('Invalid Choice, Please Try again!!! ')
        #user is asked to input choice again
        output(ticker_hist, symbol)
        
#Root function that calls all the command line child functions          
def command_line_operations():             
    symbol, ticker_data = get_ticker_symbol()
    start_date, end_date = get_date_range() 
    ticker_hist = get_ticker_data(ticker_data, start_date, end_date)
    if ticker_hist.empty == False:
        output(ticker_hist, symbol)
    else:
        command_line_operations()
        
            

   