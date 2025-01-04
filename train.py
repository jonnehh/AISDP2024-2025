from ultralytics import YOLO

DATASET_PATH = "dataset"
MODEL_SAVE_PATH = "model_results"
DATA_YAML_PATH = "dataset/data.yaml"


def train_yolo():
    model = YOLO('yolo11s.pt')
    model.train(
        data=DATA_YAML_PATH,
        epochs=100,
        imgsz=640,
        project=MODEL_SAVE_PATH,
        batch=16,           # Batch size
        workers=4,          # Number of data loader workers
        optimizer='SGD',    # Optimizer (e.g., 'SGD', 'Adam', etc.)
        lr0=0.01,           # Initial learning rate
        momentum=0.937,     # Momentum for SGD
        weight_decay=0.0005, # Weight decay for regularization
        val=True,           # Perform validation during training
    )
    print("Done")

# Main workflow
if __name__ == "__main__":
    train_yolo()
