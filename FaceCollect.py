# -*- coding: utf-8 -*-
import cv2
import numpy as np
# from tts import tts

# 将捕获照片的大小裁剪为正方形
def getpaddingSize(shape):
    # 照片的长和宽
    h, w = shape
    longest = max(h, w)
    # 将最长的边进行处理
    result = (np.array([longest]*4, int) - np.array([h, h, w, w], int)) // 2
    return result.tolist()

# 图像去噪处理，使得训练出来的模型具备一定的泛化能力
def dealwithimage(img, h=64, w=64):
    top, bottom, left, right = getpaddingSize(img.shape[0:2])
    img = cv2.copyMakeBorder(img, top, bottom, left, right, cv2.BORDER_CONSTANT, value=[0, 0, 0])
    img = cv2.resize(img, (h, w))
    return img

# 改变亮度与对比度
def relight(imgsrc, alpha=1, bias=0):
    imgsrc = imgsrc.astype(float)
    imgsrc = imgsrc * alpha + bias
    imgsrc[imgsrc < 0] = 0
    imgsrc[imgsrc > 255] = 255
    imgsrc = imgsrc.astype(np.uint8)
    return imgsrc

# 捕获人脸
def GetFace(name,face_id):
    # 0: 笔记本内置摄像头; 1: USB摄像头
    camera = cv2.VideoCapture(1, cv2.CAP_DSHOW)
    # 获取分类器
    face_detector = cv2.CascadeClassifier(r'./cv2data/haarcascade_frontalface_default.xml')
    count = 1
    # tts("人脸采集中")
    while True:
        # 默认获取100张图片作为训练数据集
        if(count<=100):
            print("It's processing %s image." % count)
            # 读取图片
            success,img = camera.read()
            # 图片灰度化
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            # 检测人脸
            faces = face_detector.detectMultiScale(gray,1.3,8)
            for (x, y, w, h) in faces:
                # 图像预处理，处理成64*64大小的图片
                face = gray[y:y+h, x:x+w]
                face = cv2.resize(face, (64, 64))
                # 图像去噪处理
                face = dealwithimage(face)
                # 改变亮度与对比度
                #face = relight(face, random.uniform(0.5, 1.5), random.randint(-50, 50))
                # 保存图片
                cv2.imwrite("Facedata/User." + str(face_id) + '.' + str(count) + '.jpg', face)
                # 在图片上显示名字
                cv2.putText(img, name, (x, y-20), cv2.FONT_HERSHEY_SIMPLEX, 1, 255, 2)
                # 画一个矩形
                img = cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
                count+=1
            cv2.imshow('img', img)
            # 保持画面持续
            key = cv2.waitKey(30)&0xff
            # Esc退出
            if key == 27:
                break
        else:
            break
    # 关闭摄像头
    camera.release()
    cv2.destroyAllWindows()

# 补充代码
if __name__ == '__main__':

    name = input('Please input your name:')
    face_id = input('Please input face id:')
    GetFace(name, face_id)





