APP_CONFIG = {
    "DEBUG": True,
    "SQLALCHEMY_DATABASE_URI": "sqlite:///rnaquanet.db",
}

SWAGGER_TEMPLATE = {
    "info": {
        "title": "RNAQuANet API",
        "version": "v0.1",
    }
}

ALLOWED_FILE_TYPES = ["pdb", "cif"]

# path to where the files received from frontend will be saved
# relative to `{project}/API`
FILE_STORAGE_DIR = "instance/tasks"

# path to where the temp files are stored
TEMP_FILE_STORAGE_DIR = "instance/temp"

# how long should the randomly generated `task id` be
TASK_ID_LENGTH = 12
