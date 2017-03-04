#!/bin/bash

SCRIPT_FILE=$1
echo "Running sqlite script file $SCRIPT_FILE..."
sudo sqlite3 numbers.db ".read $SCRIPT_FILE"