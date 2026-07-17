from flask import Flask, render_template, jsonify, request
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from state import state, get_system_stats
from skills import weather
from skills.timer import get_time_raw, get_date_raw

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/status')
def get_status():
    stats = get_system_stats()
    return jsonify({
        **state,
        **stats,
    })

@app.route('/api/clock')
def get_clock():
    return jsonify({
        "time": get_time_raw(),
        "date": get_date_raw(),
    })

@app.route('/api/weather')
def get_weather():
    return jsonify({
        "weather": weather.get_weather()
    })

@app.route('/api/reset_memory', methods=['POST'])
def reset_memory():
    from brain import reset_chat
    reset_chat()
    state["conversation_history"] = []
    return jsonify({"success": True})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)