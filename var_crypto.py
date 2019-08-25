#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd
from scipy.stats import norm
import csv
import os
import argparse
import sys
import logging
import locale
import math

DEFAULT_SYMBOLS = {
    'BTC': 'USD',
    'ETH': 'USD',
    'XRP': 'USD',
    'LTC': 'USD',
    'EOS': 'USD',
    }
DATAFILE_PATTERN = 'datafeeds/currency_daily_{}_{}.csv'
VOL_PERIOD_t = 1
HORIZON_T = 3
CONFIDENCE_LEVEL = 0.95
SAMPLE_START = 1  # rows from beginning of file
SAMPLE_LENGTH = 90

locale.setlocale(locale.LC_ALL, '')
logging.basicConfig(stream=sys.stdout,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
                    , level=logging.INFO)
logger = logging.getLogger(os.path.basename(__file__))


def get_datafile(symbol, currency):
    return DATAFILE_PATTERN.format(symbol, currency)


def load_data(
    symbol,
    currency,
    start,
    length,
    ):

    datafile = get_datafile(symbol, currency)
    df = pd.read_csv(datafile)
    df = df[start:start + length]
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df = df.set_index('timestamp')
    return df


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Calculate VWMA.')

    parser.add_argument('--start', metavar='N', type=int,
                        default=SAMPLE_START,
                        help='start sample N days ago')
    parser.add_argument('--length', metavar='N', type=int,
                        default=SAMPLE_LENGTH, help='length of sample')

    args = parser.parse_args()
    output = []
    for (symbol, curr) in DEFAULT_SYMBOLS.items():
        close_delta = load_data(symbol, curr, args.start,
                                args.length)['close (USD)'].pct_change()
        sigma = close_delta.std()
        mu = close_delta.mean()
        kurt = close_delta.kurtosis()
        skew = close_delta.skew()
        normal_deviate = norm.ppf(CONFIDENCE_LEVEL)
        vol_horizon = sigma * math.sqrt(HORIZON_T / VOL_PERIOD_t)
        var_t_pct = vol_horizon * normal_deviate
        output.append({
            'symbol': symbol,
            'mu': mu,
            'sigma': sigma,
            'kurt': kurt,
            'skew': skew,
            'normal_deviate': normal_deviate,
            'vol_horizon': vol_horizon,
            'var_t_pct': var_t_pct,
            })
        logging.info(
            '[%s] mu = %0.4f, sigma = %0.4f, kurt = %0.4f, skew = %0.4f'
                ,
            symbol,
            mu,
            sigma,
            kurt,
            skew,
            )
        logging.info('[%s] normal_deviate = %0.4f, vol_horizon = %0.4f, VaR (%%) = %0.4f'
                     , symbol, normal_deviate, vol_horizon, var_t_pct)
    outdf = pd.DataFrame(output)
    outdf = outdf.set_index('symbol')
    outdf.to_csv("{}.output.csv".format(os.path.splitext(os.path.basename(__file__))[0]))
