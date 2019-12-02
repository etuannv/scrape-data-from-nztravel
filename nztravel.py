#!/usr/bin/python3
# -*- coding: utf-8 -*-
__author__ = ["Tuan Nguyen"]
__copyright__ = "Copyright 2018, Tuan Nguyen"
__credits__ = ["Tuan Nguyen"]
__license__ = "GPL"
__version__ = "1.0"
__status__ = "Production"
__author__ = "TuanNguyen"
__email__ = "etuannv@gmail.com"
__website__ = "https://etuannv.com"


# Start import other
from base import *
import shutil
import os
import sys
from urllib.parse import urljoin
from urllib.parse import quote_plus
from urllib.request import urlopen
import logging
import time
import requests
from time import sleep
import re
import csv
import json
import random
from datetime import datetime
from pytz import timezone
from datetime import timedelta



def checkContinue():
    result = False
    if os.path.exists(TempPath):
        #ask for continue
        os.system('clear')
        print ("============== ATTENTION !!! The previous session has not finished ==============")
        print("\n")
        is_continue = confirm(prompt='DO YOU WANT CONTINUE THE PREVIOUS SESSION?', resp=True)
        if not is_continue:
            logging.info("You choice start new session")
            print("\n")
            print("\n")
            try:
                # Delete all file in temp folder
                shutil.rmtree(TempPath)
                # Delete previous result
                # if ResultFileTempPath:
                #     os.remove(ResultFileTempPath)
            except OSError:
                
                sys.exit("Error occur when delete temp folder")
            result = False
        else:
            logging.info("You choice continue previous session")
            print("\n")
            print("\n")
            result = True
    time.sleep(1)
    createFolderIfNotExists(TempPath)
    return result


def tryEnterEndDate(end_date_string):
    retry = 5
    while retry > 0:
        retry -=1
        tag = browser.findByXpath("//input[@id='ctl00_ContentPlaceHolder1_RadDatePicker2_dateInput']")
        tag.clear()
        tag.send_keys(end_date_string)
        time.sleep(.5)

        tag = browser.findByXpath("//input[@id='ctl00_ContentPlaceHolder1_RadDatePicker2_dateInput']")
        if tag:
            if end_date_string == tag.get_attribute('value'):
                return True
    return False


def enterSearchInfo(destination, start_date, end_date, age):
    start_date_string = '{}/{}'.format(start_date.day, start_date.strftime('%m/%Y'))
    end_date_string = '{}/{}'.format(end_date.day, end_date.strftime('%m/%Y'))
    while True:
        try:
            # Start enter value
            browser.selectDropdownByText("//select[@id='ContentPlaceHolder1_dpddestinat']", destination)
            tag = browser.findByXpath("//input[@id='ctl00_ContentPlaceHolder1_RadDatePicker1_dateInput']")
            tag.clear()
            tag.send_keys(start_date_string)
            time.sleep(3)

            tag = browser.findByXpath("//input[@id='ContentPlaceHolder1_txtAge1']")
            tag.clear()
            tag.send_keys(age)
            time.sleep(.3)
            
            # Enter end date
            res = tryEnterEndDate(end_date_string)
            if not res:
                chim_moi()
                continue    

            browser.sendKeys(Keys.TAB)
            time.sleep(.3)
            break
        except:
            chim_moi()
            time.sleep(3)
            pass


def getEssentials():
    value = ''
    note = ''
    # waiting for loading
    while browser.isExistByXPath("//div[@id='ContentPlaceHolder1_AjaxLoadingPanel1ContentPlaceHolder1_lblPremium_CS_D']//img", 0.1):
        time.sleep(0.1)
    time.sleep(1)
    tag = browser.findByXpath("//span[@id='ContentPlaceHolder1_lblPremium_CS_D']")
    if tag:
        value = tag.get_attribute('innerHTML')
        value = removeHtmlTag(value)
        value = getMoney(value)
    
    # get note
    tag = browser.findByXpath("//div[contains(@class,'essentials-color')]//p[@class='prod-info']/preceding-sibling::p[1]")
    if tag:
        temp = tag.get_attribute('innerHTML')
        if 'available to travellers up to 70 years old' in temp:
            note = 'Available up to age 70 only'

    return value, note

def getPremier():
    value = ''
    note = ''
    # waiting for loading
    while browser.isExistByXPath("//div[@id='ContentPlaceHolder1_AjaxLoadingPanel1ContentPlaceHolder1_lblPremium_TI_D']//img", 0.1):
        time.sleep(.1)
    time.sleep(1)
    tag = browser.findByXpath("//span[@id='ContentPlaceHolder1_lblPremium_TI_D']")
    if tag:
        value = tag.get_attribute('innerHTML')
        value = removeHtmlTag(value)
        value = getMoney(value)
    
    # Get note
    tag = browser.findByXpath("//div[contains(@class,'comprehensive-color')]//p[@class='prod-info']/preceding-sibling::p[1]")
    if tag:
        temp = tag.get_attribute('innerHTML')
        if 'available to travellers up to 70 years old' in temp:
            note = 'Available up to age 70 only'

    return value, note

def getFrequent():
    value = ''
    note = ''
    # waiting for loading
    while browser.isExistByXPath("//div[@id='ContentPlaceHolder1_AjaxLoadingPanel1ContentPlaceHolder1_lblPremium_TI_F']//img", 0.1):
        time.sleep(0.1)
    time.sleep(1)
    tag = browser.findByXpath("//span[@id='ContentPlaceHolder1_lblPremium_TI_F']")
    if tag:
        value = tag.get_attribute('innerHTML')
        value = removeHtmlTag(value)
        value = getMoney(value)
    
    # Get Note
    tag = browser.findByXpath("//div[contains(@class,'frequent-color')]//p[@class='prod-info']/preceding-sibling::p[1]")
    if tag:
        temp = tag.get_attribute('innerHTML')
        if 'available to travellers up to 70 years old' in temp:
            note = 'Available up to age 70 only'

    return value, note


def getDataFor(data):
    result = data.copy()
    run_date = datetime.now(timezone('Pacific/Auckland'))
    # Start = Run_Date + Departure
    # End = Start + Duration - 1
    departure = int(data['Departure'])
    # if departure > 364:
    #     departure = 364
    start_date = run_date + timedelta(days=departure)
    end_date = start_date + timedelta(days=int(data['Duration']) - 1)

    result['Departure'] = departure
    result['Run_Date'] = run_date.strftime('%Y-%m-%d')
    result['Start'] = start_date.strftime('%Y-%m-%d')
    result['End'] = end_date.strftime('%Y-%m-%d')

    # Enter search info
    enterSearchInfo(data['Destination'], start_date, end_date, data['Age'])
    
    # waiting for loading
    
    while browser.isExistByXPath("//div[@id='ContentPlaceHolder1_AjaxLoadingPanel1ContentPlaceHolder1_lblPremium_CS_D']//img", 0.1):
        time.sleep(0.1)
    
    time.sleep(3)
    # Start to get data
    # import pdb; pdb.set_trace()
    # --- GET ESSENTIALS
    # click $250
    browser.tryClickByXpath("//input[@id='ContentPlaceHolder1_rdoExcessCS_D_0']", 5)
    result['Essentials250'], result['Essentials250_Note'] = getEssentials()
    # import pdb; pdb.set_trace()
    # click $100
    browser.tryClickByXpath("//input[@id='ContentPlaceHolder1_rdoExcessCS_D_1']", 5)
    result['Essentials100'], result['Essentials100_Note'] = getEssentials()
    
    # --- PREMIER
    # click $250
    browser.tryClickByXpath("//input[@id='ContentPlaceHolder1_rdoExcessTI_D_0']", 5)
    result['Premier250'], result['Premier250_Note'] = getPremier()
    
    # click $100
    browser.tryClickByXpath("//input[@id='ContentPlaceHolder1_rdoExcessTI_D_1']", 5)
    result['Premier100'], result['Premier100_Note'] = getPremier()

    # click $0
    browser.tryClickByXpath("//input[@id='ContentPlaceHolder1_rdoExcessTI_D_2']", 5)
    result['Premier0'], result['Premier0_Note'] = getPremier()

    # FREQUENT TRAVELLER
    # click $250
    browser.tryClickByXpath("//input[@id='ContentPlaceHolder1_rdoExcessTI_F_0']", 5)
    result['Frequent250'], result['Frequent250_Note'] = getFrequent()

    # click $100
    browser.tryClickByXpath("//input[@id='ContentPlaceHolder1_rdoExcessTI_F_1']", 5)
    result['Frequent100'], result['Frequent100_Note'] = getFrequent()

    # click $0
    browser.tryClickByXpath("//input[@id='ContentPlaceHolder1_rdoExcessTI_F_2']", 5)
    result['Frequent0'], result['Frequent0_Note'] = getFrequent()
    
    
    return result

def chim_moi():
    logging.info("Chim moi")
    while True:
        try:
            browser.getUrl('https://www.nz-travel-insurance.co.nz')
            time.sleep(5)
            browser.selectDropdownByText("//select[@id='ContentPlaceHolder1_Widget_dpddestinat']", 'United States')


            tag = browser.findByXpath("//input[@id='ContentPlaceHolder1_Widget_txtpeople']")
            tag.clear()
            tag.send_keys('1')

            tag = browser.findByXpath("//input[@id='ContentPlaceHolder1_Widget_txtAge1']")
            tag.clear()
            tag.send_keys('33')

            

            tag = browser.findByXpath("//input[@id='ctl00_ContentPlaceHolder1_Widget_RadDatePicker1_dateInput']")
            tag.clear()
            tag.send_keys('18/06/2019')
            time.sleep(3)
            
            # try to enter enddate
            retry = 5
            while retry > 0:
                retry -=1
                tag = browser.findByXpath("//input[@id='ctl00_ContentPlaceHolder1_Widget_RadDatePicker2_dateInput']")
                tag.clear()
                tag.send_keys('20/06/2019')

                tag = browser.findByXpath("//input[@id='ctl00_ContentPlaceHolder1_Widget_RadDatePicker2_dateInput']")
                if tag:
                    if '20/06/2019' == tag.get_attribute('value'):
                        break
            
            browser.findByXpath("//input[@id='ContentPlaceHolder1_Widget_btnQuote']").click()
            
            time.sleep(3)
            break        
        except:
            time.sleep(3)
            pass
    

def main(argv):
    global browser, CurrentPath, TempPath
    CurrentPath = os.path.dirname(os.path.realpath(sys.argv[0]))
    InputFilePath = os.path.join(CurrentPath, 'input.csv')

    TempPath = os.path.join(CurrentPath, 'temp_result')
    ResultTempFilePath = os.path.join(TempPath, "result.csv")
    DoneCheckFilePath = os.path.join(TempPath, "done_item.txt")

    # ======= CHECK IF WANT TO CONTINUE PREVIOUS SESSION ========
    checkContinue()

    # ======= READ PROXY IF ANY ========
    PROXY_LIST = [
        'us-il.proxymesh.com',
        'us.proxymesh.com',
        'us-dc.proxymesh.com',
        'us-ca.proxymesh.com',
        'us-wa.proxymesh.com',
        'open.proxymesh.com',
    ]
    proxyArgsList = []
    for proxy in PROXY_LIST:
        proxyArgsList.append({
            'proxy_host': '{}'.format(proxy),
            'proxy_port': 31280,
            'proxy_user': 'your user',
            'proxy_pass': 'your password',
        })
    
    
    # ======= READ PREVIOUS SESSION ========
    # Get done category url list
    done_list = readTextFileToList(DoneCheckFilePath)

    # ======= START MAIN PROGRAM ========
    # READ INPUT FILE
    input_data, header = readCsvToListDict(InputFilePath)
    
    if not len(input_data) > 0:
        logging.info('Input file path: {}'.format(InputFilePath))
        sys.exit("No input data")
    
    
    # changeProxyTotal =50 -- Change proxy each 50 requests   
    #browser = WebBrowser(timeout = 10, isDisableImage = True, isDisableJavascript = False, proxyArgsList=proxyArgsList, changeProxyTotal=50)
    browser = WebBrowser(timeout = 10, isDisableImage = False, isDisableJavascript = False)

    chim_moi()
    counter = 0
    total = len(input_data)
    # header.append('url')
    for data in input_data:
        counter +=1
        logging.info("Process {}/{}".format(counter, total))
        identify_data = '{}, {}, {}, {}'.format(data['Destination'], data['Age'], data['Departure'], data['Duration'])
        if identify_data in done_list:
            continue
        if 0 == counter%20:
            chim_moi()
        result = getDataFor(data)
        
        
        if result is not None:
            writeDictToCSV([result], ResultTempFilePath, 'a', header)
    
        # Write done file
        writeListToTextFile([identify_data], DoneCheckFilePath, 'a')

    
    browser.exitDriver()    
    # ========= POST DONE ===========
    # Move result file to project directory
    if os.path.exists(TempPath):
        final_result_path = os.path.join(CurrentPath, 'result_at_{}'.format(getCurrentDateString("%Y%m%d_%H%M%S")))
        shutil.move(TempPath, final_result_path)
    # Rename temp folder
    # if os.path.exists(TempPath):
        # temp_done = os.path.join(CurrentPath, "temp_at_" + getCurrentDateString("%Y%m%d_%H%M%S"))
        # shutil.move(TempPath, temp_done)
        #shutil.rmtree(TempPath)

    return True


if __name__ == "__main__":

    main(sys.argv)
    logging.info("DONE !!! etuannv@gmail.com ;)")
    sys.exit()