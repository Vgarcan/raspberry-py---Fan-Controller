# 🌀 FanSpeedInstaller - Raspberry Pi Fan Controller
**Developed by Victor GC (XEMIPROJECTS)**  
Website: [ineedtohirethisguy.com](https://ineedtohirethisguy.com)

---

## 📋 Project Overview

FanSpeedInstaller is a lightweight and smart fan controller system for Raspberry Pi 3, 4, and 5.  
It automatically detects your device model and adjusts fan speed based on CPU temperature, ensuring optimal cooling and noise control.

---

## 📦 Project Structure

```
FanSpeedInstaller/
├── install_fan_controller.sh
├── uninstall_fan_controller.sh
├── fan_controller.py
├── README.md
├── logs/
│   └── (Log files will be generated here)
└── tests/
    └── test_fan_controller.py
```

---

## 🚀 How to Download and Install on Your Raspberry Pi

1. Open a terminal on your Raspberry Pi.
2. Clone this repository from GitHub:

```bash
git clone https://github.com/Vgarcan/raspberry-py---Fan-Controller.git
```

3. Navigate to the project folder:

```bash
cd raspberry-py---Fan-Controller
```

4. Make the installer script executable:

```bash
chmod +x install_fan_controller.sh
```

5. Run the installer:

```bash
./install_fan_controller.sh
```

6. Follow the on-screen instructions.  
The installer will:
- Install required Python packages based on your Raspberry Pi model.
- Create necessary directories (`logs/`, `tests/`).
- Deploy and start the systemd service (`fan_controller.service`).
- Set correct permissions automatically.

---

## ⚙️ How It Works

- The system checks the CPU temperature every 5 seconds.
- Based on the temperature, it adjusts the fan speed using PWM control:
  - < 40°C ➔ 0% speed (off)
  - 40–49°C ➔ 30% speed
  - 50–59°C ➔ 50% speed
  - 60–69°C ➔ 70% speed
  - ≥ 70°C ➔ 100% speed
- All activity is logged at:

```
/home/youruser/scripts/fan_controller/logs/fan_controller.log
```

---

## 🧪 How to Test the Fan

A professional tester is included to verify the fan controller.

1. Navigate to the `tests/` folder:

```bash
cd /home/youruser/scripts/fan_controller/tests/
```

2. Run the tester script:

```bash
python3 test_fan_controller.py
```

The tester will:
- Safely stop the running fan controller service.
- Cycle the fan through 0%, 30%, 50%, 70%, and 100% speeds.
- Perform two full cycles.
- Log everything at:

```
/home/youruser/scripts/fan_controller/logs/fan_test.log
```
- Automatically restart the fan controller service afterward.

---

## 🗑️ How to Uninstall

If you wish to completely remove the Fan Controller:

1. Navigate to the installed project folder:

```bash
cd /home/youruser/scripts/fan_controller/
```

2. Make the uninstaller script executable:

```bash
chmod +x uninstall_fan_controller.sh
```

3. Run the uninstaller:

```bash
./uninstall_fan_controller.sh
```

This will:
- Stop and disable the systemd service.
- Remove the systemd service file.
- Delete all related project files and logs.

---

## ⚠️ Important Notes

- You must have `sudo` permissions to install and uninstall the service.
- Fully tested on Raspberry Pi 3B+, 4B, and 5 models.
- Ensure your fan is properly connected to GPIO 18 (default pin).

---

## 🛠️ Future Improvements (Ideas)

- Automatic detection and configuration for different fan models.
- Web dashboard to monitor temperatures and fan speed in real-time.
- Configurable temperature-speed mapping through a config file.

---

## 📄 License

This project is licensed under the MIT License.
