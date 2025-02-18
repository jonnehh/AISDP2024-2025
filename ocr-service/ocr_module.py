import os
from paddleocr import PaddleOCR
from PIL import Image
from io import BytesIO
import base64

os.environ['FLAGS_enable_ir_optim'] = 'false'
# 初始化 OCR
ocr = PaddleOCR(det_model_dir='inference_model/det', rec_model_dir='inference_model/rec', use_angle_cls=True, use_gpu=False, lang='en')

# 上传和结果文件夹
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def process_image(base64_image):
    """处理 Base64 图像并进行 OCR"""
    # 解码 Base64 图片
    image_data = base64.b64decode(base64_image.split(',')[1])
    image = Image.open(BytesIO(image_data))

    # 保存图片
    img_path = os.path.join(UPLOAD_FOLDER, "captured_image.jpg")
    image.save(img_path)

    # OCR 识别
    result = ocr.ocr(img_path, cls=True)[0]
    text_results = [line[1][0] for line in result]

    return text_results
