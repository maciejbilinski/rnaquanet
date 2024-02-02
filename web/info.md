## It's recommended to just run the `runAll.py` script. It will start both front and backend, as well as rq in `silent` modes.

Frontend:
- `(npm run dev --prefix web/frontend&)`

Backend:
- `service redis-server start`
- `cd web/backend` - !important to keep all paths the same
- `(rq worker --with-scheduler&)`
- `(python3 main.py&)`