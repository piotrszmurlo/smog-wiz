#!/bin/bash

echo "${0}: Creating empty CSV database if not exist..."
touch db.csv

echo "${0}: Running app.py..."
python app.py
