import cv2
import os
import numpy as np

# 设置工作目录至包含视频文件的文件夹
os.chdir('../video')  # 将路径修改为您的视频所在的文件夹

# 创建背景减除器
fgbg = cv2.createBackgroundSubtractorMOG2()

# 打开视频文件
video_path = 'TL-Video-5.mkv'  # 将视频文件名替换为您的视频文件
cap = cv2.VideoCapture(video_path)

# 检查视频是否成功打开
if not cap.isOpened():
    print("Error: 无法打开视频文件")
    exit()

# 设置处理帧的计数器
frame_count = 0

# 设置每隔多少帧处理一次
process_every = 1
# 防错计数器
count = 0

# 用于存储每辆车的图像帧
car_frames = []
car_num = 0
# 当前处理的车辆图像帧
current_car_frames = []
# 读取第一帧
ret, prev_frame = cap.read()

# 遍历视频的每一帧
while cap.isOpened():
    ret, frame = cap.read()
    if ret:
        # 比较当前帧与上一帧是否完全相同
        if frame.shape == prev_frame.shape and (frame == prev_frame).all():
            print("相同帧跳过")
            continue  # 跳过当前帧
        # 更新上一帧为当前帧
        prev_frame = frame.copy()
        # 每隔 process_every 帧处理一次
        if frame_count % process_every == 0:
            # 裁剪视频帧（示例裁剪从列150到650的区域）

            img_crop = frame[95:1080, 150:650]
            img_crop2 = frame[95:1080, 0:1200]
            # 应用背景减除器，得到前景掩码
            fgmask = fgbg.apply(img_crop)

            # 对前景掩码进行高斯模糊和二值化处理
            blur = cv2.GaussianBlur(fgmask, (5, 5), 0)
            _, thresh = cv2.threshold(blur, 200, 255, cv2.THRESH_BINARY)

            # 寻找前景区域的轮廓
            contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            detected = False

            for contour in contours:
                if cv2.contourArea(contour) > 3000:
                    # 指定旋转角度为90度（顺时针）
                    rotated_image = cv2.rotate(img_crop2, cv2.ROTATE_90_COUNTERCLOCKWISE)

                    # 存储当前车的图像帧
                    current_car_frames.append(rotated_image.copy())  # 使用copy以确保数据不受后续修改影响
                    detected = True
                    count = count + 1

            if not detected and current_car_frames and count > 20:
                if len(current_car_frames) > 60:
                    # 防错计数器
                    count = 0
                    height, width, _ = current_car_frames[0].shape
                    # 计算每一帧应该使用的宽度
                    target_width = 1800  # 假设目标图片的总宽度
                    num_frames = len(current_car_frames)
                    frame_width = target_width // num_frames  # 每一帧的宽度
                    target_width = frame_width * num_frames  # 重新计算图片宽度避免黑色部分出现
                    half = int(width / 2)
                    print(len(current_car_frames))

                    if len(current_car_frames) * frame_width > 500 and len(current_car_frames) > 10:
                        # 创建一个空白的目标图片，固定高度为每一帧的高度
                        target_height = height
                        target = np.zeros((target_height, target_width, 3), dtype=np.uint8)
                        cv2.imwrite(f'../img-long-test/car{car_num}.jpg', target)
                        print(f'../img-long-test/car{car_num}.jpg')
                        car_num = car_num + 1
                        current_car_frames = []
                    else:
                        current_car_frames = []
                else:
                    current_car_frames = []

        # 按 'q' 键退出循环
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        # 更新帧计数器
        frame_count += 1
    else:
        break

# 释放资源
print("处理完成")
cap.release()
cv2.destroyAllWindows()
