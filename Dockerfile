FROM ubuntu
MAINTAINER Penguinz Media Group LLC
RUN apt-get update && apt-get install -y python3 python3-pip git && apt-get clean
COPY upstart.sh /opt
CMD ["/opt/upstart.sh"]
COPY plugins.json /opt/rust
COPY rustpw.json /opt/rust
COPY rustconf.json /opt/rust
COPY LICENSE /opt/rust
CMD ["/opt/rust/rustserver.sh"]




