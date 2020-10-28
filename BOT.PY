import requests
import json
from bs4 import BeautifulSoup
from tkinter import *

def main():
    BotSys = Tk()
    BotSys.title("Bot: ready")
    BotSys.geometry('1280x720')
    BotSys.resizable(width=0, height=0)
    snGotovoF = []
    snGotovoS = []
    url = 'https://www.nike.com/ru/launch?s=upcoming'
    file = requests.get(url)
    soup = BeautifulSoup(file.text)
    sneakers = soup.find_all('div', {'class' : 'copy-container ta-sm-c bg-white pt6-sm pb7-sm pb7-lg'})
    for item in sneakers:
        res = item.find('h3', {'class' : 'headline-5'})
        snGotovoF.append(res.text)
        res = item.find('h6', {'class' : 'headline-3'})
        snGotovoS.append(res.text)
    label =1
    for i in range(len(snGotovoF)):
        label = Label(text = (snGotovoF[i] + ' - ' + snGotovoS[i]),padx=13, pady='2',font=12)
        label.pack()
    BotSys.mainloop()
if __name__ == '__main__':
    main()

