#!/bin/bash

git clone https://github.com/ufcg-lsd/asperathos-controller tmp/controller

cd tmp/controller

cat > controller.cfg <<EOF
[general]
host = 0.0.0.0
port = 1502
actuator_plugins = kvm_io 
metric_source_plugins = monasca

[k8s_replicas]
k8s_manifest = ~/.kube/config
EOF

./run.sh & # replace this with docker container
