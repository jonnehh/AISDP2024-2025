#!/bin/bash

# Start Minikube if not running
echo "Starting Minikube..."
minikube status | grep -q "Running"
if [ $? -ne 0 ]; then
    minikube start
else
    echo "Minikube is already running."
fi

# Run port-forward commands in the background
echo "Starting port-forwarding..."
kubectl port-forward svc/ocr-service-svc 5001:5000 -n my-app &
pid1=$!

kubectl port-forward svc/rag-service-svc 5050:5050 -n my-app &
pid2=$!

kubectl port-forward svc/main-flask-service 8080:80 -n my-app &
pid3=$!

kubectl port-forward svc/food-service-svc 5080:5080 -n my-app &
pid4=$!

kubectl proxy &
pid5=$!

kubectl port-forward svc/flask-data-server 6050:6050 -n my-app &
pid6=$!

kubectl port-forward svc/voice2text-service-svc 6000:6000 -n my-app &
pid7=$!
# Save PIDs to a file for later stopping
echo $pid1 $pid2 $pid3 $pid4 $pid5 > port_forward_pids.txt

echo "All services are running. Access them at:"
echo "- OCR Service: http://localhost:5001"
echo "- RAG Service: http://localhost:5050"
echo "- Flask Service: http://localhost:8080"
echo "- Food Service: http://localhost:5080"

kubectl -n kubernetes-dashboard create token kubernetes-dashboard

exit 0
