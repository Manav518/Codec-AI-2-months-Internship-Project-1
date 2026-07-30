import argparse
import os

import numpy as np
from PIL import Image, ImageOps
from tensorflow.keras.models import load_model

MODEL_PATH = os.path.join("models", "mnist_cnn.h5")


def parse_args():
    parser = argparse.ArgumentParser(description="Predict a digit from an image file")
    parser.add_argument("--image", type=str, required=True,
                         help="Path to the input image (png/jpg)")
    return parser.parse_args()


def preprocess_image(image_path, save_debug_path="models/last_preprocessed.png"):
    img = Image.open(image_path).convert("L")  

    img_array = np.array(img).astype("float32")
    if img_array.mean() > 127:
        img_array = 255 - img_array

    threshold = 60
    img_array = np.where(img_array > threshold, 255.0, 0.0)

    coords = np.argwhere(img_array > 0)
    if coords.size == 0:
        raise ValueError(
            "No digit detected in the image. Make sure the digit has good "
            "contrast against the background."
        )
    y0, x0 = coords.min(axis=0)
    y1, x1 = coords.max(axis=0) + 1
    digit = img_array[y0:y1, x0:x1]

    digit_img = Image.fromarray(digit.astype("uint8"))
    h, w = digit.shape
    scale = 20.0 / max(h, w)
    new_h, new_w = max(1, int(h * scale)), max(1, int(w * scale))
    digit_img = digit_img.resize((new_w, new_h))

    canvas = Image.new("L", (28, 28), color=0)
    paste_x = (28 - new_w) // 2
    paste_y = (28 - new_h) // 2
    canvas.paste(digit_img, (paste_x, paste_y))

    os.makedirs(os.path.dirname(save_debug_path), exist_ok=True)
    canvas.save(save_debug_path)
    print(f"Saved preprocessed (model-view) image to: {save_debug_path}")

    final_array = np.array(canvas).astype("float32") / 255.0
    final_array = final_array.reshape(1, 28, 28, 1)
    return final_array


def main():
    args = parse_args()

    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(
            f"No trained model found at '{MODEL_PATH}'. Run train.py first."
        )
    if not os.path.exists(args.image):
        raise FileNotFoundError(f"Image not found: {args.image}")

    print(f"Loading model from: {MODEL_PATH}")
    model = load_model(MODEL_PATH)

    print(f"Preprocessing image: {args.image}")
    processed = preprocess_image(args.image)

    predictions = model.predict(processed, verbose=0)[0]
    predicted_digit = int(np.argmax(predictions))
    confidence = float(predictions[predicted_digit]) * 100

    print(f"\nPredicted Digit: {predicted_digit}")
    print(f"Confidence: {confidence:.2f}%")
    print("\nFull probability distribution:")
    for digit, prob in enumerate(predictions):
        bar = "#" * int(prob * 40)
        print(f"  {digit}: {prob * 100:5.2f}% {bar}")


if __name__ == "__main__":
    main()