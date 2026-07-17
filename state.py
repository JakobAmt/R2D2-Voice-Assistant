import psutil
import subprocess
from datetime import datetime

# Shared state between main.py and web server
state = {
    "status": "standby",
    "last_command": "",
    "last_response": "",
    "conversation_history": [],
}

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
        "memory_used": round(psutil.virtual_memory().used / (1024**3), 2),
        "memory_total": round(psutil.virtual_memory().total / (1024**3), 2),
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

def add_to_history(role, message):
    state["conversation_history"].append({
        "role": role,
        "message": message,
        "time": datetime.now().strftime("%H:%M:%S")
    })
    # Keep last 20 entries
    if len(state["conversation_history"]) > 20:
        state["conversation_history"].pop(0)