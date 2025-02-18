#!/bin/bash

# Stop port-forward processes
if [ -f port_forward_pids.txt ]; then
    read pid1 pid2 pid3 pid4 pid5 pid6 pid7 < port_forward_pids.txt
    echo "Stopping port-forward processes..."
    kill $pid1 $pid2 $pid3 $pid4 $pid5 $pid6 $pid7
    rm port_forward_pids.txt
    echo "Processes stopped successfully."
    minikube stop
    echo "Stopped Minikube"
else
    echo "No running processes found."
fi
