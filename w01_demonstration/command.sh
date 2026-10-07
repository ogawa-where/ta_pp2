#!/bin/bash

./clean.sh
source ~/venv/py3.10.12/bin/activate
pip3 install -r requirements.txt
python3 make_facility_usage_form.py
xdg-open output/output.docx
