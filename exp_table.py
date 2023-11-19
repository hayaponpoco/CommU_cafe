import time
import PySimpleGUI as sg
from robottools import RobotTools

rt = RobotTools('192.168.11.18', 22222)
servo_map = dict(BODY_Y=0, MOUTH=1, L_SHOU_R=0, BODY_P=-2, R_EYE_Y=5, L_EYE_Y=-5,
                EYELID=-2, HEAD_R=0, R_SHOU_R=0, HEAD_P=0, EYES_P=0, R_SHOU_P=-43,
                L_SHOU_P=43, HEAD_Y=0)
pose = dict(Msec=500, ServoMap=servo_map)
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
        sg.Text("注文した品物のお届け", size=(50, 1))
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
        sg.Text("お届け後のアクション", size=(50, 1))
    ]
)

layout.append(
    [
        sg.Button('チップ案内', key='chip'),
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
window = sg.Window('Sota controller', layout)

# Event loop
while True:
    event, values = window.read(timeout=1)
    if event is None:
        print('Window event is None. exit')
        break

    elif event == 'water':
        d = rt.say_text("お待たせいたしました。お水でございます。ご注文された品は全てお揃いでしょうか？")
        m = rt.make_beat_motion(d)
        rt.play_motion(m)

    elif event == 'tea':
        d = rt.say_text("お待たせいたしました。お茶でございます。ご注文された品は全てお揃いでしょうか？")
        m = rt.make_beat_motion(d)
        rt.play_motion(m)


    elif event == 'chip':
        d = rt.say_text("承知いたしました。")
        m = rt.make_beat_motion(d)
        rt.play_motion(m)
        time.sleep(d)
        
        d = rt.say_text("それではごゆっくりお楽しみください。")
        servo_map = dict(BODY_P=1)
        pose = dict(Msec=500, ServoMap=servo_map)
        rt.play_pose(pose)
        time.sleep(d)
        
        # ポーズリセット
        servo_map = dict(BODY_Y=0, MOUTH=1, L_SHOU_R=0, BODY_P=-2, R_EYE_Y=5, L_EYE_Y=-5,
                        EYELID=-2, HEAD_R=0, R_SHOU_R=0, HEAD_P=0, EYES_P=0, R_SHOU_P=-43,
                        L_SHOU_P=43, HEAD_Y=0)
        pose = dict(Msec=500, ServoMap=servo_map)
        rt.play_pose(pose)
        
        d = rt.say_text("代金につきましては、")
        time.sleep(d)


        servo_map = dict(BODY_Y=20, L_SHOU_R=-20, L_SHOU_P=20)
        pose = dict(Msec=500, ServoMap=servo_map)
        rt.play_pose(pose)
        d = rt.say_text("こちらのテーブルのトレーにお支払いください。")
        time.sleep(d)

        # ポーズリセット
        servo_map = dict(BODY_Y=0, MOUTH=1, L_SHOU_R=0, BODY_P=-2, R_EYE_Y=5, L_EYE_Y=-5,
                        EYELID=-2, HEAD_R=0, R_SHOU_R=0, HEAD_P=0, EYES_P=0, R_SHOU_P=-43,
                        L_SHOU_P=43, HEAD_Y=0)
        pose = dict(Msec=500, ServoMap=servo_map)
        rt.play_pose(pose)

    elif event == 'order_miss':
        # お辞儀して謝る
        servo_map = dict(BODY_P=1)
        pose = dict(Msec=500, ServoMap=servo_map)
        rt.play_pose(pose)
        d = rt.say_text("大変失礼いたしました。")
        time.sleep(d)

        # ポーズを元に戻す
        servo_map = dict(BODY_P=-2)
        pose = dict(Msec=500, ServoMap=servo_map)
        rt.play_pose(pose)

        # もう一度注文を聞く
        d = rt.say_text("すぐに注文された品をお持ちしますのでもうしばらくお待ちください")
        m = rt.make_beat_motion(d)
        rt.play_motion(m)

    elif event == 'speak_free':
        d = rt.say_text(values['free_speech_field'])
        m = rt.make_beat_motion(d)
        rt.play_motion(m)

    elif event == 'start':
        # お辞儀して「いらっしゃいませ」という
        servo_map = dict(BODY_P=1)
        pose = dict(Msec=500, ServoMap=servo_map)
        rt.play_pose(pose)
        d = rt.say_text("いらっしゃいませ。")
        time.sleep(d)
        # ポーズを元に戻す
        servo_map = dict(BODY_P=-2)
        pose = dict(Msec=500, ServoMap=servo_map)
        rt.play_pose(pose)
        # 注文を聞く
        d = rt.say_text("ご注文をお伺いいたします。")
        time.sleep(d)

    elif event == 'thank':
        d = rt.say_text("この度はカフェをご利用いただき")
        time.sleep(d)
        # お辞儀して「ありがとうございました」という
        servo_map = dict(BODY_P=1)
        pose = dict(Msec=500, ServoMap=servo_map)
        rt.play_pose(pose)
        d = rt.say_text("ありがとうございました。")
        time.sleep(d)
        # ポーズを元に戻す
        servo_map = dict(BODY_P=-2)
        pose = dict(Msec=500, ServoMap=servo_map)
        rt.play_pose(pose)
        
        d = rt.say_text("またのご利用お待ちしております")
        m = rt.make_beat_motion(d)
        rt.play_motion(m)
        time.sleep(d)

    elif event == 'reset':
        servo_map = dict(BODY_Y=0, MOUTH=1, L_SHOU_R=0, BODY_P=-2, R_EYE_Y=5, L_EYE_Y=-5,
                        EYELID=-2, HEAD_R=0, R_SHOU_R=0, HEAD_P=0, EYES_P=0, R_SHOU_P=-43,
                        L_SHOU_P=43, HEAD_Y=0)
        pose = dict(Msec=500, ServoMap=servo_map)
        rt.play_pose(pose)
    else:
        pass

window.close()