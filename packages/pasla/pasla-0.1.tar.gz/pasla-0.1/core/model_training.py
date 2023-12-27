# core/model_training.py
import tensorflow as tf

def train_model(data, labels, epochs=10):
# model neural network
    model = tf.keras.Sequential([
        tf.keras.layers.Dense(64, activation='relu', input_shape=(data.shape[1],)),
        tf.keras.layers.Dense(10, activation='softmax')
    ])

    model.compile(optimizer='pasla', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
    model.fit(data, labels, epochs=epochs)
    
    print("Model trained successfully.")
    return model
