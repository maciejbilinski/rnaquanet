Launching:
- `cd rnaquanet/backend`
- `python3 -m venv .venv`
- activate venv:
  * Linux - `source .venv/bin/activate`
  * Windows - `.venv\Scripts\activate`
- `pip install -r requirements.txt`
- `python3 main.py` (run flask)
- `sudo service redis-server start`
- `rq worker --with-scheduler` (start the queue worker, needs to be ran in WSL to work on Windows)