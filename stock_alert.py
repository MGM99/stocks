#!/usr/bin/python3.5
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), "pinance"))

from pinance import Pinance

import yaml

INPUT_FILE ='stock_list.yaml'

def get_quote(symbol):
    stock = Pinance(symbol)
    stock.get_quotes()
    rec_data = stock.quotes_data
    print(rec_data)
    last_tradeprice = rec_data['LastTradePrice']
    print('LTP : %s"' %last_tradeprice)


def get_reco_list():
    ''' Returns symbol of recommended stocks '''
    with open(INPUT_FILE, 'r') as input_file:
        doc = yaml.load(input_file)
    return doc.keys()

def main():
    stock_list =  get_reco_list()
    for stock in stock_list:
        get_quote(stock)


if __name__ == '__main__':
    main()