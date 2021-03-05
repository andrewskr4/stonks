from bs4 import BeautifulSoup
from datetime import date
import sys
from random import shuffle

from urllib.request import urlopen

upgrades_url = "https://www.marketwatch.com/tools/upgrades-downgrades"

upgrades_page = urlopen(upgrades_url).read()
upgrades_soup = BeautifulSoup(upgrades_page, features="lxml")
upgrades = []
old_prices = []
firms = []
firms_ratings = []
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
if (len(sys.argv)==1):
    g = open(d+".txt", 'w')
    for tr in upgrades_soup.find_all('tr')[2:]:
        tds = tr.find_all('td')
        if(tds[3].text == 'Upgrades'):
            rating = " "
            #upgrades.append(tds[1].text)
            ticker = tds[1].text
            #firms.append(tds[4].text)
            #print(tds[1].text, tds[3].text)
            rating_url = 'https://www.benzinga.com/stock/'+str(tds[1].text)+'/ratings'
            rating_page = urlopen(rating_url).read()
            rating_soup = BeautifulSoup(rating_page, features="lxml")
            #print(rating_soup)
            for ratetr in rating_soup.find_all('tr')[1:]:
                ratetds = ratetr.find_all('td')
                rating = ratetds[3].text
                break
            ticker_url = 'https://www.marketwatch.com/investing/stock/'+ticker
            ticker_page = urlopen(ticker_url).read()
            ticker_soup = BeautifulSoup(ticker_page, features="lxml")
            change = ticker_soup.find(lambda tag: tag.name == 'h3' and tag.get('class') == ['intraday__price'])
            price = (change.text).split("\n")[2]
            entry = str(ticker+" "+ price+" "+ rating+"\n")
            print(ticker, price, entry)
            g.write(entry)
            

if sys.argv[2] == "monitor":
    f = open(sys.argv[1], 'r')
    #f = open(d+".txt", 'r')
    lines = f.readlines()
    total_change=0
    for line in lines:
        ticker = line.split()[0]
        old_price = line.split()[1]
        ticker_url = 'https://www.marketwatch.com/investing/stock/'+ticker
        ticker_page = urlopen(ticker_url).read()
        ticker_soup = BeautifulSoup(ticker_page, features="lxml")
        change = ticker_soup.find(lambda tag: tag.name == 'h3' and tag.get('class') == ['intraday__price'])
        price = (change.text).split("\n")[2]
        print(ticker+" "+old_price+" "+price+" "+str(100*(float(price)-float(old_price))/float(old_price)))
        total_change+=100*(float(price)-float(old_price))/float(old_price)
    print(total_change)
if sys.argv[2] == "random":
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
        


