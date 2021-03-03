from bs4 import BeautifulSoup
from datetime import date
import sys
from random import shuffle

from urllib.request import urlopen

url = "https://www.marketwatch.com/tools/upgrades-downgrades"

page = urlopen(url).read()
soup = BeautifulSoup(page, features="lxml")
upgrades = []
old_prices = []
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
    for tr in soup.find_all('tr')[2:]:
        tds = tr.find_all('td')
        #print(tds[0].text, tds[1].text, tds[2].text, tds[3].text, tds[4].text, tds[5].text)
        if(tds[3].text == 'Upgrades'):
            upgrades.append(tds[1].text)
            #print(tds[1].text, tds[3].text)
else:
    f = open(sys.argv[1], 'r')
    #f = open(d+".txt", 'r')
    lines = f.readlines()
    for line in lines:
        upgrades.append(line.split()[0])
        old_prices.append(line.split()[1])
        pair = (line.split()[0], line.split()[1])
        pairs.append(pair)
    if (len(sys.argv)==3):
        shuffle(pairs)
        temp = int(sys.argv[2])
        sample += pairs[:temp]
        print(sample)
print(upgrades)

if (len(sys.argv) <3):
    for i in range(len(upgrades)):
        url = 'https://www.marketwatch.com/investing/stock/'+str(upgrades[i])
        page = urlopen(url).read()
        soup = BeautifulSoup(page, features="lxml")
        change = soup.find(lambda tag: tag.name == 'h3' and tag.get('class') == ['intraday__price'])
        price = (change.text).split("\n")[2]
        #print(price)
        if (len(sys.argv)==1):
            g.write(upgrades[i] + " " +price+"\n")
            #print(upgrades[i], change.text)
        if (len(sys.argv)==2):
            print(str(upgrades[i])+" "+str(price)+" "+ str(old_prices[i]) + " " + str(100*(float(price)-float(old_prices[i]))/float(old_prices[i]))+"%")
            num = 100*(float(price)-float(old_prices[i]))/float(old_prices[i])
            total_change += num
            opening_cost += float(old_prices[i])
            current_value += float(price)
        num = (change.text).split('\n')[2]
        total += float(num)
        #num =old_prices[i].split('%')[0]
        #total_change += float(num)
    #print(total)
    #print("Percent change: "+str(100*(current_value-opening_cost)/opening_cost))
    print(total_change)

else: 
    for ticker, old_price in sample:
        url = 'https://www.marketwatch.com/investing/stock/'+str(ticker)
        page = urlopen(url).read()
        soup = BeautifulSoup(page, features="lxml")
        change = soup.find(lambda tag: tag.name == 'h3' and tag.get('class') == ['intraday__price'])
        price = (change.text).split("\n")[2]
        #if (len(sys.argv)==1):
        #    g.write(sample[i] + " " +change.text+"\n")
        #print(str(ticker)+" "+str(price)+" "+ str(old_price) + " " + str(100*(float(price)-float(old_price))/float(old_price))+"%")
        print(ticker, old_price)
        num = 100*(float(price)-float(old_price)/float(old_price))
        total += float(num)
    print(total)
