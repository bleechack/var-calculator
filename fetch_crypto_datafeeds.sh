#! /bin/bash

if [[ -z $ALPHAVANTAGE_KEY ]]; then
    echo "Don't forget to set ALPHAVANTAGE_KEY..."
    exit
fi

for symbol in $@; do
    echo ${symbol}
    URL="https://www.alphavantage.co/query?function=DIGITAL_CURRENCY_DAILY&symbol=${symbol}&market=USD&apikey=${ALPHAVANTAGE_KEY}&datatype=csv"
    echo "Fetching ${URL}..."
    wget --content-disposition -P datafeeds/ ${URL}
done
