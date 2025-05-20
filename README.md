
# Pi Node Monitor - Google Chat Alert

A lightweight Python script to monitor Raspberry Pi devices on a local network.  
When a node goes offline (ping failure), it sends real-time alerts to a Google Chat room via webhook integration.

---

## 📦 Features

- Periodically pings a list of target Pi nodes
- Logs device status with timestamps
- Sends alerts to Google Chat on connection loss or recovery
- Runs in the background as a systemd service on Linux

---

## 🧾 Project Structure

```
├── ping_monitor_chat.py       # Main monitoring script
├── pimonitor.service          # systemd service unit file
└── pimonitor_logs/            # Auto-generated logs folder
```

---

## ⚙️ Requirements

- Python 3
- `requests` library (`pip install requests`)
- Linux (Raspberry Pi OS or any Debian-based distro)

---

## 🚀 Setup Guide

### 1. Configure target IP addresses

Edit `ping_monitor_chat.py` and set the IPs of the Pi devices to monitor:

```python
pi_nodes = {
    "Pole 1": "192.168.103.201",
    "Pole 2": "192.168.103.202",
    ...
}
```

> The script auto-detects its own IP and skips self-ping.

---

### 2. Set your Google Chat webhook

Replace `WEBHOOK_URL` in `ping_monitor_chat.py` with your actual webhook URL.

How to get a webhook:
- Go to Google Chat → Add a webhook integration to your space
- Copy the generated webhook URL and paste it in the script

---

### 3. Enable auto-run with systemd

Copy the service file to system directory:

```bash
sudo cp pimonitor.service /etc/systemd/system/
sudo systemctl daemon-reexec
sudo systemctl enable pimonitor
sudo systemctl start pimonitor
```

---

## 📂 Logs

- Logs are saved daily under `/home/pi/pimonitor_logs/`
- Each entry includes timestamped messages for every ping attempt and alert status

---

## 🛑 Notes

- Ping interval is set to every 10 seconds
- If a device goes offline, an alert is sent once
- If it comes back online, a recovery message is sent

---

## 👨‍💻 Author

Phieu-Tran
