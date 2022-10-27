# NovaInv October 20, 2022
# Efficient frontier for portfolio optimization using Modern Portfolio Theory (MPT)
# Assumptions: -252 trading days in one year
#			   -no asset weight constraints
# References: https://www.machinelearningplus.com/machine-learning/portfolio-optimization-python-example/

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
from datetime import date, timedelta, datetime
import seaborn as sns
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
np.random.seed(684531561) # random seed for generating portfolio weights

tickers = ['AAPL','GOOG','BRK-B','JNJ'] # can use any ticker accesible on yahoo finance
risk_free_rate = 0.041 # current 10 year T-Bill rate (10-19-2022)
lookback_years = 3 # years to lookback when calculating returns
num_portfolios = 10000 # number of simulated portfolios
print_corr_and_cov_matrix = False # option to print and plot correaltion and covariance matrices

# date gathering
today = date.today()
start_date = today - timedelta(days=lookback_years*365)
end_date = today + timedelta(days=1)

df = yf.download(tickers,start=start_date,end=end_date,progress=False)['Adj Close'] # obtain prices from yahoo finance
if df.isnull().values.any():
	# exception handling for missing values in data request
	print('Too long of lookback period. Try shorter time frame.')

returns = df/df.shift(1) - 1 # calculate daily returns
returns.dropna(inplace=True) # remove missing values caused by returns calculation

if print_corr_and_cov_matrix:
	corr_matrix = returns.corr()
	cov_matrix = returns.cov()

	# dual pane plot for correlaiton and covariance plots
	fig, (ax0, ax1) = plt.subplots(1,2,figsize=(12,6))
	sns.heatmap(corr_matrix, ax=ax0)
	sns.heatmap(cov_matrix, ax=ax1)
	ax0.set_title('Correlation Matrix')
	ax1.set_title('Covariance Matrix')
	plt.show()
	print(corr_matrix)
	print('\n',cov_matrix)

annu_returns = np.mean(returns) * 252 # annualize the returns from daily returns
annu_st_dev = np.sqrt(returns.var() * 252) # annualize the standard deviations of daily returns

# list to store simulated portfolios
port_ret_list = []
port_std_list = []
port_wts_list = []

cov_matrix = returns.cov() # sample covariance matrix used 
for n in range(num_portfolios):
	weights = np.random.random(len(tickers)) # generate random weights for each ticker
	weights /= np.sum(weights) # standardize the weights to sum to one
	port_wts_list.append(weights) # store the weights

	port_ret_list.append(np.dot(weights,annu_returns)) # portfolio expected returns

	var = cov_matrix.mul(weights, axis=0).mul(weights, axis=1).sum().sum()# Portfolio Variance
	port_std_list.append(np.sqrt(var * 252)) # annualized portfolio standard deviation

# store results to be sorted in pandas dataframe
result = pd.DataFrame(port_wts_list, columns=tickers)
result['Returns'] = port_ret_list
result['St_Dev'] = port_std_list
result['Sharpe'] = (result['Returns'] - risk_free_rate) / result['St_Dev'] # sharpe ratio calculation

# find maximum sharpe portfolio
result.sort_values(by=['Sharpe'], inplace=True, ascending=False) # sort by largest sharpe
print('\nOptimal Portfolio:')
print(result.head(1)) # print weights of largest sharpe
max_sharpe_port_x, max_sharpe_port_y = result['St_Dev'].head(1), result['Returns'].head(1) # get coordinates for max sharpe portfolio

# find minimum variance portfolio
result.sort_values(by=['St_Dev'],inplace=True,ascending=True) # sort by smallest standard deviation
print('\nMinimum Variance Portfolio:')
print(result.head(1)) # print weights of min var
min_vol_port_x, min_vol_port_y = result['St_Dev'].head(1), result['Returns'].head(1) # get coordinates of min var portfolio

# calculate Capital Allocation Line (CAL) using coordinates of risk free rate and tangency of efficient frontier (max sharpe portfolio)
x = [0,float(max_sharpe_port_x)]
y = [risk_free_rate,float(max_sharpe_port_y)]
coeff = np.poly1d( np.polyfit(x,y, deg=1))
cal = coeff([-1,1])

# scatter plot of simulated portfolios
result.plot.scatter(x='St_Dev', y='Returns', marker='o', s=10, alpha=0.3, grid=True, figsize=[10,10])
plt.scatter(min_vol_port_x, min_vol_port_y, color='r', marker='*', s=300, label='Min Variance') # show min var portfolio
plt.scatter(max_sharpe_port_x, max_sharpe_port_y, color='g', marker='*', s=300,label='Max Sharpe') # show max sharpe portfolio
plt.plot([-1,1],cal,label='CAL',color='orange') # Capital allocation line
plt.xlim([0,result['St_Dev'].max()*1.25]) # adjust x-axis
plt.ylim([min(result['Returns'].min()-0.01,0),result['Returns'].max()*1.25]) # adjust y-axis
plt.legend(loc='upper right')
plt.show()

