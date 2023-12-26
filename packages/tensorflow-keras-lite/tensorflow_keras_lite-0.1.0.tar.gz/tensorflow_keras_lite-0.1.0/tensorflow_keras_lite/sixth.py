def print_prog():
    print(
        """

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
# Minisom library and module is used for performing Self Organizing Maps
from minisom import MiniSom
# to suppress warnings
from warnings import filterwarnings
filterwarnings('ignore')
data = pd.read_csv('/kaggle/input/ann-lab-dataset/Credit_Card_Applications.csv')
data.shape
data.info
X = data.iloc[:, 1:14].values
y = data.iloc[:, -1].values
# X variables:
pd.DataFrame(X)
pd.DataFrame(y)
from sklearn.preprocessing import MinMaxScaler
sc = MinMaxScaler(feature_range = (0, 1))
X = sc.fit_transform(X)
pd.DataFrame(X)
# Set the hyper parameters
som_grid_rows = 10
som_grid_columns = 10
iterations = 20000
sigma = 1
learning_rate = 0.5
# define SOM:
som = MiniSom(x = som_grid_rows, y = som_grid_columns, input_len=13,sigma=sigma, learning_rate=learning_rate)
# Initializing the weights
som.random_weights_init(X)
# Training
som.train_random(X, iterations)
# Shape of the weight are:
# wts.shape
# Returns the distance map from the weights:
som.distance_map()
from pylab import plot, axis, show, pcolor, colorbar, bone
bone()
pcolor(som.distance_map().T) # Distance map as background
colorbar()
show()
bone()
pcolor(som.distance_map().T)
colorbar() #gives legend
markers = ['o', 's'] # if the observation is fraud then red circular color or else green square
colors = ['r', 'g']
for i, x in enumerate(X):
    w = som.winner(x)
    plot(w[0] + 0.5,w[1] + 0.5,markers[y[i]],markeredgecolor = colors[y[i]],markerfacecolor = 'None',markersize = 10,markeredgewidth = 2)
show()
mappings = som.win_map(X)
mappings
# out of the 100 segments: 70 segments have customers and other 30 segments don't have any customers mapped to it
len(mappings.keys())
mappings[(8,7)]
# Taking some of the red circular from the heat map and mapping as Frauds:
frauds = np.concatenate((mappings[(0,9)], mappings[(8,9)]), axis = 0)
frauds
          """
    )
