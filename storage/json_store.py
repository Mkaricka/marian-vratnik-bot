import json
import os

BASE_PATH = "data"


def _path(filename):
    return os.path.join(BASE_PATH, filename)


def load_json(filename, default):
    try:
        with open(_path(filename), "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return default


def save_json(filename, data):
    with open(_path(filename), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
