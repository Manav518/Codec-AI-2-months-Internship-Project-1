import argparse
import os

import matplotlib.pyplot as plt
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
from tensorflow.keras.preprocessing.image import ImageDataGenerator

from data_loader import get_prepared_data
from model import build_cnn_model

MODELS_DIR = "models"


def parse_args():
    parser = argparse.ArgumentParser(description="Train MNIST CNN classifier")
    parser.add_argument("--epochs", type=int, default=15,
                         help="Number of training epochs (default: 15)")
    parser.add_argument("--batch-size", type=int, default=128,
                         help="Training batch size (default: 128)")
    parser.add_argument("--augment", action="store_true",
                         help="Enable data augmentation (rotation/shift/zoom)")
    return parser.parse_args()


def plot_training_history(history, save_path):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))

    ax1.plot(history.history["accuracy"], label="Train Accuracy")
    ax1.plot(history.history["val_accuracy"], label="Val Accuracy")
    ax1.set_title("Model Accuracy")
    ax1.set_xlabel("Epoch")
    ax1.set_ylabel("Accuracy")
    ax1.legend()
    ax1.grid(alpha=0.3)

    ax2.plot(history.history["loss"], label="Train Loss")
    ax2.plot(history.history["val_loss"], label="Val Loss")
    ax2.set_title("Model Loss")
    ax2.set_xlabel("Epoch")
    ax2.set_ylabel("Loss")
    ax2.legend()
    ax2.grid(alpha=0.3)

    plt.tight_layout()
    plt.savefig(save_path)
    print(f"Saved training history plot to: {save_path}")


def main():
    args = parse_args()
    os.makedirs(MODELS_DIR, exist_ok=True)

    print("Loading and preprocessing MNIST data...")
    x_train, y_train, x_test, y_test = get_prepared_data()
    print(f"Train samples: {x_train.shape[0]}, Test samples: {x_test.shape[0]}")

    print("Building CNN model...")
    model = build_cnn_model()
    model.summary()

    checkpoint_path = os.path.join(MODELS_DIR, "mnist_cnn.h5")
    callbacks = [
        ModelCheckpoint(checkpoint_path, monitor="val_accuracy",
                         save_best_only=True, verbose=1),
        EarlyStopping(monitor="val_accuracy", patience=4,
                       restore_best_weights=True, verbose=1),
    ]

    if args.augment:
        print("Data augmentation enabled.")
        datagen = ImageDataGenerator(
            rotation_range=10,
            width_shift_range=0.1,
            height_shift_range=0.1,
            zoom_range=0.1,
        )
        datagen.fit(x_train)
        history = model.fit(
            datagen.flow(x_train, y_train, batch_size=args.batch_size),
            epochs=args.epochs,
            validation_data=(x_test, y_test),
            callbacks=callbacks,
        )
    else:
        history = model.fit(
            x_train, y_train,
            batch_size=args.batch_size,
            epochs=args.epochs,
            validation_data=(x_test, y_test),
            callbacks=callbacks,
        )

    plot_training_history(history, os.path.join(MODELS_DIR, "training_history.png"))

    final_loss, final_acc = model.evaluate(x_test, y_test, verbose=0)
    print(f"\nFinal Test Accuracy: {final_acc * 100:.2f}%")
    print(f"Final Test Loss: {final_loss:.4f}")
    print(f"Model saved to: {checkpoint_path}")


if __name__ == "__main__":
    main()
