Frontend:
- `(npm run dev --prefix web/frontend&)`

Backend:
- `service redis-server start`
- `cd web/backend` - !important to keep all paths the same
- `(rq worker --with-scheduler&)`
- `(python3 main.py&)`