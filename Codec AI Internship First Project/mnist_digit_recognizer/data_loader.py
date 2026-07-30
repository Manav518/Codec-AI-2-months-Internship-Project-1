import numpy as np
from tensorflow.keras.datasets import mnist
from tensorflow.keras.utils import to_categorical


def load_data():
    (x_train, y_train), (x_test, y_test) = mnist.load_data()
    return (x_train, y_train), (x_test, y_test)


def preprocess_data(x_train, y_train, x_test, y_test, num_classes=10):
    x_train = x_train.reshape(-1, 28, 28, 1).astype("float32")
    x_test = x_test.reshape(-1, 28, 28, 1).astype("float32")

    x_train /= 255.0
    x_test /= 255.0

    y_train = to_categorical(y_train, num_classes)
    y_test = to_categorical(y_test, num_classes)

    return x_train, y_train, x_test, y_test


def get_prepared_data():
    (x_train, y_train), (x_test, y_test) = load_data()
    return preprocess_data(x_train, y_train, x_test, y_test)


if __name__ == "__main__":

    x_train, y_train, x_test, y_test = get_prepared_data()
    print("Training data shape:", x_train.shape)   
    print("Training labels shape:", y_train.shape)  
    print("Test data shape:", x_test.shape)          
    print("Test labels shape:", y_test.shape)        
    print("Pixel value range:", x_train.min(), "to", x_train.max())
