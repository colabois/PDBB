#!/usr/bin/env bash

# if any command inside script returns error, exit and return that error 
set -e


cd "${0%/*}/../src"


echo "Running tests"
# Run test and ignore warnings
pipenv run pytest -p no:warnings

cd "../"

