import os


def _find_dotenv_path(directory=os.getcwd()):
    assert os.path.isdir(directory)
    for cur_path, directories, files in os.walk(directory):
        if ".env" in files:
            return os.path.join(directory, cur_path, ".env")
    return None


def dump_dotenv(dotenv_path="./.env", env_dict=os.environ):
    with open(dotenv_path, "w+") as f:
        for k, v in env_dict.items():
            f.write(f"{k}={v}\n")


def load_dotenv(dotenv_path=_find_dotenv_path(), env_dict=os.environ, failsafe=False):
    if not failsafe:
        assert dotenv_path, "No .env File found!"
    elif failsafe and not dotenv_path:
        return
    with open(dotenv_path) as f:
        for line in f.read().splitlines():
            if line.startswith("#"):
                continue
            k, v = line.split("=")
            k = k.rstrip()
            v = v.lstrip()
            env_dict[k] = v
