import numpy as np
import csv
import matplotlib.pyplot as plt

data = np.loadtxt(open("K.csv", "rb"), delimiter=",", skiprows=1, usecols = 1)

plt.plot(data)
plt.show()

print(data)
