import cv2
import os
import numpy as np
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

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

# 设置处理帧的计数器和视频计数器
frame_count = 0
video_count = 0

# 设置每隔多少帧处理一次
process_every = 1

# 用于存储每辆车的图像帧
car_frames = []

# 遍历视频的每一帧
while cap.isOpened():
    ret, frame = cap.read()

    if ret:
        # 每隔 process_every 帧处理一次
        if frame_count % process_every == 0:
            # 裁剪视频帧（示例裁剪从列150到650的区域）
            img_crop = frame[:, 150:650]

            # 应用背景减除器，得到前景掩码
            fgmask = fgbg.apply(img_crop)

            # 对前景掩码进行高斯模糊和二值化处理
            blur = cv2.GaussianBlur(fgmask, (5, 5), 0)
            _, thresh = cv2.threshold(blur, 200, 255, cv2.THRESH_BINARY)

            # 寻找前景区域的轮廓
            contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            detected = False
            for contour in contours:
                if cv2.contourArea(contour) > 30000:
                    # # 获取边界框坐标
                    # x, y, w, h = cv2.boundingRect(contour)
                    # car_img = img_crop[y:y+h, x:x+w]

                    # 存储当前车的图像帧
                    car_frames.append(img_crop)
                    detected = True

            if not detected and car_frames:
                # 确定输出视频路径
                output_video_path = f'../video_cut/output_video_{video_count}.mp4'

                # 选取尺寸最大的图像作为基准
                max_size_img = max(car_frames, key=lambda x: x.shape[0] * x.shape[1])

                # 获取最大图像的大小
                height, width, _ = max_size_img.shape

                # 设置视频的帧率（FPS）和分辨率
                fps = 1  # 帧率
                video_size = (width, height)  # 视频分辨率

                # 创建视频写入对象
                video_writer = cv2.VideoWriter(output_video_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, video_size)

                # 逐帧读取图像并写入视频
                for img in car_frames:
                    video_writer.write(img)

                print(output_video_path+"  ready")
                # 释放视频写入对象
                video_writer.release()

                # 增加视频计数器
                video_count += 1

                # 清空当前车的图像帧列表
                car_frames = []

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
