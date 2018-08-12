import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
import matplotlib.pylab as plt
from sklearn.model_selection import GridSearchCV

df = pd.read_csv('/Users/tuantuan/Downloads/log2.csv')
df_data = pd.DataFrame(df)
df_data = df_data.head(256)
data, throught = np.split(df_data, (13,), axis=1)
data, throught = np.split(data, (12,), axis=1)

data, temp = np.split(data,(11,),axis=1)

throught = np.array(throught,dtype=float)
data = np.array(data)
throught = throught.ravel()


rfr = RandomForestRegressor()
# param_grid = {"n_estimators":range(50,55),"min_samples_leaf":range(10,15)}
# rfr = GridSearchCV(rfr,cv=10,param_grid = param_grid)
rfr.fit(data,throught)
# print(rfr.best_params_)

linreg = LinearRegression()
linreg.fit(data,throught)


df = pd.read_csv('/Users/tuantuan/Downloads/log.csv')
df_data_2 = pd.DataFrame(df)
df_data_2 = df_data_2.head(256)
data_2, throught_2 = np.split(df_data_2, (13,), axis=1)
data_2, throught_2 = np.split(data_2, (12,), axis=1)

data_2,temp_2 = np.split(data_2,(11,),axis=1)

throught_2 = np.array(throught_2,dtype=float)
data_2 = np.array(data_2)
throught_2 = throught_2.ravel()

s = rfr.predict(data_2)
o = linreg.predict(data_2)

s = s[np.argsort(s)]
throught_2 = throught_2[np.argsort(throught_2)]

o = o[np.argsort(o)]
o_throught_2 = throught_2[np.argsort(throught_2)]

color = ['r','y','k','g','m']
plt.scatter(s, throught_2, color = 'b', marker='>', alpha=0.5, label = 'Regression Tree')
plt.scatter(o, o_throught_2, color = 'k', marker='*', alpha=0.5, label = 'Linear Regression')
plt.legend()
plt.title('Scatter diagram with Predit Output and Actual Output')
plt.xlabel('Predit Output')
plt.ylabel('Actual Output')
plt.grid(True)
plt.show()