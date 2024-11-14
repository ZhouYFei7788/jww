# -*- coding: utf-8 -*-
import cv2
from tts import tts

idnum = 0
# 用户需要在此添加场次号+座位号，下标序号要与名字对应(ID从0开始，依次递增)
names = ['','']
# 人脸识别函数
def Face():
    # 初始化识别器
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    # 加载训练好的模型文件
    recognizer.read(r'./Model/trainer-2023.yml')
    # 获取分类器
    faceCascade = cv2.CascadeClassifier(r'./cv2data/haarcascade_frontalface_default.xml')
    # 设置图片显示的字体
    font = cv2.FONT_HERSHEY_SIMPLEX
    # 捕获图像
    camera = cv2.VideoCapture(1, cv2.CAP_DSHOW)
    # 设置格式
    minW = 0.1*camera.get(3)
    minH = 0.1*camera.get(4)
    #tts('请正对着摄像头')
    confidence = 150.00
    name = "unknown"
    while True:
        # 读取图片
        success,img = camera.read()
        # 图片灰度化
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # 检测人脸
        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.3,
            minNeighbors=5,
            minSize=(int(minW), int(minH))
        )
        for (x, y, w, h) in faces:
            # 画一个矩形
            cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
            # 图像预测
            idnum, confidence = recognizer.predict(gray[y:y+h, x:x+w])
            print(confidence)
            # 阈值为110（即匹配指数大于等于90即可验证通过人脸）   
            if confidence < 150:
                name = names[idnum]
            else:
                name = "unknown"
            cv2.putText(img, str(name), (x+5, y-5), font, 1, (230, 250, 100), 1)
            cv2.putText(img, str(confidence), (x+5, y+h-5), font, 1, (255, 0, 0), 1)
        cv2.imshow('camera', img)
        # 保持画面持续
        key = cv2.waitKey(10)
        # 按Esc键退出
        if key==27 or confidence < 150:
            cv2.imwrite('./image.jpg', img)
            break
    # 关闭摄像头
    camera.release()
    cv2.destroyAllWindows()
    return name,confidence
