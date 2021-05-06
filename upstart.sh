#!/bin/bash
python3 --version
pip3 install zipfile38 requests
git clone --branch Development https://github.com/Penguinz-Media-Group/rust_oxide_python_updater.git /opt/rust
ansible-playbook -i localhost  /opt/rust/buildrustserver.yml


