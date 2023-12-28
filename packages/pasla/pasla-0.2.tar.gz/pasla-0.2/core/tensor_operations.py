# core/tensor_operations.py
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
import matplotlib.pyplot as plt
import seaborn as sns

def preprocess_data(data):
    """pra-pemrosesan data untuk model machine learning."""
    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(data)
    
    return scaled_data

def build_and_train_nn_model(X_train, y_train, X_test, y_test, epochs=10, batch_size=32):
    """Bangun dan latih model neural network."""
    model = tf.keras.Sequential([
        tf.keras.layers.Dense(64, activation='relu', input_shape=(X_train.shape[1],)),
        tf.keras.layers.Dense(32, activation='relu'),
        tf.keras.layers.Dense(1, activation='sigmoid')
    ])

    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

    history = model.fit(X_train, y_train, epochs=epochs, batch_size=batch_size, validation_data=(X_test, y_test), verbose=2)

    predictions = (model.predict(X_test) > 0.5).astype(int)
    accuracy = accuracy_score(y_test, predictions)

    return model, history, accuracy

def evaluate_nn_model(model, test_data, test_labels):
    """Evaluasi model neural network menggunakan beberapa metrik."""
    predictions = (model.predict(test_data) > 0.5).astype(int)

    accuracy = accuracy_score(test_labels, predictions)
    cm = confusion_matrix(test_labels, predictions)
    classification_rep = classification_report(test_labels, predictions)

    return accuracy, cm, classification_rep

def plot_loss_curve(history):
    """Plot kurva loss selama pelatihan model."""
    loss = history.history['loss']
    val_loss = history.history['val_loss']
    
    epochs = range(1, len(loss) + 1)
    
    plt.figure(figsize=(8, 6))
    plt.plot(epochs, loss, 'bo', label='Training Loss')
    plt.plot(epochs, val_loss, 'b', label='Validation Loss')
    plt.title('Training and Validation Loss')
    plt.xlabel('Epochs')
    plt.ylabel('Loss')
    plt.legend()
    plt.show()

def plot_confusion_matrix(cm):
    """Plot confusion matrix."""
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", cbar=False)
    plt.title('Confusion Matrix')
    plt.xlabel('Predicted Labels')
    plt.ylabel('True Labels')
    plt.show()

def build_and_train_cnn_model(X_train, y_train, X_test, y_test, epochs=10, batch_size=32):
    """Bangun dan latih model Convolutional Neural Network (CNN)."""
    model = tf.keras.Sequential([
        tf.keras.layers.Conv2D(32, (3, 3), activation='relu', input_shape=(X_train.shape[1], X_train.shape[2], 1)),
        tf.keras.layers.MaxPooling2D((2, 2)),
        tf.keras.layers.Flatten(),
        tf.keras.layers.Dense(64, activation='relu'),
        tf.keras.layers.Dense(1, activation='sigmoid')
    ])

    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

    
    history = model.fit(X_train, y_train, epochs=epochs, batch_size=batch_size, validation_data=(X_test, y_test), verbose=2)

    predictions = (model.predict(X_test) > 0.5).astype(int)
    accuracy = accuracy_score(y_test, predictions)

    return model, history, accuracy

def plot_accuracy_curve(history):
    """Plot kurva akurasi selama pelatihan model."""
    accuracy = history.history['accuracy']
    val_accuracy = history.history['val_accuracy']
    
    epochs = range(1, len(accuracy) + 1)
    
    plt.figure(figsize=(8, 6))
    plt.plot(epochs, accuracy, 'bo', label='Training Accuracy')
    plt.plot(epochs, val_accuracy, 'b', label='Validation Accuracy')
    plt.title('Training and Validation Accuracy')
    plt.xlabel('Epochs')
    plt.ylabel('Accuracy')
    plt.legend()
    plt.show()

def build_and_train_rnn_model(X_train, y_train, X_test, y_test, epochs=10, batch_size=32):
    """Bangun dan latih model Recurrent Neural Network (RNN)."""
    model = tf.keras.Sequential([
        tf.keras.layers.Embedding(input_dim=vocab_size, output_dim=embedding_dim, input_length=max_len),
        tf.keras.layers.LSTM(64, return_sequences=True),
        tf.keras.layers.LSTM(32),
        tf.keras.layers.Dense(1, activation='sigmoid')
    ])

    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

    history = model.fit(X_train, y_train, epochs=epochs, batch_size=batch_size, validation_data=(X_test, y_test), verbose=2)

    predictions = (model.predict(X_test) > 0.5).astype(int)
    accuracy = accuracy_score(y_test, predictions)

    return model, history, accuracy


def other_function():
    pass
