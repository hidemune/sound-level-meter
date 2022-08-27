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

python3 noise_level_measurement.py Shure &

tail -f log.txt

