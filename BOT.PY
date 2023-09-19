import requests
import json
import time
from threading import Thread
from selenium.webdriver.common.keys import Keys
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
from discordwebhook import Discord
import math
import random

atc = ''
threadWinAdidas = []
threadsWin = []
listWin = []
delay = 0.5


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
        executable_path='C:/chromedriver.exe',
        chrome_options=chrome_options)
    return driver


def writelogs(text):
    now = datetime.datetime.now()
    h = now.hour
    m = now.minute
    s = now.second
    ms = (now.microsecond / 1000)
    print('[', h, ':', m, ':', s, ':', int(ms), '] TASK ' + text)


def is_non_zero_file(fpath):
    return os.path.isfile(fpath) and os.path.getsize(fpath) > 0


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


def checkexist(driver, xpath):
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
    email_input.click()
    time.sleep(delay)
    email_input.clear()
    time.sleep(delay)
    email_input.click()
    time.sleep(delay)
    email_input.send_keys(username)
    time.sleep(delay)
    password_input = driver.find_element_by_xpath("//input[@name='password']")
    password_input.click()
    time.sleep(delay)
    password_input.clear()
    time.sleep(delay)
    password_input.click()
    time.sleep(delay)
    password_input.send_keys(password + '\n')
    time.sleep(delay)
    # sumbit = driver.find_element_by_xpath('//input[@value="ВОЙТИ"]')
    # @sumbit.click()
    time.sleep(5)
    if (len(driver.find_elements_by_xpath('//div[@class="nike-unite-error-close"]')) > 0):
        return False
    else:
        return True


def uvedomit(s,ms, num):
    discord = Discord(url="https://discord.com/api/webhooks/804434798772486165/64KBiHJI_1owIB9DkoUUMlw4K7kgvFccwHLDlQpovT-Am07UDyz6reW12U_JNVpTKKfR")
    discord.post(content=("@Holopyolo\nТайминг №" + str(num)+' - '+str(s)+ ' '+ str(ms)))

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
    while (checkexist(driver, '//*[@value="ОБРАБОТКА..."]') == 1):
        time.sleep(0.5)


def entercard(driver, num):
    cards = loadCard()  # пример заполнения: номеркарты:дата:свв        todo: перенести в отдельную функцию
    cardmain = cards[random.randint(0, (len(cards) - 1))]
    card = cardmain.split(':')
    print('Ввод карты.. ', num)
    id = 'cardNumber-input'
    wait_until_visible(driver=driver, xpath='//iframe[@title="payment"]', duration=10000)
    if (not(checkexist(driver, '//iframe[@title="payment"]'))):
        writelogs(num + ' FAILED FILL CARD DATA\n')
    f = driver.find_element_by_xpath('//iframe[@title="payment"]')
    driver.switch_to.frame(f)
    # print(f.text)
    h = driver.find_element_by_id("cardNumber-input");
    h.send_keys(str(card[0]), Keys.ARROW_DOWN)
    h = driver.find_element_by_id("cardExpiry-input");
    h.send_keys(str(card[1]), Keys.ARROW_DOWN)
    h = driver.find_element_by_id("cardCvc-input");
    h.send_keys(str(card[2]), Keys.ARROW_DOWN)
    driver.switch_to.default_content()
    print('Успешно введена карта ', num)


def waitMessage():
    print("wait...")


def acceptbuttonSec(driver):
    f = driver.find_element_by_class_name("button-continue")
    f.click()


def acceptEnd(driver, num, taiming):
    time.sleep(1)
    while (len(driver.find_elements_by_xpath('//span[@class="error"]')) > 0):
        time.sleep(0.5)
    print(taiming[0], ' ', int(taiming[0]))

    while (True):
        now = datetime.datetime.now()
        h = now.hour
        m = now.minute
        s = now.second
        ms = now.microsecond
        if (h != 13):
            time.sleep(5)
            writelogs(num, ' WAITING')
            continue
        elif (m != 59):
            time.sleep(1)
            continue
        elif (s < int(taiming[0])):
            time.sleep(0.2)
            continue
        elif (ms < int(taiming[1])):
            time.sleep(25)
            continue
        uvedomit(s, ms, num)
        break
    driver.find_element_by_xpath('//button[@class="button-submit"]').click()
    writelogs(num + ' IN QUEUE')

def waitingwhilelog(driver, logs, pass1, num):
    check = login(driver, logs, pass1)
    time.sleep(6)
    while (check == False):
        writelogs(str(num) + ' FAILED LOGIN (BANNED SESSION BY HOST)\n')
        time.sleep(20)
        check = login(driver, logs, pass1)


def checkmenuphone(driver, number):
    if (checkexist(driver, xpath='//div[@class="view-header"]')):
        print(str(number) + ' Таск. Error: obstacle. Retry...')
    driver.find_element_by_xpath('//button[@aria-Label="Закрыть"]').click()
    if (not (checkexist(driver, '//div[@class="view-header"]'))):
        writelogs(str(number) + ' The obstacle is closed')
        return 1
    else:
        print(str(number) + ' Таск. Error: obstacle')
        return 0


def pushTasks(driver, logs, pass1, num, taiming, page_load1):
    num = str(num)
    waitingwhilelog(driver, logs, pass1, num)
    change_color = lambda: os.system('color 3'); change_color()
    writelogs(num + ' Logged in!')
    change_color = lambda: os.system('color'); change_color ()

    sizes = ['6','6.5','7','7.5','8']
    page_load_with_size = page_load1 + sizes[random.randint(0, 2)]
    driver.get(page_load_with_size)
    # print('ss ', num)
    time.sleep(6)  #
    wait_until_visible(driver=driver, xpath='//*[@id="middleName"]')
    writelogs(num + ' Filling chechout info')

    lname = driver.find_element_by_id("middleName")
    lname.click()
    lname.clear()
    lname.send_keys("YOUR MIDDLENAME", Keys.ARROW_DOWN)

    sname = driver.find_element_by_id("lastName")
    sname.click()
    sname.clear()
    sname.send_keys("YOUR SURNAME", Keys.ARROW_DOWN)

    wait_until_clickable(driver, class_name='button-continue')
    time.sleep(delay)
    driver.find_element_by_class_name('button-continue').click()
    time.sleep(2)
    entercard(driver, num)
    acceptEnd(driver, num, taiming)


def updateUserInfo():
    clear = lambda: os.system('cls')
    clear()
    # что-то..


def loadAtc():
    with open('savedata.txt') as f:
        return (f.read())


def addAtcTodump():
    clear = lambda: os.system('cls')
    clear()
    print('Enter new atc (WITHOUT SIZE:  ...&size=) ')
    atc1 = input()
    file = open('savedata.txt', 'w')
    file.write(atc1)
    file.close()


def loadProxies():
    proxies = []
    with open('proxies.txt') as f:
        proxies = f.readlines()
    return proxies


def loadCard():
    card = []
    with open('card.txt') as f:
        card = f.readlines()
    return card


def loadlog():
    logs = []
    with open('logins.txt') as f:
        logs = f.readlines()
    return logs


def loadpass():
    pass1 = []
    with open('pass.txt') as f:
        pass1 = f.readlines()
    return pass1


def waiting():
    while (True):
        now = datetime.datetime.now()
        h = now.hour
        m = now.minute
        if (h == 13 and m > 41):
            break
        time.sleep(60)


def windows(kolvoacc, taimings, page_load1):
    infosTasks = []
    logs = loadlog()
    pass1 = loadpass()
    proxy = loadProxies()
    path = "D:\chromedriver.exe"
    window = int(kolvoacc)
    kolvoproxies = len(proxy)
    iterAcc = 0
    u = 0
    # print(len(proxy))
    while u < kolvoproxies:
        k = 0
        j = proxy[u].split(':')
        j = [line.rstrip() for line in j]
        print(math.floor(kolvoacc / kolvoproxies))
        while (k < math.floor(kolvoacc / kolvoproxies)):
            # print('LOL\n')
            listWin.append(
                get_chromedriver(PROXY_HOST=j[2], PROXY_PORT=j[3], PROXY_USER=j[0], PROXY_PASS=j[1], use_proxy=True))
            iterAcc += 1
            k += 1
        u += 1
    if (kolvoacc - iterAcc > 0):
        # print('GG')
        k = 0
        while (k < (kolvoacc - iterAcc)):
            listWin.append(
                get_chromedriver(PROXY_HOST='', PROXY_PORT='', PROXY_USER='', PROXY_PASS='', use_proxy=False))
            k += 1
    it = 0
    for driver in listWin:
        t = threading.Thread(target=pushTasks, args=(driver, logs[it], pass1[it], (it + 1), taimings[it], page_load1))
        threadsWin.append(t)
        t.start()
        it += 1
    for t in threadsWin:
        t.join()
    #delete





# снизу доп. софт


def streetBeat():
    # login
    delay1 = 1
    driver = webdriver.Chrome('D:\chromedriver.exe')
    # login
    driver.get('https://street-beat.ru/multicabinet/')
    wait_until_visible(driver=driver, xpath='//a[@class="h-nav__link js_popup"]')
    time.sleep(delay1)
    driver.find_element_by_class_name('h-nav__link js_popup').click()
    time.sleep(delay1)
    wait_until_visible(driver=driver, xpath='//input[@type="tel"]')
    time.sleep(delay1)
    driver.find_element_by_xpath('//input[@type="tel"]').send_keys('NUM')
    driver.find_element_by_xpath('//button[@type="sumbit"]').click()


def wildBotps5():
    options.add_argument("user-data-dir=C:\\Users\\AtechM_03\\AppData\\Local\\Google\\Chrome\\User Data\\SS")
    driver = webdriver.Chrome(executable_path='D:\chromedriver.exe', chrome_options=options)
    driver.get("http://static.sellars.cf/links?site=wildberries&code=15298664&cid=44592460&targeturl=MS")
    time.sleep(10)
    while (True):
        if (not (checkexist(driver, '//div[@class="c-achtung"]'))):
            driver.find_element_by_xpath('//button[@name="ConfirmOrderByRegisteredUser"]').click()
        else:
            print('didn"t found\n')
        time.sleep(3)


def main():
    choise = 0
    print('any number other than 2,3,4 - START\n',
          '2 - update user information\n',
          '3 - wildberries bot\n',
          '4 - to add new atc\n',
          '5 - streetbeat bot\n',
          '6 - load SIZES (DONT SAVE)')
    choise = input()
    if (int(choise) == 2):
        updateUserInfo()
    elif (int(choise) == 4):
        addAtcTodump()
    elif (int(choise) == 3):
        wildBotps5()
    elif (int(choise) == 5):
        streetBeat()
    # print('url atc nike: ')
    # page_load1 = input()
    atcm = loadAtc()
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
        it += 1
    windows(kolvoacc, taimings, atcm)


if __name__ == '__main__':
    main()
