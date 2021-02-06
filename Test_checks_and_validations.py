#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 29 15:29:09 2020

NAME:
    Test_checks_and_validations - This module contains functions that are used for 
                                  unit testing some functions in checks_and_validations module

FILE:
    Test_checks_and_validations.py
    
CLASSES:
    test_checks_and_validations

FUNCTIONS:
    test_nw_check
    test_null_input_check
    test_date_format_validation
    test_date_range_validation

@author: donsam
"""

#pre-defined module
import unittest

#user-defined module
import checks_and_validations as cv


class test_checks_and_validations(unittest.TestCase):
    #unit test for network check function 
    def test_nw_check(self):

        nw_chk, msg =  cv.nw_check('http://www.google.com')
        self.assertTrue(nw_chk >= 0) 
        
    #unit test for null input check function   
    def test_null_input_check(self):
        #null input is tested where no input is given in the main window
        null_chk, msg =  cv.null_input_check(0,0, 0,0, '', '',0)
        #null input is tested where only date range is passed  in the main window
        self.assertAlmostEqual(null_chk, 1) 
        null_chk, msg =  cv.null_input_check(0,0, 0,0, '2018-01-01', '2017-03-05',1)
        self.assertAlmostEqual(null_chk, 1)  
        null_chk, msg =  cv.null_input_check(0,0, 0,0, '', '',1)
        self.assertAlmostEqual(null_chk, 1) 
        null_chk, msg =  cv.null_input_check(4,3, 1,1, '2020-02-02', '2020-03-04',1)
        self.assertAlmostEqual(null_chk, 0) 

    #unit test for date_format_validation function         
    def test_date_format_validation(self):
        #negative case test where invalid date format is passed
        dflag, msg = cv.date_format_validation('2020')
        self.assertAlmostEqual(dflag, 1)
        #positive case test where valid date is passed
        dflag, msg = cv.date_format_validation('2020-02-02')
        self.assertAlmostEqual(dflag, 0)
        
    #unit test for date_range_validation function        
    def test_date_range_validation(self):
        #negative case test where invalid date range is passed for start date and end date
        dr_chk, msg = cv.date_range_validation('2018-01-01', '2017-03-05',0)
        self.assertAlmostEqual(dr_chk, 1)
        #positive case test where valid date range is passed for start date and end date
        dr_chk, msg = cv.date_range_validation('2018-01-01', '2018-03-05',0)
        self.assertAlmostEqual(dr_chk, 0)
        
        #negative case test where invalid date range is passed for end date and predict date
        dr_chk, msg = cv.date_range_validation('2018-01-01', '2017-03-05',1)
        self.assertAlmostEqual(dr_chk, 1)
        #positive case test where valid date range is passed for end date and predict date
        dr_chk, msg = cv.date_range_validation('2018-01-01', '2018-03-05',1)
        self.assertAlmostEqual(dr_chk, 0)
        
#specifies the interpreter this program is the main program to be run
if __name__ =='__main__':
    unittest.main()    
 
    