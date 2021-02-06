#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 28 09:49:32 2020

NAME:
    genesis - This module contains functions that accept user choice for interface and call related modules.

FILE:
    command_line_functions.py

FUNCTIONS:
    get_ui_choice

@author: donsam
"""

#pre-defined modules
import sys

#user-defined modules
import main_window as mw
import command_line_functions as cf


#Function to get the choice of interface
def get_ui_choice():
    #Print message to get the choice
    print('Welcome to Bull Stocks\nEnter the user interface choice')
    #The different choice are displayed and ui_choice stores 1 or 2 based on choice
    ui_choice = input('1. Graphical User Interface\n2. Command Line Interface\n3. Quit\n')
    #if user choice is 1 ie, Graphical User Interface    
    if ui_choice == '1':
       #main window operations are executed from module main_window
       mw.main_win_operations() 
    #if user choice is 2 ie, Command Line Interface      
    elif ui_choice == '2':
         #command line operations are executed from module command_line_functions
         cf.command_line_operations()
    #if user choice is 3 ie. Quit      
    elif ui_choice == '3':
        #Quit1
        sys.exit('Quitting')     
    #Otherwise     
    else:
        #Error message saying Invalid Choice is printed
        print('Invalid choice')
        #User choice menu is displayed again to get the right choice from menu options
        get_ui_choice()

#specifies the interpreter this program is the main program to be run
if __name__ == '__main__':
    get_ui_choice()
    
