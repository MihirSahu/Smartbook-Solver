from tkinter import *
from bs4 import BeautifulSoup
from selenium import webdriver
from googlesearch import search
import requests

window = Tk()

driver = webdriver.Chrome()
    
def startBrowser():
    url = 'https://connect.mheducation.com/connect/login/'
    driver.get(url)

def getSourceCode():
    return driver.find_element_by_xpath("//body").get_attribute('outerHTML')

def googleSearch(query):
    results = []
    for result in search(query, tld="com", num=10, stop=10, pause=2):
        results.append(result)
    for result in results:
        if "quizlet" in result:
            return results[0].strip()

def quizletScraper(quizletURL, question):
    header = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36" ,
    'referer':'https://www.google.com/'}

    html_text = requests.get(quizletURL, headers=header).text
    soup = BeautifulSoup(html_text, 'lxml')
    tags = soup.find_all('div', class_='SetPageTerms-term')

    for item in tags:
        if item.find('span', class_='TermText notranslate lang-en').text == question:
            #return item.find_all('span', class_='TermText notranslate lang-en')[1].text
           print(item.find_all('span', class_='TermText notranslate lang-en')[1].text)

def mainFunction():
    html_text = getSourceCode()
    t1.insert(END, "HTML downloaded \n")
    soup = BeautifulSoup(html_text, 'lxml')
    prompt = soup.find_all('div', class_='prompt')
    for item in prompt:
        question = item.find('p').text
    t1.insert(END, "Question detected \n")
    url = googleSearch(question)
    t1.insert(END, "Resource found \n")
    #answer = quizletScraper(url, question)
    quizletScraper(url, question)
    t1.insert(END, "Answer found \n")

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
