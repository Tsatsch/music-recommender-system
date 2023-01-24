import json
from dotenv import dotenv_values


@staticmethod
def setup(
    config_path: str = "config/config.json", env_path: str = "config/.env"
) -> tuple(dict, dict):
    # get config
    with open(config_path) as c:
        config = json.load(c)
    # get secrets
    secrets = dotenv_values(env_path)
    return config, secrets
