#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 27 17:37:57 2020

NAME:
    plots_and_averages - This module contains functions that are used for 
                            generating plots and calculating averages.

FILE:
    plots_and_averages.py

FUNCTIONS:
    plot_prices
    plot_average
    average
    plot_linear
    plot_svr

@author: donsam
"""

#pre-defined modules
import tkinter as tk
from bokeh.io import output_file, show
from bokeh.layouts import gridplot
from bokeh.plotting import figure
from bokeh.models import BasicTickFormatter, ColumnDataSource
from bokeh.themes import built_in_themes
from bokeh.io import curdoc
import matplotlib.pyplot as plt
from matplotlib.figure import Figure 
import pandas as pd
import math
from pandastable import Table, TableModel
import auxillary_functions as af

#Function to plot the different prices
def plot_prices(ticker_hist, symbol,state, interface):
        if interface != 2:
            af.play_sound('Button2.wav')
        #output of the plots is displayed in an html file plot.html with title as symbol name
        output_file('plots.html', 
        title = symbol)
        #the date string is conerted to date
        ticker_hist['Date'] = pd.to_datetime(ticker_hist['Date'])
        #x axis taxes the date column
        x = ticker_hist['Date']
        #y axis taxes the Close prices
        y1= ticker_hist['Close']
        #y axis taxes the Open prices
        y2= ticker_hist['Open']
        #y axis taxes the High prices
        y3= ticker_hist['High']
        #y axis taxes the Low prices
        y4= ticker_hist['Low']
        
        #checking for dark theme set in main window
        if state == 1:
            #setting dark theme to graph
            curdoc().theme = 'dark_minimal'

        #graph for Closing Price Vs. Date
        p1 = figure(x_axis_type='datetime',title = 'Closing Price Vs. Date',  
                    x_axis_label = 'Date', y_axis_label = 'Closing Price',
                    tools='crosshair,pan,reset,save,wheel_zoom')
        #setting the color of the plot line to blue and the width to 5
        p1.line(x,y1, color='blue', line_width=5)
        #rotating the x asix by 60 degree, the angle here is shown in radiants
        p1.xaxis.major_label_orientation = math.pi/3

        #graph for Opening Price Vs. Date
        p2 = figure(x_axis_type='datetime',title = 'Opening Price Vs. Date', 
                    x_axis_label = 'Date', y_axis_label = 'Opening Price',
                    tools='crosshair,pan,reset,save,wheel_zoom')
        #setting the color of the plot line to red and the width to 5        
        p2.line(x,y2, color='red',  line_width=5)
        #rotating the x asix by 60 degree, the angle here is shown in radiants        
        p2.xaxis.major_label_orientation = math.pi/3
  
        #graph for Low Price Vs. Date
        p3 = figure(x_axis_type='datetime', title = 'Low Price Vs. Date', 
                    x_axis_label = 'Date', y_axis_label = 'Low Price',
                    tools='crosshair,pan,reset,save,wheel_zoom')
        #setting the color of the plot line to green and the width to 5        
        p3.line(x,y3, color='green', alpha=0.5,line_width=5)
        #rotating the x asix by 60 degree, the angle here is shown in radiants        
        p3.xaxis.major_label_orientation = math.pi/3
        
        #graph for High Price Vs. Date       
        p4 = figure(x_axis_type='datetime', title = 'High Price Vs. Date',
                    x_axis_label = 'Date', y_axis_label = 'High Price', 
                    tools='crosshair,pan,reset,save,wheel_zoom')
        #setting the color of the plot line to yellow and the width to 5        
        p4.line(x,y4, color= 'yellow', alpha=0.5, line_width=5)
        #rotating the x asix by 60 degree, the angle here is shown in radiants        
        p4.xaxis.major_label_orientation = math.pi/3
        
        #displaying all graphs in a single page
        grid = gridplot([p1, p2, p3, p4], ncols=2, plot_width=650, plot_height=350)
        show(grid)


#Function to plot the different average prices        
def plot_average(ticker_hist,column_name, symbol, option, state):
    #checking for dark theme set in main window
    if state == 1:
        theme = 'dark_background'
    else:
        theme = 'fivethirtyeight'
   #setting theme for graphs 
    with plt.style.context(theme):
        #average price is plotted against date
        plt.plot(ticker_hist['Date'], ticker_hist[column_name], label = option)
        #closing price is plotted against date in the same graph
        plt.plot(ticker_hist['Date'], ticker_hist['Close'], label = 'Closing Price')
        fig = plt.gcf()
        fig.canvas.set_window_title(option)
        #rotation for the x axis labels is done
        plt.xticks(rotation= 60)
        #title of the graph is set to the company name
        plt.title(symbol)
        #y axis label is set to the closing price
        plt.ylabel('Closing Price')
        #x axis label is set to Date 
        plt.xlabel('Date')
        #the layout of the graph is tightly bound to avoid x axis label cutoff
        plt.tight_layout()
        #legend of the graph is set
        plt.legend()
        #the graph is displayed
        plt.show()


#Function to compute and show the different average prices
def average(field, option, ticker_hist, symbol, all_data_f, state):
    if all_data_f != 2:
        af.play_sound('Button2.wav')
    #Function to calculate weights           
    def wma_cal(weights):
        def g(x):
            return sum(weights * x)/ sum(weights)
        return g
    #if average computed for GUI
    if all_data_f != 2:
        no_of_days = field.get()
    else:
        no_of_days = field
    
    #if average computed for GUI   
    if all_data_f != 2:
        option = option.get()
    
    # number of days is not required for MACD        
    if no_of_days == '' and option != 'MACD' :
        status_msg = tk.messagebox.showerror(title='Error Message',
                    message= 'Msg: Number of Days not specified' )
        return
    #number of days string is converted to integer    
    if option != 'MACD':         
        no_of_days = int(no_of_days)
        #if number of days is given a value other than a number greater than 0
        if no_of_days <= 0:
            status_msg = tk.messagebox.showerror(title='Error Message', 
                     message= 'Msg: Number of Days must be greater than 1' )
            return
    #if Simple Moving Average option is selected         
    if option == 'Simple Moving Average':
        column_name = str('Close SMA' + str(no_of_days)) 
        ticker_hist[column_name]= ticker_hist.Close.rolling(no_of_days).mean()
        ticker_hist[column_name] = ticker_hist[column_name].shift(-no_of_days)
        
    #if Cummulative Moving Average option is selected             
    elif option == 'Cummulative Moving Average':            
        column_name = str('Close CMA' + str(no_of_days)) 
        ticker_hist[column_name] = ticker_hist.expanding(no_of_days).mean()
        ticker_hist[column_name] = ticker_hist[column_name].shift(-no_of_days)
                        
    #if Exponential Moving Average option is selected                  
    elif option == 'Exponential Moving Average':     
        column_name = str('Close EMA' + str(no_of_days)) 
        ticker_hist[column_name]= ticker_hist.Close.ewm(span= no_of_days).mean()
        ticker_hist[column_name] = ticker_hist[column_name].shift(-no_of_days)
            
    #if Weighted Moving Average option is selected            
    elif option == 'Weighted Moving Average':     
        column_name = str('Close WMA' + str(no_of_days))             
        weights = list(reversed([(no_of_days - n) * no_of_days for n in range(no_of_days)]))
        ticker_hist[column_name]= ticker_hist.Close.rolling(no_of_days).apply(wma_cal(weights), raw = True)
        ticker_hist[column_name] = ticker_hist[column_name].shift(-no_of_days)
  
    #if MACD option is selected            
    elif option == 'MACD':     
        column_name = str('Close EMA' + str(12)) 
        ticker_hist[column_name]= ticker_hist.Close.ewm(span= 12).mean()
        ticker_hist[column_name] = ticker_hist[column_name].shift(-12)  
        
        column_name = str('Close EMA' + str(26)) 
        ticker_hist[column_name]= ticker_hist.Close.ewm(span= 26).mean()
        ticker_hist[column_name] = ticker_hist[column_name].shift(-26)
        
        column_name = 'MACD'
        ticker_hist[column_name] = ticker_hist['Close EMA12'] - ticker_hist['Close EMA26']
        ticker_hist = ticker_hist.drop(columns =['Close EMA12','Close EMA26'], axis=1)

    #Function to plot averages is called
    plot_average(ticker_hist, column_name, symbol, option, state)
    
    #if average computed for GUI  
    if all_data_f != 2:
        #data is displayed in the pandas table
        all_data_f.table = pt = Table(all_data_f, dataframe=ticker_hist)
        pt.redraw()      


def plot_linear(df,ticker_hist,symbol,state):
    #if dark mode is enabled    
    if state == 1:
        theme = 'dark_background'
    #if dark mode is not eabled         
    else:
        theme = 'fivethirtyeight'
    #setting the theme of plot based on dark/light mode           
    with plt.style.context(theme):
        #plot date and predicted closing price
        plt.plot(df['Date'], df['Predicted Closing Price'], label = 'Predicted Closing Price')
        #plot date and closing price         
        plt.plot(ticker_hist['Date'], ticker_hist['Close'], label = 'Closing Price')
        #set window title
        fig = plt.gcf()
        fig.canvas.set_window_title('Linear Regression')
        #rotate x axis labels by 60 degree        
        plt.xticks(rotation= 60)
        #title of the plot is the ticker symbol       
        plt.title(symbol)
        #x axis label is date        
        plt.xlabel('Date')
        #y axis label is Closing Price        
        plt.ylabel('Closing Prices')
        #remove surrounding spaces        
        plt.tight_layout()
        #show plot legend        
        plt.legend()
        #show plot        
        plt.show()  

#Function to plot the graph for support vector regression
def plot_svr(df,ticker_hist,symbol,state):
    #if dark mode is enabled
    if state == 1:
        theme = 'dark_background'
    #if dark mode is not eabled    
    else:
        theme = 'fivethirtyeight'
    #setting the theme of plot based on dark/light mode        
    with plt.style.context(theme):  
        #plot date and predicted closing price for RBF 
        plt.plot(df['Date'], df['Predicted Closing Price (RBF)'],
                 label = 'Predicted Closing Price (RBF)')
        #plot date and predicted closing price for linear 
        plt.plot(df['Date'], df['Predicted Closing Price (linear)'], 
                 label = 'Predicted Closing Price (linear)')
        #plot date and predicted closing price for polynomial
        plt.plot(df['Date'], df['Predicted Closing Price (polynomial)'], 
                 label = 'Predicted Closing Price (polynomial)')
        #plot date and closing price 
        plt.plot(ticker_hist['Date'], ticker_hist['Close'], label = 'Closing Price')
        #set window title
        fig = plt.gcf()
        fig.canvas.set_window_title('Support Vector Regression')
        #x axis label is date
        plt.xlabel('Date')
        #y axis label is Closing Price
        plt.ylabel('Closing Price')
        #rotate x axis labels by 60 degree
        plt.xticks(rotation= 60)
        #title of the plot is the ticker symbol
        plt.title(symbol)
        #remove surrounding spaces
        plt.tight_layout()
        #show plot legend
        plt.legend()
        #show plot
        plt.show()            