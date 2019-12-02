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
from enum import Enum
from lxml import html

class Package(Enum):
    P_250 = '2'
    P_100 = '1'
    P_0 = '0'
    


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


def getEssentials():
    # waiting for loading
    while browser.isExistByXPath("//div[@id='ContentPlaceHolder1_AjaxLoadingPanel1ContentPlaceHolder1_lblPremium_CS_D']//img", 0.2):
        time.sleep(0.2)

    tag = browser.findByXpath("//span[@id='ContentPlaceHolder1_lblPremium_CS_D']")
    if tag:
        value = tag.get_attribute('innerHTML')
        value = removeHtmlTag(value)
        value = getMoney(value)
        return value
    return ''

def getPremier():
    # waiting for loading
    while browser.isExistByXPath("//div[@id='ContentPlaceHolder1_AjaxLoadingPanel1ContentPlaceHolder1_lblPremium_TI_D']//img", 0.2):
        time.sleep(0.2)

    tag = browser.findByXpath("//span[@id='ContentPlaceHolder1_lblPremium_TI_D']")
    if tag:
        value = tag.get_attribute('innerHTML')
        value = removeHtmlTag(value)
        value = getMoney(value)
        return value
    return ''

def getFrequent():
    # waiting for loading
    while browser.isExistByXPath("//div[@id='ContentPlaceHolder1_AjaxLoadingPanel1ContentPlaceHolder1_lblPremium_TI_F']//img", 0.2):
        time.sleep(0.2)

    tag = browser.findByXpath("//span[@id='ContentPlaceHolder1_lblPremium_TI_F']")
    if tag:
        value = tag.get_attribute('innerHTML')
        value = removeHtmlTag(value)
        value = getMoney(value)
        return value
    return ''

def requestData(destination_code, start_date, end_date, age, essential_pack, premier_pack, frequent_pack):
    essential =''
    premier=''
    frequent=''
    while True:
        payload = {
            'ctl00$RadScriptManager1': 'ctl00$RadScriptManager1|ctl00$ContentPlaceHolder1$btnPremiumUpdate',
            'RadScriptManager1_TSM': '',
            '__EVENTTARGET': 'ctl00$ContentPlaceHolder1$btnPremiumUpdate',
            '__EVENTARGUMENT': '',
            '__LASTFOCUS': '',
            '__VIEWSTATE': ViewState,
            '__VIEWSTATEGENERATOR': ViewStateGenerator,
            'ctl00$ContentPlaceHolder1$dpddestinat': destination_code,
            'ctl00$ContentPlaceHolder1$RadDatePicker1': start_date.strftime('%Y-%m-%d'),
            'ctl00$ContentPlaceHolder1$RadDatePicker1$dateInput': start_date.strftime('%d/%m/%Y'),
            'ctl00_ContentPlaceHolder1_RadDatePicker1_dateInput_ClientState': '',
            'ctl00_ContentPlaceHolder1_RadDatePicker1_calendar_SD': '[]',
            'ctl00_ContentPlaceHolder1_RadDatePicker1_calendar_AD': '[[2019,5,15],[2099,12,30],[2019,5,15]]',
            'ctl00_ContentPlaceHolder1_RadDatePicker1_ClientState': '',
            'ctl00$ContentPlaceHolder1$RadDatePicker2': end_date.strftime('%Y-%m-%d'),
            'ctl00$ContentPlaceHolder1$RadDatePicker2$dateInput': end_date.strftime('%d/%m/%Y'),
            'ctl00_ContentPlaceHolder1_RadDatePicker2_dateInput_ClientState': '',
            'ctl00_ContentPlaceHolder1_RadDatePicker2_calendar_SD': '[]',
            'ctl00_ContentPlaceHolder1_RadDatePicker2_calendar_AD': '[[2019,5,15],[2099,12,30],[2019,5,15]]',
            'ctl00_ContentPlaceHolder1_RadDatePicker2_ClientState': '',
            'ctl00$ContentPlaceHolder1$txtpeople': '1',
            'ctl00$ContentPlaceHolder1$txtChildren': '0',
            'ctl00$ContentPlaceHolder1$txtAge1': age,
            'ctl00$ContentPlaceHolder1$txtAge2': '',
            'ctl00$ContentPlaceHolder1$txtAge3': '',
            'ctl00$ContentPlaceHolder1$txtAge4': '',
            'ctl00$ContentPlaceHolder1$txtAge5': '',
            'ctl00$ContentPlaceHolder1$txtAge6': '',
            'ctl00$ContentPlaceHolder1$txtAge7': '',
            'ctl00$ContentPlaceHolder1$txtAge8': '',
            'ctl00$ContentPlaceHolder1$txtAge9': '',
            'ctl00$ContentPlaceHolder1$txtAge10': '',
            'ctl00$ContentPlaceHolder1$rdoExcessCS_D': essential_pack,
            # 'ctl00$ContentPlaceHolder1$hdnPremium_CS_D': '6600',
            'ctl00$ContentPlaceHolder1$hdnDiscount_CS_D': '0',
            'ctl00$ContentPlaceHolder1$hdnPlan_CS_D': 'F',

            'ctl00$ContentPlaceHolder1$rdoExcessTI_D': premier_pack,
            # 'ctl00$ContentPlaceHolder1$hdnPremium_TI_D': '8600',
            'ctl00$ContentPlaceHolder1$hdnDiscount_TI_D': '0',
            'ctl00$ContentPlaceHolder1$hdnPlan_TI_D': 'F',

            'ctl00$ContentPlaceHolder1$rdoExcessTI_F': frequent_pack,
            # 'ctl00$ContentPlaceHolder1$hdnPremium_TI_F': '34900',
            'ctl00$ContentPlaceHolder1$hdnDiscount_TI_F': '0',
            'ctl00$ContentPlaceHolder1$hdnPlan_TI_F': 'F',
            '__ASYNCPOST': 'true',
            '': ''
        }

        response = requests.post('https://www.nz-travel-insurance.co.nz/processing/ChooseAPlan.aspx', headers=headers, cookies=cookies, data=payload)
        
        root = html.fromstring(response.text)

        essential = root.xpath("//input[@id='ContentPlaceHolder1_hdnPremium_CS_D']/@value")
        if essential:
            essential = essential[0]
        
        premier = root.xpath("//input[@id='ContentPlaceHolder1_hdnPremium_TI_D']/@value")
        if premier:
            premier = premier[0]

        frequent = root.xpath("//input[@id='ContentPlaceHolder1_hdnPremium_TI_F']/@value")
        if frequent:
            frequent = frequent[0]

        import pdb ; pdb.set_trace()
        return essential, premier, frequent

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

    # Get $250
    essential250, premier250, frequent250 = requestData(data['DestinationCode'], start_date, end_date, data['Age'], Package.P_250.value, Package.P_250.value, Package.P_250.value)
    result['Essentials250'] = essential250
    result['Premier250'] = premier250
    result['Frequent250'] = frequent250
    
    # Get $100
    essential100, premier100, frequent100 = requestData(data['DestinationCode'], start_date, end_date, data['Age'], Package.P_100.value, Package.P_100.value, Package.P_100.value)
    result['Essentials100'] = essential100
    result['Premier100'] = premier100
    result['Frequent100'] = frequent100

    # Get $0
    essential0, premier0, frequent0 = requestData(data['DestinationCode'], start_date, end_date, data['Age'], Package.P_100.value, Package.P_0.value, Package.P_0.value)
    # result['Essentials100'] = essential0
    result['Premier0'] = premier0
    result['Frequent0'] = frequent0
    
    
    return result

def getViewStateInfo(sourcecode):
    global ViewState, ViewStateGenerator
    # Search viewstate
    ViewState = re.findall(r'id="__VIEWSTATE" value="(.[^\"]*)', sourcecode, re.MULTILINE)
    if ViewState:
        ViewState = ViewState[0]

    # search viewstagegenerator
    ViewStateGenerator = re.findall(r'id="__VIEWSTATEGENERATOR" value="(.[^\"]*)', sourcecode, re.MULTILINE)
    if ViewStateGenerator:
        ViewStateGenerator = ViewStateGenerator[0]

    return ViewState, ViewStateGenerator

def chim_moi():
    global cookies
    cookies = {}
    session = requests.Session()
    headers = {
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9,sv;q=0.8,vi;q=0.7',
    }

    # response = session.get('https://www.nz-travel-insurance.co.nz/', headers=headers)

    # getViewStateInfo(response.text)

    # data = readTextFile('cookies.json')
    # cookies = json.loads(data)


    browser = WebBrowser(timeout = 10, isDisableImage = False, isDisableJavascript = False)
    while True:
        try:
            browser.getUrl('https://www.nz-travel-insurance.co.nz')
            browser.findByXpath("//input[@id='ctl00_ContentPlaceHolder1_Widget_RadDatePicker1_dateInput']").send_keys('17/06/2019')
            browser.findByXpath("//input[@id='ctl00_ContentPlaceHolder1_Widget_RadDatePicker2_dateInput']").send_keys('20/06/2019')
            browser.selectDropdownByText("//select[@id='ContentPlaceHolder1_Widget_dpddestinat']", 'United States')
            browser.findByXpath("//input[@id='ContentPlaceHolder1_Widget_txtpeople']").send_keys('1')
            browser.findByXpath("//input[@id='ContentPlaceHolder1_Widget_txtAge1']").send_keys('40')
            browser.findByXpath("//input[@id='ContentPlaceHolder1_Widget_btnQuote']").click()
            
            time.sleep(3)
            break        
        except:
            time.sleep(3)
            pass

    # get view state and set to global
    getViewStateInfo(browser.getPageSource())

    # get cookie and set to global
    # cookies = readCookie()
    webcookies = browser.getCookie()
    
    for item in webcookies:
        if 'name' in item:
            if 'ASP.NET_SessionId' == item['name']:
                cookies['ASP.NET_SessionId'] = item['value']
                continue
            
            if 'CTISales_STA' == item['name']:
                cookies['CTISales_STA'] = item['value']
                continue

            if '_ga' == item['name']:
                cookies['_ga'] = item['value']
                continue
            
            if '_gid' == item['name']:
                cookies['_gid'] = item['value']
                continue

            if '_gat' == item['name']:
                cookies['_gat'] = item['value']
                continue
            
            if '_gat_STA' == item['name']:
                cookies['_gat_STA'] = item['value']
                continue
        
    browser.exitDriver()
    
    

def readCookie():

    data = readTextFile('cookies.json')
    jdata = json.loads(data)
    return jdata

def main(argv):
    global browser, CurrentPath, TempPath, ViewState, ViewStateGenerator, headers, cookies
    CurrentPath = os.path.dirname(os.path.realpath(sys.argv[0]))
    InputFilePath = os.path.join(CurrentPath, 'input.csv')

    TempPath = os.path.join(CurrentPath, 'temp_result')
    ResultTempFilePath = os.path.join(TempPath, "result.csv")
    DoneCheckFilePath = os.path.join(TempPath, "done_item.txt")

    headers = {
        'Origin': 'https://www.nz-travel-insurance.co.nz',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9,sv;q=0.8,vi;q=0.7',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Accept': '*/*',
        'Cache-Control': 'no-cache',
        'X-Requested-With': 'XMLHttpRequest',
        'Connection': 'keep-alive',
        'X-MicrosoftAjax': 'Delta=true',
        'Referer': 'https://www.nz-travel-insurance.co.nz/processing/ChooseAPlan.aspx',
    }

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
            'proxy_user': 'Your user',
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
    # browser = WebBrowser(timeout = 10, isDisableImage = False, isDisableJavascript = False)

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
        result = getDataFor(data)
        
        if result is not None:
            writeDictToCSV([result], ResultTempFilePath, 'a', header)
    
        # Write done file
        writeListToTextFile([identify_data], DoneCheckFilePath, 'a')

    
    # browser.exitDriver()    
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