import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import pandas as pd
import auquanToolbox.dataloader as dl
from statsmodels.tsa.stattools import coint

start = '2012-01-01'
end = '2016-12-31'
# Load prices data for HP and Microsoft
data = dl.load_data_nologs('nasdaq', ['MSFT', 'HP'], start, end)
X = data['ADJ CLOSE']['MSFT']
Y = data['ADJ CLOSE']['HP']
# Compute the p-value for the cointegration of the two series
_, pvalue, _ = coint(X,Y)
print pvalue

# Plot their difference and the cumulative moving average of their difference
val = pd.DataFrame(index = X.index, columns=['diff','mu'])
val['diff'] = X - Y
val['mu']= [val['diff'][:i].mean() for i in range(len(val['diff']))]
plt.figure(figsize=(15,7))
plt.plot(val['diff'])
plt.plot(val['mu'])
plt.show()

mu_60d = pd.rolling_mean(val['diff'], window=90)
plt.figure(figsize=(15,7))
plt.plot(val['diff'], label='X-Y')
plt.plot(val['mu'], label='CMA')
plt.plot(mu_60d, label='60d MA')
plt.legend();

# Compute the z-score of the difference on each day
zscores = [(val['diff'][i] - val['mu'][i]) / np.std(val['diff'][:i]) for i in range(len(val['diff']))]

# Start with no money and no positions
money = 0
count = 0
for i in range(len(val['diff'])):
    # Sell short if the z-score is > 1
    if zscores[i] > 1:
        money += val['diff'][i]
        count -= 1
    # Buy long if the z-score is < 1
    elif zscores[i] < -1:
        money -= val['diff'][i]
        count += 1
    # Clear positions if the z-score between -.5 and .5
    elif abs(zscores[i]) < 0.5:
        money += count*val['diff'][i]
        count = 0
        
print money