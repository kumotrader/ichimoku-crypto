# Ichimoku Crypto 

# Description
An example of crypto-modified ichimoku clouds in Python / pandas / Matplotlib.
This demo shows how to calculate and generate beautiful Ichimoku diagrams.

Sample Generated Image:

![Ichimoku Crypto (Python) Sample Code](https://github.com/kumotrader/ichimoku-crypto/blob/master/sample-data/sample.png "Ichimoku Crypto Python/Matplotlib")


Telegram Group: https://t.me/kumo_trading_tech_analysis
- Learn how to use Ichimoku strategies for crypto trading
- Stay updated with automated daily Kumo Reports and analysis on promising coins


# Installation
1. install pipenv to manage dependencies (https://docs.pipenv.org/)
2. Install python-tk
3. Run `pipenv` - will install all dependencies in a virtual environment


# Running in console `pipenv run python`
```
from ichimoku import *
# Load Sample Data into a dataframe
df = pd.read_csv('./sample-data/ohcl_sample.csv',index_col=0)
# Initialize with ohcl dataframe
i = Ichimoku(df)
# Generates ichimoku dataframe
ichimoku_df = i.run()

# Plot ichimoku
i.plot()
```



# Crypto-modified Ichimoku Values
| Signal                 |  Stocks(9a-5p) | Crypto (adj 24/7) | Double it (accepted value)  | Formula                                 |
|------------------------|----------------|-------------------|-----------------------------|-----------------------------------------|
| Tenkan (conversion):   |   9            | 10                |  20                         | (eg. 9-period high + 9-period low)/2))  |
| Kijun (base):          |  26            | 30                |  60                         | (eg. 26-period high + 26-period low)/2))|
| Senkou span A (faster):|                |                   |                             | (Conversion Line + Base Line)/2))       |
| Senkou span B (slower):|  52            | 60                | Double: 120                 | (eg. 52-period high + 52-period low)/2))|
| Cloud displacement:    |  26            | 30                | Double: 30                  |                                         |
| Chikou (lagging span): |  26            | 30                | Double: 30                  |                                         |
