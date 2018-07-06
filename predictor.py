from datetime import datetime

from pandas._libs.tslibs.timestamps import Timestamp
from sklearn.metrics import r2_score
from sklearn.preprocessing import MinMaxScaler
from sklearn.svm import SVR


class Predictor(object):
    def train(self, x, y):
        pass

    def predict(self, days):
        pass


class SVRPredictor(Predictor):
    def __init__(self, penalty=100):
        """
        uses SVR to predict te stock value
        :param penalty:
        """
        self.svr = SVR(C=penalty)
        self.scaler = MinMaxScaler()

    def test(self, stock):
        x,y = stock.get_axis()
        x = self._convert_from_timestamp(x)
        x = self._scale_x(x)
        train_x, test_x = split_array(x, 2)
        train_y, test_y = split_array(y, 2)
        self._train(train_x, train_y)
        prediction = self._predict(test_x)
        print(r2_score(test_y, prediction))
        prediction_x = self._unscale_x(test_x)
        prediction_x = self._convert_to_timestap(prediction_x)
        return prediction_x, prediction

    def _train(self, x, y):
        self.svr.fit(x, y)

    def _predict(self, test_x):
        predictions = self.svr.predict(test_x)
        return predictions

    def _convert_from_timestamp(self, dates_array):
        return [(i, z.value) for i,z in enumerate(dates_array)]

    def _convert_to_timestap(self, dates_array):
        return [Timestamp(z) for i, z in dates_array]

    def _scale_x(self, x):
        return self.scaler.fit_transform(x)

    def _unscale_x(self, x):
        return self.scaler.inverse_transform(x)


def split_array(array, chunks=2):
    length = len(array)
    if length< chunks:
        return array
    chunk_size = length // chunks
    for i in range(chunks):
        if i == chunks -1:
            yield array[i*chunk_size:]
        else:
            yield array[i*chunk_size:(i+1) * chunk_size]


