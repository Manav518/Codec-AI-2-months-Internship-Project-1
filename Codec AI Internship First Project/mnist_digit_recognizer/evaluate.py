import os

import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix, classification_report
from tensorflow.keras.models import load_model

from data_loader import get_prepared_data

MODEL_PATH = os.path.join("models", "mnist_cnn.h5")
MODELS_DIR = "models"


def plot_confusion_matrix(cm, save_path):
    fig, ax = plt.subplots(figsize=(8, 8))
    im = ax.imshow(cm, cmap="Blues")
    ax.set_title("Confusion Matrix")
    ax.set_xlabel("Predicted Label")
    ax.set_ylabel("True Label")
    ax.set_xticks(range(10))
    ax.set_yticks(range(10))
    fig.colorbar(im)

    for i in range(cm.shape[0]):
        for j in range(cm.shape[1]):
            ax.text(j, i, str(cm[i, j]), ha="center", va="center",
                     color="white" if cm[i, j] > cm.max() / 2 else "black",
                     fontsize=8)

    plt.tight_layout()
    plt.savefig(save_path)
    print(f"Saved confusion matrix to: {save_path}")


def plot_sample_predictions(x_test, y_true, y_pred, save_path, n=16):
    fig, axes = plt.subplots(4, 4, figsize=(8, 8))
    indices = np.random.choice(len(x_test), n, replace=False)

    for ax, idx in zip(axes.flat, indices):
        ax.imshow(x_test[idx].reshape(28, 28), cmap="gray")
        correct = y_true[idx] == y_pred[idx]
        color = "green" if correct else "red"
        ax.set_title(f"True: {y_true[idx]} Pred: {y_pred[idx]}",
                     color=color, fontsize=9)
        ax.axis("off")

    plt.tight_layout()
    plt.savefig(save_path)
    print(f"Saved sample predictions grid to: {save_path}")


def main():
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(
            f"No trained model found at '{MODEL_PATH}'. Run train.py first."
        )

    print("Loading test data...")
    _, _, x_test, y_test = get_prepared_data()

    print(f"Loading trained model from: {MODEL_PATH}")
    model = load_model(MODEL_PATH)

    print("Evaluating on test set...")
    loss, accuracy = model.evaluate(x_test, y_test, verbose=0)
    print(f"Test Accuracy: {accuracy * 100:.2f}%")
    print(f"Test Loss: {loss:.4f}")

    y_pred_probs = model.predict(x_test, verbose=0)
    y_pred = np.argmax(y_pred_probs, axis=1)
    y_true = np.argmax(y_test, axis=1)

    print("\nClassification Report:")
    print(classification_report(y_true, y_pred, digits=4))

    cm = confusion_matrix(y_true, y_pred)
    plot_confusion_matrix(cm, os.path.join(MODELS_DIR, "confusion_matrix.png"))
    plot_sample_predictions(x_test, y_true, y_pred,
                             os.path.join(MODELS_DIR, "sample_predictions.png"))


if __name__ == "__main__":
    main()
