#!/bin/bash

#Build the project
echo "Building the project"
python3.12 -m pip install -r requirements.txt

echo "Collect static files"
python3.12 manage.py collectstatic 