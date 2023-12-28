import os

import tomli

from .loader import pyproject_toml

with pyproject_toml.open("rb") as f:
    pyproject_data = tomli.load(f)
config = pyproject_data.get("tool", {}).get("hyperfunc", {}).get("config", {})

BASE_DIR = pyproject_toml.parent

if "redis-url" in config:
    REDIS_URL = config["redis-url"]
else:
    raise ValueError("redis-url is not defined")

if "django-settings-module" in config:
    DJANGO_SETTINGS_MODULE = config["django-settings-module"]
else:
    DJANGO_SETTINGS_MODULE = None

if "cpus" in config:
    CPUS = config["cpus"]
else:
    CPUS = max(os.cpu_count(), 4)

if "threads-per-cpu" in config:
    THREADS_PER_CPU = config["threads-per-cpu"]
else:
    THREADS_PER_CPU = 2
