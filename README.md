CareCompanion

An Ai Solution Development Project

by

Jonathan James Thomas (222666X)
Chen Jinnan (224531M)
Jovan Chua (220700K)

All the images are in files labelled as <service-name> with the exception of main-flask

Use build and push after going into the folder directory using CD

minikube start

#create name space
kubectl apply -f namespace.yaml

#repeat for all services
docker build -t <docker-name>/<service-name>:<version> .
docker push <docker-name>/<service-name>:<version>
cd k8s
kubectl apply -f .
#done

once done pushing, 
ensure that all images have been built

to run everything use the automated script.
1  ./stop_services.sh
2  ./start_services.sh
#Ensure all pods are running:
3  kubectl get pods -n my-app
#In a Browser open:
http://127.0.0.1:8080/
http://localhost:8001/api/v1/namespaces/kubernetes-dashboard/services/https:kubernetes-dashboard:/proxy/#/workloads?namespace=my-app

#Obtain token for dashboard
kubectl -n kubernetes-dashboard create token kubernetes-dashboard


# For Augmenting User Traffic
hey -z 60s -c 100 http://127.0.0.1:8080

# For Rollout of New Version
for deploy in $(kubectl get deployments -n my-app -o jsonpath='{.items[*].metadata.name}'); do
  kubectl set image deployment/$deploy *=jonnehh/$deploy:v1 -n my-app
done

#Undo Rollout
for deploy in $(kubectl get deployments -n my-app -o jsonpath='{.items[*].metadata.name}'); do
  kubectl rollout undo deployment/$deploy -n my-app
done




