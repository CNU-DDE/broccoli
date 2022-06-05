#!/bin/bash

set -e

curl -X GET \
    -v \
    http://localhost:8000/api/resume/all

echo ""
