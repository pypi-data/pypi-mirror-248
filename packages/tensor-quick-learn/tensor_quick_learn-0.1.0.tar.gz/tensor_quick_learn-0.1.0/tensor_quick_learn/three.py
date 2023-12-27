import inspect
def func():

   '''
from sklearn.metrics import r2_score
from sklearn.neural_network import MLPRegressor
from sklearn.model_selection import train_test_split

import numpy as np
import pandas as pd
df = pd.read_csv("CR_Data.csv")

x = df.drop(['label'], axis=1).values
y = df['label'].values

x_train, x_test, y_train, y_test = train_test_split(x,y,test_size= 0.25, random_state = 0)

# bpn = MLPRegressor(random_state=1, max_iter=300)

clr = MLPRegressor(hidden_layer_sizes=(100,100,100), max_iter=500, alpha=0.0001,solver='sgd', random_state=1,tol=0.000000001, verbose=1, activation="logistic")
model = clr.fit(x_train, y_train,)
y_pred = model.predict(x_test)
print("Accuracy = ", r2_score(y_test, y_pred) )
'''
def px():
    code=inspect.getsource(func)
    print(code)

