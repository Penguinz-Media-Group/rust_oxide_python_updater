#!/bin/bash

# TODO add Ansible alternative for Premium
while :
do
  cd /opt/
  git clone https://github.com/Penguinz-Media-Group/rust_oxide_python_updater.git rust
  cd /opt/rust
  python3 updaterust.py
  python3 updateoxide.py
  python3 runrust.py
  sleep 10
done
