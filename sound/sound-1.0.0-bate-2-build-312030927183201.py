'''
名称:字节节拍
作者:wilber-20130410
版权: © 2025 wilber-20130410
版本:1.0.0-bate-2-[312030927183201](测试版)
日期:2025.9.27
简介:使用Python实现字节节拍的音效算法,并进行播放。
留言:
1.本代码仅供学习交流使用,请勿用于商业用途。
2.本代码参考了网络上部分代码,在此表示感谢。
3.使用前请确保已经安装以下所使用的库。
4.本人推荐使用Visual Studio Code或PyCharm Community作为IDE(集成开发环境)。
5.需要安装python3及以上python环境(本人使用python3.12.3)。
6.本代码无法直接使用，请在最后一行调整检查目录
7.如果您有建议、发现了Bug、问题或者您进行优化后的代码,欢迎向本人邮箱xuwb0410@163.com发送邮件,本人将在21天内进行回复。
8.感谢Lambdaexec提供的字节节拍的音效算法。
9.以上留言不分先后。
'''
# -*- coding: utf-8 -*-

import pyaudio
import numpy as np
import time
from math import *

class AudioGenerator:
    def __init__(self):
        self.p = pyaudio.PyAudio()
        self.streams = []
    
    def generate_wave(self, algorithm_func, sample_rate=8000, duration=5):    #duration为播放时长，需在下面也进行调整
        samples = int(sample_rate * duration)
        buffer = np.zeros(samples, dtype=np.int8)
        for t in range(samples):
            buffer[t] = algorithm_func(t)
        return buffer
    
    def play(self, buffer, sample_rate):
        stream = self.p.open(format=pyaudio.paInt8,
                           channels=1,
                           rate=sample_rate,
                           output=True)
        stream.write(buffer.tobytes())
        self.streams.append(stream)
    
    def stop_all(self):
        for stream in self.streams:
            stream.stop_stream()
            stream.close()
        self.streams = []
    
    def close(self):
        self.stop_all()
        self.p.terminate()

# 音效算法
def sound1(t): 
    return (t * (t << 2 | t >> 7)) % 256 - 128

def sound2(t): 
    return (((t & (t >> 7 | t >> 8 | t >> 16) ^ t) * t)) % 256 - 128

def sound3(t): 
    return ((((t * (42 & t >> 10)) + (t * (42 & t >> 10)) % 114) + (t | t % 255 | t % 257) + (t & t >> 8))) % 256 - 128

def sound4(t): 
    return (t * (t >> 5 | t >> 8)) % 256 - 128

def sound5(t): 
    return (100 * ((t << 2 | t >> 5 | t ^ 63) & (t << 10 | t >> 11))) % 256 - 128

def sound6(t): 
    return (t + (t & t ^ t >> 6) - t * (t >> 9 & (t & 16) & t >> 9) * (t >> 9 | t >> 7)) % 256 - 128

def sound7(t): 
    return (2 * (t >> 5 & t) + (t >> 5) + t * (t >> 14 & 14)) % 256 - 128

def sound8(t): 
    return (t * ((t >> 10 & 5)) * (5 + (3 & t >> 14)) >> (t >> 8 & 3)) % 256 - 128

def sound9(t): 
    return (11 * (t * (4 | (t >> 5 - (t >> 14) % 4) % 8) & (8 << (t >> 13) % 4) * (1 | (t >> 15) % 8)) * (t >> 10)) % 256 - 128

def sound10(t): 
    return (t * (t >> (0xdead & t >> 12)) | t << (t >> 8)) % 256 - 128

def sound11(t): 
    return ((t & t // 2 & t // 4) * t // 4 >> 4) % 256 - 128

def sound12(t):
    return ((t | (t >> 9 | t >> 7)) * t & (t >> 11 | t >> 9)) % 256 - 128

def sound13(t):
    return (((t >> 8 & t >> 4) >> ((t >> 10) & (t >> 8) & 31)) * t) % 256 -128

def sound14(t):
    return (10 * (t >> 6 | t | t >> (t >> 16)) + (7 & t >> 11)) % 256 - 128

def sound15(t):
    return ((t & t + (1 + (t >> 9 & t >> 8)))) % 256 - 128

def sound16(t):
    return (t ^ t * (1 + (t >> 9 & t >> 8)) & 128) % 256 - 128

def sound17(t):
    return (3 * t ^ t >> 6 | t) % 256 - 128

def sound18(t):
    return ((t | t % 255 | t % 257) + (t & t >> 8) + (t * (42 & t >> 10)) + ((t % ((t >> 8 | t >> 16) + 1)) ^ t)) % 256 - 128

def sound19(t):
    return ((t & t >> 6) + (t | t >> 8) + (t | t >> 7) + (t | t >> 9)) % 256 - 128

def sound20(t):
    return ((t >> 3 + 3 * t | t << 3 % (t + 1))) % 256 - 128

def sound21(t):
    return (((t * (t >> 13 | t >> 8) | t >> 16 ^ t) + 64)) % 256 - 128

def sound22(t):
    return (t * (t >> 11 * (t >> 4 | t >> 5) & (14 | 19 * (t >> 19) >> t | t >> 81)) + 0) % 256 - 128

def sound23(t):
    return (5 * (t + (t ^ t >> 7) ^ 5) | 19 * (2 * t >> 43 | 15 * t >> 4) & (7 * t >> 172) // 2 * t * ((t >> 9 | t >> 13) & 15) & 129 | t * ((t >> 9 | 3 < t) & 25 & t >> 10)) % 256 - 128

def sound24(t):
    return (2 * t ^ 2 * t + (t >> 7) & t >> 12 | t >> 4 + (1 ^ 7 & t >> 19) | t >> 7) % 256 - 128

def sound25(t):
    return ((t >> 10 | t * 5) & (t >> 8 | t * 4) & (t >> 4 | t * 6)) % 256 - 128

def sound26(t):
    return ((t & t >> 8) + (t ^ t >> 5) & (t | t << 4)) % 256 - 128

def sound27(t):
    return ((t & t >> 12) * (t >> 4 | t >> 8)) % 256 - 128

def sound28(t):
    return ((t | t % 255 | t % 257) + (t & t >> 8) + (t * (42 & t >> 10)) + ((t % ((t >> 8 | t >> 16) + 1)) ^ t) & (t & t >> 8)) % 256 - 128

def sound29(t):
    return (t & t >> 8) % 256 - 128

def sound30(t):
    return ((t & t >> 6) + (t | t >> 8) + (t | t >> 7) + (t | t >> 9) & t >> 6) % 256 - 128

def sound31(t):
    return (t & (t >> (t >> 12 & 15)) * t) % 256 - 128

def sound32(t):
    return ((6 * t & t >> 5 | 127 * t >> 4) >> t + 64 & t >> 5 | t >> 4 | t >> t // 64) % 256 - 128

def sound33(t):
    return (t >> (t >> 13) * t + 127 | t >> 4) % 256 - 128

def sound34(t):
    return (10 * (t >> 8 | t | t >> (t >> 16)) + (1 & t >> 11)) % 256 - 128

def sound35(t):
    return (((t & t % 255) ^ t) - t) % 256 - 128

def sound36(t):
    return (t * (t >> 8 | t >> 9) & 46 & t >> 8 ^ (t & t >> 13 | t >> 6)) % 256 - 128

#def sound37(t):
#    return ((((t * ((114 >> (t >> 51) % 4 & 19) + 19) / 8 | t / 10) & t / 1 - (t >> 14) % 5 + 14) - t / 191 + 98)) % 256 - 128

#def sound38(t):
#    return (((t / 4 * ((t >> 12 ^ (t >> 12) - 2) % 11) | t >> 13) & 127) + (t / 4 * (0x98646363 >> (t >> 11 & 28) & 15) & 128)) % 256 - 128

def sound39(t):
    return (t * (t & t + (t >> 9 | 1))) % 256 - 128

def sound40(t):
    return ((t * (t & (11 << 4 + (t >> 51 & 4)) + 3) >> 8) + t) % 256 - 128

def sound41(t):
    return (114 * ((t << 5 | t >> 5 | t ^ 63) & (t << 10 | t >> 11))) % 256 - 128

def sound42(t):
    return ((t << (t >> 11 & 45)) + (t << (t >> 14 & 19)) + (t << (t >> 19 & 810))) % 256 - 128

def sound43(t):
    return ((t & 64 | t >> 5) ^ (t & 33 | t >> 8) ^ (t & 14 | t >> 9 | t & 76) ^ (t | 187) ^ t * (t >> 8 & 838 + t >> 13) & 644) % 256 - 128

def sound44(t):
    return (t * ((t >> 7 | t >> 9) & 30) & t << 1) % 256 - 128

def sound45(t):
    return (((t & t >> 8) | (t & t >> 13)) * t) % 256 - 128

def sound46(t):
    return (t * +(t >> 8 | t | t >> 9 | t >> 13) ^ t) % 256 - 128

def sound47(t):
    return (9 * t & t >> 45 * t & t >> 7 | 3 * t & t >> 10) % 256 - 128

def sound48(t):
    return (t & (t >> (t >> 12 & 15)) * t) % 256 - 128

def sound49(t):
    return (t >> 6 ^ t & t >> 9 ^ t >> 12 | ((t >> 6 | t << 1) + (t >> 5 | t << 3 | t >> 3) | t >> 2 | t << 1)) % 256 - 128

#def sound50(t):
#    return (t * (t ^ t + (t >> 9 | 1) / (t - 12800 ^ t) >> 10)) % 256 - 128

def sound51(t):
    return (t * (t >> 5 & t >> 7)) % 256 - 128

def sound52(t):
    return (((t >> 6 | t >> 8) * t) & 128) % 256 - 128

def sound53(t):
    return (t * (t >> (t >> 13 & t))) % 256 - 128

def sound54(t):
    return (t * (t >> 13)) % 256 - 128

def sound55(t):
    return ((~t >> 2) * ((127 & t * (7 & t >> 10)) < (245 & t * (2 + (5 & t >> 14))))) % 256 - 128

def sound56(t):
    return (t * ((t >> 12 | t >> 6) & 69 & t >> 2) | t * 4 | t * (t >> 9)) % 256 - 128

def sound57(t):
    return (t * (t >> 10 & t >> 8)) % 256 - 128

def sound58(t):
    return (t ^ t * (1 + (t >> 9 & t >> 8)) & 128) % 256 - 128

def sound59(t):
    return ((t ^ t >> 12) * t >> 8) % 256 - 128

def sound60(t):
    return (t * (0xDEAD >> (t >> 9 & 44) & 15) | t >> 8 | 40000) % 256 - 128

#def sound61(t):
#    return ((t >> 10 ^ t >> 11) % 5 * ((t >> 14 & 3 ^ t >> 15 & 1) + 1) * t % 100 + ((3 + (t >> 14 & 3) - (t >> 16 & 1)) / 3 * t % 100 & 64)) % 256 - 128

def sound62(t):
    return (t * (0xCA98 >> (t >> 9 & 14) & 15) | t >> 8) % 256 - 128

def sound63(t):
    return (sin(((t >> 8) & (t >> 13)) * t) * ((t >> 8 | t >> 10) & 127) + 127) % 256 - 128

if __name__ == "__main__":
    audio = AudioGenerator()
    sound_params = [
        (sound1, 8000),
        (sound2, 16000),
        (sound3, 16000),
        (sound4, 32000),
        (sound5, 16000),
        (sound6, 11025),
        (sound7, 8000),
        (sound8, 8000),
        (sound9, 8000),
        (sound10, 16000),
        (sound11, 22050),
        (sound12, 8000),
        (sound13, 16000),
        (sound14, 32000),
        (sound15, 11025),
        (sound16, 11025),
        (sound17, 16000),
        (sound18, 16050),
        (sound19, 32050),
        (sound20, 8000),
        (sound21, 22050),
        (sound22, 22050),
        (sound23, 8000),
        (sound24, 8000),
        (sound25, 8000),
        (sound26, 22050),
        (sound27, 22050),
        (sound28, 16000),
        (sound29, 32000),
        (sound30, 32000),
        (sound31, 16000),
        (sound32, 16000),
        (sound33, 32000),
        (sound34, 8000),
        (sound35, 16000),
        (sound36, 8000),
#        (sound37, 8000),
#        (sound38, 32000),
        (sound39, 16000),
        (sound40, 8000),
        (sound41, 8000),
        (sound42, 8000),
        (sound43, 8000),
        (sound44, 8000),
        (sound45, 8000),
        (sound46, 22500),
        (sound47, 8000),
        (sound48, 16000),
        (sound49, 8000),
#        (sound50, 32000),
        (sound51, 32000),
        (sound52, 16000),
        (sound53, 16000),
        (sound54, 32000),
        (sound55, 11025),
        (sound56, 8000),
        (sound57, 11025),
        (sound58, 11025),
        (sound59, 22050),
        (sound60, 8000),
#        (sound61, 8000),
        (sound62, 8000),
        (sound63, 16000)
    ]
    
    try:
        for i, (func, rate) in enumerate(sound_params, 1):
            print(f"正在生成音效 {i}...")
            buffer = audio.generate_wave(func, sample_rate=rate, duration=5)   #duration为播放时长，需在上面也进行调整
            audio.play(buffer, rate)
            time.sleep(2)  #两个音效播放中间的间隔时间
            audio.stop_all()
    except KeyboardInterrupt:
        print("\n用户中断播放")
    finally:
        audio.close()
