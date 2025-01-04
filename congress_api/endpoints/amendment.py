# congress_api/endpoints/amendment.py
from typing import Optional, Dict, Any, Union, Literal
from datetime import datetime

from .base import BaseEndpoint
from ..config import (
    VALID_AMENDMENT_TYPES,
    TEXT_SUPPORTED_AMENDMENT_TYPES,
    MIN_TEXT_CONGRESS
)
from ..exceptions import AmendmentTypeError, AmendmentTextError


class AmendmentEndpoint(BaseEndpoint):
    """Handler for amendment-related API endpoints."""

    def __init__(self, client):
        super().__init__(client)
        self.base_path = "amendment"

    def _validate_amendment_type(self, amendment_type: Literal['hamdt', 'samdt', 'suamdt'], text_endpoint: bool = False) -> None:
        """
        Validate the amendment type.
        
        Args:
            amendment_type: Type of amendment to validate
            text_endpoint: Whether this is for the text endpoint (which has stricter requirements)
        
        Raises:
            AmendmentTypeError: If amendment type is invalid
        """
        valid_types = TEXT_SUPPORTED_AMENDMENT_TYPES if text_endpoint else VALID_AMENDMENT_TYPES
        if amendment_type.lower() not in valid_types:
            raise AmendmentTypeError(amendment_type, valid_types)

    def list_all(self,
                format: Optional[str] = "json",
                offset: Optional[int] = 0,
                limit: Union[int, Literal['all']] = 20,
                from_datetime: Optional[datetime] = None,
                to_datetime: Optional[datetime] = None) -> Dict[str, Any]:
        """
        Get a list of amendments sorted by date of latest action.
        
        Args:
            format: Response format ('xml' or 'json')
            offset: Starting record number (0-based)
            limit: Number of records to return (max 250, or 'all' for all records)
            from_datetime: Start of update date filter
            to_datetime: End of update date filter
            
        Returns:
            API response data containing list of amendments
        """
        params = {
            'format': format,
            'offset': offset,
            'fromDateTime': from_datetime.isoformat() if from_datetime else None,
            'toDateTime': to_datetime.isoformat() if to_datetime else None
        }
        
        return self._get(self.base_path, params=params, limit=limit)

    def list_by_congress(self,
                        congress: Optional[int] = None,
                        format: Optional[str] = "json",
                        offset: Optional[int] = 0,
                        limit: Union[int, Literal['all']] = 20,
                        from_datetime: Optional[datetime] = None,
                        to_datetime: Optional[datetime] = None) -> Dict[str, Any]:
        """
        Get amendments for a specific congress.
        
        Args:
            congress: Congress number (defaults to current congress from config)
            format: Response format ('xml' or 'json')
            offset: Starting record number (0-based)
            limit: Number of records to return (max 250, or 'all' for all records)
            from_datetime: Start of update date filter
            to_datetime: End of update date filter
            
        Returns:
            API response data containing list of amendments for the specified congress
        """
        params = {
            'format': format,
            'offset': offset,
            'fromDateTime': from_datetime.isoformat() if from_datetime else None,
            'toDateTime': to_datetime.isoformat() if to_datetime else None
        }
        
        congress = congress or self.client.config.default_congress
        endpoint = f"{self.base_path}/{congress}"
        return self._get(endpoint, params=params, limit=limit)

    def list_by_congress(self,
                     amendment_type: Literal['hamdt', 'samdt', 'suamdt'],
                     congress: Optional[int] = None,
                     format: Optional[str] = "json",
                     offset: Optional[int] = 0,
                     limit: Union[int, Literal['all']] = 20,
                     from_datetime: Optional[datetime] = None,
                     to_datetime: Optional[datetime] = None) -> Dict[str, Any]:
        """
        Get amendments filtered by congress and amendment type.
        
        Args:
            amendment_type: Type of amendment ('hamdt', 'samdt', or 'suamdt')
            congress: Congress number (defaults to current congress from config)
            format: Response format ('xml' or 'json')
            offset: Starting record number (0-based)
            limit: Number of records to return (max 250, or 'all' for all records)
            from_datetime: Start of update date filter
            to_datetime: End of update date filter
        
        Info:
            hamdt: House Amendment
            samdt: Senate Amendment
            suamdt: Senate Unanimous Consent Agreement Amendment
            
        Returns:
            API response data containing list of amendments for the specified congress and type
        """
        self._validate_amendment_type(amendment_type)
        
        params = {
            'format': format,
            'offset': offset,
            'fromDateTime': from_datetime.isoformat() if from_datetime else None,
            'toDateTime': to_datetime.isoformat() if to_datetime else None
        }
        
        congress = congress or self.client.config.default_congress
        endpoint = f"{self.base_path}/{congress}/{amendment_type.lower()}"
        return self._get(endpoint, params=params, limit=limit)

    def get_amendment(self,
                     amendment_type: Literal['hamdt', 'samdt', 'suamdt'],
                     amendment_number: int,
                     congress: Optional[int] = None,
                     format: Optional[str] = "json") -> Dict[str, Any]:
        """
        Get detailed information for a specific amendment.
        
        Args:
            amendment_type: Type of amendment ('hamdt', 'samdt', or 'suamdt')
            amendment_number: Amendment number (e.g., 2137)
            congress: Congress number (defaults to current congress from config)
            format: Response format ('xml' or 'json')
        
        Info:
            hamdt: House Amendment
            samdt: Senate Amendment
            suamdt: Senate Unanimous Consent Agreement Amendment

        Returns:
            API response data containing detailed information for the specified amendment
        """
        self._validate_amendment_type(amendment_type)
        
        params = {'format': format}
        congress = congress or self.client.config.default_congress
        
        endpoint = f"{self.base_path}/{congress}/{amendment_type.lower()}/{amendment_number}"
        return self._get(endpoint, params=params)

    def get_actions(self,
                   amendment_type: Literal['hamdt', 'samdt', 'suamdt'],
                   amendment_number: int,
                   congress: Optional[int] = None,
                   format: Optional[str] = "json",
                   offset: Optional[int] = 0,
                   limit: Union[int, Literal['all']] = 'all') -> Dict[str, Any]:
        """
        Get the list of actions on a specific amendment.
        
        Args:
            amendment_type: Type of amendment ('hamdt', 'samdt', or 'suamdt')
            amendment_number: Amendment number (e.g., 2137)
            congress: Congress number (defaults to current congress from config)
            format: Response format ('xml' or 'json')
            offset: Starting record number (0-based)
            limit: Number of records to return (max 250, or 'all' for all records)
        
        Info:
            hamdt: House Amendment
            samdt: Senate Amendment
            suamdt: Senate Unanimous Consent Agreement Amendment
            
        Returns:
            API response data containing list of actions for the specified amendment
        """
        self._validate_amendment_type(amendment_type)
        
        params = {
            'format': format,
            'offset': offset
        }
        
        congress = congress or self.client.config.default_congress
        endpoint = f"{self.base_path}/{congress}/{amendment_type.lower()}/{amendment_number}/actions"
        return self._get(endpoint, params=params, limit=limit)

    def get_cosponsors(self,
                      amendment_type: Literal['hamdt', 'samdt', 'suamdt'],
                      amendment_number: int,
                      congress: Optional[int] = None,
                      format: Optional[str] = "json",
                      offset: Optional[int] = 0,
                      limit: Union[int, Literal['all']] = 'all') -> Dict[str, Any]:
        """
        Get the list of cosponsors for a specific amendment.
        
        Args:
            amendment_type: Type of amendment ('hamdt', 'samdt', or 'suamdt')
            amendment_number: Amendment number (e.g., 2137)
            congress: Congress number (defaults to current congress from config)
            format: Response format ('xml' or 'json')
            offset: Starting record number (0-based)
            limit: Number of records to return (max 250, or 'all' for all records)
        
        Info:
            hamdt: House Amendment
            samdt: Senate Amendment
            suamdt: Senate Unanimous Consent Agreement Amendment
            
        Returns:
            API response data containing list of cosponsors for the specified amendment
        """
        self._validate_amendment_type(amendment_type)
        
        params = {
            'format': format,
            'offset': offset
        }
        
        congress = congress or self.client.config.default_congress
        endpoint = f"{self.base_path}/{congress}/{amendment_type.lower()}/{amendment_number}/cosponsors"
        return self._get(endpoint, params=params, limit=limit)

    def get_amendments(self,
                      amendment_type: Literal['hamdt', 'samdt', 'suamdt'],
                      amendment_number: int,
                      congress: Optional[int] = None,
                      format: Optional[str] = "json",
                      offset: Optional[int] = 0,
                      limit: Union[int, Literal['all']] = 'all') -> Dict[str, Any]:
        """
        Get the list of amendments to a specific amendment.
        
        Args:
            amendment_type: Type of amendment ('hamdt', 'samdt', or 'suamdt')
            amendment_number: Amendment number (e.g., 2137)
            congress: Congress number (defaults to current congress from config)
            format: Response format ('xml' or 'json')
            offset: Starting record number (0-based)
            limit: Number of records to return (max 250, or 'all' for all records)
        
        Info:
            hamdt: House Amendment
            samdt: Senate Amendment
            suamdt: Senate Unanimous Consent Agreement Amendment
            
        Returns:
            API response data containing list of amendments to the specified amendment
        """
        self._validate_amendment_type(amendment_type)
        
        params = {
            'format': format,
            'offset': offset
        }
        
        congress = congress or self.client.config.default_congress
        endpoint = f"{self.base_path}/{congress}/{amendment_type.lower()}/{amendment_number}/amendments"
        return self._get(endpoint, params=params, limit=limit)

    def get_text(self,
                amendment_type: Literal['hamdt', 'samdt', 'suamdt'],
                amendment_number: int,
                congress: Optional[int] = None,
                format: Optional[str] = "json",
                offset: Optional[int] = 0,
                limit: Union[int, Literal['all']] = 'all') -> Dict[str, Any]:
        """
        Get the list of text versions for a specific amendment from the 117th Congress onwards.
        
        Args:
            amendment_type: Type of amendment ('hamdt' or 'samdt')
            amendment_number: Amendment number (e.g., 287)
            congress: Congress number (must be >= 117, defaults to current congress)
            format: Response format ('xml' or 'json')
            offset: Starting record number (0-based)
            limit: Number of records to return (max 250, or 'all' for all records)
        
        Info:
            hamdt: House Amendment
            samdt: Senate Amendment
            suamdt: Senate Unanimous Consent Agreement Amendment
            
        Returns:
            API response data containing list of text versions for the specified amendment
            
        Raises:
            AmendmentTypeError: If amendment type not supported for text endpoint
            AmendmentTextError: If congress is below 117
        """
        self._validate_amendment_type(amendment_type, text_endpoint=True)
        
        congress = congress or self.client.config.default_congress
        if congress < MIN_TEXT_CONGRESS:
            raise AmendmentTextError(congress)
        
        params = {
            'format': format,
            'offset': offset
        }
        
        endpoint = f"{self.base_path}/{congress}/{amendment_type.lower()}/{amendment_number}/text"
        return self._get(endpoint, params=params, limit=limit)