#!/bin/bash
aws ecr get-login-password --region sa-east-1 | docker login --username AWS --password-stdin 963485456147.dkr.ecr.sa-east-1.amazonaws.com  # Login
# aws ecr create-repository  --region sa-east-1 --repository-name sii-erut-qr-manager --image-tag-mutability MUTABLE --image-scanning-configuration scanOnPush=false  # Build ECRepo
docker build -t sii-erut-qr-manager:latest .
docker tag sii-erut-qr-manager:latest 963485456147.dkr.ecr.sa-east-1.amazonaws.com/sii-erut-qr-manager
docker push 963485456147.dkr.ecr.sa-east-1.amazonaws.com/sii-erut-qr-manager