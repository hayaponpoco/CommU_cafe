import time
import PySimpleGUI as sg
from robottools import RobotTools

rt = RobotTools('192.168.11.18', 22222)    # まぶたが故障しているCommU
reset_servo_map = dict(
    BODY_P=0, BODY_Y=0,
    L_SHOU_P=43, L_SHOU_R=0, R_SHOU_P=-43, R_SHOU_R=0,
    HEAD_P=-12, HEAD_R=0, HEAD_Y=0,
    EYES_P=0, L_EYE_Y=-5, R_EYE_Y=5, EYELID=-2,
    MOUTH=1
)
pose = dict(Msec=500, ServoMap=reset_servo_map)
rt.play_pose(pose)

# GUI設定
sg.theme()
# ウインドウのレイアウトの作成
# レイアウトはグリッド（2次元リスト）で表現される
layout = []

# モーションボタンのレイアウト
layout.append(
    [
        sg.Button('いらっしゃいませ', key='start'),
        sg.Button('ポーズリセット', key='reset')
    ]
)

layout.append(
    [
        sg.Text("注文内容確認", size=(50, 1))
    ]
)

# 発話ボタンのレイアウト
layout.append(
    [
        sg.Button('お水', key='water'),
        sg.Button('お茶', key='tea')
    ]
)

layout.append(
    [
        sg.Text("確認後のアクション", size=(50, 1))
    ]
)

layout.append(
    [
        sg.Button('席案内', key='seat'),
        sg.Button('ありがとう', key='thank'),
        sg.Button('注文聞き間違い', key="order_miss")
    ]
)
layout.append(
    [
        sg.Text("その他の会話時に使用", size=(50, 1))
    ]
)

# テキストの自由入力
layout.append(
    [
        sg.InputText(key='free_speech_field', size=(50, 1)),
        sg.Button('発話', key='speak_free')
    ]
)


# ウインドウにレイアウトを設定
window = sg.Window('CommU controller for counter', layout)

# Event loop
while True:
    event, values = window.read(timeout=1)
    if event is None:
        print('Window event is None. exit')
        break

    elif event == 'start':
        # お辞儀して「いらっしゃいませ」という
        servo_map = dict(BODY_P=1, HEAD_P=23)
        pose = dict(Msec=500, ServoMap=servo_map)
        rt.play_pose(pose)
        d = rt.say_text("いらっしゃいませ。")
        time.sleep(d)

        # ポーズを元に戻す
        pose = dict(Msec=500, ServoMap=reset_servo_map)
        rt.play_pose(pose)

        # 注文を聞く
        d = rt.say_text("ご注文をお伺いします。")
        time.sleep(d)


    elif event == 'water':
        d = rt.say_text("ご注文はお水でお間違い無いでしょうか？")
        m = rt.make_beat_motion(d)
        rt.play_motion(m)

    elif event == 'tea':
        d = rt.say_text("ご注文はお茶でお間違い無いでしょうか？")
        m = rt.make_beat_motion(d)
        rt.play_motion(m)


    elif event == 'seat':
        d = rt.say_text("承知いたしました。")
        m = rt.make_beat_motion(d)
        rt.play_motion(m)
        time.sleep(d)

        d = rt.say_text("それでは")
        time.sleep(d)

        servo_map = dict(BODY_Y=20,  L_SHOU_P=-20, L_SHOU_R=-20)
        pose = dict(Msec=500, ServoMap=servo_map)
        rt.play_pose(pose)
        d = rt.say_text("あちらのお席でお待ちくださいませ。")
        time.sleep(d)

        # ポーズリセット
        pose = dict(Msec=500, ServoMap=reset_servo_map)
        rt.play_pose(pose)

    elif event == 'thank':
        # お辞儀して「ありがとうございました」という
        servo_map = dict(BODY_P=1, HEAD_P=23)
        pose = dict(Msec=500, ServoMap=servo_map)
        rt.play_pose(pose)
        d = rt.say_text("ありがとうございました。")
        time.sleep(d)

        # ポーズを元に戻す
        pose = dict(Msec=500, ServoMap=reset_servo_map)
        rt.play_pose(pose)

    elif event == 'order_miss':
        # お辞儀して謝る
        servo_map = dict(BODY_P=1, HEAD_P=23)
        pose = dict(Msec=500, ServoMap=servo_map)
        rt.play_pose(pose)
        d = rt.say_text("大変失礼いたしました。")
        time.sleep(d)

        # ポーズを元に戻す
        pose = dict(Msec=500, ServoMap=reset_servo_map)
        rt.play_pose(pose)

        # もう一度注文を聞く
        d = rt.say_text("もう一度注文をお聞きしてもよろしいでしょうか？")
        m = rt.make_beat_motion(d)
        rt.play_motion(m)


    elif event == 'speak_free':
        d = rt.say_text(values['free_speech_field'])
        m = rt.make_beat_motion(d)
        rt.play_motion(m)


    elif event == 'reset':
        pose = dict(Msec=500, ServoMap=reset_servo_map)
        rt.play_pose(pose)
    else:
        pass

window.close()
