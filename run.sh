#!/bin/bash
export $(grep -v '^#' .env | xargs)
python src/app.py
