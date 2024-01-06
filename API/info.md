Launching:
- `cd rnaquanet/API`
- `python -m venv .venv`
- activate venv:
  * Linux - `source .venv/bin/activate`
  * Windows - `.venv\Scripts\activate`
- `pip install -r requirements.txt`
- `python main.py` (run flask)
- `rq worker --with-scheduler` (start the queue worker, needs to be ran in WSL to work on Windows)