#!/usr/bin/env bash
NAME="rds-alarms-lambda.zip"
rm -f ${NAME}
docker build . -f Dockerfile.package -t rds-alarms-lambda
docker run --name lambda-package rds-alarms-lambda zip -r ${NAME} .
docker cp lambda-package:/src/${NAME} .
docker rm -f lambda-package
echo "Built ${NAME}"
echo "Done."
