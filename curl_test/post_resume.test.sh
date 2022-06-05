#!/bin/bash

set -e

# Remove all whitespace
# Ref: https://www.baeldung.com/linux/remove-whitespace-from-file#2-removing-all-whitespace-characters-
TEST_BODY=$(sed ':a; N; s/[[:space:]]//g; ta' ./post_resume.json)
TEST_COOKIE=$1

curl -d "$TEST_BODY" \
    -b "$TEST_COOKIE" \
    -H "Content-Type: application/json" \
    -X POST \
    -v \
    http://localhost:8000/api/resume

echo ""


