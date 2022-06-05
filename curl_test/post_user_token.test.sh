#!/bin/bash

set -e

# Remove all whitespace
# Ref: https://www.baeldung.com/linux/remove-whitespace-from-file#2-removing-all-whitespace-characters-1
TEST_BODY=$(sed ':a; N; s/[[:space:]]//g; ta' ${1:-'employee'}_test_keystore.json)

curl -d "$TEST_BODY" \
    -H "Content-Type: application/json" \
    -X POST \
    -v \
    http://localhost:8000/api/user/token

echo ""


