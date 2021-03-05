import sys
f = open(sys.argv[1],'r')
lines = f.readlines()
num_tickers = float(len(lines))
investment = float(sys.argv[2])
tickers = []
total_cost = 0

for line in lines:
    temp = (line.split()[0], line.split()[1])
    tickers.append(temp)

for ticker, price in tickers:
    max_per_share = investment/num_tickers
    num_buy = int(max_per_share/float(price))
    if (num_buy == 0):
        num_buy = 1
    if (max_per_share - num_buy*float(price) < 0.5*float(price)):
        #print("added another")
        num_buy += 1
        
    print(ticker, num_buy)
    total_cost += num_buy*float(price)
print(total_cost)

for ticker, price in tickers:
    max_per_share = investment/num_tickers
    num_buy = int(max_per_share/float(price))
    if (num_buy == 0):
        num_buy = 1
    if (max_per_share - num_buy*float(price) < 0.5*float(price)):
        #print("added another")
        num_buy += 1
    cost = float(price)*num_buy
    percentage = 100*(cost/total_cost)
    print(ticker, percentage)
        
    
