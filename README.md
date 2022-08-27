# 騒音計

・重低音の成分について、独自の基準で音圧を計測しています。

サンプル）

2022/08/28 04:37:50  全域:36.3[dB]     重低音:14.0[dB]     Peak:低音100Hz ・図書館
2022/08/28 04:37:52  全域:37.6[dB]     重低音:15.8[dB]     Peak:低音135Hz ・図書館
2022/08/28 04:37:54  全域:38.2[dB]     重低音:15.6[dB]     Peak:低音133Hz ・図書館
2022/08/28 04:37:55  全域:37.7[dB]     重低音:17.2[dB]     Peak:重低音99Hz ・図書館
2022/08/28 04:37:57  全域:39.4[dB]     重低音:15.9[dB]     Peak:低音104Hz ・図書館


# install

sudo apt-get install python3-pyaudio

pip3 install pyaudio

# 使い方(ターミナルにて)

Shure の部分は、マイクを特定する文字列を入力します。

python3 noise_level_measurement.py Shure &

tail -f log.txt

# マイクの特定について

log.txt の先頭に、以下のような出力が出ますので、これを参考にユニークな文字列を指定して下さい。

DEVICE_INDEX:0, DEVICE_NAME:Shure MV7: USB Audio (hw:1,0)
DEVICE_INDEX:1, DEVICE_NAME:HDA Intel PCH: ALC887-VD Analog (hw:2,0)
DEVICE_INDEX:2, DEVICE_NAME:HDA Intel PCH: ALC887-VD Alt Analog (hw:2,2)
DEVICE_INDEX:3, DEVICE_NAME:HDA NVidia: HDMI 0 (hw:3,3)
DEVICE_INDEX:4, DEVICE_NAME:HDA NVidia: HDMI 1 (hw:3,7)
DEVICE_INDEX:5, DEVICE_NAME:HDA NVidia: HDMI 2 (hw:3,8)
DEVICE_INDEX:6, DEVICE_NAME:HDA NVidia: HDMI 3 (hw:3,9)
DEVICE_INDEX:7, DEVICE_NAME:HDA NVidia: HDMI 4 (hw:3,10)
DEVICE_INDEX:8, DEVICE_NAME:HDA NVidia: HDMI 5 (hw:3,11)
DEVICE_INDEX:9, DEVICE_NAME:pulse
DEVICE_INDEX:10, DEVICE_NAME:default
