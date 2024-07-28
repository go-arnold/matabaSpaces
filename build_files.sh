#!/bin/bash

#Build the project
echo "Building the project"
python3.12 -m pip install -r requirements.txt

export PATH="/python312/bin:$PATH"


echo "Collect static files"
python3.12 manage.py collectstatic 