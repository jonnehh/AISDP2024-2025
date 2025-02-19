# CareCompanion

## An AI Solution Development Project

### by  
Jonathan James Thomas (222666X)  
Chen Jinnan (224531M)  
Jovan Chua (220700K)  

---

All the images are in files labelled as `<service-name>` with the exception of `main-flask`.

Use **build and push** after going into the folder directory using `cd`.

```bash
minikube start
```

### Create Namespace

```bash
kubectl apply -f namespace.yaml
```

### Build and Push Docker Images (Repeat for All Services)

```bash
docker build -t <docker-name>/<service-name>:<version> .
docker push <docker-name>/<service-name>:<version>
cd k8s
kubectl apply -f .
```

Once done pushing, ensure that all images have been built.

---

## Running the Application

To run everything, use the automated script:

```bash
./stop_services.sh
./start_services.sh
```

Ensure all pods are running:

```bash
kubectl get pods -n my-app
```

### In a Browser, Open:

- [http://127.0.0.1:8080/](http://127.0.0.1:8080/)
- [http://localhost:8001/api/v1/namespaces/kubernetes-dashboard/services/https:kubernetes-dashboard:/proxy/#/workloads?namespace=my-app](http://localhost:8001/api/v1/namespaces/kubernetes-dashboard/services/https:kubernetes-dashboard:/proxy/#/workloads?namespace=my-app)

### Obtain Token for Kubernetes Dashboard

```bash
kubectl -n kubernetes-dashboard create token kubernetes-dashboard
```

---

## Additional Commands

### For Augmenting User Traffic

```bash
hey -z 60s -c 100 http://127.0.0.1:8080
```

### For Rollout of New Version

```bash
for deploy in $(kubectl get deployments -n my-app -o jsonpath='{.items[*].metadata.name}'); do
  kubectl set image deployment/$deploy *=jonnehh/$deploy:v1 -n my-app
done
```

### Undo Rollout

```bash
for deploy in $(kubectl get deployments -n my-app -o jsonpath='{.items[*].metadata.name}'); do
  kubectl rollout undo deployment/$deploy -n my-app
done
```
