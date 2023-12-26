def print_prog():
    print(
        """

import tensorflow as tf
from tensorflow.keras import layers, models
import matplotlib.pyplot as plt
import numpy as np

# Specify the path to the MNIST dataset file
mnist_path = '/kaggle/input/ann-lab-dataset/mnist.npz'

# Load and preprocess MNIST dataset
with np.load(mnist_path, allow_pickle=True) as data:
    train_images, train_labels = data['x_train'], data['y_train']
    test_images, test_labels = data['x_test'], data['y_test']

train_images, test_images = train_images / 255.0, test_images / 255.0

# Build a simple neural network model
def build_model(optimizer):
    model = models.Sequential([
        layers.Flatten(input_shape=(28, 28)),
        layers.Dense(128, activation='relu'),
        layers.Dense(10)
    ])
    model.compile(optimizer=optimizer, loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True), metrics=['accuracy'])
    return model

# List of optimization techniques to compare
optimizers = ['adam', 'adagrad', 'rmsprop']

# Train models with different optimizers
for optimizer in optimizers:
    model = build_model(optimizer)
    history = model.fit(train_images, train_labels, epochs=5, validation_data=(test_images, test_labels))
    plt.plot(history.history['loss'], label=optimizer)

# Display the results
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.legend()
plt.show()"""
    )
