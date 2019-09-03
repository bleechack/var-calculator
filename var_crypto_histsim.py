#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
from scipy.stats import norm
from scipy.stats import normaltest
import csv
import os
import argparse
import sys
import logging
import locale
import math
import matplotlib.pyplot as plt

DEFAULT_SYMBOLS = {
    'BTC': 'USD',
    'ETH': 'USD',
    'XRP': 'USD',
    'LTC': 'USD',
    'EOS': 'USD',
    }
DATAFILE_PATTERN = 'datafeeds/currency_daily_{}_{}.csv'

# TODO: convert configuration parameters to command-line options

VOL_PERIOD_t = 1
HORIZON_T = 30
CONFIDENCE_LEVEL = 0.95
SAMPLE_START = 1  # rows from beginning of file
SAMPLE_LENGTH = 200
PEARSON_ALPHA = 1e-3

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
    parser = argparse.ArgumentParser(description='Calculate VaR.')

    parser.add_argument('--start', metavar='N', type=int,
                        default=SAMPLE_START,
                        help='start sample N days ago')
    parser.add_argument('--length', metavar='N', type=int,
                        default=SAMPLE_LENGTH + 1,
                        help='length of sample')

    args = parser.parse_args()
    output = []
    for (symbol, curr) in DEFAULT_SYMBOLS.items():
        close_delta = load_data(symbol, curr, args.start,
                                args.length)['close (USD)'].pct_change()

        # This method assumes normality, insure you cannot reject that assumption.

        reject_normal = normaltest(close_delta, axis=None,
                                   nan_policy='omit') < PEARSON_ALPHA

        # close_delta.hist(bins=int(math.sqrt(n)))
        # plt.show()

        # summary statistics

        n = close_delta.count()
        mu = close_delta.mean()
        sigma = close_delta.std()
        normal_deviate = norm.ppf(CONFIDENCE_LEVEL)
        logging.info(
            '[%s] Reject Normal = %s. n = %d. mu = %0.04f. sigma = %0.04f. normal_deviate = %0.03f'
                ,
            symbol,
            reject_normal,
            n,
            mu,
            sigma,
            normal_deviate,
            )

        # scale volatility

        vol_horizon = sigma * math.sqrt(HORIZON_T / VOL_PERIOD_t)

        # simulate

        sim = np.random.normal(mu, vol_horizon, n)
        sim = np.msort(sim)
        selected = int((1 - CONFIDENCE_LEVEL) * n) + 1
        var_dowd = sim[selected]
        var_allen = np.mean([sim[selected], sim[selected + 1]])
        logging.info('[%s] Selected = %d. VaR (Dowd count) = %0.4f. VaR (Allen count+mean) = %0.04f'
                     , symbol, selected, var_dowd, var_allen)

        output.append({
            'symbol': symbol,
            'n': n,
            'mu': mu,
            'sigma': sigma,
            'vol_horizon': vol_horizon,
            'normal_deviate': normal_deviate,
            'selected': selected,
            'var_dowd': var_dowd,
            'var_allen': var_allen,
            })
    outdf = pd.DataFrame(output)
    outdf = outdf.set_index('symbol')
    outdf.to_csv('{}.output.csv'.format(os.path.splitext(os.path.basename(__file__))[0]))
