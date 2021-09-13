from tkinter import *
from bs4 import BeautifulSoup
from selenium import webdriver
from googleapi import google

window = Tk()

driver = webdriver.Chrome()
    
def startBrowser():
    url = 'https://connect.mheducation.com/connect/login/'
    driver.get(url)

def getSourceCode():
    return driver.find_element_by_xpath("//body").get_attribute('outerHTML')

def mainFunction():
    html_text = getSourceCode()
    t1.insert(END, "HTML downloaded")
    soup = BeautifulSoup(html_text, 'lxml')
    prompt = soup.find_all('div', class_='prompt')
    for item in prompt:
        question = item.find('p').text
    print(question)

l1 = Label(master=window,text="McGrawHill Smartbook Connect Solver")
l1.grid(row=0,column=1)

b1 = Button(master=window,text="Go to McgrawHill",width=11, command=startBrowser)
b1.grid(row=1,column=1)

e1_value = StringVar()
e1 = Entry(master=window,textvariable=e1_value)
e1.grid(row=2,column=1)

b2 = Button(master=window,text="Start",width=5, command=mainFunction)
b2.grid(row=3,column=1)

t1 = Text(master=window,height=9,width=30)
t1.grid(row=4,column=1)

window.mainloop()