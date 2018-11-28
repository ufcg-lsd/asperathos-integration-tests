#!/bin/bash

git clone https://github.com/ufcg-lsd/asperathos-monitor tmp/monitor

cd tmp/monitor

cat > monitor.cfg <<EOF
[general]
host = 0.0.0.0
port = 1501
plugins = openstack_generic
debug = True
retries = 5

EOF

./run.sh & # replace this with docker container
