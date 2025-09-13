from tensorflow.keras.models import load_model

# Load the model
model = load_model("chess_model.h5", compile=False)

# Print the model architecture to understand its structure
model.summary()