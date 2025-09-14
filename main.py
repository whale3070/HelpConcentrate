import time
import random
import os
import pandas as pd
from datetime import datetime
import pygame  # 用 pygame 播放音乐

# ===== 配置部分 =====
SOUND_FILE = "biVLA2vKtxVwSM4.mp3"   # 直接支持 mp3 / wav
FOCUS_DURATION = 90 * 60  # 专注 90 分钟 (秒)
BREAK_DURATION = 20 * 60  # 休息 20 分钟 (秒)
MIN_INTERVAL = 3 * 60     # 最短提示间隔 (3分钟, 秒)
MAX_INTERVAL = 5 * 60     # 最长提示间隔 (5分钟, 秒)
LOG_FILE = "focus_log.csv"

# 初始化日志文件
if not os.path.exists(LOG_FILE):
    df = pd.DataFrame(columns=["start_time", "end_time", "duration_minutes"])
    df.to_csv(LOG_FILE, index=False)

# 初始化 pygame 音频
pygame.mixer.init()

def play_sound_background(file):
    """开始播放音乐，并在后台随机10-30秒后自动停止"""
    pygame.mixer.music.load(file)
    pygame.mixer.music.play()

    play_time = random.randint(10, 30)

    # 启动一个后台定时器来停止音乐
    def stop_music_after_delay(delay):
        time.sleep(delay)
        pygame.mixer.music.stop()
        print(f"🎵 音乐已播放 {delay} 秒后停止")

    import threading
    threading.Thread(target=stop_music_after_delay, args=(play_time,), daemon=True).start()

def log_focus_session(start, end):
    duration = (end - start).seconds // 60
    df = pd.read_csv(LOG_FILE)
    new_entry = pd.DataFrame([{
        "start_time": start.strftime("%Y-%m-%d %H:%M:%S"),
        "end_time": end.strftime("%Y-%m-%d %H:%M:%S"),
        "duration_minutes": duration
    }])
    df = pd.concat([df, new_entry], ignore_index=True)
    df.to_csv(LOG_FILE, index=False)
    print(f"✅ 已记录专注 {duration} 分钟")

def summary_stats():
    df = pd.read_csv(LOG_FILE)
    if df.empty:
        print("暂无打卡记录。")
        return
    total = df["duration_minutes"].sum()
    sessions = len(df)
    avg = total / sessions
    print("📊 专注统计：")
    print(f"- 总专注时长：{total} 分钟")
    print(f"- 总打卡次数：{sessions}")
    print(f"- 平均每次专注：{avg:.1f} 分钟")

def focus_session():
    print("🎯 开始 90 分钟专注，请保持投入！")
    start_time = datetime.now()
    end_time = start_time + pd.Timedelta(seconds=FOCUS_DURATION)

    while datetime.now() < end_time:
        wait_time = random.randint(MIN_INTERVAL, MAX_INTERVAL)
        time.sleep(wait_time)

        play_sound_background(SOUND_FILE)
        print("🔔 音乐响起！请闭眼休息 10 秒...")
        time.sleep(10)

    log_focus_session(start_time, datetime.now())
    print(f"⏸️ 请休息 {BREAK_DURATION // 60} 分钟...")
    time.sleep(BREAK_DURATION)

if __name__ == "__main__":
    try:
        while True:
            focus_session()
            summary_stats()
    except KeyboardInterrupt:
        print("\n🛑 已手动退出。")
        summary_stats()
