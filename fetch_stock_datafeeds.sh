#! /bin/bash

if [[ -z $ALPHAVANTAGE_KEY ]]; then
    echo "Don't forget to set ALPHAVANTAGE_KEY..."
    exit
fi

for symbol in $@; do
    echo ${symbol}
    URL="https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol=${symbol}&apikey=${ALPHAVANTAGE_KEY}&datatype=csv&outputsize=full"
    echo "Fetching ${URL}..."
    wget --content-disposition -P datafeeds/ ${URL}
done
