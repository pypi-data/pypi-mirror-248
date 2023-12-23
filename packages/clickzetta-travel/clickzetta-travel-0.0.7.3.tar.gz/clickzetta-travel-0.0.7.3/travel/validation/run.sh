#!/bin/bash

current_directory=$(dirname "$0")
nohup python "$current_directory"/check_unify.py > "$current_directory"/check_unify.log 2>&1 &

cd "$current_directory"/view && nohup streamlit run main.py --server.port 9095 > validation_view.log 2>&1 &