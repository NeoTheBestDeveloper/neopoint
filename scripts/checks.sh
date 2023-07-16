#!/bin/sh

echo '#################################'
echo '######## CHECK LINTING  #########'
echo '#################################'

pylint neopoint tests
ruff neopoint tests
echo -e "\n\n"

echo '#################################'
echo '######## CHECK FORMATING ########'
echo '#################################'
isort --check-only --profile black neopoint tests
black --check neopoint tests
echo -e "\n\n"

echo '#################################'
echo '########## CHECK TYPES ##########'
echo '#################################'
pyright neopoint tests
mypy neopoint tests
