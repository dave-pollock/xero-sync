#!/bin/bash

PACKAGING_DIR=./terraform/package

uv sync --all-extras

if [[ -d "$PACKAGING_DIR" ]]; then rm -rf "$PACKAGING_DIR"; fi
mkdir -p "$PACKAGING_DIR"

cp -r ./src/* "$PACKAGING_DIR"
cp -r ./.venv/lib/python3.13/site-packages/* "$PACKAGING_DIR"
