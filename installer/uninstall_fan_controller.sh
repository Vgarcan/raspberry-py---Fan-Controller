#!/bin/bash
# ========================================================
# uninstall_fan_controller.sh
# Uninstaller for FanSpeedInstaller Project (Ultra Pro Edition)
# Safely removes the Fan Controller systemd service and all installed files.
# Author: Victor GC (XEMIPROJECTS)
# ========================================================

clear

# ASCII Art mini

ascii_art=(
"                                                                                                                     "
"   ██████       ███████  ██       ███       ███████         ██       ██     ███  ████████   ███████   ██       ██   "
"   ██   ████    ██        ██     ███        ██    ███      ████      ██    ██    ██         ██    ███  ██     ██    "
"   ██      ██   ██         ██    ██         ██     ██     ███ ██     ██  ██      ██         ██     ██   ██   ██     "
"   ██      ██   ███████    ██   ██   █████  ████████      ██   ██    █████       ███████    ██    ███    ██ ██      "
"   ██      ██   ██          ██  ██   █████  ██     ███   ███   ███   ███ ███     ██         ███████       ███       "
"   ██    ███   ███          █████           ██      ██  ██      ██   ██    ██    ██         ██   ███      ███       "
"   ███████      ████████     ███            █████████  ███       ██  ██     ███  ████████   ██     ██     ███       "
"      
"       Fan Controller Uninstaller"                                                                                                               "
)

ascii_art=(
"██╗   ██╗███╗   ██╗██╗   ██╗██╗███╗   ██╗"
"██║   ██║████╗  ██║██║   ██║██║████╗  ██║"
"██║   ██║██╔██╗ ██║██║   ██║██║██╔██╗ ██║"
"╚██╗ ██╔╝██║╚██╗██║╚██╗ ██╔╝██║██║╚██╗██║"
" ╚████╔╝ ██║ ╚████║ ╚████╔╝ ██║██║ ╚████║"
"  ╚═══╝  ╚═╝  ╚═══╝  ╚═══╝  ╚═╝╚═╝  ╚═══╝"
""
"       Fan Controller Uninstaller"
)

for line in "${ascii_art[@]}"
do
    echo "$line"
    sleep 0.03
done

echo ""

# Detect current user
CURRENT_USER=$(whoami)
INSTALL_DIR="/home/$CURRENT_USER/scripts/fan_controller"
SERVICE_FILE="/etc/systemd/system/fan_controller.service"

# Confirm uninstallation
read -p "[QUESTION] Are you sure you want to uninstall Fan Controller? (y/n): " confirm
if [[ "$confirm" != "y" && "$confirm" != "Y" ]]; then
    echo "[CANCELLED] Uninstallation aborted."
    exit 1
fi

# Stop the systemd service if active
if systemctl is-active --quiet fan_controller.service; then
    echo "[INFO] Stopping active service..."
    sudo systemctl stop fan_controller.service
else
    echo "[INFO] Service not running, skipping stop..."
fi

# Disable the systemd service
if systemctl is-enabled --quiet fan_controller.service; then
    echo "[INFO] Disabling service..."
    sudo systemctl disable fan_controller.service
else
    echo "[INFO] Service already disabled or not found, skipping disable..."
fi

# Remove the systemd service file
if [ -f "$SERVICE_FILE" ]; then
    echo "[INFO] Removing systemd service file..."
    sudo rm "$SERVICE_FILE"
else
    echo "[WARNING] Service file not found, skipping removal..."
fi

# Reload systemd to apply changes
echo "[INFO] Reloading systemd daemon..."
sudo systemctl daemon-reload

# Remove the installation directory
if [ -d "$INSTALL_DIR" ]; then
    echo "[INFO] Removing installation directory..."
    rm -rf "$INSTALL_DIR"
else
    echo "[WARNING] Installation directory not found, skipping..."
fi

echo ""
echo "========================================"
echo "[SUCCESS] Fan Controller successfully uninstalled."
echo "========================================"
