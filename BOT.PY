import requests
import json
import time
from threading import Thread
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from tkinter import *
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC






def entercard(driver):
    id = 'cardNumber-input'
    f = driver.find_elements_by_tag_name("iframe")
    print(len(f))
    driver.switch_to.frame(f[1])
    # print(f.text)
    h = driver.find_element_by_id("cardNumber-input"); h.send_keys("5469400021821413", Keys.ARROW_DOWN)
    h = driver.find_element_by_id("cardExpiry-input"); h.send_keys("0723", Keys.ARROW_DOWN)
    h = driver.find_element_by_id("cardCvc-input"); h.send_keys("245", Keys.ARROW_DOWN)
    driver.switch_to.default_content()

def acceptbuttonSec(driver):
    f = driver.find_element_by_class_name("button-continue")
    f.click()

def acceptEnd(driver):
    f = driver.find_element_by_class_name("button-submit")
    f.click()

def pushTasks(driver1):
    for driver in driver1:


        driver.get("https://www.nike.com/RU/launch/t/%D0%BE%D0%B1%D1%83%D0%B2%D1%8C-%D0%B4%D0%BB%D1%8F-%D1%81%D0%BA%D0%B5%D0%B9%D1%82%D0%B1%D0%BE%D1%80%D0%B4%D0%B8%D0%BD%D0%B3%D0%B0-sb-dunk-low-pro/?productId=fe4310ff-b754-52d9-8eda-33d11b6f2b9f&size=8.5")
        gg = driver.find_elements_by_id("middleName")
        while (len(gg) == 0):
            gg = driver.find_elements_by_id("middleName")
            time.sleep(0.2)
        gg[0].send_keys("Аслиддинович", Keys.ARROW_DOWN)
        cc = driver.find_element_by_class_name("button-continue");
        cc.click()
        time.sleep(2)

        entercard(driver)
        time.sleep(2)
        acceptbuttonSec(driver)
        acceptEnd(driver)

def windows():


    path = "D:\chromedriver.exe"
    window = 1
    listWin = []
    while window != 3:
        options = Options()
        options.add_argument("--user-data-dir=C:/Users/лллл/AppData/Local/Google/Chrome/User Data/g" + str(window))
        options.add_argument('--profile-directory=Profile '+str(window))
        listWin.append(webdriver.Chrome(executable_path=path, chrome_options=options))
        window +=1
    pushTasks(listWin)


def main():
    BotSys = Tk()
    BotSys.title("Bot: ready")
    BotSys.geometry('1280x720')
    BotSys.resizable(width=0, height=0)
    snGotovoF = []
    snGotovoS = []
    sneakersPhoto = []
    url = 'https://www.nike.com/ru/launch?s=upcoming'
    file = requests.get(url)
    soup = BeautifulSoup(file.text)
    sneakers = soup.find_all('div', {'class' : 'copy-container ta-sm-c bg-white pt6-sm pb7-sm pb7-lg'})
    Photo = soup.find_all('img', {'class' : 'image-component mod-image-component u-full-width'})
    for item in sneakers:
        res = item.find('h3', {'class' : 'headline-5'})
        snGotovoF.append(res.text)
        res = item.find('h6', {'class' : 'headline-3'})
        snGotovoS.append(res.text)
    label =1
    for i in range(len(snGotovoF)):
        label = Label(text = (snGotovoF[i] + ' - ' + snGotovoS[i]),padx='12', pady='2',font=15)
        label.pack()

    button = Button(text='Create tasks', width=7,height=1, padx='20',pady='2',font = 10,bg = 'black'
                    , fg = 'red', command=windows)


    button.pack()
    button.place(x = 1100, y = 360)
    BotSys.mainloop()
if __name__ == '__main__':
    main()

