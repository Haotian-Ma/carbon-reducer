# predict_with_yolo_classifier.py
from ultralytics import YOLO
from PIL import Image 
import os
import torch 

def run_inference(model_path, image_source):
    """
    Runs inference using a trained YOLO classification model.

    Args:
        model_path (str): Path to the trained .pt model file (e.g., 'path/to/best.pt').
        image_source (str): Path to a single image, a directory of images, or a video file.
    """

    # --- Device Check (Optional but good practice) ---
    if torch.cuda.is_available():
        device_name = torch.cuda.get_device_name(0)
        print(f"CUDA is available. Using GPU: {device_name} for inference.")
        device = 'cuda' # or 0 for the first GPU
    else:
        print("CUDA not available. Using CPU for inference (this might be slower).")
        device = 'cpu'

    # 1. Load your trained model
    try:
        print(f"Loading model from: {model_path}")
        model = YOLO(model_path)
        model.to(device) # Move model to the selected device
        print("Model loaded successfully.")
    except Exception as e:
        print(f"Error loading model: {e}")
        return

    # 2. Perform prediction
    print(f"Running prediction on: {image_source}")
    try:
        results = model.predict(source=image_source, stream=False, save=False, conf=0.25, device=device)
        print("Prediction complete.")
    except Exception as e:
        print(f"Error during prediction: {e}")
        return

    # 3. Process and display results
    for i, r in enumerate(results):
        print(f"\n--- Results for Image/Frame {i+1} ---")
        if r.path: # Path of the input image
            print(f"Source: {r.path}")

        if r.probs is not None:
            top1_index = r.probs.top1
            top1_confidence = r.probs.top1conf.item() # .item() to get Python number from tensor
            predicted_class_name = r.names[top1_index]

            print(f"  Predicted Class: {predicted_class_name}")
            print(f"  Confidence: {top1_confidence:.4f}")

        else:
            print("  No probabilities found in the result object.")

       # Display the image (optional)
        if r.orig_img is not None:
            img = Image.fromarray(r.orig_img[..., ::-1]) # Convert BGR to RGB
            img.show() # Display the image
        print("---------------------------------")

if __name__ == '__main__':
    # --- CONFIGURATION ---
    # 1. Set the path to your trained model
    MODEL_PATH = 'models/best-large.pt' 

    # 2. Set the path to the image(s) or video you want to predict on
    IMAGE_OR_VIDEO_SOURCE = 'test6.jpg' # <<< CHANGE THIS
    # ---------------------

    if not os.path.exists(MODEL_PATH):
        print(f"ERROR: Model file not found at '{MODEL_PATH}'")
        print("Please update MODEL_PATH to the correct location of your 'best.pt' file.")
    elif not os.path.exists(IMAGE_OR_VIDEO_SOURCE) and not IMAGE_OR_VIDEO_SOURCE.startswith(('http', 'rtsp', 'screen')):
        print(f"ERROR: Image/video source not found at '{IMAGE_OR_VIDEO_SOURCE}'")
        print("Please update IMAGE_OR_VIDEO_SOURCE to a valid image, directory, or video.")
    else:
        run_inference(MODEL_PATH, IMAGE_OR_VIDEO_SOURCE)