import subprocess
import time
import requests
import socket
import datetime
import os

# === CONFIG ===
WEBHOOK_URL = "https://chat.googleapis.com/v1/spaces/AAQA0UnHlxE/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=V__HctzSudwX-qabltNnQ6n0mU61xdFtMzhRiF2ktrY"

pi_nodes = {
    "Tru 1": "192.168.103.201",
    "Tru 2": "192.168.103.202",
    "Tru 3": "192.168.103.203",
    "Tru 4": "192.168.103.204"
}

# === DETECT SELF ===
local_ip = socket.gethostbyname(socket.gethostname())
last_status = {ip: True for ip in pi_nodes.values()}

# === LOGGING ===
log_folder = "/home/pi/pimonitor_logs"
os.makedirs(log_folder, exist_ok=True)

def get_log_path():
    today = datetime.date.today().strftime("%Y-%m-%d")
    return os.path.join(log_folder, f"log_{today}.log")

def log(msg):
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    full_msg = f"[{timestamp}] {msg}"
    print(full_msg)
    with open(get_log_path(), "a") as f:
        f.write(full_msg + "\n")

# === PING FUNCTION ===
def ping(ip):
    try:
        subprocess.check_output(['ping', '-c', '1', '-W', '1', ip], stderr=subprocess.DEVNULL)
        return True
    except subprocess.CalledProcessError:
        return False

# === ALERT FUNCTION ===
def send_google_chat_alert(msg):
    payload = {"text": msg}
    try:
        requests.post(WEBHOOK_URL, json=payload)
    except Exception as e:
        log(f"Lỗi gửi Google Chat: {e}")

# === MONITOR LOOP ===
while True:
    for name, ip in pi_nodes.items():
        if ip == local_ip:
            continue
        log(f"Đang ping: {name} ({ip})...")
        status = ping(ip)
        if not status and last_status[ip]:
            msg = f"⚠️ CẢNH BÁO: Thiết bị **{name} ({ip})** mất kết nối!"
            log(msg)
            send_google_chat_alert(msg)
        elif status and not last_status[ip]:
            msg = f"✅ ĐÃ KHÔI PHỤC: Thiết bị **{name} ({ip})** đã online lại."
            log(msg)
            send_google_chat_alert(msg)
        last_status[ip] = status
    time.sleep(10)
