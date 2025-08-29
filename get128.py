import os
import cv2
import numpy as np
from pathlib import Path


def crop_center_region(img, mask, crop_size=128):
    """
    根据mask中病灶区域的中心，在img和mask中裁剪出以中心为128x128大小的区域。
    """
    # 找到病灶区域的所有像素点
    lesion_coords = np.column_stack(np.where(mask == 255))

    if lesion_coords.size == 0:
        # 若没有病灶区域，则返回None，跳过该图像
        return None, None

    # 计算病灶区域的中心点
    center_y, center_x = lesion_coords.mean(axis=0).astype(int)

    # 确定裁剪区域的起始坐标（保证在边界内）
    start_x = max(center_x - crop_size // 2, 0)
    start_y = max(center_y - crop_size // 2, 0)
    end_x = min(start_x + crop_size, img.shape[1])
    end_y = min(start_y + crop_size, img.shape[0])

    # 裁剪图像和mask
    cropped_img = img[start_y:end_y, start_x:end_x]
    cropped_mask = mask[start_y:end_y, start_x:end_x]

    # 检查裁剪区域大小是否符合预期
    if cropped_img.shape != (crop_size, crop_size):
        # 如果裁剪出的区域不是128x128大小，则填充或截断使其符合
        cropped_img = cv2.resize(cropped_img, (crop_size, crop_size), interpolation=cv2.INTER_NEAREST)
        cropped_mask = cv2.resize(cropped_mask, (crop_size, crop_size), interpolation=cv2.INTER_NEAREST)

    return cropped_img, cropped_mask


# 定义文件夹路径
image_dir = Path("png_images")
mask_dir = Path("png_masks")
output_image_dir = Path("png_images128")
output_mask_dir = Path("png_masks128")

# 创建输出文件夹
output_image_dir.mkdir(exist_ok=True)
output_mask_dir.mkdir(exist_ok=True)

# 遍历每个子文件夹
for image_subfolder in image_dir.iterdir():
    if image_subfolder.is_dir():
        mask_subfolder = mask_dir / image_subfolder.name  # 与image子文件夹对应的mask子文件夹
        if not mask_subfolder.exists():
            print(f"Warning: {mask_subfolder} not found, skipping...")
            continue

        # 创建对应的输出子文件夹
        output_image_subfolder = output_image_dir / image_subfolder.name
        output_mask_subfolder = output_mask_dir / mask_subfolder.name
        output_image_subfolder.mkdir(exist_ok=True)
        output_mask_subfolder.mkdir(exist_ok=True)

        # 遍历每张图像
        for image_file in image_subfolder.glob("*.png"):
            mask_file = mask_subfolder / image_file.name  # 找到对应的mask文件

            if not mask_file.exists():
                print(f"Warning: {mask_file} not found, skipping {image_file}...")
                continue

            # 读取图像和mask
            img = cv2.imread(str(image_file), cv2.IMREAD_GRAYSCALE)
            mask = cv2.imread(str(mask_file), cv2.IMREAD_GRAYSCALE)

            # 裁剪128x128区域
            cropped_img, cropped_mask = crop_center_region(img, mask)
            if cropped_img is None:
                print(f"No lesion found in {mask_file}, skipping...")
                continue

            # 保存裁剪后的图像和mask
            cropped_img_rgb = cv2.cvtColor(cropped_img, cv2.COLOR_GRAY2RGB)
            cv2.imwrite(str(output_image_subfolder / image_file.name), cropped_img_rgb)
            #cv2.imwrite(str(output_image_subfolder / image_file.name), cropped_img)
            cv2.imwrite(str(output_mask_subfolder / mask_file.name), cropped_mask)

print("All images processed successfully.")
