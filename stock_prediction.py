# Modules
import quandl
import numpy as np
import matplotlib.pyplot as plt
from sklearn import linear_model
from sklearn.preprocessing import MinMaxScaler
from sklearn.svm import SVR
from random import randint
from sklearn.metrics import r2_score

# Functions
def define_quandl_api_key(api_key):
    """Defines the api_key as the token for using Quandl"""
    quandl.ApiConfig.api_key = api_key

def split_list(array):
    """Splits a given array into 3 parts: half, and two quarters"""
    n = len(array)
    first_slice = int(n/2)
    second_slice = int(3*n/4)
    return array[:first_slice], array[first_slice:second_slice], array[second_slice:]

def get_stock_data(stock_full_name):
    """Queries the data for stock_full_name using Quandl, and gets it into X and y"""
    stock = quandl.get(stock_full_name)
    stock = stock.reset_index(0)
    dates = stock['Date']
    X = [(i, z.value) for i,z in enumerate(dates)]
    y = stock['Adj. Open']
    scaler = MinMaxScaler()
    X_scaled = scaler.fit_transform(X)
    return X_scaled, y

def split_stock_data_into_train_test(X, y):
    """Splits each of the stock arrays X and y into three different arrays: train, train_penalty and test"""
    X_train, X_train_penalty, X_test = split_list(X)
    y_train, y_train_penalty, y_test = split_list(y)
    return X_train, X_train_penalty, X_test, y_train, y_train_penalty, y_test

def svr_predict_stock_price(penalty, X_train, y_train, X_test):
    """Predicts the stock price using penalty, while training on X_train and y_train"""
    svr = SVR(C=penalty)
    svr.fit(X_train, y_train)
    predictions = svr.predict(X_test)
    return predictions

def calculate_best_penalty(X_train, y_train, X_train_penalty, y_train_penalty):
    """Calculates the best penalty for the train_penalty section"""
    penalty_values = []
    penalty_scores = []
    for penalty in range(1,10000,50):
        penalty_values.append(penalty)
        predictions = svr_predict_stock_price(penalty, X_train, y_train, X_train_penalty)
        penalty_scores.append(r2_score(y_train_penalty, predictions))
    best_penalty = penalty_values[penalty_scores.index(max(penalty_scores))]
    return best_penalty

define_quandl_api_key("5BBkZzTWi4Lmsh8MyRyT")
X, y = get_stock_data("WIKI/FB")
X_train, X_train_penalty, X_test, y_train, y_train_penalty, y_test = split_stock_data_into_train_test(X, y)
best_penalty = calculate_best_penalty(X_train, y_train, X_train_penalty, y_train_penalty)
predictions = svr_predict_stock_price(best_penalty, X_train, y_train, X_test)

print("best_penalty:", best_penalty)
print("prediction accuracy score:", r2_score(predictions, y_test))

ax = plt.gca()
plt.xlabel('time')
plt.ylabel('value')
plt.title('Google Stock')
plt.plot(X_train, y_train, color='red')
plt.plot(X_test, y_test, color='blue')
plt.plot(X_train_penalty, y_train_penalty, color='purple')
plt.plot(X_test, predictions, color='black')
plt.show()

print("done!")
