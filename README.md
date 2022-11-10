# Efficient Frontier
Portfolio optimization using modern portfolio theory. Any group of assets accessible from Yahoo Finance can be used to estimate
Maximum Sharpe Ratio portfolios and Minimum Variance portfolios. Ten thousand randomly weighted portfolios are created, and
portfolio expected returns and standard deviation is calculated from historical returns ranging back a selected number of years. 

# Correlation and Covariance Matrices
Assets with low to negative correlations will produce portfolios with lower variance. A correlation and covariance matrix is plotted
to visualize or manually select a smaller group of assets to test.
![Corr and Cov Matrices](https://user-images.githubusercontent.com/45056473/201168924-6aa3c498-fb94-4aa1-8fd8-9e68fc286aca.PNG)

# Two-Asset Portfolio Optimization
Every portfolio is plotted on a graph of expected returns vs standard deviations. The minimum variance portfolio is the furthermost
left point on the plot. The maximum sharpe portfolio is calculated by sorting the portfolios by sharpe ratios. Finally, the capital
allocation line is plotted tangent to the efficent frontier and connects the risk-free rate and maximum sharpe ratio portfolio.
![Eff_front_two_assets](https://user-images.githubusercontent.com/45056473/201169225-031d9ff8-f264-4a0c-a08c-c6f02f51a1cd.PNG)

# Mult-Asset Portfolio Optimization
![Eff_front](https://user-images.githubusercontent.com/45056473/201169241-5c47ed9f-49c9-44b0-a77e-00f2a2c29c36.PNG)
Optimal Portfolio:
AAPL: 0.918863,
GOOG: 0.051395,
BRK-B: 0.021941,     
JNJ: 0.0078,
Returns: 0.292986,
St_Dev: 0.317209,
Sharpe: 0.910714 

Minimum Variance Portfolio:
AAPL: 0.005377,
GOOG: 0.272814,
BRK-B: 0.091699,
JNJ: 0.630109,
Returns: 0.109641,    
St_Dev: 0.191628,  
Sharpe: 0.550759

TO-DO: Add asset constraints.
