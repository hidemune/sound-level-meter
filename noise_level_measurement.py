#!/usr/bin/env python3
# coding: utf-8

import pyaudio
import numpy as np
import sys
import time
from scipy.fft import fft
import numpy as np
import matplotlib.pyplot as plt
import japanize_matplotlib
import psutil
from scipy import signal
import datetime

#import pow

# String identifying the microphone
MICROPHONE = 'Shure'

file_path = 'log.txt'
sys.stdout = open(file_path, "w")

print("注意：あくまでも目安です。")

mst = [[0,"・無音"],
        [15,"・木の葉のふれあう音"],
        [25,"・郊外の深夜"],
        [35,"・図書館"],
        [45,"・静かな事務所"],
        [55,"・掃除機（１ｍ） "],
        [65,"・セミの鳴き声（２ｍ） "],
        [75,"・地下鉄の車内 "],
        [85,"・犬の鳴き声（５ｍ） "],
        [95,"・電車が通るときのガード下 "],
        [105,"・自動車のクラクション（２ｍ） "],
        [115,"・ジェット（飛行機）エンジンの近く "],
    ]


def getIndex(strp):
    ret = -1
    p = pyaudio.PyAudio()
    for index in range(0, p.get_device_count()):
        device_info = p.get_device_info_by_index(index)
        print("DEVICE_INDEX:{}, DEVICE_NAME:{}".format(device_info["index"], device_info["name"]))
        if strp in device_info["name"]:
            ret = device_info["index"]
    p.terminate()
    return ret

# check args
#if (len(sys.argv) < 2) or (not sys.argv[1].isdecimal()):
#    print("Please specify input_device_index in integer")
#    sys.exit(-1)

p = pyaudio.PyAudio()

# set prams
INPUT_DEVICE_INDEX = int(getIndex(MICROPHONE))
CHUNK = 1024 # 1024
FORMAT = pyaudio.paInt16
CHANNELS = int(p.get_device_info_by_index(INPUT_DEVICE_INDEX)["maxInputChannels"])
SAMPLING_RATE = int(p.get_device_info_by_index(INPUT_DEVICE_INDEX)["defaultSampleRate"])
RECORD_SECONDS = 1

print(str(CHANNELS) + ' CHANNELS')
print(str(SAMPLING_RATE) + ' SAMPLING_RATE')
print(str(CHUNK) + ' CHUNK')

if CHANNELS == 0:
    exit(0)

T = 1
fs = SAMPLING_RATE
t = np.linspace(0.0, T, int(T*fs))

# amp to db
def to_db(x, base=1):
    if x == 0:
        return 0;
    y=20*np.log10(x/base)
    return y

from PIL import Image

import numpy as np
from scipy.signal import butter, lfilter, freqz
import matplotlib.pyplot as plt


def butter_lowpass(cutoff, fs, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return b, a

def butter_lowpass_filter(data, cutoff, fs, order=5):
    b, a = butter_lowpass(cutoff, fs, order=order)
    y = lfilter(b, a, data)
    return y


# Setting standard filter requirements.
order = 6
fs = SAMPLING_RATE
cutoff = 50.0

b, a = butter_lowpass(cutoff, fs, order)

# main loop
def main():
    while True:
        start = time.time()

        stream = p.open(format = FORMAT,
                        channels = CHANNELS,
                        rate = SAMPLING_RATE,
                        input = True,
                        frames_per_buffer = CHUNK,
                        input_device_index = INPUT_DEVICE_INDEX
                )

        # get specified range of data. size of data equals (CHUNK * (SAMPLING_RATE / CHUNK) * RECORD_SECONDS)
        data = np.empty(0)
        for i in range(0, int(SAMPLING_RATE / CHUNK * RECORD_SECONDS)):
            elm = stream.read(CHUNK, exception_on_overflow = False)
            elm = np.frombuffer(elm, dtype="int16")/float((np.power(2,16)/2)-1)
            data = np.hstack([data, elm])
        # calc RMS
        rms = np.sqrt(np.mean([elm * elm for elm in data]))
        # RMS to db
        db = to_db(rms, 20e-6)
        stream.close()

        strw = ""
        wgflg = False
        elapsed_time = time.time() - start
        if db != 0:
            for v, s in mst:
                if db > v:
                    strw = s
            now = datetime.datetime.now()
            print(now.strftime("%Y/%m/%d %H:%M:%S "), end='')
            print(" 全域:{:.1f}[dB] ".format(db),'  ', end='')
            
            if True:
                fft_signal = fft(data)
                
                power = np.hstack( \
                        ( \
                             np.abs( fft_signal[0] /(T*fs) )**2.0, \
                        2.0* np.abs( fft_signal[1:int(T*fs/2.0-1.0)] /(T*fs) )**2.0 \
                        ) \
                        )
                power_min = (20.0e-6)**2.0
                power_dB = 10.0*np.log10(power/power_min)
                #maxid = signal.argrelmax(power_dB, order=1) #最大値
                maxid = np.argmax(power_dB) #最大値
                id50 = 50
                id10k = 10000
                bk = 0
                bki = 0
                for i in range(id50, id10k):
                    if bk < power_dB[i]:
                        bk = power_dB[i]
                        bki = i
                maxid = bki
                strp = ''
                flg = False
                if maxid < 100:
                    flg = True
                    strp = '重低音' + str(maxid) + 'Hz'
                elif maxid < 300:
                    strp = '低音' + str(maxid) + 'Hz'
                elif maxid < 5000:
                    strp = '中音' + str(maxid) + 'Hz'
                else:
                    strp = '高音' + str(maxid) + 'Hz'
                if db >= 55.0:
                    strw += ' ◆注意◆'
                    wgflg = True
                
                
                y = butter_lowpass_filter(data, cutoff, fs, order)
                fft_signal2 = fft(y)
                # calc RMS
                rms2 = np.sqrt(np.mean([elm * elm for elm in y]))
                # RMS to db
                db2 = to_db(rms2, 20e-6)
                print(" 重低音:{:.1f}[dB] ".format(db2),'  ', end='')
                if db2 >= 40.0:
                    strw += ' ◆注意◆'
                    wgflg = True
                print(' Peak:'+ strp, strw, end='')
                
                print('')
                sys.stdout.flush()
            if wgflg:
                # Generating Frequency Vector
                f = np.linspace(0.0, fs/2.0, len(power)) /1.0e3
                # Plotting
                size_f = 8
                fig = plt.figure(figsize=[4,3], dpi=72, linewidth=0.0, tight_layout=T)
                #plt.xscale("log",basex=10)
                
                axs = fig.subplots(1, 1)

                ax1 = axs
                ax1.set_xscale('log')
                #ax1.plot(f[maxid],power_dB[maxid],'ro',label='ピーク値')
                ax1.plot(f[maxid],power_dB[maxid],'ro',label='最大値')
                ax1.plot(f, power_dB)
                ax1.set_xlabel('frequency[kHz]', fontsize=size_f)
                ax1.set_ylabel('power spectra[dB SPL]', fontsize=size_f)
                #ax1.tick_params(axis='x', labelsize=size_f)
                ax1.tick_params(axis='y', labelsize=size_f)
                #ax1.set_xlim(f[0], f[-1])
                ax1.set_xlim(0.050, 10.000)
                ax1.set_ylim(0, 80)
                
                ############################################
                pos = [0.050, 0.100, 0.300, 5.000, 10.000] 
                ticks = ['50 重', '100 低', '300 中', '5k 高', '10k ']
                ax1.set_xticks(pos)
                ax1.set_xticklabels(ticks)
                ############################################
                
                
                timestr = now.strftime("%Y%m%d_%H%M%S")
                timestr = 'Last'
                fig.align_ylabels()
                fig.suptitle( strw.replace('注意','').replace('◆','') + " 全{:.1f}[dB] 重{:.1f}[dB] ".format(db, db2) + " / " + strp, fontsize=size_f)
                fig.savefig(timestr + '.png')
                im = Image.open(timestr + '.png')
                im.show()
                for proc in psutil.process_iter():
                    if proc.name() == "display":
                        proc.kill()
            
try:
    main()
except KeyboardInterrupt:
    pass
finally:
    p.terminate()


'''

python3  noise_level_measurement.py

'''

