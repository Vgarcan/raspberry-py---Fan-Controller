#!/usr/bin/env python3
# ========================================================
# test_fan_controller.py
# Tester script for FanSpeedInstaller Project
# Safely stops systemd service, tests fan speeds, and restarts the service.
# Author: Victor GC (XEMIPROJECTS)
# ========================================================

import time
import os
import sys
import subprocess
import logging

# Configuration
FAN_GPIO_PIN = 18
PWM_FREQUENCY = 100
SLEEP_BETWEEN_CHANGES = 3  # Seconds between speed changes
NUMBER_OF_CYCLES = 2
SERVICE_NAME = "fan_controller.service"
LOG_FILE_PATH = os.path.join(os.path.dirname(
    os.path.dirname(__file__)), "logs", "fan_test.log")

# Setup logging
try:
    os.makedirs(os.path.dirname(LOG_FILE_PATH), exist_ok=True)
except Exception as e:
    print(f"[ERROR] Failed to create log directory: {e}")
    sys.exit(1)

logging.basicConfig(
    filename=LOG_FILE_PATH,
    filemode='w',
    format='%(asctime)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    level=logging.INFO
)

# Detect Raspberry Pi model


def detect_pi_model():
    try:
        with open("/proc/device-tree/model", "r") as model_file:
            model = model_file.read().strip()
            return model
    except Exception as e:
        logging.error(f"Failed to detect Raspberry Pi model: {e}")
        return ""


PI_MODEL = detect_pi_model()

# Flags
USE_LGPIO = False
USE_RPI_GPIO = False

# Import appropriate library
try:
    if "Raspberry Pi 5" in PI_MODEL:
        import lgpio
        USE_LGPIO = True
        logging.info("Detected Raspberry Pi 5: using lgpio library for test.")
    else:
        import RPi.GPIO as GPIO
        USE_RPI_GPIO = True
        logging.info(f"Detected {PI_MODEL}: using RPi.GPIO library for test.")
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

# Systemd management functions


def stop_service():
    try:
        subprocess.run(["sudo", "systemctl", "stop", SERVICE_NAME], check=True)
        print(f"[INFO] Service {SERVICE_NAME} stopped.")
        logging.info(f"Service {SERVICE_NAME} stopped before test.")
    except subprocess.CalledProcessError:
        print(f"[WARNING] Could not stop {SERVICE_NAME} (maybe not running).")
        logging.warning(f"Could not stop {SERVICE_NAME} (maybe not running).")


def start_service():
    try:
        subprocess.run(["sudo", "systemctl", "start",
                       SERVICE_NAME], check=True)
        print(f"[INFO] Service {SERVICE_NAME} restarted.")
        logging.info(f"Service {SERVICE_NAME} restarted after test.")
    except subprocess.CalledProcessError:
        print(f"[ERROR] Failed to restart {SERVICE_NAME}.")
        logging.error(f"Failed to restart {SERVICE_NAME}.")

# Set fan speed


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


# Start of the script
try:
    print("[INFO] Starting Fan Controller Test...")
    logging.info("Starting Fan Controller Test...")

    # Stop the service first
    stop_service()

    fan_speeds = [0, 30, 50, 70, 100]

    for cycle in range(1, NUMBER_OF_CYCLES + 1):
        print(f"[INFO] Starting test cycle {cycle}")
        logging.info(f"Starting test cycle {cycle}")

        for speed in fan_speeds:
            print(f"[TEST] Setting fan speed to {speed}%")
            logging.info(f"Setting fan speed to {speed}%")
            set_fan_speed(speed)
            time.sleep(SLEEP_BETWEEN_CHANGES)

    # After test, turn fan off
    set_fan_speed(0)
    print("[INFO] Test completed. Turning fan off.")
    logging.info("Test completed. Turning fan off.")

except KeyboardInterrupt:
    print("\n[INFO] Test interrupted by user.")
    logging.info("Test interrupted by user.")
    set_fan_speed(0)

except Exception as e:
    logging.error(f"Unexpected error during test: {e}")
    set_fan_speed(0)

finally:
    # Clean up GPIOs
    if USE_LGPIO:
        lgpio.gpiochip_close(gpio_chip)
    elif USE_RPI_GPIO:
        fan_pwm.stop()
        GPIO.cleanup()

    # Restart the service
    start_service()

    print("[INFO] Fan Controller Test completed successfully.")
    logging.info("Fan Controller Test completed successfully.")
