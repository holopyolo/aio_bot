import requests
import json
from bs4 import BeautifulSoup
from tkinter import *



def parsPhoto(ssilka):
    photka = requests.get(ssilka, headers=headers).content
    return  photka
def pushTasks():
    Tasks = Tk()
    Tasks.title("create tasks")
    Tasks.geometry('720x620')
    Tasks.resizable(width=0, height=0)
    label = Label(text='name')
    Tasks.mainloop()

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
                    , fg = 'red', command=pushTasks)


    button.pack()
    button.place(x = 1100, y = 360)
    BotSys.mainloop()
if __name__ == '__main__':
    main()

