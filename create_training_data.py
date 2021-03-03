import numpy as np
import csv
import matplotlib.pyplot as plt

raw = np.loadtxt(open("K.csv", "rb"), delimiter=",", skiprows=1, usecols = 1)
flattened = []
augmented = []
training = []

for i in range(len(raw)):
    flattened.append(float(raw[i]))

for i in range(2,20):
    augmented += flattened*i
print(len(augmented))
#ls = [type(item) for item in augmented]
#print(ls)
print(type(augmented))
for i in range(len(augmented)):
    if(i == 47815):
        break
    #print(augmented[i])
    if (i%5!=0):
        continue
    row = []
    to_train = False
    for j in range(0,5):
        #print(augmented[i+j])
        row.append(augmented[i+j])
        if (j==4):
            if (augmented[i+j+1]>augmented[i+j]):
                row.append(1)
                to_train = True
            elif(augmented[i+j+1]<augmented[i+j]):
                row.append(0)
                to_train = True
            else:
                print("Held")
                to_train = False
    #print(row)
    if (to_train):
        training.append(row)

print(len(training))
