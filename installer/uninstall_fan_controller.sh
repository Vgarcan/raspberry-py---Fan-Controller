#!/bin/bash
# ========================================================
# uninstall_fan_controller.sh
# Uninstaller for FanSpeedInstaller Project
# Safely removes the Fan Controller systemd service and all installed files.
# Author: Victor GC (XEMIPROJECTS)
# ========================================================

clear

echo ""
echo "========================================"
echo "        Fan Controller Uninstaller"
echo "========================================"
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

# Stop the systemd service
echo "[INFO] Stopping service if running..."
sudo systemctl stop fan_controller.service 2>/dev/null

# Disable the service
echo "[INFO] Disabling service..."
sudo systemctl disable fan_controller.service 2>/dev/null

# Remove the systemd service file
if [ -f "$SERVICE_FILE" ]; then
    echo "[INFO] Removing systemd service file..."
    sudo rm "$SERVICE_FILE"
else
    echo "[WARNING] Service file not found, skipping..."
fi

# Reload systemd to apply changes
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
