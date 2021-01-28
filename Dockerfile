FROM ubuntu
MAINTAINER Penguinz Media Group LLC
RUN apt-get update && apt-get install -y python3 python3-pip git && apt-get clean
ENV host_ip=0.0.0.0
ENV server_port=28015
ENV rcon_port=28016
ENV player_cap=125
ENV server_name="PMGBuiltServer"
ENV seed=404
ENV worldsize=3000
ENV server_desc="A PMG Server! https://penguinzmedia.group/rust"
ENV server_img="https://cdn.cloudflare.steamstatic.com/steam/apps/252490/header.jpg?t=1608404151"
ENV server_url="https://penguinzmedia.group/rust"
ENV logfile="stdout"
ENV modded=1
COPY upstart.sh /opt
CMD ["/opt/upstart.sh"]
COPY plugins.json /opt/rust
COPY rustpw.json /opt/rust
COPY rustconf.json /opt/rust
COPY LICENSE /opt/rust
CMD ["/opt/rust/rustserver.sh"]




