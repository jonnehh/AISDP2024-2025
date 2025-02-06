import json
from ultralytics import YOLO

# Load the messages from the external JSON file
def load_class_messages(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def infer_yolo(image_path, class_messages):
    model = YOLO(f"C:/Users/divin/OneDrive/Desktop/Y3S2_projects/AISDP/Code/model_results/train/weights/best.pt")
    results = model.predict(source=image_path, imgsz=640, conf=0.6)
    
    # Access the class names from the model (model.names contains the mapping)
    class_names = model.names  # This is a dictionary mapping class IDs to class names
    
    for result in results:
        # Iterate through the detected objects
        for i, box in enumerate(result.boxes):
            class_id = int(box.cls[0])  # Get the class ID
            confidence = box.conf[0]    # Get the confidence score
            
            # Get the actual class name using the class_id
            class_name = class_names[class_id]
            
            # If the class name is in the dictionary, print the corresponding message
            if class_name in class_messages:
                print(class_messages[class_name])
            else:
                print(f"Detected class: {class_name} with confidence: {confidence:.2f}")
    
    result_image_path = "output.jpg"
    result.save(result_image_path)

if __name__ == "__main__":
    # Load the class messages from the JSON file
    CLASS_MESSAGES = load_class_messages('class_messages.json')

    TEST_IMAGE_PATH = "test.jpg"
    infer_yolo(TEST_IMAGE_PATH, CLASS_MESSAGES)
