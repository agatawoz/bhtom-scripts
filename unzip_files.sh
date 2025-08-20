#!/bin/bash


if [ -z "$1" ]; then
    echo "No directory name provided."
    exit 1
fi

DATA_DIR="$1"

echo "Proccesing files in: $DATA_DIR"
cd "$DATA_DIR" || { echo "Folder $DATA_DIR not found"; exit 1;}

echo "Unzipping .gz files."
gunzip -v *.gz