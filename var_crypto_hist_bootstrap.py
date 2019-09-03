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
INITIAL_CAPITAL = 1e4
NUM_TRIALS = 500

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
        close = load_data(symbol, curr, args.start,
                                args.length)['close (USD)']
        close_delta = close.pct_change()

        trials = []
        for i in range(0, NUM_TRIALS):
            sample = close_delta.sample(HORIZON_T, replace=True)
            value = INITIAL_CAPITAL
            for delta in sample:
                value *= (1 + delta)
            gain = value - INITIAL_CAPITAL
            gain_pct = gain / INITIAL_CAPITAL
            trials.append(gain_pct)

        # summary statistics
        trial_series = pd.Series(trials)
        n = trial_series.count()
        mu = trial_series.mean()
        sigma = trial_series.std()
        logging.info(
            '[%s] n = %d. mu = %0.04f. sigma = %0.04f.'
                ,
            symbol,
            n,
            mu,
            sigma,
            )

        # simulate

        sim = np.random.normal(mu, sigma, n)
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
            'selected': selected,
            'var_dowd': var_dowd,
            'var_allen': var_allen,
            })
    outdf = pd.DataFrame(output)
    outdf = outdf.set_index('symbol')
    outdf.to_csv('{}.output.csv'.format(os.path.splitext(os.path.basename(__file__))[0]))
