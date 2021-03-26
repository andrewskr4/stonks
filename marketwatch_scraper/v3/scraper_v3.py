from bs4 import BeautifulSoup
from datetime import date
import sys
from random import shuffle

from urllib.request import urlopen

upgrades_url = "https://www.marketwatch.com/tools/upgrades-downgrades"

upgrades_page = urlopen(upgrades_url).read()
upgrades_soup = BeautifulSoup(upgrades_page, features="lxml")
pairs = []
sample = []
nums = []
total =0
total_change = 0
opening_cost = 0
current_value = 0
frac_increase = 0
investment = 6000
first=True
today = date.today()
d = today.strftime("%Y-%m-%d")
#print(len(sys.argv))
if (len(sys.argv)==1):
    g = open(d+".txt", 'w')
    for tr in upgrades_soup.find_all('tr')[2:]:
        tds = tr.find_all('td')
        if(tds[3].text == 'Upgrades'):
            average_rating = " "
            #ratings = []
            #upgrades.append(tds[1].text)
            ticker = tds[1].text
            if(str(ticker) == 'EURMF' or str(ticker)=='FMCC'):
                continue
            #firms.append(tds[4].text)
            #print(tds[1].text, tds[3].text)
            rating_url = 'https://www.marketwatch.com/investing/stock/'+ticker
            rating_page = urlopen(rating_url).read()
            rating_soup = BeautifulSoup(rating_page, features="lxml")
            rating_ul = rating_soup.find(lambda tag: tag.name == 'ul' and tag.get('class') == ['analyst__rating'])
            num_ratings_span = rating_soup.find(lambda tag: tag.name == 'span' and tag.get('class') == ['count'])
            num_ratings = (num_ratings_span.text).split("\n")[0]

            #print(ticker)
            if(ticker == 'MTW'):
                continue
            for li in rating_ul.find_all('li'):
                if(str(li).split("\"")[1] == 'analyst__option active'):
                    average_rating = (str(li).split("\"")[2]).split("<")[0]
                    average_rating = average_rating.split(">")[1]

            ticker_url = 'https://www.marketwatch.com/investing/stock/'+ticker
            ticker_page = urlopen(ticker_url).read()
            ticker_soup = BeautifulSoup(ticker_page, features="lxml")
            change = ticker_soup.find(lambda tag: tag.name == 'h3' and tag.get('class') == ['intraday__price'])
            price = (change.text).split("\n")[2]
            entry = str(ticker+" "+ price+" "+ average_rating+" "+num_ratings+"\n")
            print(entry)
            
            g.write(entry)

if (len(sys.argv)>1 and sys.argv[2] == "monitor"):
    f = open(sys.argv[1], 'r')
    #f = open(d+".txt", 'r')
    lines = f.readlines()
    total_change=0
    num_tickers = len(lines)
    for line in lines:
        ticker = line.split()[0]
        old_price = line.split()[1]
        ticker_url = 'https://www.marketwatch.com/investing/stock/'+ticker
        ticker_page = urlopen(ticker_url).read()
        ticker_soup = BeautifulSoup(ticker_page, features="lxml")
        change = ticker_soup.find(lambda tag: tag.name == 'h3' and tag.get('class') == ['intraday__price'])
        #num_ratings = ticker_soup.find(lambda tag: tag.name == 'span' and tag.get('class') == ['count'])
        #print(num_ratings.text)
        price = (change.text).split("\n")[2]
        print(ticker+" "+old_price+" "+price+" "+str(100*(float(price)-float(old_price))/float(old_price)))
        total_change+=(investment/num_tickers)*(float(price)-float(old_price))/float(old_price)
    total_change+= investment
    print(100*(total_change-investment)/investment)
if (len(sys.argv)>1 and sys.argv[2] == "random"):
    temp = int(sys.argv[3])
    f = open(sys.argv[1], 'r')
    g = open(sys.argv[1].split(".")[0]+"_rand_"+str(temp)+".txt", 'w')
    lines = f.readlines()
    for line in lines:
        if(line.split()[2] =='Buy' or line.split()[2] =='Over' and int(line.split()[3])>4):
            pair = (line.split()[0], line.split()[1], line.split()[3])
            pairs.append(pair)
    shuffle(pairs)
    sample += pairs[:temp]
    print(sample)
    for ticker, price, rating in sample:
        g.write(ticker+" "+price+" "+rating+"\n")
        


