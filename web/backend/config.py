APP_CONFIG = {
    "DEBUG": False,
    "SQLALCHEMY_DATABASE_URI": "sqlite:///rnaquanet.db",
}

SWAGGER_TEMPLATE = {
    "info": {
        "title": "RNAQuANet API",
        "version": "v0.1",
    }
}

ALLOWED_FILE_TYPES = ["pdb", "cif"]

# list of available ml models
AVAILABLE_MODELS = ["ares", "seg1", "seg2", "seg3", "transfer_seg2_ares"]

# path to where the files received from frontend will be saved
# relative to `{project}/API`
FILE_STORAGE_DIR = "instance/tasks"

# path to where the temp files are stored
TEMP_FILE_STORAGE_DIR = "instance/temp"

# how long should the randomly generated `task id` be
TASK_ID_LENGTH = 12
