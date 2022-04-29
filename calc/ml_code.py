import numpy as np
from sklearn.linear_model import LinearRegression

def train(x,y):
    new_x = np.array(x).reshape((-1,1))
    new_y = np.array(y)
    model = LinearRegression()
    model.fit(new_x, new_y)
    model = LinearRegression().fit(new_x, new_y)
    y_pred = model.predict(new_x)
    y_pred = y_pred.astype(int)
    return y_pred
    

