FROM Ubuntu
MAINTAINER Penguinz Media Group LLC
RUN apt-get update apt-get install -y python3 && apt-get clean
COPY ../
