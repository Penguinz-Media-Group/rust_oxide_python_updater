#!/bin/bash

if ! -d "/opt/rust" ; then
  git clone https://github.com/Penguinz-Media-Group/rust_oxide_python_updater.git /opt/rust
fi
if ! -f "/etc/systemd/rust.service"; then
  cp /opt/rust/rust.service /etc/systemd/rust.service
  systemctl enable rust.service
fi
# TODO add Ansible alternative for Premium
while :
do
  cd /opt/rust
  git fetch origin Development
  git reset --hard FETCH_HEAD
  chmod +x *.py *.sh
  echo "Updating Rust and Oxide"
  python3 updaterust.py
  echo "Installing Oxide Mod Bundles"
  python3 getmods.py
  echo "Starting Server"
  python3 runrust.py
  sleep 10
  echo "restarting"
done
