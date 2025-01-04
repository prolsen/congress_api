# congress_api/__init__.py
import os
from pathlib import Path
from dotenv import load_dotenv

def find_root_dir() -> Path:
    """Find the project root directory containing .env file."""
    current = Path.cwd()
    while current != current.parent:
        if (current / '.env').exists():
            return current
        current = current.parent
    return Path.cwd()

# Load .env from project root
root_dir = find_root_dir()
load_dotenv(dotenv_path=root_dir / '.env', override=True)

from .config import APIConfig, load_config
from .client import CongressClient
from .exceptions import CongressAPIError, AmendmentTypeError, AmendmentTextError