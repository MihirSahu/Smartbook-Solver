from tkinter import *
from bs4 import BeautifulSoup
from selenium import webdriver
from googlesearch import search
import requests
from difflib import SequenceMatcher
import itertools

window = Tk()

driver = webdriver.Chrome()
    
def startBrowser():
    url = 'https://connect.mheducation.com/connect/login/'
    driver.get(url)

def getSourceCode():

    #with open('test.html', 'w') as file:
    #    file.write(driver.find_element_by_xpath("//body").get_attribute('outerHTML'))

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
           return item.find_all('span', class_='TermText notranslate lang-en')[1].text

#Helper function to find xpath of a bs4 element
def xpath_soup(element):
    """
    Generate xpath of soup element
    :param element: bs4 text or node
    :return: xpath as string
    """
    components = []
    child = element if element.name else element.parent
    for parent in child.parents:
        """
        @type parent: bs4.element.Tag
        """
        previous = itertools.islice(parent.children, 0, parent.contents.index(child))
        xpath_tag = child.name
        xpath_index = sum(1 for i in previous if i.name == xpath_tag) + 1
        components.append(xpath_tag if xpath_index == 1 else '%s[%d]' % (xpath_tag, xpath_index))
        child = parent
    components.reverse()
    return '/%s' % '/'.join(components)

def radioQuestions(answer, soup):
    list1 = []
    list2 = []
    div = soup.find_all('span', class_='choiceText rs_preserve')
    for item in div:
        list1.append(item.p.text)
        list2.append(SequenceMatcher(None, answer, item.p.text).ratio())
    maximum = max(list2)
    for item in list2:
        if maximum == item:
            radioAnswer = list1[list2.index(item)]

    div = soup.find('div', class_='responses-container')
    choices = div.find_all('label')
    for item in choices:
        if item.find('span', class_='choiceText rs_preserve').p.text == radioAnswer:
            #print('#' + item.find('input')['id'])
            #driver.find_element_by_css_selector('#' + item.find('input')['id']).click()
            driver.find_element_by_xpath(xpath_soup(item)).click()

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
    answer = quizletScraper(url, question)
    print(answer)
    t1.insert(END, "Answer found \n")
    #while True:
    #    if 'type="radio"' in html_text:
    radioQuestions(answer, soup)

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
