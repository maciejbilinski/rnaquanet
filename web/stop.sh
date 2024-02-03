#!/bin/bash
pkill -f "npm run dev"
pkill -f "rq worker --with-scheduler"
pkill -f "python main.py"