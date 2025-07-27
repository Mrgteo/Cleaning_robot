# import cv2
# import numpy as np
# import os

# # 1. 创建输出目录
# os.makedirs('calibration_data', exist_ok=True)

# # 2. 超参数
# INPUT_H, INPUT_W = 640, 640
# VAL_DIR = './val_images'          # 放原始图片
# CAL_DIR = './calibration_data'    # 输出 .bin
# MAX_NUM = 400                     # 最多 500 张

# def letterbox(im, new_shape=(640, 640), color=(114, 114, 114)):
#     h0, w0 = im.shape[:2]
#     r = min(new_shape[0] / h0, new_shape[1] / w0)
#     h, w = int(round(h0 * r)), int(round(w0 * r))
#     im = cv2.resize(im, (w, h), interpolation=cv2.INTER_LINEAR)
#     dh, dw = new_shape[0] - h, new_shape[1] - w
#     dh, dw = dh % 2, dw % 2
#     im = cv2.copyMakeBorder(im, dh//2, dh-dh//2, dw//2, dw-dw//2,
#                             cv2.BORDER_CONSTANT, value=color)
#     return im

# # 3. 主循环
# for idx, fname in enumerate(os.listdir(VAL_DIR)):
#     if not fname.lower().endswith(('.jpg', '.png', '.jpeg')):
#         continue
#     img = cv2.imread(os.path.join(VAL_DIR, fname))   # BGR
#     img = letterbox(img, (INPUT_H, INPUT_W))
#     img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)       # → RGB
#     img = img.transpose(2, 0, 1).astype(np.float32)  # HWC→CHW, 0-1
#     img = img * 255.0   
#     img = img.astype(np.float32)                               # ← 加这行
#     img.tofile(os.path.join(CAL_DIR, f'{idx:05d}.bin'))
#     if idx >= MAX_NUM - 1:   # 最多 400 张
#         break



# print("✅ 已生成 400 个校准样本")


import cv2
import numpy as np
import os

# 1. 创建输出目录
os.makedirs('calibration_data', exist_ok=True)

# 2. 超参数
INPUT_H, INPUT_W = 640, 640
VAL_DIR = './val_images'          # 放原始图片
CAL_DIR = './calibration_data'    # 输出 .bin
MAX_NUM = 400                     # 最多 400 张

def letterbox(im, new_shape=(640, 640), color=(114, 114, 114)):
    h0, w0 = im.shape[:2]
    r = min(new_shape[0] / h0, new_shape[1] / w0)
    h, w = int(round(h0 * r)), int(round(w0 * r))
    im = cv2.resize(im, (w, h), interpolation=cv2.INTER_LINEAR)
    dh, dw = new_shape[0] - h, new_shape[1] - w
    dh, dw = dh // 2, dw // 2
    im = cv2.copyMakeBorder(im, dh, dh, dw, dw, cv2.BORDER_CONSTANT, value=color)
    return im

# 3. 主循环
for idx, fname in enumerate(os.listdir(VAL_DIR)):
    if not fname.lower().endswith(('.jpg', '.png', '.jpeg')):
        continue
    img = cv2.imread(os.path.join(VAL_DIR, fname))   # BGR
    img = letterbox(img, (INPUT_H, INPUT_W))
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)       # → RGB
    img = img.transpose(2, 0, 1).astype(np.float32)  # HWC→CHW, 0-1
    img = img * 255.0                                # 0-255
    img.tofile(os.path.join(CAL_DIR, f'{idx:05d}.bin'))
    if idx >= MAX_NUM - 1:   # 最多 400 张
        break

print("✅ 已生成 400 个校准样本")
