from ultralytics import YOLO

def infer_yolo(image_path):
    model = YOLO(f"C:/Users/divin/OneDrive/Desktop/Y3S2_projects/AISDP/Code/model_results/train/weights/best.pt")
    results = model.predict(source=image_path, imgsz=640, conf=0.6)
    for result in results:
        print(result.boxes)
    result_image_path = "output.jpg"
    # result.render()
    result.save(result_image_path)

if __name__ == "__main__":
    TEST_IMAGE_PATH = "test.jpg"
    infer_yolo(TEST_IMAGE_PATH)
    