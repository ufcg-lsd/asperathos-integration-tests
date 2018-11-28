#!/bin/bash

git clone https://github.com/ufcg-lsd/asperathos-manager tmp/manager

cd tmp/manager

cat > manager.cfg <<EOF
[general]
host = 0.0.0.0
port = 1500
plugins = kubejobs

[services]
controller_url = http://0.0.0.0:1502
monitor_url = http://0.0.0.0:1501
optimizer_url = http://0.0.0.0:5002
authorization_url = http://0.0.0.0:5003

[kubejobs]
k8s_conf_path = ~/.kube/config
redis_ip = 
count_queue = :30666
EOF

./run.sh & # replace this with docker container
