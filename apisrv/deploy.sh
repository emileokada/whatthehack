#!/usr/bin/env bash
env AWS_PROFILE=hack sam package --template-file template.yml --s3-bucket ol.pyfive.com --output-template-file package.yml --s3-prefix cloudformation
env AWS_PROFILE=hack aws cloudformation deploy --template-file package.yml --capabilities CAPABILITY_IAM --stack-name early003

rm -f package.yml
