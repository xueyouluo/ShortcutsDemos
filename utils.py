
from PIL import Image
import io
import base64
    
def decode_image(base64_str):
    # 解码base64字符串
    img_bytes = base64.b64decode(base64_str)

    # 将字节转换为图像
    img = Image.open(io.BytesIO(img_bytes))

    return img


def resize_image(img, max_dim=1024):
    # 获取图片的宽和高
    width, height = img.size

    # 计算缩放比例
    if height > width:
        new_height = max_dim
        new_width = int(max_dim * width / height)
    else:
        new_width = max_dim
        new_height = int(max_dim * height / width)

    # 缩放图片
    img_resized = img.resize((new_width, new_height), Image.ANTIALIAS)

    # 将图片转换为base64编码
    buffered = io.BytesIO()
    img_resized.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue())

    return img_str.decode('utf-8')
