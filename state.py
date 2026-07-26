import psutil
import subprocess
import json
import os
from datetime import datetime

STATE_FILE = "/home/jakob/Desktop/r2d2/state.json"

def _load():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, 'r') as f:
            return json.load(f)
    return {
        "status": "standby",
        "last_command": "",
        "last_response": "",
        "conversation_history": []
    }

def _save(data):
    with open(STATE_FILE, 'w') as f:
        json.dump(data, f)

def get_state():
    return _load()

def set_status(status):
    data = _load()
    data["status"] = status
    _save(data)

def add_to_history(role, message):
    data = _load()
    data["last_command"] = message if role == "user" else data.get("last_command", "")
    data["last_response"] = message if role == "assistant" else data.get("last_response", "")
    data["conversation_history"].append({
        "role": role,
        "message": message,
        "time": datetime.now().strftime("%H:%M:%S")
    })
    if len(data["conversation_history"]) > 20:
        data["conversation_history"].pop(0)
    _save(data)

def reset_history():
    data = _load()
    data["conversation_history"] = []
    data["last_command"] = ""
    data["last_response"] = ""
    _save(data)

def get_cpu_temp():
    try:
        result = subprocess.run(['vcgencmd', 'measure_temp'], capture_output=True, text=True)
        temp = result.stdout.replace('temp=', '').replace("'C\n", '')
        return float(temp)
    except:
        return 0.0

def get_system_stats():
    return {
        "cpu_temp": get_cpu_temp(),
        "cpu_usage": psutil.cpu_percent(),
        "memory_usage": psutil.virtual_memory().percent,
        "uptime": get_uptime(),
    }

def get_uptime():
    try:
        with open('/proc/uptime', 'r') as f:
            seconds = float(f.readline().split()[0])
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        return f"{hours}h {minutes}m"
    except:
        return "unknown"