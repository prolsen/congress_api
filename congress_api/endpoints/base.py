from typing import Optional, Dict, Any, TYPE_CHECKING, Literal, Union
from copy import deepcopy

if TYPE_CHECKING:
    from congress_api.client import CongressClient

class BaseEndpoint:
    """Base class for API endpoints."""
    
    MAX_LIMIT = 250  # API's maximum limit per request

    def __init__(self, client: 'CongressClient'):
        self.client = client

    def _get(self,
             endpoint: str,
             params: Optional[Dict[str, Any]] = None,
             limit: Union[int, Literal['all']] = 20,
             **kwargs) -> Dict[str, Any]:
        """
        Make GET request to endpoint with automatic pagination handling.

        Args:
            endpoint: API endpoint to call
            params: Query parameters for the request
            limit: Maximum number of results to fetch (integer between 1-250, or 'all' for all results)
            **kwargs: Additional arguments to pass to the get function

        Returns:
            Dict containing results with pagination handled automatically
            
        Raises:
            ValueError: If limit is invalid or response structure is unexpected
        """
        params = params or {}
        current_params = deepcopy(params)
        
        # Remove limit from params if it exists, we'll handle it separately
        if 'limit' in current_params:
            del current_params['limit']

        # Handle integer limits
        if isinstance(limit, int):
            if 1 <= limit <= self.MAX_LIMIT:
                current_params['limit'] = limit
                return self.client.get(endpoint, params=current_params, **kwargs)
            raise ValueError(f"Limit must be between 1 and {self.MAX_LIMIT} or 'all'")

        # Handle 'all' limit
        if limit != 'all':
            raise ValueError("Limit must be an integer between 1-250 or 'all'")

        # Begin pagination handling for 'all'
        current_params['limit'] = self.MAX_LIMIT
        response = self.client.get(endpoint, params=current_params, **kwargs)
        
        data_key = next((k for k in response.keys() 
                        if k not in ['pagination', 'request']), None)
        if not data_key:
            raise ValueError("Unable to determine data key in response")

        pagination = response.get('pagination', {})
        total_count = pagination.get('count', 0)
        
        # If no more pages, return as is
        if 'next' not in pagination:
            return response
            
        # Initialize results with first page
        all_results = response[data_key]
        offset = self.MAX_LIMIT
        
        # Continue fetching while there are more results
        while 'next' in pagination:
            # Update parameters for next request
            current_params = deepcopy(params)
            current_params['offset'] = offset
            current_params['limit'] = self.MAX_LIMIT
            
            # Make next request
            response = self.client.get(endpoint, params=current_params, **kwargs)
            current_results = response[data_key]
            pagination = response.get('pagination', {})
            
            all_results.extend(current_results)
            offset += len(current_results)
                
        # Construct final response
        final_response = {
            data_key: all_results,
            'pagination': {'count': total_count},
            'request': response.get('request', {})
        }
        
        return final_response