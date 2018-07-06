import os
import pickle

import quandl

from stock import Stock


class StockDataRetriver(object):
    def __init__(self):
        pass

    def get_stock_by_name(self, name):
        pass


class QuandlStockDataRetriver(StockDataRetriver):
    def __init__(self, cache_path, api_key, exchange='WIKI'):
        super().__init__()
        self.cache_path = cache_path
        self.exchange = exchange
        self._define_quandl_api_key(api_key)

    def get_stock_by_name(self, name):
        file_path = os.path.join(self.cache_path, self.exchange + '_' + name.upper())
        if os.path.exists(file_path):
            with open(file_path, 'rb') as f:
                stock = pickle.load(f)
        else:
            stock = quandl.get(self.exchange + '/' + name.upper())
            with open(file_path, 'wb') as f:
                pickle.dump(stock, f)
        # reseting the index makes it so the data will be stored per a increasing integer instead of the date
        stock = stock.reset_index(0)
        return Stock(name, stock)

    def _define_quandl_api_key(self, api_key):
        """Defines the api_key as the token for using Quandl"""
        quandl.ApiConfig.api_key = api_key