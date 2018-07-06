import matplotlib.pyplot as plt


class StockGraph(object):
    AVAILABLE_COLORS = ['red', 'blue', 'black', 'green', 'purple', 'yellow', 'brown']

    def __init__(self, title):
        """
        utility that wraps around matplotlib
        :param title:
        """
        self.title = title
        self.plt = plt.gca()
        self._picked_colors = set()

    def add_stock(self, stock, color=None):
        x, y = stock.get_axis()
        self.add_line(x, y, color)

    def add_line(self, x, y, color=None):
        if not color:
            color = list(set(self.AVAILABLE_COLORS) - self._picked_colors)[0]
        self._picked_colors.add(color)
        plt.plot(x, y, color)

    def show(self):
        plt.title(self.title)
        plt.xlabel('time')
        plt.ylabel('value')
        plt.show()
