#!/bin/bash

### Login
# $aws ecr get-login-password --region <REPOSITORY_REGION> | docker login --username AWS --password-stdin <REPOSITORY_URI>
aws ecr get-login-password --region sa-east-1 | docker login --username AWS --password-stdin 963485456147.dkr.ecr.sa-east-1.amazonaws.com

### Build docker image
# $docker image build -t <IMAGE_NAME>:<IMAGE_TAG> .
docker build -t sii-erut-qr-manager:latest .

### Tag docker image to ECR (map)
# $docker image tag <IMAGE_NAME>:<IMAGE_TAG>  <REPOSITORY_URI>:<IMAGE_TAG>
docker tag sii-erut-qr-manager:latest 963485456147.dkr.ecr.sa-east-1.amazonaws.com/sii-erut-qr-manager

#### Push docker image to ECR
# $docker image push <IMAGE_NAME[:TAG]>
docker push 963485456147.dkr.ecr.sa-east-1.amazonaws.com/sii-erut-qr-manager

