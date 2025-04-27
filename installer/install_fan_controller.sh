#!/bin/bash
# ========================================================
# install_fan_controller.sh
# Installer for FanSpeedInstaller Project
# Author: Victor GC (XEMIPROJECTS)
# ========================================================

clear

# ASCII Art Banner
ascii_art=(
"      ________                              _________                    "
"     /  _____/_____    _____   ____   ____  \\\\_   ___ \\\\  __ __  ______     "
"    /   \\\\  ___\\\\__  \\\\  /     \\\\_/ __ \\\\_/ __ \\\\ /    \\\\  \\\\/ |  |  \\\\/  ___/     "
"    \\\\    \\\\_\\\\  \\\\/ __ \\\\|  Y Y  \\\\  ___/\\\\  ___/ \\\\     \\\\____|  |  /\\\\___ \\\\      "
"     \\\\______  (____  /__|_|  /\\\\___  >\\\\___  > \\\\______  /|____//____  >     "
"            \\\\/     \\\\/      \\\\/     \\\\/     \\\\/         \\\\/            \\\\/      "
""
"    ______          _        ______                      _               "
"   |  ____|        (_)      |  ____|                    | |              "
"   | |__  __  ___   _  ___  | |__  _ __ _ __   ___  _ __ | |_  ___  _ __   "
"   |  __| \\\\ \\\\/ / | | |/ _ \\\\ |  __|| '__| '_ \\\\ / _ \\\\| '_ \\\\| __|/ _ \\\\| '__|  "
"   | |____ >  <| |_| |  __/ | |___| |  | |_) | (_) | | | | |_| (_) | |     "
"   |______/_/\\\\_\\\\__, |\\\\___| |______|_|  | .__/ \\\\___/|_| |_|\\\\__|\\\\___/|_|     "
"                  __/ |                | |                                "
"                 |___/                 |_|                                "
""
"            XEMIPROJECTS presents...                                      "
"            FanSpeedInstaller - Fan Controller Installer                  "
"         www.ineedtohirethisguy.com                                        "
)

# Print ASCII Art with slight animation
for line in "${ascii_art[@]}"
do
    echo "$line"
    sleep 0.08
done

sleep 1

# Detect current user
CURRENT_USER=$(whoami)
INSTALL_DIR="/home/$CURRENT_USER/scripts/fan_controller"

echo ""
echo "[INFO] Detected user: $CURRENT_USER"
echo "[INFO] Installation directory will be: $INSTALL_DIR"
echo ""

# Confirm before proceeding
read -p "[QUESTION] Ready to start installation? (y/n): " confirm
if [[ "$confirm" != "y" && "$confirm" != "Y" ]]; then
    echo "[CANCELLED] Installation aborted."
    exit 1
fi

# Detect Raspberry Pi model
MODEL=$(tr -d '\\0' < /proc/device-tree/model)
echo "[INFO] Raspberry Pi model detected: $MODEL"
echo ""

# Install necessary Python packages
echo "[INFO] Installing required Python packages..."
sudo apt update
if [[ "$MODEL" == *"Raspberry Pi 5"* ]]; then
    sudo apt install -y python3-lgpio
else
    sudo apt install -y python3-rpi.gpio
fi

# Create installation directories
echo "[INFO] Creating installation directories..."
mkdir -p "$INSTALL_DIR/logs"
mkdir -p "$INSTALL_DIR/tests"

# Copy scripts to installation directory
echo "[INFO] Copying project files..."
cp ./fan_controller.py "$INSTALL_DIR/fan_controller.py"
cp ./tests/test_fan_controller.py "$INSTALL_DIR/tests/test_fan_controller.py"
cp ./uninstall_fan_controller.sh "$INSTALL_DIR/uninstall_fan_controller.sh"
cp ./README.md "$INSTALL_DIR/README.md"

# Set correct permissions
echo "[INFO] Setting file permissions..."
sudo chown -R "$CURRENT_USER":"$CURRENT_USER" "$INSTALL_DIR"
chmod -R 755 "$INSTALL_DIR"

# Create systemd service
echo "[INFO] Creating systemd service..."
SERVICE_FILE="/etc/systemd/system/fan_controller.service"
sudo bash -c "cat <<EOF > $SERVICE_FILE
[Unit]
Description=Fan Controller Service
After=multi-user.target

[Service]
Type=simple
ExecStart=/usr/bin/python3 $INSTALL_DIR/fan_controller.py
Restart=on-failure
User=$CURRENT_USER
WorkingDirectory=$INSTALL_DIR
StandardOutput=append:$INSTALL_DIR/logs/fan_controller.log
StandardError=append:$INSTALL_DIR/logs/fan_controller.log

[Install]
WantedBy=multi-user.target
EOF"

# Reload and start systemd service
echo "[INFO] Enabling and starting fan_controller.service..."
sudo systemctl daemon-reload
sudo systemctl enable fan_controller.service
sudo systemctl start fan_controller.service

echo ""
echo "========================================"
echo "[SUCCESS] Installation complete!"
echo "[INFO] Fan Controller service is now running."
echo "[INFO] Logs available at: $INSTALL_DIR/logs/fan_controller.log"
echo "========================================"
