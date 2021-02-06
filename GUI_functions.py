#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 27 19:08:02 2020

NAME:
    GUI_functions - This module contains functions that are used for 
                            handling certain GUI components.

FILE:
    GUI_functions.py

FUNCTIONS:
    initialise_main_window
    get_ticker_symbol
    update_listbox
    check_click
    set_text
    cal_sel
    enable_drange
    disable_drange
    get_date_range
    get_date_radio
    browseFiles
    output_type
    
@author: donsam
"""

#pre-defined modules
import tkinter as tk
from tkcalendar import Calendar,DateEntry
from tkinter import ttk, filedialog 
from functools import partial
from ttkthemes import ThemedStyle
import auxillary_functions as af


#Function to initialise main window and set theme and other properties
def initialise_main_window():
    #Creating main window
    main_win = tk.Tk()
    #Title of main window
    main_win.title('Bull Stocks')
    #Default size of main window
    main_win.geometry('1150x300')
    # Default theme of main window
    style = ThemedStyle(main_win)
    style.set_theme('clearlooks')
    #Background colour for main window
    main_win['bg']='ivory'
    #Returning the variable main window
    return main_win

#Function to get the ticker symbol from the user               
def get_ticker_symbol(main_win, ticker_symbols):        
    #Label for ticker symbol
    symbol_l = ttk.Label(text='Enter the Ticker Symbol').grid(row=1,column=1)
    #Input field for ticker symbol
    ticker_symbol_e = ttk.Entry(width = 45)
    #it is positioned appropriately 
    ticker_symbol_e.grid(row=1,column=2, columnspan = 3)
    #on press of key in the ticker symbol entry field
    ticker_symbol_e.bind('<KeyRelease>', lambda event: check_key(event, 
                                          symbol_list, ticker_symbols))      
       
    #List box with all ticker symbols
    symbol_list = tk.Listbox(main_win, width=45, height=3) 
    #it is positioned appropriately 
    symbol_list.grid(row=2,column=2, columnspan=3)
    update_listbox(ticker_symbols, symbol_list) 
    #selection from the listbox on click selection
    symbol_list.bind('<<ListboxSelect>>',lambda event: check_click(event, 
                                            symbol_list, ticker_symbol_e))
    symbol_list.config(bg = 'khaki')
    
    #Scrollbar for symbol list
    ver_scroll = ttk.Scrollbar( main_win, command=symbol_list.yview, 
                               orient= 'vertical')
    #it is positioned appropriately 
    ver_scroll.grid(row=2, column=5, sticky='w')
    symbol_list.configure(yscrollcommand=ver_scroll.set)
    #Returning the symbol listbox ticker symbol entry field and the ticker symbols    
    return symbol_list, ticker_symbol_e, ticker_symbols  
               
#Function to update the listbox
def update_listbox(data, symbol_list):       
    #clear previous data 
    symbol_list.delete(0,'end')    
    # if the text entered is present in the list of elements in listbox
    for item in data:
        #update the listbox with the text entered in the ticker symbol field
        symbol_list.insert('end', item)
        
#Function for checking the key pressed 
def check_key(event, symbol_list, ticker_symbols): 
    value = event.widget.get()  
    value = value.upper()   
    # get data from ticker_symbols
    if value == '': 
        data = ticker_symbols 
    else: 
        data = ticker_symbols[ticker_symbols.str.contains(value, case=False)]
    # update data in listbox 
    update_listbox(data, symbol_list)  

    
#Function for checking the ticker clicked from symbol_list
def check_click(event, symbol_list, ticker_symbol_e):
    value= symbol_list.get('anchor')
    #splitting ticker symbol and company name by double pipes
    value = value.split(' || ', 1)
    #The first value in the list is selected
    value = value[0]
    #the entry field is set by the value selected
    set_text(ticker_symbol_e, value)  



#Function to set entry field by selection   
def set_text(field, value):
    field.delete(0,'end')
    field.insert(0,value)       
    return


#Function that selects calendar date
def cal_sel(field):
    af.play_sound('Button2.wav')
    def quit_cal():
        af.play_sound('Button2.wav')
        #setting the date variable to the calendar selection
        date = cal.selection_get()
        #setting the entry field by calendar selected date
        set_text(field, date) 
        #calendar window is destroyed after use
        cal_win.destroy()  
    
    #Calendar Window
    cal_win = tk.Tk()
    #title of the calendar is set
    cal_win.title('Calendar')
    #size of the calendar window is set
    cal_win.geometry('450x350')
    #theme style of calendar window is set
    style = ttk.Style(cal_win)
    style.theme_use('clam')
    #calendar popup is created passing the calendar window
    cal = Calendar(cal_win)
    #it is positioned appropriately
    cal.pack(fill='both', expand=True)
    #OK button in Calendar Window    
    ok_b = ttk.Button(cal_win, text='ok', command=quit_cal).pack()
    


    
#Function to enable date range entry and buttons based on user selection of radio button     
def enable_drange(start_date_e, start_date_b, end_date_e, end_date_b ):
    #start date entry field is enabled
    start_date_e.config(state='normal')
    #start date button is enabled
    start_date_b.config(state='normal')
    #end date entry field is enabled
    end_date_e.config(state='normal')
    #end date button is enabled
    end_date_b.config(state='normal')

#Function to disable date range entry and buttons based on user selection of radio button      
def disable_drange(start_date_e, start_date_b, end_date_e, end_date_b ):
    #start date entry field is disabled
    start_date_e.config(state='disabled')
    #start date button is disabled
    start_date_b.config(state='disabled')
    #end date entry field is disabled
    end_date_e.config(state='disabled')
    #end date button is disabled
    end_date_b.config(state='disabled') 

#Function to get the date range entry and buttons based on user selection of radio button  
def get_date_range(main_win):    
    #Start Date Input Field
    start_date_e = ttk.Entry(width=10)
    #it is positioned appropriately
    start_date_e.grid(row=3,column=5, columnspan = 2)
    #start date entry field is disabled by default
    start_date_e.config(state='disabled')
    
    #Start Date Button
    start_date_b=ttk.Button(main_win, text='Start', command=partial(cal_sel, start_date_e))
    #it is positioned appropriately
    start_date_b.grid(row=3,column=9)
    #start date button is disabled by default    
    start_date_b.config(state='disabled')
        
    #End Date Input Field
    end_date_e = ttk.Entry(width=10)
    end_date_e.grid(row=3,column=10)
    #end date entry field is disabled by default    
    end_date_e.config(state='disabled')
    
    #End Date Button
    end_date_b=ttk.Button(main_win, text='End', command=partial(cal_sel, end_date_e))
    #it is positioned appropriately
    end_date_b.grid(row=3,column=11)
    #end date button is disabled by default     
    end_date_b.config(state='disabled') 

    #the entry fields and buttons are returned 
    return start_date_e, start_date_b, end_date_e, end_date_b      



    
#Function to display radio buttons for date selection      
def get_date_radio(main_win, start_date_e, start_date_b, end_date_e, end_date_b):
    selected = tk.IntVar()
    #label for time period
    ttk.Label(main_win, 
            text='Choose a Time Period:').grid(row=3,column=1)
    ttk.Radiobutton(main_win, 
                  text='1 Year',
                  variable= selected, 
                  value=1,
                  command = partial(disable_drange,start_date_e,
                            start_date_b, end_date_e, end_date_b )).grid(row=3,
                                                    column=2, sticky = 'sw')
    #radio button for 5 years                                                                          
    ttk.Radiobutton(main_win, 
                  text='5 Years',
                  variable= selected, 
                  value=2,
                  command = partial(disable_drange,start_date_e, 
                            start_date_b, end_date_e, end_date_b )).grid(row=3,
                            column=3, sticky = 'sw')
    #radio button for Date Range                                                                          
    ttk.Radiobutton(main_win, 
                  text='Date Range\nyyyy-mm-dd format',
                  variable= selected, 
                  value=3,
                  command = partial(enable_drange,start_date_e, start_date_b,
                                    end_date_e, end_date_b )).grid(row=3,
                                    column=4, sticky = 'sw')
    #radio button for 1 Day                                                                  
    ttk.Radiobutton(main_win, 
                  text='1 Day',
                  variable=selected, 
                  value=4,
                  command = partial(disable_drange,start_date_e, start_date_b,
                                    end_date_e, end_date_b )).grid(row=4,
                                    column=2, sticky = 'sw')
    #radio button for 5 Days                                                                   
    ttk.Radiobutton(main_win, 
                  text='5 Days',
                  variable=selected, 
                  value=5,
                  command = partial(disable_drange,start_date_e, start_date_b, 
                                    end_date_e, end_date_b )).grid(row=4,
                                    column=3, sticky = 'sw')
    #radio button for 3 Months                                                                   
    ttk.Radiobutton(main_win, 
                  text='3 Months', 
                  variable=selected, 
                  value=6,
                  command = partial(disable_drange,start_date_e, start_date_b,
                                    end_date_e, end_date_b )).grid(row=5,
                                    column=2, sticky = 'sw')
    #radio button for 6 Months                                                                    
    ttk.Radiobutton(main_win, 
                  text='6 Months',
                  variable=selected, 
                  value=7,
                  command = partial(disable_drange,start_date_e, start_date_b,
                                    end_date_e, end_date_b )).grid(row=5,
                                    column=3, sticky = 'sw')  
    return selected
        

    
#Function to display file explorer window 
def browseFiles(field):
    af.play_sound('Button2.wav')
    filename = filedialog.askopenfilename(initialdir = '/', 
                                          title = 'Select a File', 
                                          filetypes = (('Excel files', 
                                                        '*.xls*'), 
                                                       ('all files', 
                                                      '*.*')))
    #setting the entry field by filepathname
    set_text(field, filename)


#Function to ask user to select the output type      
def output_type(main_win):        
    #Checkbox
    check_l = ttk.Label(main_win,text='Select output format')
    #it is positioned appropriately 
    check_l.grid(row=6,column=1)
    check1_val = tk.IntVar()
    check_c1 = ttk.Checkbutton(main_win, text='Download as Excel file',
                               variable=check1_val)
    #it is positioned appropriately 
    check_c1.grid(row=7 ,column=1, sticky='w')
    #Filename Input Field
    filename_e = ttk.Entry()
    #it is positioned appropriately 
    filename_e.grid(row=7,column=2)
    
    filename_b =ttk.Button(main_win, text='Choose Path', 
                           command=partial(browseFiles, filename_e))
    #it is positioned appropriately 
    filename_b.grid(row=7,column=3)
    check2_val = tk.IntVar()
    check_c2 = ttk.Checkbutton(main_win, text='Display Output Window',
                               variable=check2_val)
    #it is positioned appropriately 
    check_c2.grid(row=8 ,column=1, sticky='w') 
    #the checkboxes and the entry field for filename are returned
    return check1_val, check2_val, filename_e
          