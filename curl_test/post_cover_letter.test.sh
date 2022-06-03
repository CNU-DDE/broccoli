#!/bin/bash

set -e

. ./post_cover_letter.env

curl -d "$TEST_BODY" \
    -b "$TEST_COOKIE_KEY=$TEST_COOKIE_VALUE" \
    -H "Content-Type: application/json" \
    -X POST \
    -v \
    http://localhost:8000/api/cover-letter

echo ""


