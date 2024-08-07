import os
import hashlib
from PIL import Image

def calculate_image_hash(image_path):
    """
    计算图像的哈希值
    """
    image = Image.open(image_path)
    image_hash = hashlib.md5(image.tobytes()).hexdigest()
    return image_hash

def find_and_delete_duplicate_images(folder_path):
    """
    找到并删除文件夹中的重复图像
    """
    hash_map = {}
    duplicate_images = []

    for filename in os.listdir(folder_path):
        if filename.endswith('.jpg') or filename.endswith('.png'):  # 可根据实际情况修改扩展名
            image_path = os.path.join(folder_path, filename)
            image_hash = calculate_image_hash(image_path)

            if image_hash in hash_map:
                duplicate_images.append(image_path)
            else:
                hash_map[image_hash] = image_path

    # 删除重复的图片
    for duplicate_image in duplicate_images:
        os.remove(duplicate_image)
        print(f"Deleted duplicate image: {duplicate_image}")

if __name__ == "__main__":
    folder_path = '../img'
    find_and_delete_duplicate_images(folder_path)
