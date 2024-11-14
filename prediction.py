import os
import cv2
import numpy as np
from PIL import ImageFont, ImageDraw, Image
import torch
from torchvision import datasets, models, transforms
import torch.nn.functional as F
import torch.nn as nn
import time

# 模型推理
def modelpre(src_roi):
    grey_img = cv2.cvtColor(src_roi, cv2.COLOR_BGR2GRAY)
    tsfrm = transforms.Compose([
        transforms.Grayscale(3),
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize([0.5, 0.5, 0.5], [0.5, 0.5, 0.5])
    ])
    classes = ('fangbianmian', 'fenda', 'guantou', 'kele', 'kuangquanshui', 'maojin', 'mianbao', 'pingguo', 'xifashui', 'xuebi', 'yagao', 'zhijin')
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    model_eval = models.resnet18(pretrained=False)
    num_ftrs = model_eval.fc.in_features
    model_eval.fc = nn.Linear(num_ftrs, len(classes))
    model_eval.load_state_dict(torch.load('./model/1008.pkl', map_location=device))
    # 在推理前，务必调用model.eval()去设置dropout和batch normalization层为评估模式
    model_eval.eval()
    # OpenCV转PIL格式
    image = Image.fromarray(cv2.cvtColor(grey_img, cv2.COLOR_GRAY2RGB))
    # PIL图像数据转换为tensor数据，并归一化
    img = tsfrm(image)
    # 图像增加1维[batch_size,通道,高,宽]
    img = img.unsqueeze(0)
    # 输出推理结果
    output = model_eval(img)
    # prob是8个分类的概率
    prob = str(F.softmax(output, dim=1))
    print(prob)
    value, predicted = torch.max(output.data, 1)
    prob_stat = prob[prob.find("[[")+2 : prob.find("]]")].replace(" ", "").split(",")
    for num in range(len(classes)):
        if float(prob_stat[num]) > 0.2: #预测模型的概率筛选
            label = predicted.numpy()[0]
            pred_class = classes[predicted.item()]
            break
        else:
            label = len(classes)
            pred_class = '未知物料'
    label = predicted.numpy()[0]
    pred_class = classes[predicted.item()]
    return label,pred_class

# 显示推理结果
def showResult(img,text):
    # 设置图片显示分辨率
    newimg = cv2.resize(img,(640,480))
    fontpath = "font/simsun.ttc"
    font = ImageFont.truetype(fontpath, 48)  
    img_pil = Image.fromarray(newimg)
    draw = ImageDraw.Draw(img_pil)
    # 绘制文字信息
    draw.text((10, 100), text, font=font, fill=(0, 0, 255))
    bk_img = np.array(img_pil)
    # 获取实时时间作为命名，将识别图片和结果保存到文件夹
    str_time = time.strftime("%Y%m%d%H%M%S", time.localtime(time.time()))
    img_name = str_time + '.jpg'
    cv2.imwrite('./result/' + img_name, bk_img)    
    cv2.imshow('frame', bk_img)
    # 持续显示3s
    key = cv2.waitKey(1500)
    cv2.destroyAllWindows()

# 清空缓存图片
def remove_result():
    path = './result/'
    # 判断是否存在result文件夹
    if os.path.exists(path):                  
        for i in os.listdir(path):
            # 遍历拼接文件路径
            path_file = os.path.join(path, i) 
            # 判断该路径对象是否为文件
            if os.path.isfile(path_file):
                # 删掉文件    
                os.remove(path_file)          
    else:
        # 新建一个result文件夹
        os.mkdir(path)
if __name__ == "__main__":
    # 读取图片
    img = cv2.imread('./image.jpg')
    # 图像预测
    label, pred_class = modelpre(img)
    print("物料类别:", pred_class)
    showResult(img,pred_class)
    remove_result()

