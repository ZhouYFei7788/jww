from aip import AipSpeech
from playsound import playsound
import os

def tts(text):
    APP_ID = ''
    API_KEY = ''
    SECRET_KEY = ''
    #path = 'C:/Users/Administrator/Desktop/1/'
    client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)
    #vol：音量；spd:语速；pit:音调；per:精品音库5为度小娇，103为度米朵，106为度博文，110为度小童，111为度小萌，默认为度小美 
    result  = client.synthesis(text,'zh',1,{'vol':9,'spd':5,'pit':5,'per':4})
    if not isinstance(result,dict):
        with open('audio.mp3','wb+') as f:
            f.write(result)
    playsound('audio.mp3')
    os.remove('audio.mp3')
def record():

    print('Start recording.')
    tts("开始录音")  # 调用 tts 函数，将“开始录音”作为参数传入，进行语音播放

















if __name__ == '__main__':
    record()

