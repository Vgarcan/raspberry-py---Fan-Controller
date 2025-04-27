#!/usr/bin/env python3
# ========================================================
# fan_controller.py
# Main script to control the fan based on CPU temperature.
# Automatically adapts to the Raspberry Pi model.
# Author: Victor GC (XEMIPROJECTS)
# ========================================================

import time
import os
import sys
import logging

# Configuration
FAN_GPIO_PIN = 18               # GPIO pin where the fan is connected
PWM_FREQUENCY = 100             # PWM frequency (Hz)
CHECK_INTERVAL_SEC = 5          # Time between temperature checks (seconds)
LOG_FILE_PATH = os.path.join(os.path.dirname(
    __file__), "logs", "fan_controller.log")

# Setup Logging
try:
    os.makedirs(os.path.dirname(LOG_FILE_PATH), exist_ok=True)
except Exception as e:
    print(f"[ERROR] Failed to create log directory: {e}")
    sys.exit(1)

logging.basicConfig(
    filename=LOG_FILE_PATH,
    filemode='a',
    format='%(asctime)s - Temp: %(message)s°C - Fan: %(levelname)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    level=logging.INFO
)

# Function to detect Raspberry Pi model


def detect_pi_model():
    try:
        with open("/proc/device-tree/model", "r") as model_file:
            model = model_file.read().strip()
            return model
    except Exception as e:
        logging.error(f"Failed to detect Raspberry Pi model: {e}")
        return ""


PI_MODEL = detect_pi_model()

# Flags to control which library is being used
USE_LGPIO = False
USE_RPI_GPIO = False

# Try to import the appropriate library based on the model
try:
    if "Raspberry Pi 5" in PI_MODEL:
        import lgpio
        USE_LGPIO = True
        logging.info("Detected Raspberry Pi 5: using lgpio library.")
    else:
        import RPi.GPIO as GPIO
        USE_RPI_GPIO = True
        logging.info(f"Detected {PI_MODEL}: using RPi.GPIO library.")
except ImportError as e:
    logging.error(f"Failed to import GPIO library: {e}")
    sys.exit(1)

# GPIO Setup
if USE_LGPIO:
    try:
        gpio_chip = lgpio.gpiochip_open(0)
        lgpio.gpio_claim_output(gpio_chip, FAN_GPIO_PIN)
    except Exception as e:
        logging.error(f"Failed to setup lgpio: {e}")
        sys.exit(1)
elif USE_RPI_GPIO:
    try:
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(FAN_GPIO_PIN, GPIO.OUT)
        fan_pwm = GPIO.PWM(FAN_GPIO_PIN, PWM_FREQUENCY)
        fan_pwm.start(0)
    except Exception as e:
        logging.error(f"Failed to setup RPi.GPIO: {e}")
        sys.exit(1)

# Function to get CPU temperature


def get_cpu_temperature():
    try:
        temp_str = os.popen("vcgencmd measure_temp").readline()
        return float(temp_str.replace("temp=", "").replace("'C\n", ""))
    except Exception as e:
        logging.error(f"Failed to read CPU temperature: {e}")
        return 0.0

# Function to set fan speed


def set_fan_speed(duty_cycle_percent):
    try:
        if USE_LGPIO:
            period_us = int(1_000_000 / PWM_FREQUENCY)
            duty_us = int(period_us * duty_cycle_percent / 100)
            lgpio.tx_pwm(gpio_chip, FAN_GPIO_PIN, period_us, duty_us)
        elif USE_RPI_GPIO:
            fan_pwm.ChangeDutyCycle(duty_cycle_percent)
    except Exception as e:
        logging.error(f"Failed to set fan speed: {e}")

# Function to determine fan speed based on temperature


def determine_fan_speed(temp_celsius):
    if temp_celsius < 40:
        return 0
    elif temp_celsius < 50:
        return 30
    elif temp_celsius < 60:
        return 50
    elif temp_celsius < 70:
        return 70
    else:
        return 100


# Main execution
try:
    logging.info("Fan Controller started.")
    print("[INFO] Fan Controller started successfully.")

    while True:
        cpu_temp = get_cpu_temperature()
        fan_speed = determine_fan_speed(cpu_temp)

        set_fan_speed(fan_speed)

        if fan_speed == 0:
            fan_status = "OFF"
        else:
            fan_status = f"{fan_speed}%"

        logging.info(f"{cpu_temp} - {fan_status}")
        time.sleep(CHECK_INTERVAL_SEC)

except KeyboardInterrupt:
    print("\n[INFO] Fan Controller stopped manually.")
    logging.info("Stopped manually.")
    if USE_LGPIO:
        lgpio.gpiochip_close(gpio_chip)
    elif USE_RPI_GPIO:
        fan_pwm.stop()
        GPIO.cleanup()
    sys.exit(0)

except Exception as e:
    logging.error(f"Unexpected error: {e}")
    if USE_LGPIO:
        lgpio.gpiochip_close(gpio_chip)
    elif USE_RPI_GPIO:
        fan_pwm.stop()
        GPIO.cleanup()
    sys.exit(1)
