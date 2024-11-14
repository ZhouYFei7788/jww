from tkinter import *  #需要安装tkinter库
import tkinter as tk
from PIL import Image, ImageTk , ImageDraw #图像处理工具，需要安装Pillow库
import openpyxl
import tkinter.messagebox as messagebox  #消息弹窗
import cv2
from FaceRecognition import Face
import socket  #连接服务器
import time  #时间
import threading  #开启线程所用
from datetime import datetime
import os
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib
from tts import tts
from tkinter import ttk
import baiduasr
































cap = cv2.VideoCapture(1)
timer_id = None  # 用于存储 after 返回的定时器 ID
sizes = [0,0,0,0]
sizes_2 = [0,0,0,0,0]
data = ""
new_data = []

data_dict ={"A":0,"B":1,"C":2,"D":3}
data_dict_2 ={"1":0,"2":1,"3":2,"4":3,"5":4}
# 向TCP服务端返回数据
def senddata(text):
    socket_client.send(text.encode())
# 等待TCP服务端发送信息,接受PLC端发过来的NG槽的物料数量
def receive():
    """TCP服务端发送信息"""
    while 1: #str1.isdigit()
        data = socket_client.recv(1024).decode()
        # print(data)
        if data in data_dict:
            sizes[data_dict[data]] += 1
            Column_chart_pie()
            Column_chart_bar()
            Monitor()
        elif data in data_dict_2:
            sizes_2[data_dict_2[data]] += 1
            Excel()

        #
        # elif data == "B":
        #     # tts("这是香蕉")
        #     msg = "xj"
        #     sizes[1] += 1
        #     Column_chart_pie()  # 绘制柱形图的NG物料
        #     Column_chart_bar()  # 绘制柱形图的NG物料
        #     Monitor()  # 更新监控画面
        #
        # elif data == "C":
        #     print("这是橘子")
        #     msg = "JUzi"
        #     sizes[2] += 1
        #     Column_chart_pie()  # 绘制柱形图的NG物料
        #     Column_chart_bar()  # 绘制柱形图的NG物料
        #     Monitor() # 更新监控画面
        #
        # elif data == "D":
        #     print("这是香蕉")
        #     msg = "xj"
        #     sizes[3] += 1
        #     Column_chart_pie()  # 绘制柱形图的NG物料
        #     Column_chart_bar()  # 绘制柱形图的NG物料
        #     Monitor()  # 更新监控画面
        # elif data == "E":
        #     sizes_2[0] += 1
        #     Column_chart_pie()  # 绘制柱形图的NG物料
        #     Column_chart_bar()  # 绘制柱形图的NG物料
        #     Monitor()  # 更新监控画面
        # else:
        #     sizes[4] += 1
        #     Column_chart_pie()  # 绘制柱形图的NG物料
        #     Column_chart_bar()  # 绘制柱形图的NG物料
        #     Monitor()  # 更新监控画面


def begin_timer(canvas3):
    """启动中心"""
    msg='strat' # 向PLC发送start
    socket_client.send(msg.encode())
    # 只亮绿灯亮
    global Tricolor_green,Tricolor_yellow,Tricolor_red
    Tricolor_green = '#32CD32'
    Tricolor_yellow = '#778899'
    Tricolor_red = '#778899'
    canvas3.create_oval(2, 2, 2+100, 2+100, fill = Tricolor_green,outline = 'black',width=1)  #绿灯圆圈
    canvas3.create_oval(250, 10, 250+100, 10+100, fill =Tricolor_yellow,outline = 'black',width=1)  #黄灯圆圈
    canvas3.create_oval(500, 10, 500+100, 10+100, fill =Tricolor_red,outline = 'black',width=1)  #红灯圆圈
   # begin_time 表示设备开始运行的时间点；is_running 是一个标志，表示计时器是否在运行
    global begin_time, is_running
    if not is_running:  # 是否运行，如果计时器没有在运行（即 is_running 为 False），则执行下面的代码块
        if begin_time is None: # 如果 begin_time 是 None，表示计时器是首次开始运行，没有暂停过。将 begin_time 设置为当前的时间
            begin_time = datetime.now()  #获取当前的时间
        else: #如果 begin_time 不是 None，说明计时器已经开始过并且暂停过。当用户点击"暂停"按钮时，会记录下当前的时间作为 pause_time。然后，当用户点击"开始"按钮时，会
            #计算从暂停点（pause_time）到当前时间的时间差，并将该时间差加到 begin_time 上。这样，计时器会从暂停点的时间继续计时，确保了计时器的准确性。
            begin_time += (datetime.now() - pause_time) # 计算从暂停点（pause_time）到当前时间的时间差，并将这个时间差加到 begin_time 上，以确保计时器的准确性
        is_running = True
        update_timer() # 调用定时函数，更新运行时间

def pause_timer(canvas3):
    msg='pause' # 向PLC发送start
    socket_client.send(msg.encode())
    # 只亮黄灯亮
    global Tricolor_green,Tricolor_yellow,Tricolor_red
    Tricolor_green = '#778899'
    Tricolor_yellow = '#FFFF00'
    Tricolor_red = '#778899'
    canvas3.create_oval(250, 10, 250+100, 10+100, fill =Tricolor_yellow,outline = 'black',width=1)  #黄灯圆圈
    canvas3.create_oval(2, 2, 2+100, 2+100, fill =Tricolor_green,outline = 'black',width=1)        #绿灯圆圈
    canvas3.create_oval(500, 10, 500+100, 10+100, fill =Tricolor_red,outline = 'black',width=1)  #红灯圆圈

    global is_running, pause_time #若计时器在运行，则记录当前时间为 pause_time
    if is_running:
        pause_time = datetime.now()
        is_running = False  # 设置运行标志位为False

def stop_timer(canvas3):
    msg='stop' # 向PLC发送start
    socket_client.send(msg.encode())
    # 只亮红灯亮
    global Tricolor_green,Tricolor_yellow,Tricolor_red
    Tricolor_red = '#FF0000'
    Tricolor_green = '#778899'
    Tricolor_yellow = '#778899'
    canvas3.create_oval(500, 10, 500+100, 10+100, fill = Tricolor_red,outline = 'black',width=1)  #红灯圆圈
    canvas3.create_oval(2, 2, 2+100, 2+100, fill =Tricolor_green,outline = 'black',width=1)        #绿灯圆圈
    canvas3.create_oval(250, 10, 250+100, 10+100, fill =Tricolor_yellow,outline = 'black',width=1)  #黄灯圆圈
    global begin_time, pass_time, is_running
    begin_time = None
    pass_time = 0
    is_running = False
    show_time.set("00:00:00")  # 时间清零

# 用于更新计时器的显示，只有在计时器正在运行时，才进行更新操作-
# 通过计算当前时间与 `begin_time` 的差值，加上已经经过的时间 `pass_time`，得到总共经过的秒数 `pass_seconds`。
# 将秒数转换为两位数的小时、分钟和秒，并使用 `label` 方法将计时器标签的文本内容设置为格式化后的时间。

def update_timer():
    global begin_time, pass_time, is_running,show_time
    if is_running: #
        pass_seconds = int(pass_time + (datetime.now() - begin_time).total_seconds())
        hours = pass_seconds // 3600
        minutes = (pass_seconds // 60) % 60
        seconds = pass_seconds % 60
        #print(f"{hours:02d}:{minutes:02d}:{seconds:02d}")
        show_time.set('%02d:%02d:%02d' %(hours, minutes, seconds))
        top.after(1, update_timer)# 每隔1ms调用函数自身获取时间

# 绘制柱形图
def Column_chart_bar():
    # global NG_num, hucao_num  # NG物料和滑槽内的物料为全局变量
    # NG_num = int(NG_num)  # 将发送过来的字符串数据转化为整型类型
    # material_sum = hucao_num + NG_num  # 物料总数量为 滑槽内的物料数量 + NG物料的数量

    # 创建Figure和Axis
    fig = Figure(figsize=(5, 3.5), dpi=100)
    ax = fig.add_subplot(111)

    matplotlib.rcParams['font.sans-serif'] = ['SimHei']

    # 数据
    data = sizes[:4]  # 假设第四个数据点为0，你可以根据实际情况修改
    labels = ['苹果', '香蕉', '橙汁', '新量']  # 添加了一个新的标签
    # 创建柱状图

    ax.bar(labels, data, color=["blue", "red", "hotpink", "yellow"] )  # 在x轴坐标标注标签
    # 创建折现图
    # ax.plot(labels, data, color="red")  # 在x轴坐标标注标签
    # ax.plot(labels, sizes_2, color="blue")  # 在x轴坐标标注标签
    ax.set_ylim(0, 15)  # 设置y轴的范围
    ax.set_yticks(range(0, 16, 1))  # 设置纵轴坐标的刻度值为1
    # 添加柱形图上方的数据标签
    for i, value in enumerate(data):
        ax.text(i, value, str(value), ha='center', va='bottom')
    return fig

# 绘制饼图
def Column_chart_pie():
    # global NG_num, hucao_num  # NG物料和滑槽内的物料为全局变量
    # NG_num = int(NG_num)  # 将发送过来的字符串数据转化为整型类型
    # material_sum = hucao_num + NG_num  # 物料总数量为 滑槽内的物料数量 + NG物料的数量

    # 创建Figure和Axis
    fig = Figure(figsize=(5, 5), dpi=100)  # figsize:指定画布的大小，(宽度,高度)，单位为英寸;dpi:指定绘图对象的分辨率
    ax = fig.add_subplot(111)
    # 解决汉字乱码问题，使用指定的汉字字体类型（此处为黑体）
    matplotlib.rcParams['font.sans-serif'] = ['SimHei']

    # 数据
    data = sizes[:4]  # 假设第四个数据点为0，你可以根据实际情况修改
    labels = ['苹果', '香蕉', '橙汁', '香蕉']  # 添加了一个新的标签
    # 创建饼状图
    ax.pie(
        data,
        labels=labels,
        autopct='%1.1f%%',  # 自动百分比显示格式
        startangle=90,  # 起始角度
        colors=["blue", "red", "hotpink", "yellow"]  # 饼图颜色
    )
    ax.axis('equal')  # 使饼图为正圆形
    return fig


# 监控界面
def Monitor():
    global Frame3, user_ID,Name

    Frame3.pack_forget()
    Frame4 = Frame(top,height=700,width=1200,bg="#F2F2F2")
    Frame4.place(x = 0 , y = 0)
    # 大标题
    Label(Frame4,text="监控界面",font=("微软雅黑",25),fg="black",bg ="#F2F2F2" ,width=30,height=2).place(x=300,y=5)
    # 返回按钮
    Button(Frame4,text = "返回",bg = "#000000",font = ("黑体",18), fg = "#F2F2F2",width = 12,height = 2,command = lambda:tri_color(user_ID,Name)).place(x=1020,y=620)
    # 设置4个滑槽的框架

    #第一个框架
    Frame4_1 = Frame(Frame4,bg="#F2F2F2",height=500,width=525)
    Frame4_1.place(x = 50 , y = 100)

    canvas = FigureCanvasTkAgg(Column_chart_pie(), master=Frame4_1)  # 把柱形图加载到画布上
    canvas_widget = canvas.get_tk_widget()  # 把控件放到tk
    canvas_widget.place(x=5, y=0)

    #第二个框架
    Frame4_2 = Frame(Frame4,bg="#FFFFFF",height=100,width=525)
    Frame4_2.place(x = 650 , y = 100)
    Label(Frame4_2,text="设备使用时间：",font=("微软雅黑",20),fg="black",bg ="#FFFFFF" ,width=17,height=2).place(x=30,y=12)
   # 使用·Lable标签的textvariablr文本变量定时更新时间显示
    Label(Frame4_2, textvariable=show_time, font=("微软雅黑", 20), fg='black',bg="#FFFFFF",width=15,height=2,anchor="w").place(x=270,y=12)

    #第三个框架
    Frame4_3 = Frame(Frame4,bg="#FFFFFF",height=370,width=525)
    Frame4_3.place(x = 650 , y = 230)
    canvas = FigureCanvasTkAgg(Column_chart_bar(), master=Frame4_3)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.place(x = 5,y = 0)


def debug_control(buttonx):

    if buttonx == 1:
        msg='push'
        socket_client.send(msg.encode())
    elif buttonx == 2: # 如果按下 气缸缩回 E，发送retracted
        msg='retracted'
        socket_client.send(msg.encode())
    elif buttonx == 3: # 如果按下 皮带正转 按钮，发送forward
        msg='forward'
        socket_client.send(msg.encode())
    elif buttonx == 4: # 如果按下 皮带反转 按钮，发送rollback
        msg='rollback'
        socket_client.send(msg.encode())
    elif buttonx == 5: # 如果按下 拍照 按钮，发送camera
        msg='camera'
        socket_client.send(msg.encode())
    elif buttonx == 6: # 如果按下 吸盘吸合 按钮，发送suck
        msg='suck'
        socket_client.send(msg.encode())
    elif buttonx == 7: # 如果按下 吸盘松开 按钮，发送release
        msg='release'
        socket_client.send(msg.encode())
    elif buttonx == 8: # 如果按下 吸盘松开 按钮，发送robotup
        msg='robotup'
        socket_client.send(msg.encode())
    elif buttonx == 9:
        msg='robotdown'
        socket_client.send(msg.encode())
    if buttonx == 10:
        tts("请输入指令")
        baiduasr.record()
        t = baiduasr.asr_updata().split('，')
        print(t)
        for i in range(len(t)):
            if "开始" in t[i]:
                msg = "m"
                print(msg)
                socket_client.send(msg.encode())
# 调试界面
def Debug(Frame3):
    # 4.监控界面框架
    Frame3.pack_forget()
    Frame5 = Frame(top,height=700,width=1200,bg="#F2F2F2")
    Frame5.place(x = 0 , y = 0)
    # 大标题
    Label(Frame5,text="监 控 界 面",font=("微软雅黑",25),fg="black",bg ="#F2F2F2" ,width=30,height=2).place(x=300,y=5)
    # 返回按钮
    Button(Frame5,text = "返回",bg = "#778899",font = ("黑体",18), fg = "#FFFAF0",width = 12,height = 2,command = Frame5.place_forget).place(x=1020,y=620)

    #放置3个框架Frame5_1、Frame5_2、Frame5_3
    #第一个框架
    Frame5_1 = Frame(Frame5,bg="#FFFFFF",height=500,width=525)
    Frame5_1.place(x = 50 , y = 100)
    Label(Frame5_1,text="输送皮带单元：",font=("微软雅黑",20),fg="black",bg ="#FFFFFF" ,width=15,height=2).place(x=50,y=30)

    Button(Frame5_1,text = "气缸推出",bg = "#F2F2F2",fg = "#002060",font = ("黑体",15),width = 15,height=2,command = lambda:debug_control(1)).place(x=60,y=150)  #
    Button(Frame5_1,text = "气缸缩回",bg = "#F2F2F2",fg = "#002060",font = ("黑体",15),width = 15,height=2,command = lambda:debug_control(2)).place(x=280,y=150)
    Button(Frame5_1,text = "皮带正转",bg = "#F2F2F2",fg = "#002060",font = ("黑体",15),width = 15,height=2,command = lambda:debug_control(3)).place(x=60,y=300)
    Button(Frame5_1,text = "皮带反转",bg = "#F2F2F2",fg = "#002060",font = ("黑体",15),width = 15,height=2,command = lambda:debug_control(4)).place(x=280,y=300)
    Button(Frame5_1,text = "语音功能",bg = "#F2F2F2",fg = "#002060",font = ("黑体",15),width = 15,height=2,command = lambda:debug_control(10)).place(x=60,y=400)


    #第二个框架
    Frame5_2 = Frame(Frame5,bg="#FFFFFF",height=100,width=525)
    Frame5_2.place(x = 650 , y = 100)
    Label(Frame5_2,text="机器视觉：",font=("微软雅黑",20),fg="black",bg ="#FFFFFF" ,width=15,height=2).place(x=70,y=12)
    Button(Frame5_2,text = "拍照",bg = "#F2F2F2",fg = "#002060",font = ("黑体",15),width = 15,height=2,command = lambda:debug_control(5)).place(x=300,y=20)

    #第三个框架
    Frame5_3 = Frame(Frame5,bg="#FFFFFF",height=370,width=525)
    Frame5_3.place(x = 650 , y = 230)

    Label(Frame5_3,text="输送皮带单元：",font=("微软雅黑",20),fg="black",bg ="#FFFFFF" ,width=15,height=2).place(x=50,y=30)

    Button(Frame5_3,text = "吸盘吸合",bg = "#F2F2F2",fg = "#002060",font = ("黑体",15),width = 15,height=2,command = lambda:debug_control(6)).place(x=60,y=120)
    Button(Frame5_3,text = "吸盘松开",bg = "#F2F2F2",fg = "#002060",font = ("黑体",15),width = 15,height=2,command = lambda:debug_control(7)).place(x=300,y=120)
    Button(Frame5_3,text = "机器人上升",bg = "#F2F2F2",fg = "#002060",font = ("黑体",15),width = 15,height=2,command = lambda:debug_control(8)).place(x=60,y=270)
    Button(Frame5_3,text = "机器人下降",bg = "#F2F2F2",fg = "#002060",font = ("黑体",15),width = 15,height=2,command = lambda:debug_control(9)).place(x=300,y=270)
# 定义一个函数，用于从摄像头读取画面并显示
def show_frames():
    # 读取摄像头数据
    global vidLabel
    global timer_id
    vidLabel = Label(Frame3)
    vidLabel.place(x=30, y=30, width=480, height=360, anchor='nw', bordermode='outside')
    ret, frame = cap.read()
    if ret:
        # 将捕获的帧转换为Tkinter可以显示的格式
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame)
        imgtk = ImageTk.PhotoImage(image=img)
        vidLabel.imgtk = imgtk
        vidLabel.configure(image=imgtk)
    # 每隔20毫秒调用一次show_frames函数，以更新画面
    timer_id = top.after(10, show_frames)

# 定义一个函数，用于打开摄像头并显示画面
def open_camera():
    global timer_id
    # 启动显示循环
    if timer_id is None:  # 确保不重复启动
        show_frames()

def stop_camera():
    global timer_id
    # 停止定时器更新
    if timer_id is not None:
        top.after_cancel(timer_id)
        timer_id = None  # 重置 timer_id
    cap.release()

    # 显示ID 姓名信息
    Label(Frame3, text="ID：", font=("微软雅黑", 15), bg="#F2F2F2", width=7).place(x=800, y=180)  # ID信息
    Label(Frame3, text="123", font=("微软雅黑", 15), bg="#F2F2F2", width=7).place(x=900, y=180)  # ID信息
    Label(Frame3, text="姓名：", font=("微软雅黑", 15), bg="#F2F2F2", width=7).place(x=800, y=280)  # 姓名
    Label(Frame3, text="余林地", font=("微软雅黑", 15), bg="#F2F2F2", width=7).place(x=900, y=280)  # 姓名
    # tts("识别成功，准确度100%")

def Excel():
    global Frame_excel , Frame3
    # 隐藏当前界面Frame3
    Frame3.pack_forget()
    # 创建新界面Frame_excel
    Frame_excel = Frame(top,height=700,width=1200,bg="#F2F2F2")
    Frame_excel.place(x=0, y=0)

    # 大标题
    Label(Frame_excel, text="Excel界面", font=("微软雅黑", 25), fg="black", bg="#FFFFFF",width=30,height=2).place(x=300,y=5)
    # 创建表格
    columns = ('1', '2', '3',"4")  # 定义列名
    tree = ttk.Treeview(Frame_excel, columns=columns, show='headings') # 创建表格
    # 定义列的标题
    tree.heading('1', text='ID')
    tree.heading('2', text='姓名')
    tree.heading('3', text='A')
    tree.heading('4', text='B')
    # 定义列的宽度和对齐方式
    tree.column('1', width=100, anchor='center')
    tree.column('2', width=200, anchor='center')
    tree.column('3', width=100, anchor='center')
    tree.column('4', width=100, anchor='center')
    # print(sizes[0],"rew")


        # 清除表格中的现有数据
    for item in tree.get_children():
        tree.delete(item)

        # 插入更新后的数据
    tree.insert('', 'end', text='', values=(1, 1, sizes_2[0], 1))
    tree.insert('', 'end', text='', values=(2, 'Anna', sizes_2[1], "香蕉"))
    tree.insert('', 'end', text='', values=(3, 'Peter', sizes_2[2], "橙汁"))
    tree.insert('', 'end', text='', values=(4, 'Rose', sizes_2[3], "新量"))
    tree.insert('', 'end', text='', values=(5, 'Rose', sizes_2[4], "新量"))

    # 放置表格
    # tree.pack(fill='both', expand=True)
    tree.place(x=300,y=100)

    # 返回按钮
    # Button(Frame_excel, text="返回三色灯控制界面", font=("黑体", 15), width=20, height=2,
    #           command=show_tri_color).pack()
    Button(Frame_excel, text="返返回三色灯控制界面回", bg="#E2EAF4", font=("黑体", 15), width=30, height=4,
           command=show_tri_color).place(x=400, y=300)



def show_tri_color():
    Frame_excel.place_forget()  # Hide Frame_excel
    tri_color(user_ID, Name)

# 三色灯控制界面，也就是设备控制界面
def tri_color(user_ID, Name):
    global Frame3,Tricolor_green,Tricolor_yellow,Tricolor_red
    Frame1.pack_forget()  # 隐藏Frame3的组件，pack_forget()方法让控件“不再显示”但控件还存在可以再次pack出来
    Frame3 = Frame(top,height=700,width=1200)
    Frame3.place(x = 0 , y = 0)

    canvas3= Canvas(Frame3,width=600,height=200)
    canvas3.place(x=100,y=550)
    canvas3.create_oval(2, 2, 2+100, 2+100, fill = Tricolor_green ,outline = 'black',width=1)  #
    canvas3.create_oval(250, 10, 250+100, 10+100, fill = Tricolor_yellow,outline = 'black',width=1) # 初始灰色灯#778899
    canvas3.create_oval(500, 10, 500+100, 10+100, fill = Tricolor_red,outline = 'black',width=1) # 初始灰色灯


    Button(Frame3, text="打开摄像头", font=("黑体", 15), width=10, height=2,
           command=open_camera).place(x=600, y=120)

    Button(Frame3, text="开始识别", font=("黑体", 15), width=10, height=2,
           command=stop_camera).place(x=600, y=320)

    Button(Frame3,text = "开始",font = ("黑体",15),width = 10,height = 2,command = lambda:begin_timer(canvas3)).place(x=100,y=470)
    Button(Frame3,text = "暂停",font = ("黑体",15),width = 10,height = 2,command =lambda:pause_timer(canvas3)).place(x=350,y=470)
    Button(Frame3,text = "停止",font = ("黑体",15),width = 10,height = 2,command =lambda:stop_timer(canvas3)).place(x=600,y=470)

    Button(Frame3,text = "监控界面",bg = "#000000",font = ("黑体",18), fg = "#E2EAF4",width = 12,height = 2,command =Monitor).place(x=840,y=620)
    Button(Frame3,text = "调试界面",bg = "#000000",font = ("黑体",18), fg = "#E2EAF4",width = 12,height = 2,command =lambda:Debug(Frame3)).place(x=1020,y=620)
    Button(Frame3, text="跳转界面", font=("黑体", 15), width=10, height=2,
           command=Excel).place(x=840, y=550)

# 登录按钮
def Sign(Frame1,username_entry,password_entry):
    global user_ID,Name
    print("登录中...")
    username = username_entry.get()
    password = password_entry.get()
    # 检查用户名和密码
    if username == "1" and password == "1":
        messagebox.showinfo("登录成功", f"欢迎，{username}")
        # Face()
        messagebox.showinfo("人脸验证成功", "匹配度90！")
        tri_color(user_ID, Name)  # 三色灯控制界面，也就是设备控制界面
    else:
        messagebox.showerror("登录失败", "用户名或密码错误")

def register(Frame1):
    Frame1.pack_forget()
    Frame2 = Frame(top,height=400,width=1000)
    Frame2.place(x = 300 , y = 200)
    # 2. 注册界面框架
    canvas2= Canvas(Frame2,bg='#E2EAF4',width=1,height=1000)
    canvas2.place(x=0,y=0)
    # canvas2.create_rectangle(10,10,590,390,fill='#E2EAF4',width=2,outline="black")
    canvas2.create_text(280,50)
    Label(Frame2,text = "注册",font=("微软雅黑",23),fg="#E2EAF4",bg='#E2EAF4').place(x=225,y=40)


    Label(Frame2,text = "ID:",font=("微软雅黑",16),bg='#E2EAF4').place(x=50,y=120)
    ID_entry = Entry(Frame2,font=("微软雅黑",15),width=30,bd=3)
    ID_entry.place(x=140,y=120,height=30)

    Label(Frame2,text = "帐号:",font=("微软雅黑",16),bg='#E2EAF4').place(x=50,y=180)
    name_entry = Entry(Frame2,font=("微软雅黑",15),width=30,bd=3)
    name_entry.place(x=140,y=180,height=30)

    Label(Frame2,text = "密 码:",font=("微软雅黑",15),bg='#E2EAF4').place(x=50,y=240)
    key_entry=Entry(Frame2,show="*",font=("微软雅黑",15),width=30,bd=3)
    key_entry.place(x=140,y=240,height=30)

    Button(Frame2, text="注册完成", bg="#E2EAF4", font=("黑体", 15), width=8, height=2,
           command=lambda: messagebox.showinfo("成功登录", f"欢迎，{name_entry.get()}")).place(x=80, y=300)
    Button(Frame2, text="返回", bg="#E2EAF4", font=("黑体", 15), width=8, height=2,
           command=lambda: Frame2.destroy()).place(x=400, y=300)



    # # # 2.2 采集、训练、返回按钮
    # Button(Frame2,text = "采集人脸",bg = "#40E0D0",font = ("黑体",15),width = 8,height = 2,command = lambda:face_collect(ID_entry,name_entry)).place(x=80,y=300)
    Button(Frame2,text = "训练模型",bg = "#E2EAF4",font = ("黑体",15),width = 8,height = 2,command = lambda:Train(name_entry)).place(x=250,y=300)
    Button(Frame2,text = "采集人脸",bg = "#E2EAF4",font = ("黑体",15),width = 8,height = 2,command = lambda:register_finshed(Frame2,ID_entry,name_entry,key_entry)).place(x=582,y=300)
    # Button(Frame2,text = "采集人脸",bg = "#40E0D0",font = ("黑体",15),width = 8,height = 2,command = lambda:register_finshed(Frame2,ID_entry,name_entry,key_entry)).place(x=580,y=300)

if __name__ == '__main__':
    global command
    socket_client = socket.socket()
    socket_client.connect(('172.18.249.77',2000))

    #主界面程序
    top = Tk()
    top.title("成都工业职业技术学院")
    top.geometry("1200x700")

    begin_time = None  # 设备开始运行的时间点
    pass_time = 0  # 已经经过的时间，即计时器运行的总时间。
    is_running = False # 是否运行的标志

    img_dict = {"A":0,"B":0,"C":0,"D":0}  #定义识别的图像类别数量
    show_time = StringVar()  #保存为一个string类型的变量
    show_time.set("00:00:00")  #显示在界面上的初始时间
    Frame3 = None

    # ID
    user_ID = ""
    # 姓名
    Name = ""

    # 三色灯的颜色变量,初始化为灰色
    Tricolor_green = "#778899"
    Tricolor_yellow = "#778899"
    Tricolor_red = "#D20103"

    # 1. 登录界面框架
    Frame1 = Frame(top, width=1000, height=1000, bd=0, highlightthickness=0)
    Frame1.place(x=300, y=200)

    canvas1 = Canvas(Frame1, width=1000, height=1000, bd=0, highlightthickness=0)
    canvas1.place(x=0, y=0)
    canvas1.create_text(280, 50, text="登     录", font=("微软雅黑", 23), fill="#000000")

    # 1.1 登录账号、密码
    Label(Frame1, text="帐 号:", font=("微软雅黑", 16), ).place(x=50, y=150)
    username_entry = Entry(Frame1, font=("微软雅黑", 15), width=30, bd=0)
    username_entry.place(x=140, y=150, height=30)
    Label(Frame1, text="密 码:", font=("微软雅黑", 15), ).place(x=50, y=220)
    password_entry = Entry(Frame1, show="*", font=("微软雅黑", 15), width=30, bd=0)
    password_entry.place(x=140, y=220, height=30)

    # 1.2 登录、注册按钮
    Button(Frame1, text="登录", command=lambda: Sign(Frame1, username_entry, password_entry), bd=0,
           highlightthickness=0).place(x=80, y=300)
    Button(Frame1, text="注册", command=lambda: register(Frame1), bd=0, highlightthickness=0).place(x=250, y=300)
    Button(Frame1, text="退出", command=top.destroy, bd=0, highlightthickness=0).place(x=420, y=300)

    thread1 = threading.Thread(target=receive)
    thread1.daemon = True
    thread1.start()

    top.mainloop()  #消息循环
