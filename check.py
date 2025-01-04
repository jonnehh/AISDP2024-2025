import torch
print(torch.cuda.is_available())
print(torch.cuda.get_device_name(0))  # Optional: Get GPU name

from torchvision.ops import nms

boxes = torch.tensor([[0, 0, 10, 10], [1, 1, 11, 11]], device='cuda')
scores = torch.tensor([0.8, 0.9], device='cuda')
iou_threshold = 0.5

try:
    indices = nms(boxes, scores, iou_threshold)
    print("NMS indices:", indices)
except Exception as e:
    print("Error:", e)
