#!/bin/bash
supervisord
python3 /opt/rnaquanet/main.py

while :; do
	sleep 10
done
