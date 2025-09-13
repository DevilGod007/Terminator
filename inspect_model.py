# Add this at the top if you see "Import 'tensorflow' could not be resolved" in your editor:
# Try running: pip install tensorflow

import tensorflow as tf

def inspect_model(model):
    for layer in model.layers:
        print(f"Name: {layer.name}")
        print(f"Type: {layer.__class__.__name__}")
        # Some layers may not have input_shape/output_shape attributes until built
        input_shape = getattr(layer, "input_shape", "N/A")
        output_shape = getattr(layer, "output_shape", "N/A")
        print(f"Input shape: {input_shape}")
        print(f"Output shape: {output_shape}")
        activation = getattr(layer, "activation", None)
        if activation is not None:
            # If activation is a function, get its name
            activation = getattr(activation, "__name__", str(activation))
        else:
            activation = "N/A"
        print(f"Activation: {activation}")
        print("-" * 30)

if __name__ == "__main__":
    import sys
    import os
    from tensorflow.keras.utils import plot_model

    # Usage: python inspect_model.py path_to_model.h5
    if len(sys.argv) < 2:
        print("Usage: python inspect_model.py path_to_model.h5")
        sys.exit(1)

    model_path = sys.argv[1]
    model = tf.keras.models.load_model(model_path, compile=False)
    inspect_model(model)

    # Save model plot
    try:
        plot_model(model, to_file="model.png", show_shapes=True, show_layer_names=True)
        print("Model plot saved as model.png")
    except Exception as e:
        print(f"Could not plot model: {e}")
        print("To enable model plotting, install Graphviz and add it to your PATH. See: https://graphviz.gitlab.io/download/")
