import cv2
import os

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

# 设置处理帧的计数器和保存计数器
frame_count = 0
save_count = 0

# 设置每隔多少帧保存一次图片
save_every = 1

# 遍历视频的每一帧
while cap.isOpened():
    ret, frame = cap.read()

    if ret:
        # 裁剪视频帧（示例裁剪从列150到650的区域）
        img_crop = frame[95:1080, 150:650]

        # 应用背景减除器，得到前景掩码
        fgmask = fgbg.apply(img_crop)


        # 对前景掩码进行高斯模糊和二值化处理
        blur = cv2.GaussianBlur(fgmask, (5, 5), 0)
        _, thresh = cv2.threshold(blur, 200, 255, cv2.THRESH_BINARY)

        # 寻找前景区域的轮廓
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # 绘制边界框并保存帧（每20帧保存一次）
        if frame_count % save_every == 0:
            for contour in contours:
                if cv2.contourArea(contour) > 30000:
                    # 存储当前帧，使用递增的文件名
                    file_name = f"{save_count}.png"
                    save_path = '../img/' + file_name
                    cv2.imwrite(save_path, img_crop)
                    print("保存帧:", file_name)

                    # 更新保存计数器
                    save_count += 1

        # 显示裁剪后的视频帧和移动检测结果（可选）
        # cv2.imshow('Frame', img_crop)
        # cv2.imshow('FG Mask', fgmask)

        # 按 'q' 键退出循环
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        # 更新帧计数器
        frame_count += 1
    else:
        break

# 释放资源
print("剪切完成")
cap.release()
cv2.destroyAllWindows()
