import os
from ultralytics import YOLO
import cv2 # OpenCV for image handling (optional, but useful)

def run_inference(model_path, source_path, confidence_threshold=0.6, save_dir='runs/detect/predictions'):
    """
    Runs YOLOv11 inference on a given source (image, directory, or video).

    Args:
        model_path (str): Path to the trained YOLOv11 model (.pt file).
        source_path (str): Path to the input image, directory of images, or video file.
                           Use '0' for webcam.
        confidence_threshold (float): Minimum confidence score for detected objects (0.0 to 1.0).
        save_dir (str): Directory where prediction results (images/videos with boxes) will be saved.
    """
    print(f"Loading model from: {model_path}")
    print(f"Running inference on: {source_path}")

    # --- Input Validation (Optional but Recommended) ---
    if not os.path.exists(model_path):
        print(f"Error: Model file not found at {model_path}")
        return
    # For non-webcam sources, check if the path exists
    if source_path != '0' and not os.path.exists(source_path):
        print(f"Error: Source path not found at {source_path}")
        return

    # --- Load the trained YOLOv11 model ---
    try:
        model = YOLO(model_path)
        print("Model loaded successfully.")
    except Exception as e:
        print(f"Error loading model: {e}")
        return

    # --- Run Prediction ---
    # The model.predict() method handles different source types automatically.
    # It returns a list of Results objects (one per image/frame).
    # You can customize prediction with arguments like:
    #   conf: confidence threshold
    #   iou: IoU threshold for NMS (Non-Maximum Suppression)
    #   imgsz: image size for inference (e.g., 640)
    #   save: Set to True to automatically save annotated images/videos
    #   save_txt: Set to True to save results in YOLO label format (.txt files)
    #   save_conf: Set to True to include confidence scores in saved .txt files
    #   show: Set to True to display results in a popup window (good for quick tests)
    #   project: Name for the parent directory of saved results (defaults to 'runs/detect')
    #   name: Name for the specific run directory (defaults to 'predict', 'predict2', etc.)

    try:
        results_list = model.predict(
            source=source_path,
            conf=confidence_threshold,
            save=True,             # Save images/video with bounding boxes
            save_txt=True,         # Save detection results as text files
            save_conf=True,        # Include confidence in the text files
            project=os.path.dirname(save_dir), # Use the parent dir of save_dir as project
            name=os.path.basename(save_dir),   # Use the last part of save_dir as the run name
            exist_ok=True          # Overwrite existing predictions in the save_dir if it exists
            # show=True            # Uncomment to display results in a window (blocks script execution until closed)
        )
        print(f"Prediction complete. Results saved to: {save_dir}")

        # --- (Optional) Process Results Programmatically ---
        # If you need to access bounding box data, confidences, classes etc., in your code:
        print("\n--- Detailed Detection Results ---")
        for i, results in enumerate(results_list): # results_list contains results for each image/frame
            print(f"\nResults for image/frame {i+1}:")
            img_path = results.path if results.path else f"frame_{i+1}" # Get image path or frame number
            print(f"  Source: {img_path}")
            print(f"  Detected {len(results.boxes)} objects.")

            # Access boxes information
            for box in results.boxes:
                # Get coordinates (xyxy format: top-left x, top-left y, bottom-right x, bottom-right y)
                coords = box.xyxy[0].tolist()
                # Get confidence score
                confidence = box.conf[0].item() # Use .item() to get Python float
                # Get class ID
                class_id = int(box.cls[0].item()) # Use .item() and cast to int
                # Get class name using the model's names dictionary
                class_name = model.names[class_id]

                print(f"    - Class: {class_name} (ID: {class_id}), Confidence: {confidence:.4f}, Box: {coords}")

            # You can also access the annotated image as a NumPy array if needed:
            # annotated_image_numpy = results.plot() # Returns BGR NumPy array
            # cv2.imshow("Annotated Image", annotated_image_numpy)
            # cv2.waitKey(0) # Wait for key press (if displaying images one by one)

    except Exception as e:
        print(f"Error during prediction: {e}")

    # cv2.destroyAllWindows() # Close any OpenCV windows if you used cv2.imshow

if __name__ == '__main__':
    # --- Configuration ---
    # IMPORTANT: Change these paths to match your setup!
    MODEL_WEIGHTS_PATH = 'runs/detect/train2/weights/last.pt' # <-- CHANGE THIS
    # SOURCE can be an image file, a directory of images, a video file, or '0' for webcam
    SOURCE_INPUT_PATH = 'can.jpg' 
    CONFIDENCE = 0.6  # Adjust based on how sensitive you want the detection to be
    SAVE_DIRECTORY = 'predictions' # Directory to save annotated outputs

    # --- Run the function ---
    run_inference(
        model_path=MODEL_WEIGHTS_PATH,
        source_path=SOURCE_INPUT_PATH,
        confidence_threshold=CONFIDENCE,
        save_dir=SAVE_DIRECTORY
    )

    print("Script finished.")