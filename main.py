from tkinter import *
from selenium import webdriver
import csv

from datetime import datetime as DateTime
from datetime import date

def writeToCSV(daily_liste):
    aktuellesDatum = date.today()
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


def auslesen(filter_true, driver_pfad, fitler_mrd):
    driver = webdriver.Safari(executable_path=driver_pfad)
    driver.maximize_window()
    driver.get("https://www.nasdaq.com/market-activity/earnings")
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
        if (int(DateTime.now().strftime('%H%M')) > 2200):
            j = 2
        symbol_array_wert = symbol_array[2 + j].replace(",", "")
        symbol_array_wert = symbol_array_wert.replace("$", "")
        if (int(symbol_array_wert) > (fitler_mrd * (10 ** 9)) and filter_true):
            daily_array.append(symbol_array)
    driver.close()
    return daily_array


def start_scraper(driver_pfad, filter_mrd):
    filter_true = False
    filter_mrd = float(filter_mrd)
    if filter_mrd != 0:
        filter_true = True
    writeToCSV(auslesen(filter_true, driver_pfad, filter_mrd))



# Die folgende Funktion soll ausgeführt werden, wenn
# der Benutzer den Button Klick me anklickt
def button_action():
    entry_text = eingabefeld.get()
    entry_text2 = eingabefeld_filter.get()
    if (entry_text == ""):
        welcome_label.config(text="Gib einen Pfad ein")
    else:
        ausgabe_text = "Pfad eingegeben " + entry_text + " - Filter in Mrd: " + entry_text2
        if( "/usr/bin/safaridriver" == entry_text):
            print("passt")
        else:
            print(ausgabe_text)
        start_scraper(entry_text,entry_text2)
        welcome_label.config(text=ausgabe_text)
        fenster.quit()


fenster = Tk()
fenster.title("Ich warte auf eine Eingabe von dir.")

# Anweisungs-Label
my_label = Label(fenster, text="Gib deinen Pfad ein: ")
label_filter = Label(fenster, text="Filter in Mrd: ")

# In diesem Label wird nach dem Klick auf den Button der Benutzer
# mit seinem eingegebenen Namen begrüsst.
welcome_label = Label(fenster)

# Hier kann der Benutzer eine Eingabe machen
eingabefeld = Entry(fenster, bd=5, width=40)
eingabefeld_filter = Entry(fenster, bd=8, width=40)

welcom_button = Button(fenster, text="Bestätigen", command=button_action)
exit_button = Button(fenster, text="Beenden", command=fenster.quit)

# Nun fügen wir die Komponenten unserem Fenster hinzu
my_label.grid(row=0, column=0)
label_filter.grid(row=1, column=0)
eingabefeld.grid(row=0, column=1)
eingabefeld_filter.grid(row=1, column=1)
welcom_button.grid(row=2, column=0)
exit_button.grid(row=2, column=1)
welcome_label.grid(row=3, column=0, columnspan=2)

mainloop()
