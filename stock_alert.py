#!/usr/bin/python3.5
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), "pinance"))

import multiprocessing

from pinance import Pinance

import yaml

INPUT_FILE ='stock_list.yaml'

def get_quote(symbol, q):
    stock = Pinance(symbol)
    stock.get_quotes()
    rec_data = stock.quotes_data
    #print(rec_data)
    last_tradeprice = rec_data['LastTradePrice']
    #print('LTP : %s"' %last_tradeprice)
    #return rec_data
    q.put(rec_data)

def get_reco_list():
    ''' Returns symbol of recommended stocks '''
    with open(INPUT_FILE, 'r') as input_file:
        doc = yaml.load(input_file)
    return doc.keys()

def main():
    stock_list =  get_reco_list()
    p_list = []
    for stock in stock_list:
        q = multiprocessing.Queue() 
        p = multiprocessing.Process(target=get_quote, args=(stock, q,))
        #get_quote(stock)
        p.start()
        p_list.append((p,q))

    for p,q in p_list:
        print(q.get())
        p.join()


if __name__ == '__main__':
    main()
