import os
from PIL import Image
 
def batch_ocr(input_dir, output_dir):
    from paddleocr import PaddleOCR, draw_ocr
 
    ocr = PaddleOCR(det_model_dir='inference_model/det',rec_model_dir='inference_model/rec', use_angle_cls=True, use_gpu=False, lang='en')

    for filename in os.listdir(input_dir):
        if filename.endswith('.jpg') or filename.endswith('.jpeg') or filename.endswith('.png'):
            img_path = os.path.join(input_dir, filename)
 

            result = ocr.ocr(img_path, cls=True)[0]
 
            # 获取识别结果的坐标、文本和置信度
            boxes = [line[0] for line in result]
            txts = [line[1][0] for line in result]
            scores = [line[1][1] for line in result]
 
            # 读取原始图片
            image = Image.open(img_path).convert('RGB')
 
            # 在原始图片上绘制识别结果
            im_show = draw_ocr(image, boxes, txts, scores, font_path='doc/fonts/simfang.ttf')
            im_show = Image.fromarray(im_show)
 
            # 保存绘制结果的图片
            output_path = os.path.join(output_dir, filename)
            im_show.save(output_path)
 
 
if __name__ == '__main__':
    # Ocr()
    input_dir = r'text_img/Eval_img'
    output_dir = r'text_img/result_img'
 
    batch_ocr(input_dir, output_dir)