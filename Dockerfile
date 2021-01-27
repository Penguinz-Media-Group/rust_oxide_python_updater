FROM Ubuntu
MAINTAINER Penguinz Media Group LLC
RUN apt-get update apt-get install -y python3 python3-pip && apt-get clean
COPY getmods.py
COPY runrust.py
COPY installsteamcmd.sh
COPY plugins.json
COPY upstart.sh
COPY rustpw.json
COPY rustconf.json
COPY LICENSE



