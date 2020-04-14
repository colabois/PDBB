#!/usr/bin/env bash

cdroot() {
    cd "${0%/*}/.."
}


echo "Running pre-commit hook"
./scripts/run-tests.sh

if [ $? -ne 0 ]; then
 echo "Tests must pass before commit!"
 exit 1
fi

./scripts/build-docs.sh

if [ $? -ne 0 ]; then
 echo "Doc must pass before commit!"
 exit 1
fi

echo "Done."
