import logging
import os
from pathlib import Path
from typing import Optional

from core.config import BASE_DIR


logger = logging.getLogger(__name__)


def load_env(filename: Optional[str] = None):
    if filename is None:
        filename = os.environ.get('DONENV_FILE', '.env')
    filename = Path(BASE_DIR, filename)
    logger.info(f"Opening file {filename} as env file")
    with open(filename, 'r') as f:
        for line in f.readlines():
            key, value = line.split('=')
            logger.info(f"Found {key} as env var")
            os.environ[key] = value
    return True
