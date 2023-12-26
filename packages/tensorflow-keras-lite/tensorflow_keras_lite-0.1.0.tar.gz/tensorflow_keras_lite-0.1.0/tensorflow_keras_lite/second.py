def print_prog():
    print(
        """
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sn
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import tensorflow as tf
from tensorflow import keras
from sklearn.metrics import confusion_matrix, accuracy_score
# Load the Wheat Seed dataset from a local CSV file
# Replace 'your_dataset.csv' with the actual file path
data = pd.read_csv('/kaggle/input/ann-lab-dataset/wheat.csv')

# Preprocess the dataset
X = data.iloc[:, :-1].values
y = data.iloc[:, -1].values
# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
# Adjust labels to start from 0
y_train = y_train - 1
y_test = y_test - 1
# Normalize the data
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)
# Define the neural network model using Keras
model = keras.Sequential([
keras.layers.Input(shape=(X_train.shape[1],)),
keras.layers.Dense(100, activation='relu'),
keras.layers.Dense(3, activation='softmax') # Assuming 3 classes in the dataset
])
model.compile(optimizer='adam',
loss='sparse_categorical_crossentropy',
metrics=['accuracy'])
# Train the model using backpropagation
model.fit(X_train, y_train, epochs=10, verbose=2)
# Evaluate the performance of the trained model
loss, accuracy = model.evaluate(X_test, y_test)
print('Test loss:', loss)
print('Test accuracy:', accuracy)
# Predict on the test set
y_predicted = model.predict(X_test)
y_predicted_labels = [np.argmax(i) for i in y_predicted]
# Calculate the confusion matrix
accuracy = accuracy_score(y_test, y_predicted_labels)
cm = confusion_matrix(y_test, y_predicted_labels)
print('Test accuracy:', accuracy)
# Larger network with more neurons
model_large = keras.Sequential([
keras.layers.Input(shape=(X_train.shape[1],)),
keras.layers.Dense(200, activation='relu'), # Increased neurons
keras.layers.Dense(3, activation='softmax')
])
model_large.compile(optimizer='adam',loss='sparse_categorical_crossentropy',metrics=['accuracy'])
model_large.fit(X_train, y_train, epochs=20, verbose=2) # Trained for more epochs
# Larger network with tanh activation and different weight initialization
model_tanh = keras.Sequential([
keras.layers.Input(shape=(X_train.shape[1],)),
keras.layers.Dense(100,activation='tanh',kernel_initializer='random_normal'),keras.layers.Dense(3, activation='softmax')
])
model_tanh.compile(optimizer='adam',
loss='sparse_categorical_crossentropy',
metrics=['accuracy'])
model_tanh.fit(X_train, y_train, epochs=10, verbose=2)
# More hidden layers
model_multi_layer = keras.Sequential([
keras.layers.Input(shape=(X_train.shape[1],)),
keras.layers.Dense(100, activation='relu'),
keras.layers.Dense(50, activation='relu'), # Additional hidden layer
keras.layers.Dense(25, activation='relu'), # Additional hidden layer
keras.layers.Dense(3, activation='softmax')
])
model_multi_layer.compile(optimizer='adam',loss='sparse_categorical_crossentropy',metrics=['accuracy'])
model_multi_layer.fit(X_train, y_train, epochs=10, verbose=2)
# Regression network
model_regression = keras.Sequential([
keras.layers.Input(shape=(X_train.shape[1],)),
keras.layers.Dense(100, activation='relu'),
keras.layers.Dense(1, activation='linear') # One neuron for regression with linear activation
])
model_regression.compile(optimizer='adam', loss='mean_squared_error') #Using mean squared error for regression
model_regression.fit(X_train, y_train, epochs=10, verbose=2)
# You need to change this line
loss = model_regression.evaluate(X_test, y_test)
# Batch Gradient Descent
model_batch = keras.Sequential([
keras.layers.Input(shape=(X_train.shape[1],)),
keras.layers.Dense(100, activation='relu'),
keras.layers.Dense(3, activation='softmax')
])
model_batch.compile(optimizer='adam',loss='sparse_categorical_crossentropy',metrics=['accuracy'])
# Training using batch gradient descent
model_batch.fit(X_train, y_train, epochs=10, batch_size=32, verbose=2)
"""
    )
