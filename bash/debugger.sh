#!/bin/bash
# build image & specify name:tag
docker build -t rvm-scanner-aws:latest .

# create & run container naming it
docker run -p 9000:8080 --rm -t --name rvm-scanner rvm-scanner-aws:latest
