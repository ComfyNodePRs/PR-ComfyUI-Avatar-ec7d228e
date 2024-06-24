from PIL import Image, ImageDraw
import torch
import numpy as np
import pandas as pd 
import os
import cv2
import matplotlib.pyplot as plt

# Tensor to PIL
def tensor2pil(image):
    return Image.fromarray(np.clip(255. * image.cpu().numpy().squeeze(), 0, 255).astype(np.uint8))

# Convert PIL to Tensor
def pil2tensor(image):
    return torch.from_numpy(np.array(image).astype(np.float32) / 255.0).unsqueeze(0)

def resize_and_crop_to_circle(image, size):
    # 创建一个新的图片，背景为透明
    output_image = Image.new('RGBA', image.size, (0, 0, 0, 0))
    # 缩放图像到指定尺寸
    image = image.resize((size, size))
    
    # 创建一个圆形蒙版
    mask = Image.new("L", (size, size), 0)
    draw = ImageDraw.Draw(mask)
    radius = size // 2
    draw.ellipse((0, 0, size, size), fill=255)  # 绘制圆形蒙版
    
    # 使用蒙版裁剪图像
    image = image.convert("RGBA")  # 确保图像是RGBA模式
    image.putalpha(mask)  # 应用蒙版
    
    # 保存图像
    output_image.paste(image, (0, 0), image)

    return output_image

class ImageToAvatar:
    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "image": ("IMAGE",),
                "size": ("INT", {"default": 0, "min": 0, "max": 8192, "step": 8}),
            },
        }

    CATEGORY = "👽 小智模块组/👦 Avatar 用户头像制作"
    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("image",)
    FUNCTION = "image2avatar"

    def image2avatar(self, image, size):
        image = tensor2pil(image)
        image = pil2tensor(resize_and_crop_to_circle(image, size))
        return (image,)


NODE_CLASS_MAPPINGS = {
  "ImageToAvatar": ImageToAvatar,
}

NODE_DISPLAY_NAME_MAPPINGS = {
  "ImageToAvatar": "👦 ImageToAvatar",
}
