from PIL import Image, ImageDraw

def resize_and_crop_to_circle(image_path, output_path, size):
    # 打开图像
    with Image.open(image_path) as img:
        # 缩放图像到指定尺寸
        img = img.resize((size, size))
        
        # 创建一个圆形蒙版
        mask = Image.new("L", (size, size), 0)
        draw = ImageDraw.Draw(mask)
        radius = size // 2
        draw.ellipse((0, 0, size, size), fill=255)  # 绘制圆形蒙版
        
        # 使用蒙版裁剪图像
        img = img.convert("RGBA")  # 确保图像是RGBA模式
        img.putalpha(mask)  # 应用蒙版
        
        # 保存图像
        img.save(output_path, "PNG")

# 使用示例
resize_and_crop_to_circle("./assets/avatar.png", "output_image.png", 512)