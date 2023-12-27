# core/tensor_operations.py
import tensorflow as tf

def perform_tensor_operation(tensor):
    # Logika operasi tensor sederhana
    squared_tensor = tf.square(tensor)
    print("Tensor operation performed successfully.")
    return squared_tensor
