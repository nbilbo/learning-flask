from pathlib import Path


BASE_DIR = Path('.').parent
INSTANCE_DIR = BASE_DIR / 'instance'
TEMPLATES_DIR = BASE_DIR / 'templates'
STATIC_DIR = BASE_DIR / 'static'
LOCAL_DATABASE_PATH = INSTANCE_DIR / 'database.sqlite'
