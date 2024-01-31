#!/bin/bash
cd /app/web/frontend
npm install
npm run dev&

cd /app/web/backend
service redis-server start
rq worker --with-scheduler&
python main.py&