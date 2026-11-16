#!/usr/bin/env python3
"""SG90 test using hardware PWM on GPIO18 (Pi 5)."""
from time import sleep
from rpi_hardware_pwm import HardwarePWM

# Pi 5: GPIO18 = PWM channel 2. Chip is 0 on newer kernels (6.12+), 2 on older.
# Check `ls /sys/class/pwm/` if this fails.
PWM_CHANNEL = 2
PWM_CHIP = 0
FREQ = 50  # Hz -> 20 ms period

MIN_PULSE_MS = 0.5
MAX_PULSE_MS = 2.4

pwm = HardwarePWM(pwm_channel=PWM_CHANNEL, hz=FREQ, chip=PWM_CHIP)

def angle_to_duty(angle):
    """Map -90..90 degrees to duty cycle percent."""
    angle = max(-90, min(90, angle))
    pulse_ms = MIN_PULSE_MS + (angle + 90) / 180 * (MAX_PULSE_MS - MIN_PULSE_MS)
    return pulse_ms / 20 * 100

def set_angle(angle):
    pwm.change_duty_cycle(angle_to_duty(angle))

try:
    pwm.start(angle_to_duty(0))
    sleep(1)

    print("Step test")
    for a in (-90, 0, 90, 0):
        print(f"  {a:>4}°")
        set_angle(a)
        sleep(1)

    print("Sweep test")
    for _ in range(2):
        for a in list(range(-90, 91, 5)) + list(range(90, -91, -5)):
            set_angle(a)
            sleep(0.03)

    set_angle(0)
    print("Holding at 0° for 5 s — watch for jitter")
    sleep(5)
except KeyboardInterrupt:
    pass
finally:
    pwm.stop()
    print("Done")