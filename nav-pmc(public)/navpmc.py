#!/Users/{your name}/Code/pythonProjects/Navigate_PMC/navpmc-env/bin/Python3

#^^^ The above is the directory of Python Virtual Environment that contains imported libraries. ** YOU MUST INSTALL VIRTUAL ENVIRONMENT**

import os
import shutil
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import time
from datetime import date



#Make sure you have the correct chrome webdriver(version 78.0 is the correct one as of 11.21.19
#For MAC, Make sure webdriver is installed in /usr/local/bin

driver = webdriver.Chrome() # Connect to Driver
driver.get('https://pmccoingroup.com/login') # Connect to Website


username = driver.find_element_by_name('email') #Get DOM name of username box from website
password = driver.find_element_by_name('password') # Get DOM name of password box from website
loginButton = driver.find_element_by_xpath("//button[@type='submit']") #Get login button via XPATH

#There is an easy way to set it up so that email and password is not hard coded into the script,
#   In this instance it just made sense to hard code the email and password.

username.send_keys('{your email}') #Pass username into email field
password.send_keys('{your password}') #Pass password into password field
loginButton.click()

pmcDash = driver.find_element_by_xpath("//ul[@class='navbar-nav']/li[7]") #Get dashboard tab button
pmcDash.click() #Click on dashboard tab button

trxRep = driver.find_element_by_xpath("//ul[@class='nav nav-tabs']/li[4]")#Get transaction report tab button
trxRep.click() #Click on transaction report tab button

time.sleep(1) #Quick wait timer to avoid issues
exportFile = driver.find_element_by_xpath("//button[@class='btn btn-link']") #Get 'export file' hyperlink button
action = ActionChains(driver) 
time.sleep(1)
action.move_to_element(exportFile)#"Hover over 'export file'
time.sleep(1)
exportFile.click()#Click on 'export file'
time.sleep(8)

#In case there is a delay in downloading export, an 8 second wait occurs before the following code:
#Get the date, format date as M.D.Y -> rename the download exports as "PMC {M.D.Y}.csv"
#2 files are exported, same steps are repeated for the second file

today = date.today()
DMY = today.strftime("%m.%d.%y")

destination = f'/Users/{your name}/Downloads/PMC Import {DMY}.csv'
source = '/Users/{your name}/Downloads/transactions_report.csv'
send = shutil.move(source,destination)

destination = f'/Users/{your name}/Downloads/Contacts Report {DMY}.csv'
source = '/Users/{your name}/Downloads/contacts_report.csv'
send = shutil.move(source,destination)

