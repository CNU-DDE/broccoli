#!/bin/bash

set -e

TEST_COOKIE=$1

curl -X GET \
    -b $TEST_COOKIE \
    -v \
    http://localhost:8000/api/resume

echo ""
