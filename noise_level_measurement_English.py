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
# check args
if (len(sys.argv) < 2) :
    print("Please specify MICROPHONE in String")
    sys.exit(-1)
MICROPHONE = sys.argv[1]

file_path = 'log.txt'
sys.stdout = open(file_path, "w")

print("Note: This is only a guide.")

mst = [[0,"silence"],
        [15,"the_sound_of_leaves_rustling_against_each_other"],
        [25,"Suburban_Late_Night"],
        [35,"library"],
        [45,"Quiet_office"],
        [55,"Vacuum_cleaner_(1m)"],
        [65,"Cicada_chirping_(2m)"],
        [75,"Inside_a_subway_car"],
        [85,"Dog_barking_(5m)"],
        [95,"Under_the_guard_when_the_train_goes_by"],
        [105,"Car_horn_(2m)"],
        [115,"Near_jet_(airplane)_engines"],
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
            print(" whole:{:5.1f}[dB] ".format(db), end='')
            
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
                    strp = 'bass' + "{:4d}".format(maxid) + 'Hz'
                elif maxid < 300:
                    strp = 'low ' + "{:4d}".format(maxid) + 'Hz'
                elif maxid < 5000:
                    strp = 'mid ' + "{:4d}".format(maxid) + 'Hz'
                else:
                    strp = 'high' + "{:4d}".format(maxid) + 'Hz'
                if db >= 55.0:
                    strw += ' *caution'
                    wgflg = True
                
                
                y = butter_lowpass_filter(data, cutoff, fs, order)
                fft_signal2 = fft(y)
                # calc RMS
                rms2 = np.sqrt(np.mean([elm * elm for elm in y]))
                # RMS to db
                db2 = to_db(rms2, 20e-6)
                print("BASS:{:5.1f}[dB] ".format(db2), end='')
                if db2 >= 40.0:
                    strw += ' *caution'
                    wgflg = True
                print('Peak:'+ strp, strw, end='')
                
                print('')
                sys.stdout.flush()
            if wgflg:
                # Generating Frequency Vector
                f = np.linspace(0.0, fs/2.0, len(power)) /1.0e3
                # Plotting
                size_f = 8
                fig = plt.figure(figsize=[3.2,2.4], dpi=100, linewidth=0.0, tight_layout=T)
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
                ticks = ['50', '100', '300', '5k', '10k ']
                ax1.set_xticks(pos)
                ax1.set_xticklabels(ticks)
                ############################################
                
                
                timestr = now.strftime("%Y%m%d_%H%M%S")
                timestr = 'Last'
                fig.align_ylabels()
                fig.suptitle(now.strftime("%Y/%m/%d %H:%M:%S ") + '\n' + strw.replace('*caution','') + "\nWHOLE {:.1f}[dB]  BASS {:.1f}[dB] ".format(db, db2) + " " + strp, fontsize=size_f)
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

