
class Stock(object):
    def __init__(self, stock_name, stock_data):
        """
        A placeholder class to represent a stock

        :param stock_name: the stock name
        :type stock_name: str
        :param stock_data: a table of data about the stock
        :type stock_data: pandas.DataFrame
        """
        self.stock_data = stock_data
        self.stock_name = stock_name

    def get_axis(self):
        """
        returns 2 lists
        one containing a list of dates
        the other containing there respective values (the value of the stock that day)
        :return:
        """
        return self.stock_data['Date'], self.stock_data['Adj. Open']



