import os
from env_var import PINATA_API_JWT, PINATA_API_KEY, PINATA_API_SECRET


def set_env_var():
    os.environ["PINATA_API_JWT"] = PINATA_API_JWT
    os.environ["PINATA_API_KEY"] = PINATA_API_KEY
    os.environ["PINATA_API_SECRET"] = PINATA_API_SECRET
