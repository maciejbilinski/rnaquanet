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

# path to where the files received from frontend will be saved
# relative to `{project}/API`
FILE_STORAGE_DIR = "instance/files"

# how long should the randomly generated `task id` be
TASK_ID_LENGTH = 12
