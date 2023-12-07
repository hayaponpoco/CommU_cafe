# CommUを使用したカフェ

## 環境

- macOS Sonoma 14.1.1
- Python 3.11.6
- Pythonのライブラリは`requirements.txt`を参照
- ffmpeg version 6.0

## 実行手順

### 0. CommUを設置

- CommUの配置
  - 受付：まぶたが故障しているCommU (192.168.11.1**8**)
  - お渡し：通常のCommU (192.168.11.1**9**)
- CommUのボリュームは「11」

> [!IMPORTANT]
> 以下，それぞれ別のターミナルウィンドウで実行すること

### 1. 受付

> [!WARNING]
> 受付のCommUのIPアドレスは192.168.11.1**8**であることに注意

#### 1.1 CommUのカメラの映像を見る

> [!WARNING]
> 受付のUDP通信のポートは**5000**を指定することに注意

- CommUからカメラの映像データを送信
  - `ssh root@192.168.11.18`
  - `edison00`
  - `cd ~/ffmpeg-6.0.1-i686-static`
  - `./ffmpeg -f v4l2 -s 320x240 -thread_queue_size 8192 -i /dev/video0 -c:v libx264 -preset ultrafast -tune zerolatency -f h264 udp://192.168.11.16:5000?pkt_size=1024`
    - 送信先のIPアドレスは自身のPCを指定
- PCで映像データを受信
  - `ffplay -fflags nobuffer udp://127.0.0.1:5000`

#### 1.2 CommUを動かす

- CommU上でRobotControllerを起動
  - `ssh root@192.168.11.18`
  - `edison00`
  - `cd ~/RobotController_bin`
  - `java -jar RobotController.jar`
- プログラムを実行
  - `python exp_counter.py`

### 2. お渡し

> [!WARNING]
> お渡しのCommUのIPアドレスは192.168.11.1**9**であることに注意

#### 2.1 CommUのカメラの映像を見る（＆映像をクリックするとそちらを向く）

> [!WARNING]
> お渡しのUDP通信のポートは**5001**を指定することに注意

- （クリックした場所に視線を向けたい場合）CommU上でRobotControllerを起動
  - `ssh root@192.168.11.19`
  - `edison00`
  - `cd ~/RobotController_bin`
  - `java -jar RobotController.jar`
- CommUからカメラの映像データを送信
  - `ssh root@192.168.11.19`
  - `edison00`
  - `cd ~/ffmpeg-6.0-i686-static`
  - `./ffmpeg -f v4l2 -s 320x240 -thread_queue_size 8192 -i /dev/video0 -c:v libx264 -preset ultrafast -tune zerolatency -f h264 udp://192.168.11.16:5001?pkt_size=1024`
    - 送信先のIPアドレスは自身のPCを指定
- （クリックした場所に視線を向けたい場合）プログラムを実行
  - `python click_look.py`
- （映像だけ見たい場合）PCで映像データを受信
  - `ffplay -fflags nobuffer udp://127.0.0.1:5001`

#### 2.2 CommUを動かす

- （映像だけ見たい場合）CommU上でRobotControllerを起動
  - `ssh root@192.168.11.19`
  - `edison00`
  - `cd ~/RobotController_bin`
  - `java -jar RobotController.jar`
- プログラムを実行
  - `python exp_table.py`

## 使用できる軸

参考：[https://github.com/social-robotics-lab/robotcontroller_client](https://github.com/social-robotics-lab/robotcontroller_client)

| ID | ラベル | 初期値 | 安全可動範囲 | 可動範囲 | 方向 |
| ---: | :--- | ---: | :---: | :---: | :---: |
| 1 | BODY_P | 0 | -3 ~ 3 | -15 ~ 15 | B - F |
| 2 | BODY_Y | 0 | -65 ~ 66 | -67 ~ 67 | R - L |
| 3 | L_SHOU_P | 60 | -45 ~ 60 | -108 ~ 108 | H - L |
| 4 | L_SHOU_R | 0 | -45 ~ 0 | -45 ~ 30 | H - L |
| 5 | R_SHOU_P | -60 | -45 ~ 60 | -108 ~ 108 | L - H |
| 6 | R_SHOU_R | 0 | -45 ~ 0 | -30 ~ 45 | L - H |
| 7 | HEAD_P | 0 | -17 ~ 23 | -20 ~ 25 | B - F |
| 8 | HEAD_R | 0 | -2 ~ 3 | -15 ~ 15 | L - R |
| 9 | HEAD_Y | 0 | -44 ~ 44 | -85 ~ 85 | R - L |
| 10 | EYES_P | 0 | -20 ~ 21 | -22 ~ 22 | L - H |
| 11 | L_EYE_Y | 0 | -34 ~ 0 | -35 ~ 20 | E - I|
| 12 | R_EYE_Y | 0 | 0 ~ 34 | -20 ~ 35 | I - E|
| 13 | EYELID | 0 | -27 ~ 0 | -65 ~ 3 | - |
| 14 | MOUTH | 0 | - | -3 ~ 55 | - |
