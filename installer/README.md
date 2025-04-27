# FanSpeedInstaller - Raspberry Pi Fan Controller
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

## 🚀 Installation Instructions

1. Open a terminal and navigate to the FanSpeedInstaller folder.
2. Make sure the installer script is executable:

```bash
chmod +x install_fan_controller.sh
```

3. Run the installer:

```bash
./install_fan_controller.sh
```

4. Follow the on-screen instructions.  
The installer will:
- Create necessary directories.
- Install required Python packages based on your Raspberry Pi model.
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
- All activity is logged at `/home/youruser/scripts/fan_controller/logs/fan_controller.log`.

---

## 🧪 How to Test the Fan

A professional tester is included!

1. Navigate to the `tests/` folder:

```bash
cd /home/youruser/scripts/fan_controller/tests/
```

2. Make sure the test script is executable:

```bash
chmod +x test_fan_controller.py
```

3. Run the test:

```bash
python3 test_fan_controller.py
```

What the tester does:
- Stops the running fan controller service.
- Cycles the fan through 0%, 30%, 50%, 70%, and 100% speeds.
- Performs two full cycles.
- Logs everything at `/home/youruser/scripts/fan_controller/logs/fan_test.log`.
- Automatically restarts the fan controller service afterward.

---

## 🗑️ Uninstallation Instructions

If you wish to completely remove the FanSpeedInstaller:

1. Make the uninstaller executable:

```bash
chmod +x uninstall_fan_controller.sh
```

2. Run the uninstaller:

```bash
./uninstall_fan_controller.sh
```

This will:
- Stop and disable the systemd service.
- Remove the systemd service file.
- Delete all related files and logs.

---

## ⚠️ Important Notes

- You must have `sudo` permissions to install/uninstall the service.
- Tested on Raspberry Pi 3B+, 4B, and 5.
- Ensure your fan is properly connected to the designated GPIO pin (default: GPIO 18).

---

## 🛠️ Future Improvements (Ideas)

- Automatic detection and configuration of different fan models.
- Web interface to monitor temperatures and fan status.
- Adjustable temperature-speed curves via configuration file.

---

## 📄 License

This project is licensed under the MIT License.

---
