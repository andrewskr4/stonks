from bs4 import BeautifulSoup
from datetime import date
import sys
from random import shuffle
#from http.cookiejar import CookieJar
import urllib
from urllib.request import Request, urlopen
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

upgrades_url = "https://www.marketbeat.com/ratings/canada/"
#driver = webdriver.Firefox()
#driver.get(upgrades_url)
#time.sleep(5)


#inputElement = driver.find_element_by_id("cphPrimaryContent_txtStartDate")
#inputElement.clear()
#inputElement.send_keys('3/31/2021')
#upgrades_page = driver.page_source
print("before url open")
req = Request(upgrades_url, headers={'User-Agent': 'Mozilla/5.0'})
upgrades_page = urlopen(req).read()
print("read_url")
upgrades_soup = BeautifulSoup(upgrades_page, features="lxml")
pairs = []
sample = []
nums = []
total =0
total_change = 0
opening_cost = 0
current_value = 0
frac_increase = 0
first=True
today = date.today()
d = today.strftime("%Y-%m-%d")
#print(len(sys.argv))
tickers = []

#cookieProcessor = urllib.request.HTTPCookieProcessor()
#opener = urllib.request.build_opener(cookieProcessor)



if (len(sys.argv)==1):
    g = open(d+".txt", 'w')
    for tr in upgrades_soup.find_all('tr')[3:]:
        tds = tr.find_all('td')
        if(len(tds))==1:
            continue
        tds1 = str(tds[1].text)
        a_list = tds1.split()
        new_string = " ".join(a_list)
        if(new_string == "Target Raised by"):
            already_in = False
            average_rating = " "
            #ticker = tds[0].text
            ticker_xml = tr.find(lambda tag: tag.name == 'div' and tag.get('class') == ['ticker-area'])
            ticker = ticker_xml.text
            for tick in tickers:
                if tick == ticker:
                    already_in = True
            if(already_in):
                continue
            tickers.append(ticker)
            tds3 = tds[3].text
            price = tds3.split("-")
            #print(len(price))
            if (len(price)==1):
                price = tds3.split("+")
            if(str(ticker) == 'EURMF'):
                continue
            price = price[0].split("$")[-1]
            print(ticker, price)
            entry = str(ticker+" "+price+"\n")
            g.write(entry)


if (len(sys.argv)>1 and sys.argv[2] == "monitor"):
    f = open(sys.argv[1], 'r')
    #f = open(d+".txt", 'r')
    lines = f.readlines()
    total_change=0
    for line in lines:
        ticker = line.split()[0]
        old_price = line.split()[1]
        ticker_url = 'https://www.marketbeat.com/stocks/TSE/'+ticker+'/price-target/'
        req = Request(ticker_url, headers={'User-Agent': 'Mozilla/5.0'})
        ticker_page = urlopen(req).read()
        ticker_soup = BeautifulSoup(ticker_page, features="lxml")
        change = ticker_soup.find(lambda tag: tag.name == 'div' and tag.get('class') == ['price'])
        #print(change)
        price = (change.text).split()[0]
        price = price.split('$')[1]
        #print(price)
        print(ticker+" "+old_price+" "+price+" "+str(100*(float(price)-float(old_price))/float(old_price)))
        total_change+=100*(float(price)-float(old_price))/float(old_price)
    print(total_change)

    
if (len(sys.argv)>1 and sys.argv[2] == "random"):
    temp = int(sys.argv[3])
    f = open(sys.argv[1], 'r')
    g = open(sys.argv[1].split(".")[0]+"_rand_"+str(temp)+".txt", 'w')
    lines = f.readlines()
    for line in lines:
        if(line.split()[2] =='Buy'):
            pair = (line.split()[0], line.split()[1])
            pairs.append(pair)
    shuffle(pairs)
    sample += pairs[:temp]
    print(sample)
    for ticker, price in sample:
        g.write(ticker+" "+price+"\n")
        


