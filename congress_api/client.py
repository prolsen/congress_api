# congress_api/client.py
from typing import Optional, Dict, Any
from urllib.parse import urljoin

import requests
from requests.exceptions import RequestException

from .config import APIConfig
from .exceptions import CongressAPIError
from .endpoints.amendment import AmendmentEndpoint
from .endpoints.member import MemberEndpoint
from .endpoints.bill import BillEndpoint


class CongressClient:
    """Client for accessing the Congress.gov API."""
    
    def __init__(self, config: APIConfig):
        """
        Initialize the Congress.gov API client.
        
        Args:
            config: APIConfig object containing configuration settings
        """
        self.config = config
        self.session = self._init_session()
        self.base_url = config.base_url
        
        # Initialize endpoints
        self.amendment = AmendmentEndpoint(self)
        self.member = MemberEndpoint(self)
        self.bill = BillEndpoint(self)
        
    def _init_session(self):
        """Initialize the requests session with default headers and settings."""
        session = requests.Session()
        session.headers.update({
            'x-api-key': self.config.api_key,
            'accept': 'application/json' if self.config.default_format == 'json' else 'application/xml'
        })
        return session

    def get(self, 
            endpoint: str, 
            params: Optional[Dict[str, Any]] = None,
            **kwargs) -> Dict[str, Any]:
        """
        Make GET request to API endpoint.
        
        Args:
            endpoint: API endpoint path
            params: Query parameters
            **kwargs: Additional request parameters
            
        Returns:
            API response data
            
        Raises:
            CongressAPIError: If the API request fails
        """
        try:
            url = urljoin(self.base_url, endpoint)
            response = self.session.request(
                'GET',
                url,
                params=params or {},
                timeout=self.config.timeout,
                **kwargs
            )
            
            response.raise_for_status()
            
            if 'application/json' in response.headers.get('content-type', ''):
                return response.json()
            return response.content
                
        except RequestException as e:
            raise CongressAPIError(
                f"API request failed: {str(e)}",
                status_code=getattr(e.response, 'status_code', None),
                response=getattr(e.response, 'text', None)
            )