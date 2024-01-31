Frontend:
- `cd rnaquanet/frontend`
- `(npm run dev&)`

Backend:
- `service redis-server start`
- `(rq worker --with-scheduler&)`
- `(python3 main.py&)`