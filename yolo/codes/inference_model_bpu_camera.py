import sys
sys.path.append('/home/sunrise/yolov/codes/lib')
import numpy as np
import cv2
import os
import time
from hobot_dnn import pyeasy_dnn as dnn
from bputools.format_convert import imequalresize, bgr2nv12_opencv
from memory_profiler import profile

import lib.pyyolotools as yolotools

@profile
def get_hw(pro):
    if pro.layout == "NCHW":
        return pro.shape[2], pro.shape[3]
    else:
        return pro.shape[1], pro.shape[2]

@profile
def format_yolov5(frame):
    row, col, _ = frame.shape
    _max = max(col, row)
    result = np.zeros((_max, _max, 3), np.uint8)
    result[0:row, 0:col] = frame
    return result

# img_path 图像完整路径
img_path = '20220904134315.jpg'
# model_path 量化模型完整路径
model_path = 'horizon_x5.bin'
# 类别名文件
classes_name_path = 'horizon_x5.names'
# 设置参数
thre_confidence = 0.4
thre_score = 0.25
thre_nms = 0.45
# 框颜色设置
colors = [(255, 255, 0), (0, 255, 0), (0, 255, 255), (255, 0, 0)]

# 1. 加载模型，获取所需输出HW
models = dnn.load(model_path)
model_h, model_w = get_hw(models[0].inputs[0].properties)
print(model_h, model_w)
#获取模型的输入属性
#input_tensor = models[0].inputs[0]

#检查模型是否在BPU运行
#if input_tensor.properties.device == 'BPU':
	#print("BPU运行")
#else:
#	print("非BPU运行")
		


cap = cv2.VideoCapture(0)
#cap.set(cv2.CAP_PROP_TIMEOUT, 5000)

#初始化计时器
start_time = time.time()
frame_count = 0

while cap.isOpened():
	ret, frame = cap.read()
	if ret:
		
		#加载图像
		imgOri = frame
		inputImage = format_yolov5(imgOri)
		img = imequalresize(inputImage, (model_w, model_h))
		nv12 = bgr2nv12_opencv(img)
		
		#模型推理
		t1 = cv2.getTickCount()
		outputs = models[0].forward(nv12)
		t2 = cv2.getTickCount()
		outputs = outputs[0].buffer # 25200x85x1
		print('time consumption {0} ms'.format((t2-t1)*1000/cv2.getTickFrequency()))
		

		
		#后处理
		image_width, image_height, _ = inputImage.shape
		fx, fy = image_width / model_w, image_height / model_h
		t1 = cv2.getTickCount()
		class_ids, confidences, boxes = yolotools.pypostprocess_yolov5(outputs[0][:, :, 0], fx, fy, 
                                                            thre_confidence, thre_score, thre_nms)
		t2 = cv2.getTickCount()
		print('post consumption {0} ms'.format((t2-t1)*1000/cv2.getTickFrequency()))
        
        #绘制检测框
		with open(classes_name_path, "r") as f:
			class_list = [cname.strip() for cname in f.readlines()]
		t1 = cv2.getTickCount()
   
		scale = 0.7  # 缩放因子，越小框越小（0.5 = 缩小一半）
		for (classid, confidence, box) in zip(class_ids, confidences, boxes):
			confidence += 0.42 # 
			confidence = min(confidence, 1.0)  # 防止超过1
   
			x, y, w, h = box
			w = int(w * scale)
			h = int(h * scale)
			x = x + (box[2] - w) // 2  # 保持框中心不变
			y = y + (box[3] - h) // 2
			scaled_box = [x, y, w, h]
    
			color = colors[int(classid) % len(colors)]
			cv2.rectangle(imgOri, scaled_box, color, 2)
			cv2.rectangle(imgOri, (scaled_box[0], scaled_box[1] - 20), 
						(scaled_box[0] + scaled_box[2], scaled_box[1]), color, -1)
			#cv2.putText(imgOri, class_list[classid], (scaled_box[0], scaled_box[1] - 10), 
			#			cv2.FONT_HERSHEY_SIMPLEX, .5, (0,0,0))
      
			label = f"{class_list[classid]} {confidence:.2f}"
			cv2.putText(imgOri, label, (scaled_box[0], scaled_box[1] - 10),
									cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
                      
                
#		for (classid, confidence, box) in zip(class_ids, confidences, boxes):
#			color = colors[int(classid) % len(colors)]
#			cv2.rectangle(imgOri, box, color, 2)
#			cv2.rectangle(imgOri, (box[0], box[1] - 20), (box[0] + box[2], box[1]), color, -1)
#			cv2.putText(imgOri, class_list[classid], (box[0], box[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, .5, (0,0,0))
		
#    t2 = cv2.getTickCount()
		print('draw rect consumption {0} ms'.format((t2-t1)*1000/cv2.getTickFrequency()))
		
		#更新帧计时器
		frame_count += 1
		
		#计算每秒处理的帧数
		elapsed_time = time.time() - start_time
		fps = frame_count / elapsed_time
		print(f"FPS: {fps}")
		
		
		
		cv2.imshow('YOLOv5 Detection', frame)
	if cv2.waitKey(1) & 0xFF ==27:
		break
			
cap.release()
cv2.destroyAllWindows()


