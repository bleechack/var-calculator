# Value-at-Risk (VaR) Calculator

## USAGE: Stocks

### Download datafeeds

    $ ./fetch_stock_datafeeds.sh SPY QQQ GLD
    Fetching https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol=SPY&apikey=APIKEY&datatype=csv&outputsize=full...
    --2019-08-25 20:42:44--  https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol=SPY&apikey=APIKEY&datatype=csv&outputsize=full
    Resolving www.alphavantage.co... 52.72.245.79, 3.220.125.240, 3.225.101.71, ...
    Connecting to www.alphavantage.co|52.72.245.79|:443... connected.
    HTTP request sent, awaiting response... 200 OK
    Length: unspecified [application/x-download]
    Saving to: 'datafeeds/daily_adjusted_SPY.csv'

        [  <=>                                                                                                       ] 400,291     1.00MB/s   in 0.4s   

    2019-08-25 20:42:46 (1.00 MB/s) - 'datafeeds/daily_adjusted_SPY.csv' saved [400291]

### Configure script

Inspect the constants in the calculator to adjust for your model:

    VOL_PERIOD_t - # of periods per row in datafile (typically 1 day)
    HORIZON_T - # of days in horizon (ex. 30 days = 1 month)
    CONFIDENCE_LEVEL - % confidence as float (0.95 = 95%)
    SAMPLE_START - Starting position in datafile (# of days ago)
    SAMPLE_LENGTH - Number of days to use for volatility calculation

### Run script

    usage: var_stocks.py [-h] [--start N] [--length N]

    Calculate VaR.

    optional arguments:
      -h, --help  show this help message and exit
      --start N   start sample N days ago
      --length N  length of sample


### Example usage

    $ ./var_stocks.py --start=7 --length=30
    2019-08-25 20:45:45,878 - root - INFO - [SPY] mu = 0.0018, sigma = 0.0110, kurt = 2.0627, skew = 0.8810
    2019-08-25 20:45:45,878 - root - INFO - [SPY] normal_deviate = 1.6449, vol_horizon = 0.0602, VaR (%) = 0.0990
    2019-08-25 20:45:45,904 - root - INFO - [QQQ] mu = 0.0017, sigma = 0.0130, kurt = 1.2828, skew = 0.6896
    2019-08-25 20:45:45,904 - root - INFO - [QQQ] normal_deviate = 1.6449, vol_horizon = 0.0711, VaR (%) = 0.1169
    2019-08-25 20:45:45,928 - root - INFO - [GLD] mu = -0.0022, sigma = 0.0099, kurt = -0.7155, skew = -0.1614
    2019-08-25 20:45:45,928 - root - INFO - [GLD] normal_deviate = 1.6449, vol_horizon = 0.0542, VaR (%) = 0.0891



## USAGE: Cryptocurrency

### Download datafeeds

You must first download or update the datafile for each symbol that you wish to include in your calculation.

    $ ./fetch_crypto_datafeeds.sh BTC
    Fetching https://www.alphavantage.co/query?function=DIGITAL_CURRENCY_DAILY&symbol=BTC&market=USD&apikey=APIKEY&datatype=csv...
    --2019-08-25 11:58:23--  https://www.alphavantage.co/query?function=DIGITAL_CURRENCY_DAILY&symbol=BTC&market=USD&apikey=APIKEY&datatype=csv
    Resolving www.alphavantage.co... 52.22.145.207, 34.236.110.238, 52.23.2.88, ...
    Connecting to www.alphavantage.co|52.22.145.207|:443... connected.
    HTTP request sent, awaiting response... 200 OK
    Length: unspecified [application/x-download]
    Saving to: 'datafeeds/currency_daily_BTC_USD.csv'
        [ <=>                                                                                                        ] 114,655      612KB/s   in 0.2s   
    2019-08-25 11:58:24 (612 KB/s) - 'datafeeds/currency_daily_BTC_USD.csv' saved [114655]


### Configure script

Inspect the constants in the calculator to adjust for your model:

    VOL_PERIOD_t - # of periods per row in datafile (typically 1 day)
    HORIZON_T - # of days in horizon (ex. 30 days = 1 month)
    CONFIDENCE_LEVEL - % confidence as float (0.95 = 95%)
    SAMPLE_START - Starting position in datafile (# of days ago)
    SAMPLE_LENGTH - Number of days to use for volatility calculation

### Run script

    usage: var_crypto.py [-h] [--start N] [--length N]

    Calculate VaR.

    optional arguments:
      -h, --help  show this help message and exit
      --start N   start sample N days ago
      --length N  length of sample

### Example usage

Start volatility sampling seven days ago and sample a period of thirty days.

    $ ./var_crypto.py --start=7 --length=30
    2019-08-25 11:53:48,383 - root - INFO - [LTC] mu = 0.0103, sigma = 0.0420, kurt = 0.8723, skew = 0.0874
    2019-08-25 11:53:48,383 - root - INFO - [LTC] normal_deviate = 1.6449, vol_horizon = 0.0727, VaR (%) = 0.1197
    2019-08-25 11:53:48,398 - root - INFO - [EOS] mu = 0.0061, sigma = 0.0429, kurt = 0.8756, skew = 0.2004
    2019-08-25 11:53:48,398 - root - INFO - [EOS] normal_deviate = 1.6449, vol_horizon = 0.0742, VaR (%) = 0.1221
    2019-08-25 11:53:48,413 - root - INFO - [ETH] mu = 0.0061, sigma = 0.0345, kurt = 2.9691, skew = 1.0135
    2019-08-25 11:53:48,413 - root - INFO - [ETH] normal_deviate = 1.6449, vol_horizon = 0.0598, VaR (%) = 0.0983
    2019-08-25 11:53:48,429 - root - INFO - [XRP] mu = 0.0061, sigma = 0.0333, kurt = 6.5441, skew = 1.7018
    2019-08-25 11:53:48,429 - root - INFO - [XRP] normal_deviate = 1.6449, vol_horizon = 0.0576, VaR (%) = 0.0948
    2019-08-25 11:53:48,445 - root - INFO - [BTC] mu = 0.0019, sigma = 0.0331, kurt = 0.7573, skew = 0.1477
    2019-08-25 11:53:48,445 - root - INFO - [BTC] normal_deviate = 1.6449, vol_horizon = 0.0573, VaR (%) = 0.0943
