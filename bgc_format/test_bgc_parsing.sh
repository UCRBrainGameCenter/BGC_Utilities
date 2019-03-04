#!/bin/bash

python bgc_to_json.py big_summary.bgc
cat big_summary.json | xclip -selection c
echo "copied resulting json to clipboard. Paste into http://json.parser.online.fr/"
