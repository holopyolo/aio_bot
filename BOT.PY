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
import zipfile
#from discordwebhook import Discord
import math

page_load = ''

threadWinAdidas = []
threadsWin = []
listWin = []
delay = 0.2

def get_chromedriver(PROXY_USER, PROXY_PASS, PROXY_HOST, PROXY_PORT, use_proxy=False, user_agent=None):
    manifest_json = """
    {
        "version": "1.0.0",
        "manifest_version": 2,
        "name": "Chrome Proxy",
        "permissions": [
            "proxy",
            "tabs",
            "unlimitedStorage",
            "storage",
            "<all_urls>",
            "webRequest",
            "webRequestBlocking"
        ],
        "background": {
            "scripts": ["background.js"]
        },
        "minimum_chrome_version":"22.0.0"
    }
    """

    background_js = """
    var config = {
            mode: "fixed_servers",
            rules: {
              singleProxy: {
                scheme: "http",
                host: "%s",
                port: parseInt(%s)
              },
              bypassList: ["localhost"]
            }
          };

    chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});

    function callbackFn(details) {
        return {
            authCredentials: {
                username: "%s",
                password: "%s"
            }
        };
    }

    chrome.webRequest.onAuthRequired.addListener(
                callbackFn,
                {urls: ["<all_urls>"]},
                ['blocking']
    );
    """ % (PROXY_HOST, PROXY_PORT, PROXY_USER, PROXY_PASS)

    path = os.path.dirname(os.path.abspath(__file__))
    chrome_options = webdriver.ChromeOptions()
    if use_proxy:
        pluginfile = 'proxy_auth_plugin.zip'

        with zipfile.ZipFile(pluginfile, 'w') as zp:
            zp.writestr("manifest.json", manifest_json)
            zp.writestr("background.js", background_js)
        chrome_options.add_extension(pluginfile)
    if user_agent:
        chrome_options.add_argument('--user-agent=%s' % user_agent)

    driver = webdriver.Chrome(
        'd:/chromedriver.exe',
        chrome_options=chrome_options)
    return driver


def wait_until_visible(driver, xpath=None, class_name=None, duration=10000, frequency=0.01):
    if xpath:
        WebDriverWait(driver, duration, frequency).until(EC.visibility_of_element_located((By.XPATH, xpath)))
    elif class_name:
        WebDriverWait(driver, duration, frequency).until(EC.visibility_of_element_located((By.CLASS_NAME, class_name)))

def wait_until_clickable(driver, xpath=None, class_name=None, duration=10000, frequency=0.01):
    if xpath:
        WebDriverWait(driver, duration, frequency).until(EC.element_to_be_clickable((By.XPATH, xpath)))
    elif class_name:
        WebDriverWait(driver, duration, frequency).until(EC.element_to_be_clickable((By.CLASS_NAME, class_name)))


def checkexist(driver,xpath):
    if (len(driver.find_elements_by_xpath(xpath)) > 0):
        return True
    else:
        return False


def login(driver, username, password):
    driver.get("https://www.nike.com/ru/login")
    time.sleep(4)
    if (len(driver.find_elements_by_class_name('pre-avatar-name flx-order-sm-1 flx-order-lg--1 body-4 u-bold')) > 0):
        return True
    wait_until_visible(driver=driver, xpath="//input[@name='emailAddress']")
    time.sleep(delay)
    email_input = driver.find_element_by_xpath("//input[@name='emailAddress']")
    time.sleep(delay)
    email_input.clear()
    time.sleep(delay)
    email_input.send_keys(username)
    time.sleep(delay)
    password_input = driver.find_element_by_xpath("//input[@name='password']")
    time.sleep(delay)
    password_input.clear()
    time.sleep(delay)
    password_input.send_keys(password+'\n')
    time.sleep(delay)
    #sumbit = driver.find_element_by_xpath('//input[@value="ВОЙТИ"]')
    #@sumbit.click()
    time.sleep(5)
    if (len(driver.find_elements_by_xpath('//div[@class="nike-unite-error-close"]')) > 0):
        return False
    else:
        return True

def uvedomit(s,ms, num):
    discord = Discord(url="https://discord.com/api/webhooks/792988577969602601/pa-XIotP9qP_0lK_LeQWW-JK3oHz_6Otb5zC3aj4lRq5FtAP3Qx4d_7gs6qVzkxzffyh")
    discord.post(content=("@everyone\nТайминг №" + num+' - '+s+ ' '+ ms))

def log_in(driver, login, pass1):
    driver.get("https://www.nike.com/ru/launch")
    wait_until_visible(driver=driver, xpath='//*[@data-qa="top-nav-join-or-login-button"]')
    driver.find_element_by_xpath('//*[@data-qa="top-nav-join-or-login-button"]').click()
    wait_until_visible(driver=driver, xpath='//*[@type="email"]')
    driver.find_element_by_xpath('//*[@type="email"]').click()
    driver.find_element_by_xpath('//*[@type="email"]').send_keys(login)
    time.sleep(delay)
    driver.find_element_by_xpath('//*[@type="password"]').click()
    driver.find_element_by_xpath('//*[@type="password"]').send_keys(pass1)
    time.sleep(2)
    while(checkexist(driver, '//*[@value="ОБРАБОТКА..."]') == 1):
        time.sleep(0.5)

def entercard(driver, num):
    print('Ввод карты.. ', num)
    id = 'cardNumber-input'
    f = driver.find_elements_by_tag_name("iframe")
    print(len(f))
    driver.switch_to.frame(f[1])
    # print(f.text)
    h = driver.find_element_by_id("cardNumber-input"); h.send_keys("", Keys.ARROW_DOWN)
    h = driver.find_element_by_id("cardExpiry-input"); h.send_keys("", Keys.ARROW_DOWN)
    h = driver.find_element_by_id("cardCvc-input"); h.send_keys("", Keys.ARROW_DOWN)
    driver.switch_to.default_content()
    print('Успешно введена карта ', num)

def waitMessage():
    print("wait...")

def acceptbuttonSec(driver):
    f = driver.find_element_by_class_name("button-continue")
    f.click()

def acceptEnd(driver, num, taiming):
    time.sleep(1)
    while (len(driver.find_elements_by_xpath('//span[@class="error"]'))>0):
        time.sleep(0.5)
    while (True):
        now = datetime.datetime.now()
        h = now.hour
        m = now.minute
        s = now.second
        ms = now.microsecond
        if (h != 13):
            time.sleep(5)
            print('Ожидание тайминга.. №', num)
            continue
        elif (m != 59):
            time.sleep(1)
            continue
        elif (s < taiming[0]):
            time.sleep(0.2)
            continue
        elif (ms < taiming[1]):
            time.sleep(25)
            continue
        break
        uvedomit(s, ms, num)
    driver.find_element_by_xpath('//button[@class="button-submit"]').click()

def waitingwhilelog(driver, logs, pass1,num):
    check = login(driver, logs, pass1)
    time.sleep(6)
    while (check == False):
        print('Неудачный вход! ', num, ' ошибка: не ебу')
        time.sleep(20)
        check = login(driver, logs, pass1)

def pushTasks(driver, logs, pass1, num, taiming):
    waitingwhilelog(driver, logs, pass1, num)
    print('Удача! Вошел в аккаунт ', num)
    driver.get(
        "https://www.nike.com/ru/launch/t/sb-dunk-low-pro-court-purple1?productId=99c0d47c-225f-5c50-b078-1a1044c114e9&size=10.5")
    print('ss ', num)
    gg = driver.find_elements_by_id("middleName")
    time.sleep(6)
    while (len(gg) == 0):
        gg = driver.find_elements_by_id("middleName")
        time.sleep(3)
    print('Перешел на чекаут.. Ввод.. ', num)
    gg[0].send_keys("ОТЧЕСТВО", Keys.ARROW_DOWN)
    wait_until_clickable(driver, class_name='button-continue')
    driver.find_element_by_class_name('button-continue').click()
    time.sleep(2)
    entercard(driver, num)
    print('Чекаут готов! ', num, '\nЖдем тайминга')
    acceptEnd(driver, num, taiming)

def loadProxies():
    proxies = []
    with open('proxies.txt') as f:
        proxies = f.readlines()
    return  proxies

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

def waiting():
    while (True):
        now = datetime.datetime.now()
        h = now.hour
        m = now.minute
        if ( h == 13 and m > 41):
            break
        time.sleep(60)

def windows(kolvoacc, taimings):

    infosTasks = []
    logs = loadlog()
    pass1 = loadpass()
    proxy = loadProxies()
    path = "D:\chromedriver.exe"
    window = int(kolvoacc)
    kolvoproxies = len(proxy)
    iterAcc = 0
    u = 0
    #print(len(proxy))
    while u < kolvoproxies:
        k = 0
        j = proxy[u].split(':')
        j = [line.rstrip() for line in j]
        print(math.floor(kolvoacc / kolvoproxies))
        while (k < math.floor(kolvoacc/kolvoproxies)):
            #print('LOL\n')
            listWin.append(
                get_chromedriver(PROXY_HOST=j[2], PROXY_PORT=j[3], PROXY_USER=j[0], PROXY_PASS=j[1], use_proxy=True))
            iterAcc+=1
            k+=1
        u+=1
    if (kolvoacc - iterAcc > 0):
       # print('GG')
        k = 0
        while (k < (kolvoacc - iterAcc)):
            listWin.append(
                get_chromedriver(PROXY_HOST='', PROXY_PORT='', PROXY_USER='', PROXY_PASS='',use_proxy=False))
            k+=1
    it = 0
    for driver in listWin:
        t = threading.Thread(target=pushTasks, args=(driver, logs[it], pass1[it], (it+1), taimings[it]))
        threadsWin.append(t)
        t.start()
        it += 1
    for t in threadsWin:
        t.join()
    #delete


def main():
    print('url atc nike: ')
    page_load = input()
    kolvoacc = 0
    print('кол-во тасков')
    kolvoacc = input()
    it = 0
    taimings = []
    kolvoacc = int(kolvoacc)
    for i in range(kolvoacc):
        taimings.append([0] * 2)
    while it < kolvoacc:
        print('введи тайминг на №', it + 1, ' (С и МС через новую строку)')
        j = input()
        j2 = input()
        taimings[it][0] = j
        taimings[it][1] = j2
        it +=1
    windows(kolvoacc, taimings)


if __name__ == '__main__':
    main()
