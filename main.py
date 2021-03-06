from bs4 import BeautifulSoup
from selenium import webdriver
import csv
import datetime
from datetime import date


def writeToCSV(daily_liste, tag):
    aktuellesDatum = date.today() + datetime.timedelta(days = tag - 3)
    if aktuellesDatum.weekday() == 5:
        return None
    with open('Liste_' + str(aktuellesDatum) + '.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(daily_liste)


def strtoArray(symbol_String):
    csv_array = []
    string = ""
    for i in symbol_String:
        if i == " ":
            csv_array.append(string)
            string = ""
        else:
            string = string + i
    return csv_array


def blaettern(driver, filter_true):
    content = driver.find_elements_by_class_name("time-belt__item")
    j = 0
    for i in content:
        i.click()
        print(i.text)
        daily_list = readToArray(driver, filter_true,  j)
        writeToCSV(daily_list,j)
        j += 1
    driver.close()


def readToArray(driver, filter_true, tag):
    content = driver.find_elements_by_class_name("market-calendar-table__row")
    print(content)
    symbol_key = 0  # 1 -> Pre Market; 2 -> After Hours; 3 -> Time not supplied
    daily_array = []
    j = 0
    for symbol in content:
        symbol_string = symbol.text
        symbol_string = symbol_string.replace(" ", "")
        symbol_string = symbol_string.replace("\n", " ")
        symbol_array = strtoArray(symbol_string)
        symbol_array = list(filter(None, symbol_array))
        img_src = symbol.find_element_by_class_name("market-calendar-table__icons").get_attribute("src")
        if "time-pre-market" in img_src:
            symbol_key = 1
        elif "time-after-hours" in img_src:
            symbol_key = 2
        elif "time-not-supplied" in img_src:
            symbol_key = 3
        else:
            print("Fehler - key")
        symbol_array.append(symbol_key)
        print(symbol_array)
        print("_____________")
        if (tag < 3):
            j = 2
        symbol_array_wert = symbol_array[2 + j].replace(",", "")
        symbol_array_wert = symbol_array_wert.replace("$", "")
        if (int(symbol_array_wert) > 3000000000 and filter_true):
            daily_array.append(symbol_array)
    return daily_array


filter_true = True  # 3 Mrd Market Cap
your_driver = webdriver.Safari(executable_path="/usr/bin/safaridriver")
URL = "https://www.nasdaq.com/market-activity/earnings"
page = your_driver.get(URL)
html_code = your_driver.page_source
blaettern(your_driver, filter_true)
# daily_liste = readToArray(your_driver, filter_true)
# writeToCSV(daily_liste)
