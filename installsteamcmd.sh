#!/usr/bin/env bash
# This for Debian / Ubuntu

useradd -m steam

add-apt-repository multiverse
dpkg --add-architecture i386
apt update
apt install lib32gcc1 steamcmd -y

ln -s /usr/games/steamcmd /usr/local/bin/steamcmd