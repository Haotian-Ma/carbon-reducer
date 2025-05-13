import cv2
import numpy as np
from ultralytics import YOLO
import matplotlib.pyplot as plt
import os

def run_yolo_detection():
    # 1. Install ultralytics if not already installed
    # Uncomment the line below if you need to install it
    # !pip install ultralytics
    
    # 2. Load a pre-trained YOLO model 
    model = YOLO('models/best-2.pt')  # Downloads the model
    
    # 3. Choose an image for detection 
    image_path = 'plasticBottle1.jpg'  # Image path
    
    # Check if the file exists
    if not os.path.exists(image_path):
        print(f"Image file not found at {image_path}")
        print("Please provide a valid image path.")
        return
    
    # 4. Run object detection
    results = model(image_path)
    
    # 5. Process and display results
    for result in results:
        # Convert result to numpy array for easier handling
        boxes = result.boxes.xyxy.cpu().numpy()  # Get bounding boxes
        classes = result.boxes.cls.cpu().numpy()  # Get class indices
        scores = result.boxes.conf.cpu().numpy()  # Get confidence scores
        
        # Get class names
        class_names = result.names
        
        # Load the image for visualization
        img = cv2.imread(image_path)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # Convert BGR to RGB
        
        # Draw bounding boxes and labels
        for box, cls_id, score in zip(boxes, classes, scores):
            x1, y1, x2, y2 = box.astype(int)
            class_name = class_names[int(cls_id)]
            label = f"{class_name} {score:.2f}"
            
            # Draw rectangle
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            
            # Add label
            cv2.putText(img, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 
                        0.5, (0, 255, 0), 2)
        
        # Save the result
        output_path = 'detection_result.jpg'
        plt.figure(figsize=(10, 8))
        plt.imshow(img)
        plt.axis('off')
        plt.tight_layout()
        plt.savefig(output_path)
        plt.show()
        
        print(f"Detection result saved to {output_path}")
        
        # Print detected objects
        print("\nDetected objects:")
        for cls_id, score in zip(classes, scores):
            print(f"{class_names[int(cls_id)]}: {score:.2f}")

if __name__ == "__main__":
    run_yolo_detection()