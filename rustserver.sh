#!/bin/bash

if [ ! -d "/path/to/dir" ]
then
  git clone https://github.com/Penguinz-Media-Group/rust_oxide_python_updater.git /opt/rust
fi
# TODO add Ansible alternative for Premium
while :
do
  cd /opt/rust
  git pull
  python3 updaterust.py
  python3 updateoxide.py
  python3 runrust.py
  sleep 10
done
