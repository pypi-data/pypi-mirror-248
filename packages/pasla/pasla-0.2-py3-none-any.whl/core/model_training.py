# core/model_training.py
import numpy as np
import pandas as pd
import tensorflow as tf
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, roc_auc_score, roc_curve
import matplotlib.pyplot as plt
import seaborn as sns

def train_random_forest_classifier(data, labels, test_size=0.2, random_state=42, n_estimators=100):
    X_train, X_test, y_train, y_test = train_test_split(data, labels, test_size=test_size, random_state=random_state)

    model = RandomForestClassifier(n_estimators=n_estimators, random_state=random_state)
    model.fit(X_train, y_train)

    predictions = model.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)

    return model, accuracy

def evaluate_model(model, test_data, test_labels):
    predictions = model.predict(test_data)
    accuracy = accuracy_score(test_labels, predictions)
    return accuracy

def save_model(model, filename="model.pkl"):
    import joblib
    joblib.dump(model, filename)

def load_model(filename="model.pkl"):
    import joblib
    return joblib.load(filename)

def cross_validate_model(model, data, labels, cv=5):
    scores = cross_val_score(model, data, labels, cv=cv)
    return scores.mean()

def generate_classification_report(model, test_data, test_labels):
    predictions = model.predict(test_data)
    classification_rep = classification_report(test_labels, predictions)
    return classification_rep

def generate_confusion_matrix(model, test_data, test_labels):
    predictions = model.predict(test_data)
    cm = confusion_matrix(test_labels, predictions)
    return cm

def plot_feature_importance(model, feature_names):
    feature_importances = model.feature_importances_
    sorted_idx = feature_importances.argsort()[::-1]
    
    plt.figure(figsize=(10, 6))
    sns.barplot(x=feature_importances[sorted_idx], y=feature_names[sorted_idx])
    plt.title('Feature Importance')
    plt.xlabel('Importance')
    plt.ylabel('Feature')
    plt.show()

def train_neural_network(data, labels, test_size=0.2, random_state=42, epochs=10, batch_size=32):
    X_train, X_test, y_train, y_test = train_test_split(data, labels, test_size=test_size, random_state=random_state)

    model = tf.keras.Sequential([
        tf.keras.layers.Dense(64, activation='relu', input_shape=(X_train.shape[1],)),
        tf.keras.layers.Dense(32, activation='relu'),
        tf.keras.layers.Dense(1, activation='sigmoid')
    ])

    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

    history = model.fit(X_train, y_train, epochs=epochs, batch_size=batch_size, validation_data=(X_test, y_test), verbose=2)

    return model, history

def evaluate_neural_network(model, test_data, test_labels):
    predictions = model.predict(test_data)
    predictions = (predictions > 0.5).astype(int)

    accuracy = accuracy_score(test_labels, predictions)
    auc_score = roc_auc_score(test_labels, predictions)

    return accuracy, auc_score

def plot_roc_curve(model, test_data, test_labels):
    predictions = model.predict(test_data)
    fpr, tpr, thresholds = roc_curve(test_labels, predictions)
    
    plt.figure(figsize=(8, 6))
    plt.plot(fpr, tpr, label='ROC Curve')
    plt.plot([0, 1], [0, 1], linestyle='--', label='Random')
    plt.title('Receiver Operating Characteristic (ROC) Curve')
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.legend()
    plt.show()

def plot_loss_curve(history):
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

def save_model_weights(model, filename="model_weights.h5"):
    model.save_weights(filename)

def load_model_weights(model, filename="model_weights.h5"):
    model.load_weights(filename)

def save_history(history, filename="training_history.csv"):
    history_df = pd.DataFrame(history.history)
    history_df.to_csv(filename, index=False)

def load_history(filename="training_history.csv"):
    history_df = pd.read_csv(filename)
    return history_df.to_dict('records')

def plot_confusion_matrix(model, test_data, test_labels, normalize=False):
    predictions = model.predict(test_data)
    cm = confusion_matrix(test_labels, (predictions > 0.5).astype(int))
    
    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]

    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt=".2f" if normalize else "d", cmap="Blues", cbar=False)
    plt.title('Confusion Matrix')
    plt.xlabel('Predicted Labels')
    plt.ylabel('True Labels')
    plt.show()

def feature_importance_table(model, feature_names):
    feature_importances = model.feature_importances_
    sorted_idx = feature_importances.argsort()[::-1]
    
    data = {'Feature': feature_names[sorted_idx], 'Importance': feature_importances[sorted_idx]}
    df = pd.DataFrame(data)
    return df
