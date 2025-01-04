# congress_api/config.py
import os
from dataclasses import dataclass
from typing import Set

from .exceptions import CongressAPIError

@dataclass
class APIConfig:
    """Configuration settings for the API client."""
    api_key: str
    base_url: str
    default_format: str
    max_retries: int
    timeout: int
    max_limit: int
    default_congress: int

def load_config() -> APIConfig:
    """Load configuration from environment variables."""
    api_key = os.getenv('CONGRESS_API_KEY')
    base_url = os.getenv('CONGRESS_API_BASE_URL', 'https://api.congress.gov/v3/')
    default_format = os.getenv('CONGRESS_API_FORMAT', 'json')
    max_retries = int(os.getenv('CONGRESS_API_MAX_RETRIES', '3'))
    timeout = int(os.getenv('CONGRESS_API_TIMEOUT', '30'))
    max_limit = 250
    default_congress = 118

    if not api_key:
        raise CongressAPIError("CONGRESS_API_KEY environment variable is required")

    return APIConfig(
        api_key=api_key,
        base_url=base_url,
        default_format=default_format,
        max_retries=max_retries,
        timeout=timeout,
        max_limit=max_limit,
        default_congress=default_congress
    )

# Amendment specific configurations
VALID_AMENDMENT_TYPES: Set[str] = {'hamdt', 'samdt', 'suamdt', "sres"}
TEXT_SUPPORTED_AMENDMENT_TYPES: Set[str] = {'hamdt', 'samdt', 'suamdt', "sres"}
MIN_TEXT_CONGRESS: int = 118

#Bill specific configurations
VALID_BILL_TYPES: Set[str] = {'hr', 's', 'hjres', 'sjres', 'hconres', 'sconres', 'hres', 'sres'}