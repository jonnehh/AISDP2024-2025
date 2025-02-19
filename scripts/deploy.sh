#!/bin/bash

NAMESPACE=my-app

# 创建命名空间（如果还没有）
kubectl apply -f namespace.yaml

# 应用主 Flask 配置
kubectl apply -f main-flask/deployment.yaml -n $NAMESPACE
kubectl apply -f main-flask/service.yaml -n $NAMESPACE
kubectl apply -f main-flask/hpa.yaml -n $NAMESPACE
kubectl apply -f main-flask/pdb.yaml -n $NAMESPACE

# 应用 OCR 服务配置
kubectl apply -f ocr-service/deployment.yaml -n $NAMESPACE
kubectl apply -f ocr-service/service-svc.yaml -n $NAMESPACE
kubectl apply -f ocr-service/hpa.yaml -n $NAMESPACE
kubectl apply -f ocr-service/pdb.yaml -n $NAMESPACE
kubectl apply -f ocr-service/network-policy.yaml -n $NAMESPACE

# 应用 RAG 服务配置
kubectl apply -f rag-service/deployment.yaml -n $NAMESPACE
kubectl apply -f rag-service/service-svc.yaml -n $NAMESPACE
kubectl apply -f rag-service/hpa.yaml -n $NAMESPACE
kubectl apply -f rag-service/pdb.yaml -n $NAMESPACE
kubectl apply -f rag-service/network-policy.yaml -n $NAMESPACE
