import os
from ultralytics import YOLO

# 1. Set paths for the dataset and model
DATASET_PATH = "dataset"
MODEL_SAVE_PATH = "model_results"

# dataset_yaml config
# train: dataset/images/train
# val: dataset/images/val

# nc: 10
# names: ['Chicken Rice', 'Fish Porridge', 'Char Siew Rice', 'Mee Siam', 
#         'Bak Kut Teh', 'Chwee Kueh', 'Yong Tau Foo', 'Steamed Fish', 
#         'Ngoh Hiang', 'Kueh']

DATA_YAML_PATH = "dataset/data.yaml"

# 3. Train YOLO model
def train_yolo():
    model = YOLO('yolo11s.pt')
    model.train(
        data=DATA_YAML_PATH,
        epochs=100,
        imgsz=640,
        project=MODEL_SAVE_PATH
    )
    print("Done")

# 4. Run inference
def infer_yolo(image_path):
    print(f"Running inference on {image_path}...")
    model = YOLO(f"{MODEL_SAVE_PATH}/weights/best.pt")
    results = model.predict(source=image_path, imgsz=640, conf=0.6)
    for result in results:
        print(result.boxes)
    result_image_path = "output.jpg"
    result.render()
    result.save(result_image_path)
    print(f"Results saved to {result_image_path}")

# Main workflow
if __name__ == "__main__":
    train_yolo()
    
    # TEST_IMAGE_PATH = "test_image.jpg"
    # infer_yolo(TEST_IMAGE_PATH)
