#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Created on Fri Nov 13 18:37:54 2020

NAME:
    main_window - This module contains functions that support the main window.

FILE:
    main_window.py

FUNCTIONS:
    toggle_dark
    set_date_range
    progress_bar
    submit
    main_win_operations


@author: donsam
'''

#pre-defined modules
import tkinter as tk
import tkinter.ttk as ttk 
import time
from datetime import datetime, timedelta, date
from dateutil.relativedelta import relativedelta
from ttkthemes import ThemedStyle
import pandas as pd
from functools import partial
import sys
import threading
from csv import reader

#user-defined modules
import plots_and_averages as pa
import output_window as ow
import GUI_functions as gf
import data_functions as df
import auxillary_functions as af
import checks_and_validations as cv

#Global variable declarations
state = 0
selected = 0
check1_val = ''
check2_val = '' 
toggle_b = None
toggle_text = 'Dark Mode' 


#Function to toggle between dark and light modes    
def toggle_dark(main_win,symbol_list):
    af.play_sound('Button.wav')
    global state
    # Checking if button text is equal to "Dark Mode"
    if state == 0:
        #Setting Theme Style for main window
        style = ThemedStyle(main_win)
        #Setting Black Theme 
        style.set_theme('black')
        #Setting Black Background for main window
        main_win['bg']='black'
        #Setting Theme for list box
        symbol_list.config(bg = '#CCCCCC')
        # Setting global state variable to 1
        state = 1
       
        # Otherwise
    else:
        #Setting Theme Style for main window          
        style = ThemedStyle(main_win)
        #Setting Clearlooks Theme for main window 
        style.set_theme('clearlooks')
        #Setting Ivory Background for main window       
        main_win['bg']='ivory'
        #Setting Theme for list box        
        symbol_list.config(bg = 'khaki')
        # Setting global state variable to 0
        state = 0
    #the state variable is returned to apply theme in subsequent screens   
    return state      


#Function to set date range according to radio button selection    
def set_date_range(start_date_e, end_date_e):    
    #if the radio button selected is 1 (I year)
    if selected.get() == 1:
        #start_date is set to a date 1 year before today
        start_date= date.today() + relativedelta(months=-12)
        #end_date is set to today's date 
        end_date= date.today()
   
    #if the radio button selected is 2  (5 years)       
    elif selected.get() == 2: 
        #start_date is set to a date 5 years before today
        start_date= date.today() + relativedelta(months=-60)
        #end_date is set to today's date 
        end_date= date.today()    
   
    #if the radio button selected is 3  (Date Range)
    elif selected.get() == 3: 
        #start_date is set to the date in the entry field
        start_date= start_date_e.get()
        #end_date is set to the date in the entry field
        end_date= end_date_e.get()
   
    #if the radio button selected is 4  (1 Day)        
    elif selected.get() == 4: 
        #start_date is set to yesterday
        start_date= datetime.today() - timedelta(days=1)
        start_date = start_date.strftime('%Y-%m-%d')
        #end_date is set to today's date 
        end_date= date.today()  
   
    #if the radio button selected is 5  (5 Days)       
    elif selected.get() == 5:
        #start_date is set to a date 5 days before today        
        start_date= datetime.today() - timedelta(days=5)
        start_date = start_date.strftime('%Y-%m-%d')
        #end_date is set to today's date         
        end_date= date.today()  
   
    #if the radio button selected is 6  (3 Months)
    elif selected.get() == 6:
        #start_date is set to a date 3 months before today
        start_date= date.today() + relativedelta(months=-3)
        #end_date is set to today's date         
        end_date= date.today() 
    
    #if the radio button selected is 7  (6 Months)
    elif selected.get() == 7:
        #start_date is set to a date 6 months before today        
        start_date= date.today() + relativedelta(months=-6)
        #end_date is set to today's date         
        end_date= date.today() 
        
    #otherwise    
    else:
        #start_date is assigned to empty string 
        start_date= ''
        #end_date is assigned to empty string 
        end_date= ''
        
    #start_date and end_date are returned   
    return start_date, end_date      

        
#Function to display progress of submission 
def progress_bar(main_win):
    style = ttk.Style()
    style.theme_use('clearlooks')
    style.configure('grey.Horizontal.TProgressbar', background='blue')
    bar = ttk.Progressbar(main_win, length=300, style='grey.Horizontal.TProgressbar', 
                                                      mode = "indeterminate")
    bar.grid(row = 9, column = 2, columnspan = 5)
    bar.start(10)  
    
    
#Function to Submit to the second screen with output     
def submit(ticker_symbol_e,selected, check1_val,check2_val, main_win, start_date_e, end_date_e, filename_e):
    af.play_sound('Button2.wav')
    af.progress_bar(main_win)
    #start_date and end_date values are set based on radio button selection
    start_date , end_date  = set_date_range(start_date_e, end_date_e)

        
    """precheck operations are performed to validate input and check for internet connectivity
    from checks_and_validations module"""
    precheck = cv.perform_precheck(start_date, end_date, ticker_symbol_e,selected,
                                                           check1_val,check2_val, filename_e)
    
    #if precheck returns 0     
    if precheck == 0:
        #ticker data is obtained passing start_date end_date and ticker_symbol_e
        ticker_data, ticker_hist, symbol, check_sym = df.get_ticker_data(start_date,
                                                    end_date, ticker_symbol_e)
        #if the ticker symbol is valid proceed to next steps...
        if check_sym == True:
            #ccompany summary is obtained
            try:
                ticker_infod = ticker_data.info
                comp_info = ticker_infod['longBusinessSummary']
            except:
                comp_info = 'No Data Found'
            #statistical decriptions are obtained
            describe_data = df.get_statistical_description(ticker_hist)
            #index of the dataframe ticker_hist is changed from date     
            ticker_hist.index.name = 'Date'
            ticker_hist.reset_index(inplace = True)
            #ticker_hist, date is treated as seperate column
            ticker_hist['Date'] = pd.to_datetime(ticker_hist['Date']).dt.date
            
            #if checkbox 1 is selected (Download to excel)
            if check1_val.get() == 1:
                df.write_to_excel(filename_e, symbol, comp_info, ticker_hist, describe_data)
                
            #if checkbox 2 is selected (Show output)    
            if check2_val.get() == 1:
                #Message Submitting is printed on the screen 
                print('Submitting...')
                #values are submitted to second screen 
                ow.get_output(comp_info,ticker_hist,describe_data,ticker_data, 
                              symbol, state, main_win)


                
#Function executed to invoke main window and perform related operations                                 
def main_win_operations():
    #list of company names and ticker symbols are obtained
    ticker_symbols = df.get_company_list() 
    if ticker_symbols.empty == False:
        #main window is intialised 
        main_win = gf.initialise_main_window()
                
        #ticker symbol is obtained from user by executing function from GUI_functions module
        symbol_list, ticker_symbol_e, ticker_symbols = gf.get_ticker_symbol(main_win,
                                                                    ticker_symbols)
        #Dark Mode, Light Mode toggle button
        toggle_b=tk.Button(main_win,text = 'Dark/Light Mode', 
                           command = partial(toggle_dark, main_win, symbol_list))
        toggle_b.grid(row=1,column=15, columnspan =2)
        
        """check_speech function is executed from the module auxillary_functions 
        for speech input of ticker symbol"""
        af.check_speech(main_win, ticker_symbol_e, ticker_symbols, symbol_list)
        #date range is obtained from user executing function from GUI_functions module
        start_date_e, start_date_b, end_date_e, end_date_b = gf.get_date_range(main_win)
        
        #selected variable declared globally is called
        global selected
        """selected variable that stores the radio button choice for time period is 
        obtained from GUI_functions module""" 
        selected = gf.get_date_radio(main_win, start_date_e, start_date_b, end_date_e, 
                                     end_date_b)  
        
        #check1_val variable declared globally is called
        global check1_val
        #check2_val variable declared globally is called
        global check2_val 
        
        #value checked in box is obtained from GUI_functions module
        check1_val, check2_val, filename_e = gf.output_type(main_win) 
        
            
       #Submit Button
        submit_b=ttk.Button(main_win, text='Submit', 
                            command = partial(submit, ticker_symbol_e,selected, 
                            check1_val,check2_val, main_win, start_date_e, end_date_e, filename_e))
        submit_b.grid(row=10,column=15,columnspan =2 )
               
        #main window is run in loop
        main_win.mainloop()





        
        
        
        
        
      

