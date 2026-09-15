# R2D2 Voice Assistant

An R2D2-inspired AI voice assistant running on a Raspberry Pi 5, housed inside a 22cm tall 3D-printed miniature R2D2 model. Combines hardware (GPIO, OLED, LEDs, servo) with software (voice recognition, AI integration, text-to-speech, and a web dashboard) to create a functional, characterful desk companion.

## Features

- **Voice interaction** — speech recognition and natural language responses powered by Google Gemini
- **Text-to-speech** — character voice via ElevenLabs multilingual v2
- **OLED display** — 0.96" SSD1306 (I2C) showing clock, animations, and status
- **LED indicators** — GPIO-driven lighting for visual feedback
- **Skills** — modular add-ons including weather (OpenWeatherMap) and timers
- **Web dashboard** — Flask app on port 5000 showing system stats, clock, weather, and conversation log
- **Standby/idle mode** with looping animations

## Hardware

- Raspberry Pi 5 (4GB)
- SSD1306 OLED display (I2C, address `0x3C`)
- GPIO-connected LEDs
- Servo motor
- Adafruit HUSB238 USB-C PD board (product 5991) for power delivery to the Pi + servo


## Setup

### Prerequisites

```bash
sudo apt-get install portaudio19-dev
```

### Installation

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Key dependencies:
- `google-genai` — Gemini API client
- `gpiozero` + `lgpio` — GPIO control (required for Pi 5; `RPi.GPIO` is not supported)
- `adafruit-blinka` — for the `board` module used by the OLED
- `pyaudio` — audio I/O

### Configuration

Create a `.env` or edit `config.py` with your API keys:
- Google Gemini API key
- ElevenLabs API key
- OpenWeatherMap API key

### Running

```bash
python main.py
```

The web dashboard will be available at `http://<pi-ip>:5000`.

## Notes

- Pi 5 requires the `lgpio` pin factory for `gpiozero` — set via `GPIOZERO_PIN_FACTORY=lgpio` before any GPIO imports.
- `main.py` and `web/server.py` run as separate processes and share state through `state.json`.

## Roadmap

- [ ] Implement HUSB238 power delivery solution for stable power to Pi + servo

