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
import os
import copy
import shutil
import threading
import datetime

threadWinAdidas = []
threadsWin = []
listWin = []

def wait_until_visible(driver, xpath=None, class_name=None, duration=10000, frequency=0.01):
    if xpath:
        WebDriverWait(driver, duration, frequency).until(EC.visibility_of_element_located((By.XPATH, xpath)))
    elif class_name:
        WebDriverWait(driver, duration, frequency).until(EC.visibility_of_element_located((By.CLASS_NAME, class_name)))


def end():
    path = "D:/profils/"
    if (len(listWin) != 0):
        for item in listWin:
            item.quit()     #exit from windows
    per = int(userwin.get())

    while per !=1:
        shutil.rmtree(path+str(per))
        per -= 1


def login(driver, username, password):
    driver.get("https://www.nike.com/ru/login")


    wait_until_visible(driver=driver, xpath="//input[@name='emailAddress']")

    email_input = driver.find_element_by_xpath("//input[@name='emailAddress']")
    email_input.clear()
    email_input.send_keys(username, Keys.ARROW_DOWN)
    password_input = driver.find_element_by_xpath("//input[@name='password']")
    password_input.clear()
    password_input.send_keys(password, Keys.ARROW_DOWN)
    time.sleep(1)


def log_in(driver, login, pass1):
    driver.get("https://www.nike.com/ru/launch")
    g = driver.find_elements_by_xpath('//*[@id="root"]/div/div/div[1]/div/header/div[1]/section/div/ul/li[1]/button')
    while (len(g) == 0):
        g = driver.find_elements_by_xpath('//*[@id="root"]/div/div/div[1]/div/header/div[1]/section/div/ul/li[1]/button')
        print("i can't find")
    g[0].click()
    g = driver.find_elements_by_name("emailAddress")
    while (len(g) == 0):
        print("I can't find elements\n")
        g = driver.find_elements_by_name("emailAddress")
    g[0].send_keys(login, Keys.ARROW_DOWN)
    g = driver.find_element_by_name("password")
    g.send_keys(pass1, Keys.ARROW_DOWN)
    time.sleep(4)
    #g = driver.find_element_by_name("ВОЙТИ")
   # g.click()

def entercard(driver):
    id = 'cardNumber-input'
    f = driver.find_elements_by_tag_name("iframe")
    print(len(f))
    driver.switch_to.frame(f[1])
    # print(f.text)
    h = driver.find_element_by_id("cardNumber-input"); h.send_keys("54694123213", Keys.ARROW_DOWN)
    h = driver.find_element_by_id("cardExpiry-input"); h.send_keys("2321", Keys.ARROW_DOWN)
    h = driver.find_element_by_id("cardCvc-input"); h.send_keys("213", Keys.ARROW_DOWN)
    driver.switch_to.default_content()

def waitMessage():
    print("wait...")

def acceptbuttonSec(driver):
    f = driver.find_element_by_class_name("button-continue")
    f.click()

def acceptEnd(driver):
    f = driver.find_element_by_class_name("button-submit")
    while (True):
        now = datetime.datetime.now()
        h = now.hour
        m = now.minute
        s = now.second
        ms = now.microsecond
        if (h != 13):
            time.sleep(5)
            waitMessage()
            continue
        elif (m != 59):
            time.sleep(1)
            continue
        elif (s < 57 ):
            time.sleep(0.3)
            continue
        break
    if (now.hour > 15):
        print("Дропа на сегодня нет, попробуй позже")
    f.click()

def pushTasks(driver, logs, pass1):
    log_in(driver, logs, pass1)
    driver.get("https://www.nike.com/RU/launch/t/%D0%BA%D1%80%D0%BE%D1%81%D1%81%D0%BE%D0%B2%D0%BA%D0%B8-air-force-1-07-para-noise/?productId=41ef7f6d-07a5-599a-811d-d0f3bb7c9bb8&size=10")
    gg = driver.find_elements_by_id("middleName")
    time.sleep(6)
    while (len(gg) == 0):
        gg = driver.find_elements_by_id("middleName")
        time.sleep(3)
    gg[0].send_keys("Аслиддинович", Keys.ARROW_DOWN)
    cc = driver.find_element_by_class_name("button-continue");
    cc.click()
    time.sleep(2)

    entercard(driver)
    acceptEnd(driver)

def loadlog():
    logs = []
    with open('logins.txt') as f:
        logs = f.readlines()
    return logs

def loadpass():
    pass1 = []
    with open('pass.txt') as f:
        pass1 = f.readlines()
    return  pass1

def windows():

    infosTasks = []
    logs = loadlog()
    pass1 = loadpass()
    path = "D:\chromedriver.exe"
    #while (True):
    #    now = datetime.datetime.now()
   #     h = now.hour
    #    m = now.minute
    #    if ( h == 13 and m > 41):
    #        break
    #    time.sleep(60)
    print(userwin)
    print(userwin.get())
    window = int(userwin.get())
    while window != 1:
        options = Options()
        options.add_argument("--user-data-dir=D:/profils/" + str(window))
        options.add_argument('--profile-directory=Profile1 '+str(window))
        listWin.append(webdriver.Chrome(executable_path=path, chrome_options=options))
        window -=1
    it = 0
    for driver in listWin:
        t = threading.Thread(target=pushTasks, args=(driver, logs[it], pass1[it]))
        threadsWin.append(t)
        t.start()
        it += 1
    for t in threadsWin:
        t.join()
    #delete


def main():
    BotSys = Tk()
    BotSys.title("Bot: ready")
    BotSys.geometry('1280x720')
    BotSys.resizable(width=0, height=0)

    global userwinAdidas
    userwinAdidas = StringVar()

    global userwin
    userwin = StringVar()
    global inputS
    inputS = StringVar()
    global inputmS
    inputmS = StringVar()

    lab1 = Label(text = "Кол-во тасков")
    lab1.pack()
    lab1.place(x = 860, y = 360)
    messageInput = Entry(textvariable=userwin)
    messageInput.place(x=950, y=360)

    lab1 = Label(text="Секунды")
    lab1.pack()
    lab1.place(x=900, y=300)
    messageInput1 = Entry(textvariable=inputS)
    messageInput1.place(x=950, y=300)

    lab1 = Label(text="Миллисекунды")
    lab1.pack()
    lab1.place(x=860, y=240)
    messageInput2 = Entry(textvariable=inputmS)
    messageInput2.place(x=950, y=240)

    t2 = threading.Thread(target=windows)
    button1 = Button(text='Create tasks', width=7,height=1, padx='30',pady='2',font = 10,bg = 'black'
                    , fg = 'red', command=t2.start)
    button1.pack()
    button = Button(text='Delete tasks', width=7,height=1, padx='20',pady='9',font = 10,bg = 'black'
                    , fg = 'red', command=end)

    button.pack()
    button1.place(x = 1100, y = 360)
    button.place(x=1100, y=300)

    BotSys.mainloop()
if __name__ == '__main__':
    main()
