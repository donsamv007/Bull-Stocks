#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 27 18:08:11 2020

NAME:
    output_window - This module contains functions that are used for the output window.

FILE:
    output_window.py

FUNCTIONS:
    initialise_output_window
    start_thread
    tab1_company_info
    tab2_all_data
    tab3_statistical_description
    prediction_date_operations
    prediction_precheck_pass
    display_predicted_data
    predict_linear
    predict_svm
    tab4_crystal_ball
    get_output
       
@author: donsam
"""

#pre-defined modules
import tkinter as tk
import tkinter.ttk as ttk 
from tkinter import ttk, filedialog 
from tkcalendar import Calendar,DateEntry
from ttkthemes import ThemedStyle
from functools import partial
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.svm import SVR
from pandastable import Table, TableModel
import pandas as pd
import numpy as np
import threading

#user-defined modules
import auxillary_functions as af
import plots_and_averages as pa
import GUI_functions as gf
import checks_and_validations as cv




#Function to display output window with tabs and set properties
def initialise_output_window(state):
    #output windows is assigned      
    out_win = tk.Tk() 
    #output window title is set
    out_win.title('Output Window')
    #output window size is set
    out_win.geometry('1000x600')
    #output window style is set
    style = ThemedStyle(out_win)
    #if light mode
    if state == 0:
        style.set_theme('clearlooks')
        out_win['bg']='ivory'
    #otherwise dark mode    
    else:
        style.set_theme('black')
        out_win['bg']='black'
            
    #notebook is defined for holding the tabs
    tab_ctrl = ttk.Notebook(out_win) 
    
    #tab1 frame assigned 
    tab1 = ttk.Frame(tab_ctrl) 
    #tab2 frame assigned 
    tab2 = ttk.Frame(tab_ctrl)
    #tab3 frame assigned 
    tab3 = ttk.Frame(tab_ctrl)
    #tab4 frame assigned 
    tab4 = ttk.Frame(tab_ctrl)
    
    #tab1 title set
    tab_ctrl.add(tab1, text ='Company Info') 
    #tab2 title set
    tab_ctrl.add(tab2, text ='All Data')
    #tab3 title set
    tab_ctrl.add(tab3, text ='Statistical Description')
    #tab4 title set
    tab_ctrl.add(tab4, text ='Crystal Ball') 

    #notebook using grid system
    tab_ctrl.grid()
    return tab1, tab2, tab3, tab4

#Function to create a thread 
def start_thread(comp_info):
    #a new thread is created so that even when the company info is read out user is able to navigate within GUI
    thread_listen = threading.Thread(target=af.listen_text, args=(comp_info,)).start()

#Function to display tab1
def tab1_company_info(tab1, comp_info): 
    #text widget tab 1 is created 
    Company_info = tk.Text(tab1, height = 30, width =60, font=('Helvetica', 16)) 
    #company info is populated to the text widget
    Company_info.insert(tk.END, comp_info)
    #the widget uses grid positioning
    Company_info.grid(row=1,column=1, rowspan = 10)    
    #Listen Button        
    listen_b=tk.Button(tab1, text='Listen', command= partial(start_thread, comp_info))                       
    #it is positioned appropriately
    listen_b.grid(row=1,column=3, sticky = 'sw')
    
    
#Function to display tab2
def tab2_all_data(tab2, ticker_hist, symbol, state):
    #plot button is created for plotting prices against date    
    plot_prices_b=tk.Button(tab2, text='Plot Prices',
                  command=partial(pa.plot_prices, ticker_hist, symbol, state, 1))
    plot_prices_b.grid(row = 1, column = 1, sticky = 'ns')
    
    #option menu choices for averages
    average_d = [
    'Simple Moving Average',
    'Weighted Moving Average',
    'Exponential Moving Average',
    'Cummulative Moving Average',
    'MACD']
    #variable to store the option selected
    select = tk.StringVar(tab2)
    #default value 0 ie. Simple Moving Average
    select.set(average_d[0])
    
    #average option menu
    average_o = tk.OptionMenu(tab2, select, *average_d)
    #average option menu positioned 
    average_o.grid(row = 1, column = 2, sticky = 'ns')
    #ticker history data is sorted in decending order according to dates
    ticker_hist = ticker_hist.sort_values(by='Date', ascending=False)
    
    #frame within tab 2 is created  
    all_data_f = tk.Frame(tab2,width=300, height=300)
    #it is positioned appropriately
    all_data_f.grid(row =3, column = 2, columnspan = 5)
    #pandastable is created for holding the statistical all data
    all_data_f.table = pt = Table(all_data_f, dataframe=ticker_hist, width=800, height=400)
    #pandastable is displayed
    pt.show()
    
    #entry field for number of days for calculating averages 
    average_e = tk.Entry(tab2, width=3)
    #it is positioned appropriately   
    average_e.grid(row = 1, column = 4)
    #Label for number of days
    average_l = tk.Label(tab2, text = 'Number of days')
    #it is positioned appropriately
    average_l.grid(row = 1, column = 3, sticky = 'ns')
    #button for clculating averages
    average_b= tk.Button(tab2, text='Show in Table and Plot', 
                         command=partial(pa.average, average_e, select, 
                                         ticker_hist, symbol, all_data_f, state))
    #it is positioned appropriately
    average_b.grid(row = 2, column = 2)  
    
    
#Function to display tab3    
def tab3_statistical_description(tab3, describe_data, ticker_hist):
    #frame within tab 3 is created     
    describe_data_f = tk.Frame(tab3)
    #it is positioned appropriately
    describe_data_f.grid(row =3, column = 2)
    #pandastable is created for holding the statistical description data
    describe_data_f.table = pt = Table(describe_data_f, dataframe=describe_data,
                                       width=1000, height=300)
    #pandastable is displayed
    pt.show()  

#Function to get date and perform precheck operations for input
def prediction_date_operations(start_traind_e, end_traind_e, predict_date_e, selected):
    #start date for modelling period is fetched
    start = start_traind_e.get()
    #end date for modelling period is fetched
    end = end_traind_e.get()
    #predict date is fetched
    predict = predict_date_e.get()
    
    #date validation is performed
    precheck = cv.date_chk_pred( start, end, predict, selected)
    
    return start, end, predict, precheck
    
#Function to perform date and index related operations    
def prediction_precheck_pass(start, end, predict, ticker_data):        
        #business days are obtained as pandas series
        df1 = pd.bdate_range(start= end, end= predict) 
        #it is converted to list
        date_list= list(df1) 
        
        #list is converted to dataframe
        df = pd.DataFrame(date_list)
        #number of days are counted
        cnt = df.count()
        #the count value is put to a list
        y = cnt.tolist()
        #the first count value is assigned to days
        days = y[0]

        #data fetched from yahoo finance based on modelling period
        ticker_hist = ticker_data.history(start= start, end= end)
        
        ticker_hist.index.name = 'Date'
        #the dataframe is reindexed 
        ticker_hist.reset_index(inplace = True)
        #date is assigned to a column
        ticker_hist['Date'] = pd.to_datetime(ticker_hist['Date']).dt.date
        
        return df, y, days, ticker_hist
    

def display_predicted_data( tab4, df):    
    #frame is created in tab4    
    predict_data = tk.Frame(tab4) 
    #it is positioned appropriately
    predict_data.grid(row =7, column = 1, columnspan = 5)
    #pandastable shows the dataframe
    predict_data.table = pt = Table(predict_data, dataframe=df, width=800, height=250)
    #display the dataframe
    pt.show()   
    
    
    
#Function for linear regression
def predict_linear(selected, start_traind_e, end_traind_e, 
                   predict_date_e, ticker_data, tab4, symbol, state):
        
    start, end, predict, precheck = prediction_date_operations(start_traind_e, 
                                    end_traind_e, predict_date_e, selected)
        
        
    #if date validation is successful
    if precheck == 0:
        
        df, y, days, ticker_hist = prediction_precheck_pass(start, end, predict
                                                            , ticker_data)
        
        #the index of dataframe are put to a list 
        x = ticker_hist.index.tolist()
        #it is converted to a np array
        x = np.array(x)
        #the np array is reshaped to match the 1 dimension
        x = x.reshape(-1,1)
        # count stores the number of values in the np array
        count = len(x) - 1          
        # an index is generated to identify date gap between modelling period end and predict date
        predict_index = count +  days    
        #new np array that stores indexes from modelling period end and predict date
        new = np.arange(start= count , stop= predict_index, step=1)

        #the x axis is assigned with the closing price
        y = ticker_hist['Close'].values
        
        #the linear regression method is called
        regressor = LinearRegression()
        #the x and y axis are fitted 
        regressor.fit(x,y)
        #np array store the predict indexes
        arr = np.array([new])
        #the np array is reshaped to match the 1 dimension
        arr = arr.reshape(-1,1)
        #linear prediction is done for the predict indices
        predicted = regressor.predict(arr)
    
        #dataframe that stores predicted closing price values
        df2 = pd.DataFrame(predicted)
        #the date values are added
        df = pd.concat([df, df2], axis=1)
        #the dataframe columns are named
        df.columns =['Date','Predicted Closing Price']
        #the dates are converted to datetime object
        df['Date'] = pd.to_datetime(df['Date']).dt.date
            
            
        display_predicted_data(tab4,df)
                         
        #the actual closing prices and the predicted values are plotted against dates
        pa.plot_linear(df,ticker_hist,symbol,state) 
        
        
        
#Function for support vector regression
def predict_svm(selected,start_traind_e, end_traind_e, 
                predict_date_e, ticker_data, tab4, symbol, state):
        
    start, end, predict, precheck = prediction_date_operations(start_traind_e,
                                    end_traind_e, predict_date_e, selected)
                        
    #if date validation is successful
    if precheck == 0:
        
        df, y, days, ticker_hist = prediction_precheck_pass(start, end, predict,
                                                            ticker_data)
                                   
        #index values of ticker history dataframe are put to a list
        index =  ticker_hist.index.tolist()
        #date values of ticker history dataframe are put to a list            
        dates =  ticker_hist['Date'].values.tolist()
        #closing price values of ticker history dataframe are put to a list
        prices = ticker_hist['Close'].values.tolist()
            

        x = index
        x = np.array(x)
        x = x.reshape(-1,1)
        
        count = len(x) - 1
        
        predict_index = count +  days
        new = np.arange(start= count , stop= predict_index, step=1)
         
        #converting to matrix of n X 1
        index = np.reshape(index,(len(index), 1)) 
         
        # defining the support vector regression models 
        #RBF model
        svr_rbf = SVR(kernel= 'rbf', C= 1e3, gamma= 0.1)
        #linear modek
        svr_lin = SVR(kernel= 'linear', C= 1e3, gamma = 'auto')
        #polynomial model
        svr_poly = SVR(kernel= 'poly', C= 1e3, degree= 2, gamma = 'auto')
         
        #fitting the data points in the models
        #rbf fir
        svr_rbf.fit(index, prices)
        #linear fit
        svr_lin.fit(index, prices)
        #polynomial fit
        svr_poly.fit(index, prices)
            
        #predictions
        #rbf prediction
        predicted_rbf = svr_rbf.predict(np.array(new).reshape(-1,1))
        #linear prediction
        predicted_lin = svr_lin.predict(np.array(new).reshape(-1,1))
        #polynomial prediction
        predicted_poly = svr_poly.predict(np.array(new).reshape(-1,1))
         
        #predicted values are put to dataframe
        df_rbf_p = pd.DataFrame(predicted_rbf)
        df_lin_p = pd.DataFrame(predicted_lin)
        df_poly_p = pd.DataFrame(predicted_poly)
         
        #dataframe to store predicted values with date
        df = pd.concat([df, df_rbf_p, df_lin_p, df_poly_p], axis=1)
        df.columns =['Date','Predicted Closing Price (RBF)',
                     'Predicted Closing Price (linear)','Predicted Closing Price (polynomial)']
        df['Date'] = pd.to_datetime(df['Date']).dt.date
        df = df.dropna(subset=['Predicted Closing Price (RBF)',
            'Predicted Closing Price (linear)','Predicted Closing Price (polynomial)'])
         
            
        display_predicted_data( tab4, df)
         
        #the actual closing prices and the predicted values are plotted against dates           
        pa.plot_svr(df,ticker_hist,symbol,state)        

                     
#Function to display tab4    
def tab4_crystal_ball(tab4, ticker_data, symbol, state):    
        
    #Function to check which radio button is clicked for prediction
    def check_radio():
        #if selection is 1 ie. linear regression 
        if selected.get() == 1:
            #function for linear regression is called
            predict_linear(selected.get(), start_traind_e, end_traind_e, 
                           predict_date_e, ticker_data, tab4, symbol, state)
        #if selection is 2 ie. support vector regression    
        elif selected.get() == 2:
             #function for support vector regression is called
             predict_svm(selected.get(), start_traind_e, end_traind_e, 
                           predict_date_e, ticker_data, tab4, symbol, state)
             
    #radio button selection is stored in a variable         
    selected = tk.IntVar()
    #radio buttons created for type of prediction model
    ttk.Label(tab4, 
            text='Choose a Model:').grid(row=1,column=1)
    #radio button for linear regression
    ttk.Radiobutton(tab4, 
                  text='Linear Regression',
                  variable= selected, 
                  value=1).grid(row=1,column=2, sticky = 'sw')
    #radio button for support vector regression
    ttk.Radiobutton(tab4, 
                  text='Support Vector Regression',
                  variable= selected, 
                  value=2).grid(row=1,column=3, sticky = 'sw')

    
    # Label for entering date range
    drange_l = tk.Label(tab4, text='Enter the Modelling Period in \n yyyy-mm-dd format')
    #it is positioned appropriately
    drange_l.grid(row=3,column=1) 
    
    #Start Date Input Field
    start_traind_e = tk.Entry(tab4, width=10)
    #it is positioned appropriately
    start_traind_e.grid(row=3,column=2, columnspan = 2, sticky = 'sw')

    #Start Date Button
    start_traind_b=tk.Button(tab4, text='Start', command=partial(gf.cal_sel, start_traind_e))
    #it is positioned appropriately
    start_traind_b.grid(row=3,column=3, sticky = 'sw')

    #End Date Input Field
    end_traind_e = tk.Entry(tab4, width=10)
    #it is positioned appropriately
    end_traind_e.grid(row=4,column=2, columnspan = 2, sticky = 'sw')

    #End Date Button
    end_traind_b=tk.Button(tab4, text='End', command=partial(gf.cal_sel, end_traind_e))
    #it is positioned appropriately
    end_traind_b.grid(row=4,column=3, sticky = 'sw')

    #Prediction Date label
    drange_l = tk.Label(tab4, text='Enter the Prediction Date in \n yyyy-mm-dd format')
    #it is positioned appropriately
    drange_l.grid(row=5,column=1)   
  
    #Predict Date Input Field
    predict_date_e = tk.Entry(tab4, width=10)
    #it is positioned appropriately
    predict_date_e.grid(row=5,column=2, sticky = 'sw')
    
    #Predict Date Button    
    predict_date_b=tk.Button(tab4, text='Predict Date', command=partial(gf.cal_sel, predict_date_e))
    #it is positioned appropriately
    predict_date_b.grid(row=5,column=3, sticky = 'sw')
    
    #Predict Button        
    predict_b=tk.Button(tab4, text='Predict', command= check_radio)
    #it is positioned appropriately
    predict_b.grid(row=6,column=3, sticky = 'sw')
    
           
#Function to display second output window on screen after submitting from main window      
def get_output(comp_info, ticker_hist, describe_data, ticker_data, symbol, state, main_win):
    #main window is destroyed 
    main_win.destroy()
    #output window is initialised with 4 tabs
    tab1, tab2, tab3, tab4 = initialise_output_window(state)
    #tab1 function is called to display tab1
    tab1_company_info(tab1, comp_info) 
    #tab2 function is called to display tab2
    tab2_all_data(tab2, ticker_hist, symbol, state)
    #tab3 function is called to display tab3
    tab3_statistical_description(tab3, describe_data, ticker_hist)
    #tab4 function is called to display tab4
    tab4_crystal_ball(tab4, ticker_data, symbol, state)
    
      