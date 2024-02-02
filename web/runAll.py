import os, threading

# adjust the path
backend_path = os.path.join(os.path.dirname(__file__), "backend")
os.chdir(backend_path)

# start redis queue
os.system("service redis-server start")
os.system("(rq worker --with-scheduler --quiet&)")

# start frontend
threading.Thread(
    target=lambda: os.system("(npm run dev --prefix ../frontend --silent&)")
).start()

# start backend
threading.Thread(target=lambda: os.system("(python3 main.py&)")).start()