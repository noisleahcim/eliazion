from graph import StockGraph
from predictor import SVRPredictor
from stock_data_retriever import QuandlStockDataRetriver


def main():
    retriver = QuandlStockDataRetriver()
    stock = retriver.get_stock_by_name('NFLX')
    predictor = SVRPredictor()
    prediction_x, prediction_y = predictor.test(stock)
    graph = StockGraph('Netflix')
    graph.add_stock(stock, 'green')
    graph.add_line(prediction_x, prediction_y, 'blue')
    graph.show()
    print("done")


if __name__ == '__main__':
    main()