#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 28 09:13:07 2020

NAME:
    checks_and_validations - This module contains functions that are used for 
                             checking and validating 

FILE:
    checks_and_validations.py

FUNCTIONS:
    nw_check
    null_input_check
    date_format_validation
    date_range_validation
    date_chk_pred
    perform_precheck

@author: donsam
"""
#pre-defined modules
import requests
import tkinter as tk
from datetime import datetime


#Function to check internet connection     
def nw_check(url): 
    #setting the timeout for 5 sec for checking the request retuen
    timeout = 5
    try:
        #checking if the url is loading
        request = requests.get(url, timeout=timeout)
        #message connected to the internet is printed
        msg = 'Connected to the Internet'
        #nw_chk flag is set to 0
        nw_chk = 0
    except (requests.ConnectionError, requests.Timeout) as exception:
        #message no internet connection is printed
        msg = 'Msg: No internet connection.'
        #nw_chk flag is set to 1
        nw_chk = 1
    #returning the message and the nw flag    
    return nw_chk, msg


#Function to validate input before submission          
def null_input_check(symbol_len, selected, check1_val, check2_val, start_date, end_date, filename_len):       
    """ if entry field for ticker symbol is empty or no radio button is selected or no checkbox is selected
    or date range is selected but no date range is given or checkbox for excel download is selected but no file name given"""
    if symbol_len == 0 \
    or selected == 0 \
    or (check1_val == 0 and check2_val == 0) \
    or (selected == 3 and (start_date == '' or end_date == '')) \
    or (check1_val == 1 and filename_len == 0):
        #error message is set
        msg = 'Msg: Some fields are empty.' 
        #null_chk flag is set to 1
        null_chk = 1
    else:
        #error message is set to empty string        
        msg = ''
        #null_chk flag is set to 0        
        null_chk = 0      
    return null_chk, msg 

#Function to validate date format
def date_format_validation(date):
    #check if date is in yyyy-mm-dd
    try:
        datetime.strptime(date, '%Y-%m-%d')
        #msg is assigned with empty string
        msg = ''
        #flag is set to 0 
        dform_val = 0
    except:
        #if the date is not in yyyy-mm-dd format then the below message is printed
        msg = "Incorrect data format, should be YYYY-MM-DD"
        #flag is set to 1
        dform_val = 1
        #the message and flag are returned
    return dform_val, msg
    
#Function to validate date range     
def date_range_validation(start_date, end_date, validate):
    #todays date is obtained
    todays_date = datetime.today()
    #todays date is converted to yyyy-mm-dd format
    todays_date = todays_date.strftime('%Y-%m-%d')
    #check is done if start date is greater than end date
    if start_date > end_date:
        #the coressponding flag is set to 1 in the error case
        dr_chk = 1
        #appropriate error message is stored
        msg = 'Start Date is greater than End Date'
        
        """if the end date passed is greater than todays date and this is for the case 
        for start date and end date and not end date and predict date comparison"""        
    elif end_date > todays_date and validate == 0:
        #the coressponding flag is set to 1 in the error case
        dr_chk = 1
        #appropriate error message is stored
        msg = 'End Date is greater than today''s date' 
    #otherwise    
    else:
        #message is set to a empty string
        msg = ''
        #the coressponding flag is set to 0 indicating no errors      
        dr_chk = 0 
    #the flag and the message are returned    
    return dr_chk , msg

#Function to validate the crystal ball tab(prediction) input fields
def date_chk_pred( start, end, predict, selected):
    #check if any of the input fields in the crystal ball tab is empty
    if selected == 0 or start == '' or end == '' or predict == '':
        #appropriate error message is printed 
        status_msg = tk.messagebox.showerror(title='Error Message', 
                                                     message= 'Msg: Some fields are empty.')
        #precheck is failed 
        precheck = 1
    else:
        #precheck is passed
        precheck = 0        
    
    if precheck == 0:
        dform_val, msg = date_format_validation(start)
        if dform_val == 1:
            #appropriate error message is printed 
            status_msg = tk.messagebox.showerror(title='Error Message', 
                                                         message= msg)
            #precheck is failed 
            precheck = 1
        else:
            #precheck is passed 
            precheck = 0
            
    if precheck == 0:
        dform_val, msg = date_format_validation(end)
        if dform_val == 1:
            #appropriate error message is printed 
            status_msg = tk.messagebox.showerror(title='Error Message', 
                                                         message= msg) 
            #precheck is failed 
            precheck = 1
        else:
            #precheck is passed 
            precheck = 0 
                
    if precheck == 0:
        dform_val, msg = date_format_validation(predict)
        if dform_val == 1:
            #appropriate error message is printed 
            status_msg = tk.messagebox.showerror(title='Error Message', 
                                                     message= msg)
            #precheck is failed 
            precheck = 1
        else:
            #precheck is passed
            precheck = 0         
            
    if precheck == 0:       
        dr_chk, msg = date_range_validation(start, end, 0)
        if dr_chk == 1:
            #appropriate error message is printed 
            status_msg = tk.messagebox.showerror(title='Error Message', message= msg)
            #precheck is failed 
            precheck = 1
        else:
            #precheck is passed
            precheck = 0 
            
    if precheck == 0:       
        dr_chk, msg = date_range_validation(end, predict, 1)
        msg = 'Cannot predict for date prior to modelling period'
        if dr_chk == 1:
            status_msg = tk.messagebox.showerror(title='Error Message', message= msg )
            #precheck is failed 
            precheck = 1
        else:
            #precheck is passed
            precheck = 0        
    #returning precheck 
    return precheck            
                

#Function to perform preckecks before submission        
def perform_precheck(start_date, end_date, ticker_symbol_e,selected, check1_val,check2_val, filename_e):
    #network check for google url is done
    nw_chk, msg =  nw_check('http://www.google.com')
    #if network check flag is set to 0 , this means internet is connected and no issues
    if nw_chk == 0:
        #internet is connected is printed
        print(msg) 
        #precheck flag is set to 0
        precheck = 0
    #otherwise    
    else:
        #error message is printed saying you are not connected to the internet
        status_msg = tk.messagebox.showerror(title='Error Message', message =  msg)
        #precheck flag is set to 1        
        precheck = 1   
        
    #if precheck is passed    
    if precheck == 0:
        #the length of entry field for ticker symbol is stored
        symbol_len = len(ticker_symbol_e.get())
        #the length of filepath is stored 
        filename_len = len(filename_e.get())
        #the selected radio button for time range is stored 
        selected = selected.get()  
        #the checkbox1 selected value is stored
        check1_val = check1_val.get() 
        #the checkbox2 selected value is stored        
        check2_val = check2_val.get() 
        #null input check is done for the empty fields          
        null_chk, msg =  null_input_check(symbol_len,selected, check1_val,check2_val, start_date, end_date, filename_len)
        #if null check is failed
        if null_chk == 1:
            #appropriate error message is displayed
            status_msg = tk.messagebox.showerror(title='Error Message', message= msg)
            #precheck is failed
            precheck = 1
        #otherwise    
        else:
            #precheck is passed
            precheck = 0
    
    #if precheck is passed and date range radio button is selected
    if precheck == 0 and selected == 3: 
        #date format validation is done for start date
        dform_val, msg = date_format_validation(start_date)
        #if date format validation is failed
        if dform_val == 1:
            #appropriate staus message is displayed
            status_msg = tk.messagebox.showerror(title='Error Message', 
                                                     message= msg)
            #precheck is failed
            precheck = 1
        #otherwise     
        else:           
            #precheck is passed
            precheck = 0
            
    #if precheck is passed and date range radio button is selected
    if precheck == 0 and selected == 3: 
        #date format validation is done for end date        
        dform_val, msg = date_format_validation(end_date)
        #if date format validation is failed
        if dform_val == 1:
            #appropriate staus message is displayed
            status_msg = tk.messagebox.showerror(title='Error Message', 
                                                     message= msg)
            #precheck is failed
            precheck = 1
        #otherwise   
        else:
            #precheck is passed   
            precheck = 0            
    
    #if precheck is passed and date range radio button is selected        
    if precheck == 0 and selected == 3:  
        #date range validation is performed
        dr_chk, msg = date_range_validation(start_date, end_date, 0)
        #if date range validation failed
        if dr_chk == 1:
            #appropriate staus message is printed
            status_msg = tk.messagebox.showerror(title='Error Message', message= msg)
            #precheck is failed
            precheck = 1
        #otherwise      
        else:
            #precheck is passed            
            precheck = 0                        
    #precheck vlue is returned
    return precheck


