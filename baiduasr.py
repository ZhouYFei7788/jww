# -*- encoding: UTF-8 -*-
import time
import wave
import os
from pyaudio import PyAudio,paInt16
from aip import AipSpeech
from tts import tts

# 设置采样参数
NUM_SAMPLES = 2000
# 默认录音4s
TIME = 4

# 百度智能云平台语音技能密钥
# 请输入您的BaiduAPP_ID
BaiduAPP_ID = ''
# 请输入您的BaiduAPI_KEY      
BaiduAPI_KEY = ''
# 请输入您的SECRET_KEY      
SECRET_KEY = ''
client = AipSpeech(BaiduAPP_ID, BaiduAPI_KEY, SECRET_KEY)

# 保存录音文件
def save_wave_file(filename,data):  
    wf = wave.open(filename,'wb')
    wf.setnchannels(1)              
    wf.setsampwidth(2)              
    wf.setframerate(16000)          
    wf.writeframes(b"".join(data)) 
    wf.close()

# 定义录音函数
def record():
    print('Start recording.')
    tts("开始录音")
    # 实例化PyAudio对象
    pa = PyAudio() 
    # 打开输入流并设置音频采样参数 1 channel 16K framerate 
    stream = pa.open(format = paInt16,
                        channels = 1,
                        rate = 16000,
                        input = True,
                        frames_per_buffer = NUM_SAMPLES)
    # 录音缓存数组
    audioBuffer = []   
    # 循环采集音频 默认录制4s
    count = 0
    while count<TIME*10:
        # 一次性录音采样字节的大小
        string_audio_data = stream.read(NUM_SAMPLES)  
        audioBuffer.append(string_audio_data)
        count +=1
        # 加逗号不换行输出
        print('.', end='')  
    print('')
    print('End recording.')
    # 保存录制的语音文件到audio.wav中并关闭输入流
    save_wave_file('./audio.wav',audioBuffer)
    stream.close()

# 语音识别函数
def asr_updata():
    with open('./audio.wav', 'rb') as f:
        audio_data = f.read()
    result = client.asr(audio_data, 
                        'wav', 16000, {   # 采样频率16K
                        'dev_pid': 1537, 
                                          # 1536 普通话
                                          # 1537 普通话（纯中文识别）
                                          # 1737 英语
                                          # 1637 粤语
                                          # 1837 四川话
                     })
    # print(result)
    val = 'result' in result.keys()
    if val == True:   
        result_text = result["result"][0]
    else:
        result_text = '语音未识别'
    os.remove('audio.wav')
    return result_text
if __name__ == '__main__':
    record()
    result_text = asr_updata()
    print(result_text)


