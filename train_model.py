from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
import numpy as np

# Define the new 5-7 layer model
model = Sequential([
    Dense(256, activation='relu', input_shape=(768,)),  # Input layer with 256 neurons
    Dropout(0.2),  # Dropout for regularization
    Dense(128, activation='relu'),  # Hidden layer with 128 neurons
    Dropout(0.2),  # Dropout for regularization
    Dense(64, activation='relu'),  # Hidden layer with 64 neurons
    Dense(32, activation='relu'),  # Hidden layer with 32 neurons
    Dense(1, activation='linear')  # Output layer with 1 neuron
])

# Compile the model
model.compile(optimizer='adam', loss='mse', metrics=['mae'])

# Print the model summary
model.summary()

# Load your training data
# Replace these with your actual training data
training_data = np.random.rand(1000, 768)  # Example: 1000 samples, 768 features
training_labels = np.random.rand(1000)  # Example: 1000 labels

# Train the model
model.fit(training_data, training_labels, epochs=10, batch_size=32, validation_split=0.2)

# Save the trained model
model.save("chess_model_complex.h5")