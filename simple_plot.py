import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import pandas as pd
import auquanToolbox.dataloader as dl

# Load the prices data for a stock
start = '2013-06-01'
end = '2016-12-31'
m= 'PG'
data = dl.load_data_nologs('nasdaq', [m], start, end)
prices = data['ADJ CLOSE']

# Compute the cumulative moving average of the price
prices['mu'] = [prices[m][:i].mean() for i in range(len(prices))]
# Plot the price and the moving average
plt.figure(figsize=(15,7))
plt.plot(prices[m])
plt.plot(prices['mu']);
plt.show()


# Compute the z-scores for each day using the historical data up to that day
zscores = [(prices[m][i] - prices['mu'][i]) / np.std(prices[m][:i]) for i in range(len(prices))]

# Start with no money and no positions
money = 0
count = 0
for i in range(len(prices)):
    # Sell short if the z-score is > 1
    if zscores[i] > 1:
        money += prices[m][i]
        count -= 1
    # Buy long if the z-score is < 1
    elif zscores[i] < -1:
        money -= prices[m][i]
        count += 1
    # Clear positions if the z-score between -.5 and .5
    elif abs(zscores[i]) < 0.5:
        money += count*prices[m][i]
        count = 0
print money