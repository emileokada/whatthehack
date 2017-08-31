#!/usr/bin/env bash
set -x

export AWS_PROFILE=hack

aws s3 cp index.html s3://ol.pyfive.com/index.html --acl public-read &&
aws s3 cp error.html s3://ol.pyfive.com/error.html --acl public-read