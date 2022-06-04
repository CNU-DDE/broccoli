#!/bin/bash

set -e

TEST_COOKIE=$1

curl -b "$TEST_COOKIE" \
    -X GET \
    -v \
    http://localhost:8000/api/claim

echo ""
