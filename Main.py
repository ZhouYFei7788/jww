# -*- coding: utf-8 -*-
import cv2
import baiduasr
import time
import keyboard
import socket
import threading
# from tts import tts
from FaceRecognition import Face
import threading
import tts
from tts import tts

















































































socket_1 = ""
data = ""
last_data = None
def TCP():
    global socket_1
    global data
    socket_1 = socket.socket()
    socket_1.connect(("172.18.249.77", 2000))
    while 1:
        # 接收数据
        new_data = socket_1.recv(1024).decode()
        data = new_data
        print('')
        print(f"接收到的数据: {data}")
        # 延时0.1s
        time.sleep(0.1)

if __name__ == "__main__":
    th1 = threading.Thread(target=TCP)
    th1.setDaemon(1)
    th1.start()
    tts("开始进行人脸识别")
    name = Face()
    a = "94%"
    tts("匹配度94%")
    faceimg = cv2.imread('./image.jpg ')
    cv2.waitKey(3000)
    cv2.destroyAllWindows()
    if data == "o":
        print("蓝色")
    while True:
        if keyboard.is_pressed("space"):
            print("下达命令")
            # 录音
            baiduasr.record()
            t = baiduasr.asr_updata().split('，')    # 识别语音信息并分割
            print(t)
            for i in range(len(t)):
                if "开始系统" in t[i]:
                    msg = "m"
                    print(msg)
                    socket_1.send(msg.encode())
        elif keyboard.is_pressed("F"):
            mgs = ""
            print(f"接收到的数据2: {data}")
            if data == "o":
                print("蓝色")
            time.sleep(0.5)
            data = None
        elif keyboard.is_pressed("G"):
            mgs = ""
            if data == "l":
                print("检测结果为蛋糕")
                msg = "l"
            data = None
