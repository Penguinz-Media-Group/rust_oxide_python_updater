#!/bin/bash
python3 --version
pip3 install zipfile38 requests
#sudo git clone --branch Development https://github.com/Penguinz-Media-Group/rust_oxide_python_updater.git /opt/rust
#chmod 777 /opt/rust
ansible-playbook -i localhost  /opt/rust/buildrustserver.yml


