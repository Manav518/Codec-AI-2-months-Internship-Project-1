# Handwritten Digit Recognizer (CNN + MNIST)

A CNN that classifies handwritten digits (0-9) from the MNIST dataset, built with TensorFlow/Keras.

## Project Structure

```
mnist_digit_recognizer/
├── data_loader.py     # Downloads & preprocesses MNIST data
├── model.py            # Defines the CNN architecture
├── train.py             # Trains the model, saves it + training plots
├── evaluate.py         # Evaluates the trained model, generates reports/plots
├── predict.py           # Predicts the digit in a single custom image
├── requirements.txt   # Python dependencies
├── models/               # (created automatically) saved model + result plots
└── README.md
```

## Step-by-Step Setup

### 1. Install Python
Make sure you have Python 3.9–3.11 installed. Check with:
```bash
python3 --version
```

### 2. Create a virtual environment (recommended)
```bash
python3 -m venv venv
source venv/bin/activate        
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```
This installs TensorFlow, NumPy, Matplotlib, scikit-learn, and Pillow.

## Step-by-Step Usage

### Step 1 — Sanity check the data pipeline (optional)
```bash
python data_loader.py
```
This downloads MNIST (first run only, ~11MB, cached afterward) and prints the shapes:
```
Training data shape: (60000, 28, 28, 1)
Training labels shape: (60000, 10)
Test data shape: (10000, 28, 28, 1)
Test labels shape: (10000, 10)
Pixel value range: 0.0 to 1.0
```

### Step 2 — Inspect the model architecture (optional)
```bash
python model.py
```
Prints a full layer-by-layer summary of the CNN (Conv2D → BatchNorm → MaxPool → Dropout blocks, then a Dense classifier head).

### Step 3 — Train the model
```bash
python train.py
```
Optional flags:
```bash
python train.py --epochs 20 --batch-size 64 --augment
```
- `--epochs`: number of training passes (default 15)
- `--batch-size`: samples per gradient update (default 128)
- `--augment`: enables random rotation/shift/zoom augmentation for better generalization

This will:
- Train the CNN with early stopping (stops automatically if validation accuracy stops improving)
- Save the best-performing model to `models/mnist_cnn.h5`
- Save an accuracy/loss curve to `models/training_history.png`

Expect **~99% test accuracy** within 10–15 epochs on CPU (a few minutes) or under a minute on GPU.

### Step 4 — Evaluate the model
```bash
python evaluate.py
```
This will:
- Print overall test accuracy/loss
- Print a per-digit precision/recall/F1 classification report
- Save a confusion matrix to `models/confusion_matrix.png`
- Save a grid of sample predictions (green = correct, red = wrong) to `models/sample_predictions.png`

### Step 5 — Predict on your own handwritten digit
Draw a digit (e.g., in Paint/Preview, or take a photo of pen-on-paper), save it as a PNG/JPG, then run:
```bash
python predict.py --image path/to/your_digit.png
```
Example output:
```
Predicted Digit: 7
Confidence: 98.42%

Full probability distribution:
  0:  0.01% 
  1:  0.02% 
  ...
  7: 98.42% ########################################
  ...
```
The script auto-handles grayscale conversion, resizing to 28x28, and color inversion (so both "black digit on white paper" and "white digit on black background" work).

## How It Works (Concepts)

- **Convolutional layers (Conv2D):** slide small filters over the image to detect patterns like edges and curves.
- **Batch Normalization:** stabilizes and speeds up training by normalizing layer inputs.
- **MaxPooling:** downsamples feature maps, keeping the strongest signals and reducing computation.
- **Dropout:** randomly disables neurons during training to prevent overfitting.
- **Dense (fully connected) layers:** combine the learned features to make the final classification.
- **Softmax output:** converts the final layer into a probability distribution over the 10 digit classes.

## Troubleshooting

- **"No trained model found" error in evaluate.py/predict.py:** run `python train.py` first — it creates `models/mnist_cnn.h5`.
- **Low accuracy on your own handwritten images:** make sure the digit is roughly centered, fills most of the frame, and has good contrast against the background.
- **Slow training:** if you have a GPU, TensorFlow will use it automatically if `tensorflow` (not `tensorflow-cpu`) is installed with proper CUDA/cuDNN drivers.

## Possible Extensions
- Add a simple web UI (Flask/Streamlit) with a drawable canvas for live predictions.
- Try deeper architectures (ResNet-style blocks) or transfer learning.
- Deploy the model as a REST API.
