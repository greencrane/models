import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import pandas as pd
import auquanToolbox.dataloader as dl

start = '2016-12-01'
end = '2016-12-31'
assets = ['AAPL', 'AIG', 'C', 'T', 'PG', 'JNJ', 'EOG', 'MET', 'DOW', 'AMGN']
data = dl.load_data_nologs('nasdaq', assets, start, end)
prices = data['ADJ CLOSE']
returns = prices/prices.shift(-1) -1
returns.plot(figsize=(15,7), color=['r', 'g', 'b', 'k', 'c', 'm', 'orange',
                                     'chartreuse', 'slateblue', 'silver'])
plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
plt.ylabel('Returns')

# Convert to numpy array to make manipulation easier
data = np.array(prices);

# For each security, take the return for the first week
wreturns = (data[4] - data[0])/data[0]
# Rank securities by return, with 0 being the lowest return
order = wreturns.argsort()
ranks = order.argsort()

# For each security, take the return for the month following the first week
# Normalization for the time period doesn't matter since we're only using the returns to rank them
mreturns = (data[-1] - data[5])/data[5]
order2 = mreturns.argsort()
ranks2 = order2.argsort()

# Plot the returns for the first week vs returns for the next month to visualize them
plt.figure(figsize=(15,7))
plt.scatter(wreturns, mreturns)
plt.xlabel('Returns for the first week')
plt.ylabel('Returns for the following month');

# Go long (by one share each) in the bottom 20% of securities and short in the top 20%
longs = np.array([int(x < 2)for x in ranks])
shorts = np.array([int(x > 7) for x in ranks])
print 'Going long in:', [assets[i] for i in range(len(assets)) if longs[i]]
print 'Going short in:', [assets[i] for i in range(len(assets)) if shorts[i]]

# Resolve all positions and calculate how much we would have earned
print 'Yield:', sum((data[-1] - data[4])*(longs - shorts))