from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from seleniumrequests import Chrome
import csv
import random
import string
import unidecode
import time
import numpy as np
import re
url = 'www.google.com' # URL to crawl
nextPageButtonClass = 'fa-angle-double-right' # button for next page
jquery = open("jquery.min.js", "r").read()
chromeOptions = Options()
chromeOptions.add_argument("--kiosk")

driver = webdriver.Chrome("C:/Users/damia/Downloads/chromedriver.exe")
driver.delete_all_cookies()
driver.get(url)

print(driver.title)
print(driver.current_url)
entries = []
citiesElementsArray = driver.find_element_by_xpath('/html/body/div[8]/div[2]/div[1]/div[1]/div[2]').find_elements_by_tag_name('a')
citiesLinks = []
start = False
for c in citiesElementsArray:
  citiesLinks.append([c.get_attribute('href'), c.text])
print(citiesLinks)
cityKey = 0
for cityLink in citiesLinks:
  driver.get(cityLink[0])
  currentCity = cityLink[1]
  try:
    nextPageElement = driver.find_element_by_class_name('fa-angle-double-right')
  except:
    continue
  page = 1
  while nextPageElement:
    print ('page:' + str(page))
    schoolsTiles = driver.find_elements_by_class_name('item')
    for tileOfCompany in schoolsTiles:
      try:
        headerOfCompany = tileOfCompany.find_element_by_class_name('info')
        currentCompany = headerOfCompany.find_element_by_tag_name('a').text
        showButtons = tileOfCompany.find_elements_by_class_name('btn-show')
      except:
        continue
      headerOfCompany = tileOfCompany.find_element_by_class_name('info')
      currentCompany = headerOfCompany.find_element_by_tag_name('a').text
      showButtons = tileOfCompany.find_elements_by_class_name('btn-show')
      countB = 1
      for showButton in showButtons:
        id = showButton.get_attribute('data-id')

        #### EXEVUTE POST REQUESTS ####
        ajax_query = '''
                    $.post( "/Card/Data", {
                        "id" : "%s",
                        "type" : "%s"
                    });
                    ''' % (id,'phone')
        try:
          ajax_query = ajax_query.replace(" ", "").replace("\n", "")
          unparsedPhone = driver.execute_script("return " + ajax_query)
          currentPhone = re.compile(r'<[^>]+>').sub('', unparsedPhone)
        except:
          currentPhone = 'brak'


        ajax_query = '''
                    $.post( "/Card/Data", {
                        "id" : "%s",
                        "type" : "%s"
                    });
                    ''' % (id,'email')
        try:
          ajax_query = ajax_query.replace(" ", "").replace("\n", "")
          unparsedPhone = driver.execute_script("return " + ajax_query)
          currentEmail = re.compile(r'<[^>]+>').sub('', unparsedPhone)
        except:
          currentEmail = 'brak'


        ajax_query = '''
                    $.post( "/Card/Data", {
                        "id" : "%s",
                        "type" : "%s"
                    });
                    ''' % (id,'www')

        try:
          ajax_query = ajax_query.replace(" ", "").replace("\n", "")
          unparsedPhone = driver.execute_script("return " + ajax_query)
          currentWww = re.compile(r'<[^>]+>').sub('', unparsedPhone)
        except:
          currentWww = 'brak'

        ajax_query = '''
                    $.post( "/Card/Data", {
                        "id" : "%s",
                        "type" : "%s"
                    });
                    ''' % (id,'facebook')

        try:
          ajax_query = ajax_query.replace(" ", "").replace("\n", "")
          unparsedPhone = driver.execute_script("return " + ajax_query)
          currentFb = re.compile(r'<[^>]+>').sub('', unparsedPhone)
        except:
          currentFb = 'brak'
        break
      #### ADD DATA TO ARRAY ####
      entries.append([currentCompany, currentCity, currentPhone, currentEmail, currentWww, currentFb])
    #### SAVE FILE ####
    wtr = csv.writer(open ('output.csv', 'w'), delimiter=',', lineterminator='\n')
    for x in entries :
      try:
        wtr.writerow (x)
      except:
        continue
    #### GO TO NEX PAGE ####
    nextPageElement = driver.find_element_by_class_name(nextPageButtonClass)
    page = page + 1
    hasNext = (nextPageElement.find_element_by_xpath('..').find_element_by_xpath('..').get_attribute("class") != 'disabled')
    print('hasNext' + str(hasNext))
    if hasNext:
      nextPageElement.click()
      continue
    else:
      nextPageElement = False
      break
driver.quit()