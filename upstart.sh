#!/bin/bash
pip3 install zipfile requests
if ! -d "/opt/rust" ; then
  git clone https://github.com/Penguinz-Media-Group/rust_oxide_python_updater.git /opt/rust
fi

