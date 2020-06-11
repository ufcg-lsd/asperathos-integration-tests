#!/bin/bash

KUBE_CONF_FILE=$1

kubectl --kubeconfig=$KUBE_CONF_FILE delete job --all

services=`kubectl --kubeconfig=$KUBE_CONF_FILE get services | awk '{print $1}' | grep -E "influx|grafana|redis"`

pods=`kubectl --kubeconfig=$KUBE_CONF_FILE get pods | awk '{print $1}' | grep -E "influx|grafana|redis"`

if [[ ! -z "$services" ]]
then 
	kubectl --kubeconfig=$KUBE_CONF_FILE delete services $services
fi

if [[ ! -z "$pods" ]]
then 
	kubectl --kubeconfig=$KUBE_CONF_FILE delete pods $pods
fi

