# Noise meter

Sound pressure is measured for heavy bass components based on our own standards.

A microphone with a frequency of 44 kHz or higher is required.

(Sample)

2022/08/28 07:11:53  whole:41.9[dB]  BASS:19.3[dB] Peak:low 166Hz   library<br>
2022/08/28 07:11:55  whole:42.6[dB]  BASS:17.5[dB] Peak:mid 338Hz   library<br>
2022/08/28 07:11:56  whole:42.8[dB]  BASS:18.5[dB] Peak:low 225Hz   library<br>
2022/08/28 07:11:58  whole:41.8[dB]  BASS:18.7[dB] Peak:low 203Hz   library<br>
2022/08/28 07:12:00  whole:45.5[dB]  BASS:24.1[dB] Peak:low 156Hz   Quiet office<br>
2022/08/28 07:12:02  whole:44.4[dB]  BASS:19.4[dB] Peak:low 206Hz   library<br>
2022/08/28 07:12:04  whole:44.9[dB]  BASS:20.3[dB] Peak:low 244Hz   library<br>


## install

sudo apt-get install python3-pyaudio

sudo pip3 install pyaudio
sudo pip3 install scipy
sudo pip3 install numpy


## How to use (in terminal)

For the "Shure" part, enter a string that identifies the microphone.

python3 noise_level_measurement_English.py Shure &

tail -f log.txt

## To identify the microphone

At the beginning of log.txt, you will see the following output, so refer to this and specify a unique string.

DEVICE_INDEX:0, DEVICE_NAME:Shure MV7: USB Audio (hw:1,0)<br>
DEVICE_INDEX:1, DEVICE_NAME:HDA Intel PCH: ALC887-VD Analog (hw:2,0)<br>
DEVICE_INDEX:2, DEVICE_NAME:HDA Intel PCH: ALC887-VD Alt Analog (hw:2,2)<br>
DEVICE_INDEX:3, DEVICE_NAME:HDA NVidia: HDMI 0 (hw:3,3)<br>
DEVICE_INDEX:4, DEVICE_NAME:HDA NVidia: HDMI 1 (hw:3,7)<br>
DEVICE_INDEX:5, DEVICE_NAME:HDA NVidia: HDMI 2 (hw:3,8)<br>
DEVICE_INDEX:6, DEVICE_NAME:HDA NVidia: HDMI 3 (hw:3,9)<br>
DEVICE_INDEX:7, DEVICE_NAME:HDA NVidia: HDMI 4 (hw:3,10)<br>
DEVICE_INDEX:8, DEVICE_NAME:HDA NVidia: HDMI 5 (hw:3,11)<br>
DEVICE_INDEX:9, DEVICE_NAME:pulse<br>
DEVICE_INDEX:10, DEVICE_NAME:default<br>




# 騒音計

・重低音の成分について、独自の基準で音圧を計測しています。

・44kHz以上の周波数のマイクが必要です。

サンプル）

2022/08/28 04:37:50  全域:36.3[dB]     重低音:14.0[dB]     Peak:低音100Hz ・図書館<br>
2022/08/28 04:37:52  全域:37.6[dB]     重低音:15.8[dB]     Peak:低音135Hz ・図書館<br>
2022/08/28 04:37:54  全域:38.2[dB]     重低音:15.6[dB]     Peak:低音133Hz ・図書館<br>
2022/08/28 04:37:55  全域:37.7[dB]     重低音:17.2[dB]     Peak:重低音99Hz ・図書館<br>
2022/08/28 04:37:57  全域:39.4[dB]     重低音:15.9[dB]     Peak:低音104Hz ・図書館<br>


## install

sudo apt-get install python3-pyaudio

sudo pip3 install pyaudio
sudo pip3 install scipy
sudo pip3 install numpy


## 使い方(ターミナルにて)

Shure の部分は、マイクを特定する文字列を入力します。

python3 noise_level_measurement.py Shure &

tail -f log.txt

## マイクの特定について

log.txt の先頭に、以下のような出力が出ますので、これを参考にユニークな文字列を指定して下さい。

DEVICE_INDEX:0, DEVICE_NAME:Shure MV7: USB Audio (hw:1,0)<br>
DEVICE_INDEX:1, DEVICE_NAME:HDA Intel PCH: ALC887-VD Analog (hw:2,0)<br>
DEVICE_INDEX:2, DEVICE_NAME:HDA Intel PCH: ALC887-VD Alt Analog (hw:2,2)<br>
DEVICE_INDEX:3, DEVICE_NAME:HDA NVidia: HDMI 0 (hw:3,3)<br>
DEVICE_INDEX:4, DEVICE_NAME:HDA NVidia: HDMI 1 (hw:3,7)<br>
DEVICE_INDEX:5, DEVICE_NAME:HDA NVidia: HDMI 2 (hw:3,8)<br>
DEVICE_INDEX:6, DEVICE_NAME:HDA NVidia: HDMI 3 (hw:3,9)<br>
DEVICE_INDEX:7, DEVICE_NAME:HDA NVidia: HDMI 4 (hw:3,10)<br>
DEVICE_INDEX:8, DEVICE_NAME:HDA NVidia: HDMI 5 (hw:3,11)<br>
DEVICE_INDEX:9, DEVICE_NAME:pulse<br>
DEVICE_INDEX:10, DEVICE_NAME:default<br>
