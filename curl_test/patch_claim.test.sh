#!/bin/bash

set -e

# Remove all whitespace
# Ref: https://www.baeldung.com/linux/remove-whitespace-from-file#2-removing-all-whitespace-characters-1
TEST_BODY=$(sed ':a; N; s/[[:space:]]//g; ta' patch_claim.json)
TEST_COOKIE=$1

curl -d "$TEST_BODY" \
    -b "$TEST_COOKIE" \
    -H "Content-Type: application/json" \
    -X PATCH \
    -v \
    http://localhost:8000/api/claim/2

echo ""


