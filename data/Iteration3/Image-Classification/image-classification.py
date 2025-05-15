import tensorflow as tf
from tensorflow.keras.utils import load_img, img_to_array
import numpy as np

# --- Make sure these are defined or loaded ---
# Example values, use the ones from your training
IMG_HEIGHT = 224
IMG_WIDTH = 224
class_names = [
    'Cardboard', 'Food Organics', 'Glass', 'Metal',
    'Miscellaneous Trash', 'Paper', 'Plastic', 'Textile Trash', 'Vegetation'
] # Ensure this matches your trained model's classes in order

# Load your trained model
model_path = "EfficientNetB0_best.keras" # Or whatever you named it
model = tf.keras.models.load_model(model_path)
print(f"Model loaded from {model_path}")

def preprocess_single_image(image_path):
    img = load_img(image_path, target_size=(IMG_HEIGHT, IMG_WIDTH))
    img_array = img_to_array(img)  # Converts to float32 numpy array, values 0-255
    img_array = tf.expand_dims(img_array, 0)  # Create a batch: (1, height, width, channels)
    # DO NOT call preprocess_input here if it's already in the model
    return img_array

# Example Usage:
new_image_path = 'plasticBottle1.jpg' # <--- CHANGE THIS TO AN ACTUAL IMAGE PATH
if not tf.io.gfile.exists(new_image_path):
    print(f"Error: Image file not found at {new_image_path}")
    print("Please provide a valid path to an image for prediction.")
else:
    preprocessed_img = preprocess_single_image(new_image_path)
    predictions = model.predict(preprocessed_img)
    predicted_class_index = np.argmax(predictions[0])
    predicted_class_name = class_names[predicted_class_index]
    confidence = np.max(predictions[0]) * 100 # As percentage

    print(f"Predicted class: {predicted_class_name} with confidence: {confidence:.2f}%")