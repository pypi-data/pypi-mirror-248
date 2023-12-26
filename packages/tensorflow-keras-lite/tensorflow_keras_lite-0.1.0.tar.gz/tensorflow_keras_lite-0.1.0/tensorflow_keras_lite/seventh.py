def print_prog():
    print(
        """
import numpy as np
import matplotlib.pyplot as plt
from keras.models import Sequential
from keras.layers import Embedding, LSTM, GRU, Bidirectional, Dense
from tensorflow.keras.preprocessing.sequence import pad_sequences

# Specify the path to the downloaded IMDB dataset
path_to_imdb = '/kaggle/input/ann-lab-dataset/imdb.npz'  # Replace with the actual path

# Load the IMDB dataset from the local path
with np.load(path_to_imdb, allow_pickle=True) as data:
    x_train, y_train = data['x_train'], data['y_train']
    x_test, y_test = data['x_test'], data['y_test']



max_features = 90000  # Set to a value greater than or equal to the maximum token index (88583)
max_len = 100
print("Vocabulary size (max_features):", max_features)

x_train = pad_sequences(x_train, maxlen=max_len)
x_test = pad_sequences(x_test, maxlen=max_len)

# Define models
models = [
    ('LSTM', Sequential([Embedding(max_features, 32), LSTM(32), Dense(1, activation='sigmoid')])),
    ('GRU', Sequential([Embedding(max_features, 32), GRU(32), Dense(1, activation='sigmoid')])),
    ('Bidirectional LSTM', Sequential([Embedding(max_features, 32), Bidirectional(LSTM(32)), Dense(1, activation='sigmoid')])),
    ('Bidirectional GRU', Sequential([Embedding(max_features, 32), Bidirectional(GRU(32)), Dense(1, activation='sigmoid')]))
]

# Compile and train models
epochs = 5
batch_size = 128
history_dict = {}

for name, model in models:
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    history = model.fit(x_train, y_train, epochs=epochs, batch_size=batch_size, validation_data=(x_test, y_test), verbose=0)
    history_dict[name] = history

# Plot the training loss
plt.figure(figsize=(12, 8))
for name, history in history_dict.items():
    plt.plot(history.history['loss'], label=name)

plt.title('Training Loss of Different RNN Architectures')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.legend()
plt.show()"""
    )
