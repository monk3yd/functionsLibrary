#!/bin/bash

# Login
aws ecr get-login-password --region sa-east-1 | docker login --username AWS --password-stdin 963485456147.dkr.ecr.sa-east-1.amazonaws.com

# Create ECR (Elastic Container Registry)
aws ecr create-repository  --region sa-east-1 --repository-name sii-erut-qr-manager --image-tag-mutability MUTABLE --image-scanning-configuration scanOnPush=false  # Build ECRepo
