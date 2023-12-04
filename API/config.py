DEBUG_MODE: bool = True

# path to where the data received from frontend will be saved
# relative to `{project}/API`
STORAGE_DIR = "../data/temp/"

# name of the status file containing processing status and later on the result
STATUS_FILE = "status.json"

# name of the directory user's files will be saved in
FILES_DIR = "files"

# how long should the randomly generated `task id` be
TASK_ID_LENGTH = 12