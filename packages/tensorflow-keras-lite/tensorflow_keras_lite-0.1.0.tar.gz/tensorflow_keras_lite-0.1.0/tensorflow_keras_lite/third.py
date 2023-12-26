def print_prog():
    print(
        """
import tensorflow as tf
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import pandas as pd
# Load the Sonar dataset
sonar_data = pd.read_csv('/kaggle/input/ann-lab-dataset/sonar.csv')
# Split the dataset into features and labels
X = sonar_data.iloc[:, :-1].values
y = sonar_data.iloc[:, -1].values
# Encode labels to 0 and 1
label_encoder = LabelEncoder()
y = label_encoder.fit_transform(y)
# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2,
random_state=42)
# Define the Perceptron model using TensorFlow
model = tf.keras.models.Sequential([
tf.keras.layers.Input(shape=(X_train.shape[1],)),
tf.keras.layers.Dense(1, activation='sigmoid')
])
# Compile the model
model.compile(optimizer='sgd', loss='binary_crossentropy', metrics=['accuracy'])
# Train the model
model.fit(X_train, y_train, epochs=100, verbose=1)
# Evaluate the model
test_loss, test_accuracy = model.evaluate(X_test, y_test, verbose=0)
print(f'Test Accuracy: {test_accuracy * 100:.2f}%')
# Define the Perceptron model using TensorFlow
model_tuned = tf.keras.models.Sequential([
tf.keras.layers.Input(shape=(X_train.shape[1],)),
tf.keras.layers.Dense(1, activation='sigmoid')
])
# Compile the model with a lower learning rate
model_tuned.compile(optimizer=tf.keras.optimizers.SGD(learning_rate=0.01),
loss='binary_crossentropy',
metrics=['accuracy'])
# Train the model with more epochs
model_tuned.fit(X_train, y_train, epochs=200, verbose=1)
# Evaluate the tuned model
test_loss_tuned, test_accuracy_tuned = model_tuned.evaluate(X_test,
y_test, verbose=0)
print(f'Tuned Test Accuracy: {test_accuracy_tuned * 100:.2f}%')
# Define the Perceptron model using TensorFlow with Batch Stochastic Gradient Descent
model_batch_sgd = tf.keras.models.Sequential([
tf.keras.layers.Input(shape=(X_train.shape[1],)),
tf.keras.layers.Dense(1, activation='sigmoid')
])
# Compile the model with SGD optimizer and use batch_size
model_batch_sgd.compile(optimizer=tf.keras.optimizers.SGD(),loss='binary_crossentropy',metrics=['accuracy'])
# Train the model using batch stochastic gradient descent
model_batch_sgd.fit(X_train,y_train,epochs=100,batch_size=32,verbose=1)
# Evaluate the model
test_loss_batch_sgd, test_accuracy_batch_sgd = model_batch_sgd.evaluate(X_test, y_test, verbose=0)
print(f'Batch SGD Test Accuracy: {test_accuracy_batch_sgd * 100:.2f}%')
"""
    )
