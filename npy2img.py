import numpy as np
from PIL import Image
import os

# 设置主文件夹路径
main_folder1 = './images'
main_folder2 = './masks'
output_folder1 = './png_images'
output_folder2 = './png_masks'

# 遍历主文件夹下的每个子文件夹
for subdir, _, files in os.walk(main_folder1):
    # 遍历每个子文件夹中的文件
    for file in files:
        # 检查文件是否是 .npy 文件
        if file.endswith('.npy'):
            # 构建 .npy 文件的完整路径
            npy_path = os.path.join(subdir, file)

            # 加载 .npy 文件
            data = np.load(npy_path)

            # 确保数据在 0-255 范围并转换为 uint8 类型
            data_normalized = (255 * (data - data.min()) / (data.max() - data.min())).astype(np.uint8)

            # 将 NumPy 数组转换为图像
            image = Image.fromarray(data_normalized)
            #image = Image.fromarray(data)

            relative_path = os.path.relpath(subdir, main_folder1)
            output_subdir = os.path.join(output_folder1, relative_path)
            os.makedirs(output_subdir, exist_ok=True)

            # 构建 .png 文件的保存路径
            png_path = os.path.join(output_subdir, file.replace('.npy', '.png'))

            # 保存图像为 .png 文件
            image.save(png_path)
            print(f"Saved {png_path}")

for subdir, _, files in os.walk(main_folder2):
    # 遍历每个子文件夹中的文件
    for file in files:
        # 检查文件是否是 .npy 文件
        if file.endswith('.npy'):
            # 构建 .npy 文件的完整路径
            npy_path = os.path.join(subdir, file)

            # 加载 .npy 文件
            data = np.load(npy_path)

            # 确保数据在 0-255 范围并转换为 uint8 类型
            #data_normalized = (255 * (data - data.min()) / (data.max() - data.min())).astype(np.uint8)

            # 将 NumPy 数组转换为图像
            #image = Image.fromarray(data_normalized)
            image = Image.fromarray(data)

            relative_path = os.path.relpath(subdir, main_folder2)
            output_subdir = os.path.join(output_folder2, relative_path)
            os.makedirs(output_subdir, exist_ok=True)

            # 构建 .png 文件的保存路径
            png_path = os.path.join(output_subdir, file.replace('MA', 'NI').replace('.npy', '.png'))

            # 保存图像为 .png 文件
            image.save(png_path)
            print(f"Saved {png_path}")