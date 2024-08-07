import os
# 在下面修改图片格式 image_extension='.png' 图片名称 prefix='img'
def rename_files_in_folder(folder_path, prefix='img', image_extension='.png', text_extension='.txt'):
    """
    重命名文件夹中的图片和对应的文本文件
    """
    file_list = os.listdir(folder_path)
    image_files = [f for f in file_list if f.endswith(image_extension)]
    image_files.sort()  # 根据需要排序图片文件

    count = 1
    for old_image_name in image_files:
        new_image_name = f"{prefix}_{count:03}{image_extension}"
        old_image_path = os.path.join(folder_path, old_image_name)
        new_image_path = os.path.join(folder_path, new_image_name)

        # 重命名图片文件
        os.rename(old_image_path, new_image_path)
        print(f"Renamed image: {old_image_name} -> {new_image_name}")

        # 检查对应的文本文件是否存在并重命名
        old_text_name = os.path.splitext(old_image_name)[0] + text_extension
        old_text_path = os.path.join(folder_path, old_text_name)

        if os.path.exists(old_text_path):
            new_text_name = os.path.splitext(new_image_name)[0] + text_extension
            new_text_path = os.path.join(folder_path, new_text_name)
            os.rename(old_text_path, new_text_path)
            print(f"Renamed text: {old_text_name} -> {new_text_name}")
        else:
            print("该图片不存在label文本！"+old_image_name)
        count += 1


if __name__ == "__main__":
    folder_path = '../img'
    rename_files_in_folder(folder_path)
