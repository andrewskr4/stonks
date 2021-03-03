from bs4 import BeautifulSoup
from datetime import date
import sys
from random import shuffle

from urllib.request import urlopen

url = "https://www.marketwatch.com/tools/upgrades-downgrades"

page = urlopen(url).read()
soup = BeautifulSoup(page, features="lxml")
upgrades = []
old_percentages = []
sample = []
nums = []
total =0
total_change = 0
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
        old_percentages.append(line.split()[1])
    if (len(sys.argv)==3):
        shuffle(upgrades)
        sample += upgrades[:10]
        print(sample)
print(upgrades)

if (len(sys.argv) <3):
    for i in range(len(upgrades)):
        url = 'https://www.marketwatch.com/investing/stock/'+str(upgrades[i])
        page = urlopen(url).read()
        soup = BeautifulSoup(page, features="lxml")
        change = soup.find(lambda tag: tag.name == 'span' and tag.get('class') == ['change--percent--q'])
        if (len(sys.argv)==1):
            g.write(upgrades[i] + " " +change.text+"\n")
            print(upgrades[i], change.text)
        if (len(sys.argv)==2):
            print(str(upgrades[i])+" "+str(change.text)+" "+ str(old_percentages[i]))
                
        ch = (change.text).split('%')[0]
        #total += float(num)
        old =old_percentages[i].split('%')[0]
        total_change += float(ch)-float(old)
    #print(total)
    print(total_change)
else: 
    for i in range(len(sample)):
        url = 'https://www.marketwatch.com/investing/stock/'+str(sample[i])
        page = urlopen(url).read()
        soup = BeautifulSoup(page, features="lxml")
        change = soup.find(lambda tag: tag.name == 'span' and tag.get('class') == ['change--percent--q'])
        #if (len(sys.argv)==1):
        #    g.write(sample[i] + " " +change.text+"\n")
        print(sample[i], change.text)
        num = (change.text).split('%')[0]
        total += float(num)
    print(total)
