#!/usr/bin/env bash
set -e
ENV=$1
NAME="rds-alarms-lambda.zip"
echo "Publishing lambda for environment: '$ENV'"

declare -A s3_buckets
s3_buckets=( ["dev"]="s3-bucket-dev"
             ["prod"]="s3-bucket-prod"
           )
S3_BUCKET="${s3_buckets[$ENV]}"

declare -A function_names
function_names=( ["dev"]="rds-lambda-dev"
                 ["prod"]="rds-lambda-prod"
               )
FUNCTION_NAME="${function_names[$ENV]}"

echo "Uploading to S3"
aws --profile=${ENV} s3 cp ${NAME} s3://${S3_BUCKET}/lambda/ --sse
rm ${NAME}

echo "Updating lambda"
# Update lambda function code and get the new version created
aws --profile=${ENV} lambda update-function-code --function-name ${FUNCTION_NAME} --s3-bucket ${S3_BUCKET} --s3-key "lambda/$NAME" --publish

echo "Done."