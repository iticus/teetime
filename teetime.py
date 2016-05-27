#!/usr/bin/env python2.7
'''
Created on May 13, 2016

@author: ionut
'''

import logging
import sys
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select

import settings
import utils

logging.info("starting teetime booking application")

#calculate date / time values
dates = utils.days_to_dates(settings.DAYS)
min_seconds = utils.timestr_to_seconds(settings.INTERVAL[0])
max_seconds = utils.timestr_to_seconds(settings.INTERVAL[1])

if not dates:
    logging.info('no dates to book found, exiting')
    sys.exit()

from pyvirtualdisplay import Display
display = Display(visible=0, size=(800, 600))
display.start()

logging.info('initializing browser')
browser = webdriver.Firefox()
browser.get(settings.BASE_URL)
time.sleep(2)

browser.find_element_by_id("btnSignIn").click()
time.sleep(2)

logging.info('logging in')
username = browser.find_element_by_id("txtLogInName")
password = browser.find_element_by_id("txtPassword")

username.send_keys(settings.USERNAME)
time.sleep(1)
password.send_keys(settings.PASSWORD)
time.sleep(1)
browser.find_element_by_id("btnLogIn").click()

logging.info('logged in')
for date in dates:
    found_slot = False
    logging.info('searching tee times for %s' % date.strftime('%m/%d/%Y'))
    browser.find_element_by_id("rdpSearchStartDate_popupButton").click()
    time.sleep(1)
    calendar = browser.find_element_by_id("rdpSearchStartDate_dateInput")
    calendar.click()
    calendar.clear()
    time.sleep(1)
    calendar.send_keys(date.strftime('%m/%d/%Y'))
    calendar.send_keys(Keys.ENTER)
    time.sleep(16) #wait for the ajax call to complete
    
    logging.info('selecting number of players: %s' % settings.PLAYERS)
    select = Select(browser.find_element_by_id("ddlSearchPlayers"))
    select.select_by_visible_text(str(settings.PLAYERS))
    time.sleep(16) #wait for the ajax call to complete

    elements = []
    try:
        elements.extend(browser.find_elements_by_class_name("pnlReservationSearch_PreLoaded_Even"))
    except:
        pass
    try:
        elements.extend(browser.find_elements_by_class_name("pnlReservationSearch_PreLoaded_Odd"))
    except:
        pass
    
    if not elements:
        logging.warning('could not find any available tee times for %s' % date.strftime('%m/%d/%Y'))
        continue
    
    elements = utils.sort_elements(elements)
    for element in elements:
        tms = element.find_elements_by_class_name('PodLabel_TeeTime')[0]
        text = tms.get_attribute('innerHTML')
        logging.info('checking timeslot: %s' % text)
        seconds = utils.timestr_to_seconds(text)
        if min_seconds <= seconds <= max_seconds:
            #book
            found_slot = True
            logging.info('found timeslot: %s, booking it' % text)
            button_class = 'PodButton_Reserve%d' % settings.PLAYERS
            element.find_elements_by_class_name(button_class)[0].click()
            time.sleep(16)
            
            #use this to confirm
            browser.find_element_by_id('chkPolicyAgreement').click()
            time.sleep(1)
            browser.find_element_by_id('btn_process').click()
            time.sleep(1)
            browser.find_element_by_id('btnFinish').click()

            logging.info('booked timeslot %s' % text) #TODO: lblConfirmationNumber
            time.sleep(16)
            #use this to cancel
            #browser.find_element_by_id('btnCancelReservation').click()
            break
        
    if found_slot:
        break
    else:
        logging.warning('could not find any matching timeslot for %s' % date.strftime('%m/%d/%Y'))
    
logging.info('closing browser')
browser.close()
time.sleep(1)
logging.info('exiting')
display.stop()