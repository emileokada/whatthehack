#!/usr/bin/env bash
set -x

export AWS_PROFILE=hack

aws s3 cp index.html s3://ol.pyfive.com/index.html --acl public-read &&
aws s3 cp error.html s3://ol.pyfive.com/error.html --acl public-read &&
aws s3 cp data/data.json s3://ol.pyfive.com/data/orig.json --acl public-read &&
aws s3 cp data/atm_data.json s3://ol.pyfive.com/data/atm_data.json --acl public-read &&
aws s3 cp static/beer.png s3://ol.pyfive.com/static/beer.png --acl public-read
aws s3 cp static/atm.png s3://ol.pyfive.com/static/atm.png --acl public-read
