# congress_api/endpoints/bill.py
from typing import Optional, Dict, Any, Union, Literal
from datetime import datetime

from congress_api.config import VALID_BILL_TYPES
from .base import BaseEndpoint
from ..exceptions import BillTypeError, BillNumberError, CongressNumberError

class BillEndpoint(BaseEndpoint):
    """Handler for bill-related API endpoints."""

    def __init__(self, client):
        super().__init__(client)
        self.base_path = "bill"

        self.VALID_BILL_TYPES = VALID_BILL_TYPES

    def _validate_bill_type(self, bill_type: str) -> None:
        """
        Validate the bill type.
        
        Args:
            bill_type: Type of bill to validate
        
        Raises:
            BillTypeError: If bill type is invalid
        """
        if bill_type.lower() not in self.VALID_BILL_TYPES:
            raise BillTypeError(bill_type, self.VALID_BILL_TYPES)
            
    def _validate_bill_number(self, bill_number: Any) -> None:
        """
        Validate the bill number.
        
        Args:
            bill_number: Bill number to validate
            
        Raises:
            BillNumberError: If bill number is invalid
        """
        try:
            if not isinstance(bill_number, int) or bill_number <= 0:
                raise ValueError
        except (ValueError, TypeError):
            raise BillNumberError(bill_number)
            
    def _validate_congress(self, congress: Any) -> None:
        """
        Validate the congress number.
        
        Args:
            congress: Congress number to validate
            
        Raises:
            CongressNumberError: If congress number is invalid
        """
        try:
            if not isinstance(congress, int) or congress <= 0:
                raise ValueError
        except (ValueError, TypeError):
            raise CongressNumberError(congress)

    def list_all(self,
                format: Optional[str] = "json",
                offset: Optional[int] = 0,
                limit: Union[int, Literal['all']] = 20,
                from_datetime: Optional[datetime] = None,
                to_datetime: Optional[datetime] = None,
                sort: Optional[str] = None) -> Dict[str, Any]:
        """
        Get a list of bills sorted by date of latest action.
        
        Args:
            format: Response format ('xml' or 'json')
            offset: Starting record number (0-based)
            limit: Number of records to return (max 250, or 'all' for all records)
            from_datetime: Start of update date filter
            to_datetime: End of update date filter
            sort: Sort order ('updateDate+asc' or 'updateDate+desc')
            
        Returns:
            API response data containing list of bills
        """
        params = {
            'format': format,
            'offset': offset,
            'fromDateTime': from_datetime.isoformat() if from_datetime else None,
            'toDateTime': to_datetime.isoformat() if to_datetime else None,
            'sort': sort
        }
        
        return self._get(self.base_path, params=params, limit=limit)

    def list_by_congress(self,
                        congress: Optional[int] = None,
                        format: Optional[str] = "json",
                        offset: Optional[int] = 0,
                        limit: Union[int, Literal['all']] = 20,
                        from_datetime: Optional[datetime] = None,
                        to_datetime: Optional[datetime] = None,
                        sort: Optional[str] = None) -> Dict[str, Any]:
        """
        Get bills filtered by congress.
        
        Args:
            congress: Congress number (defaults to current congress from config)
            format: Response format ('xml' or 'json')
            offset: Starting record number (0-based)
            limit: Number of records to return (max 250, or 'all' for all records)
            from_datetime: Start of update date filter
            to_datetime: End of update date filter
            sort: Sort order ('updateDate+asc' or 'updateDate+desc')
            
        Returns:
            API response data containing list of bills for the specified congress
        """
        params = {
            'format': format,
            'offset': offset,
            'fromDateTime': from_datetime.isoformat() if from_datetime else None,
            'toDateTime': to_datetime.isoformat() if to_datetime else None,
            'sort': sort
        }
        
        congress = congress or self.client.config.default_congress
        endpoint = f"{self.base_path}/{congress}"
        return self._get(endpoint, params=params, limit=limit)

    def list_by_type(self,
                     bill_type: str,
                     congress: Optional[int] = None,
                     format: Optional[str] = "json",
                     offset: Optional[int] = 0,
                     limit: Union[int, Literal['all']] = 20,
                     from_datetime: Optional[datetime] = None,
                     to_datetime: Optional[datetime] = None,
                     sort: Optional[str] = None) -> Dict[str, Any]:
        """
        Get bills filtered by congress and bill type.
        
        Args:
            bill_type: Type of bill (hr, s, hjres, sjres, hconres, sconres, hres, or sres)
            congress: Congress number (defaults to current congress from config)
            format: Response format ('xml' or 'json')
            offset: Starting record number (0-based)
            limit: Number of records to return (max 250, or 'all' for all records)
            from_datetime: Start of update date filter
            to_datetime: End of update date filter
            sort: Sort order ('updateDate+asc' or 'updateDate+desc')
            
        Returns:
            API response data containing list of bills for the specified congress and type
        """
        self._validate_bill_type(bill_type)
        
        params = {
            'format': format,
            'offset': offset,
            'fromDateTime': from_datetime.isoformat() if from_datetime else None,
            'toDateTime': to_datetime.isoformat() if to_datetime else None,
            'sort': sort
        }
        
        congress = congress or self.client.config.default_congress
        endpoint = f"{self.base_path}/{congress}/{bill_type.lower()}"
        return self._get(endpoint, params=params, limit=limit)

    def get_bill(self,
                bill_type: str,
                bill_number: int,
                congress: Optional[int] = None,
                format: Optional[str] = "json") -> Dict[str, Any]:
        """
        Get detailed information for a specific bill.
        
        Args:
            bill_type: Type of bill (hr, s, hjres, sjres, hconres, sconres, hres, or sres)
            bill_number: Bill number (e.g., 3076)
            congress: Congress number (defaults to current congress from config)
            format: Response format ('xml' or 'json')
            
        Returns:
            API response data containing detailed information for the specified bill
            
        Raises:
            BillTypeError: If bill type is invalid
            BillNumberError: If bill number is invalid
            CongressNumberError: If congress number is invalid
        """
        self._validate_bill_type(bill_type)
        self._validate_bill_number(bill_number)
        
        congress = congress or self.client.config.default_congress
        self._validate_congress(congress)
        
        params = {'format': format}
        endpoint = f"{self.base_path}/{congress}/{bill_type.lower()}/{bill_number}"
        return self._get(endpoint, params=params)

    def get_actions(self,
                   bill_type: str,
                   bill_number: int,
                   congress: Optional[int] = None,
                   format: Optional[str] = "json",
                   offset: Optional[int] = 0,
                   limit: Union[int, Literal['all']] = 'all') -> Dict[str, Any]:
        """
        Get the list of actions on a specific bill.
        
        Args:
            bill_type: Type of bill (hr, s, hjres, sjres, hconres, sconres, hres, or sres)
            bill_number: Bill number (e.g., 3076)
            congress: Congress number (defaults to current congress from config)
            format: Response format ('xml' or 'json')
            offset: Starting record number (0-based)
            limit: Number of records to return (max 250, or 'all' for all records)
            
        Returns:
            API response data containing list of actions for the specified bill
        """
        self._validate_bill_type(bill_type)
        
        params = {
            'format': format,
            'offset': offset
        }
        
        congress = congress or self.client.config.default_congress
        endpoint = f"{self.base_path}/{congress}/{bill_type.lower()}/{bill_number}/actions"
        return self._get(endpoint, params=params, limit=limit)

    def get_amendments(self,
                      bill_type: str,
                      bill_number: int,
                      congress: Optional[int] = None,
                      format: Optional[str] = "json",
                      offset: Optional[int] = 0,
                      limit: Union[int, Literal['all']] = 'all') -> Dict[str, Any]:
        """
        Get the list of amendments to a specific bill.
        
        Args:
            bill_type: Type of bill (hr, s, hjres, sjres, hconres, sconres, hres, or sres)
            bill_number: Bill number (e.g., 3076)
            congress: Congress number (defaults to current congress from config)
            format: Response format ('xml' or 'json')
            offset: Starting record number (0-based)
            limit: Number of records to return (max 250, or 'all' for all records)
            
        Returns:
            API response data containing list of amendments for the specified bill
        """
        self._validate_bill_type(bill_type)
        
        params = {
            'format': format,
            'offset': offset
        }
        
        congress = congress or self.client.config.default_congress
        endpoint = f"{self.base_path}/{congress}/{bill_type.lower()}/{bill_number}/amendments"
        return self._get(endpoint, params=params, limit=limit)

    def get_committees(self,
                      bill_type: str,
                      bill_number: int,
                      congress: Optional[int] = None,
                      format: Optional[str] = "json",
                      offset: Optional[int] = 0,
                      limit: Union[int, Literal['all']] = 'all') -> Dict[str, Any]:
        """
        Get the list of committees associated with a specific bill.
        
        Args:
            bill_type: Type of bill (hr, s, hjres, sjres, hconres, sconres, hres, or sres)
            bill_number: Bill number (e.g., 3076)
            congress: Congress number (defaults to current congress from config)
            format: Response format ('xml' or 'json')
            offset: Starting record number (0-based)
            limit: Number of records to return (max 250, or 'all' for all records)
            
        Returns:
            API response data containing list of committees for the specified bill
        """
        self._validate_bill_type(bill_type)
        
        params = {
            'format': format,
            'offset': offset
        }
        
        congress = congress or self.client.config.default_congress
        endpoint = f"{self.base_path}/{congress}/{bill_type.lower()}/{bill_number}/committees"
        return self._get(endpoint, params=params, limit=limit)

    def get_cosponsors(self,
                      bill_type: str,
                      bill_number: int,
                      congress: Optional[int] = None,
                      format: Optional[str] = "json",
                      offset: Optional[int] = 0,
                      limit: Union[int, Literal['all']] = 'all') -> Dict[str, Any]:
        """
        Get the list of cosponsors on a specific bill.
        
        Args:
            bill_type: Type of bill (hr, s, hjres, sjres, hconres, sconres, hres, or sres)
            bill_number: Bill number (e.g., 3076)
            congress: Congress number (defaults to current congress from config)
            format: Response format ('xml' or 'json')
            offset: Starting record number (0-based)
            limit: Number of records to return (max 250, or 'all' for all records)
            
        Returns:
            API response data containing list of cosponsors for the specified bill
        """
        self._validate_bill_type(bill_type)
        
        params = {
            'format': format,
            'offset': offset
        }
        
        congress = congress or self.client.config.default_congress
        endpoint = f"{self.base_path}/{congress}/{bill_type.lower()}/{bill_number}/cosponsors"
        return self._get(endpoint, params=params, limit=limit)

    def get_related_bills(self,
                         bill_type: str,
                         bill_number: int,
                         congress: Optional[int] = None,
                         format: Optional[str] = "json",
                         offset: Optional[int] = 0,
                         limit: Union[int, Literal['all']] = 'all') -> Dict[str, Any]:
        """
        Get the list of related bills to a specific bill.
        
        Args:
            bill_type: Type of bill (hr, s, hjres, sjres, hconres, sconres, hres, or sres)
            bill_number: Bill number (e.g., 3076)
            congress: Congress number (defaults to current congress from config)
            format: Response format ('xml' or 'json')
            offset: Starting record number (0-based)
            limit: Number of records to return (max 250, or 'all' for all records)
            
        Returns:
            API response data containing list of related bills for the specified bill
        """
        self._validate_bill_type(bill_type)
        
        params = {
            'format': format,
            'offset': offset
        }
        
        congress = congress or self.client.config.default_congress
        endpoint = f"{self.base_path}/{congress}/{bill_type.lower()}/{bill_number}/relatedbills"
        return self._get(endpoint, params=params, limit=limit)

    def get_subjects(self,
                    bill_type: str,
                    bill_number: int,
                    congress: Optional[int] = None,
                    format: Optional[str] = "json",
                    offset: Optional[int] = 0,
                    limit: Union[int, Literal['all']] = 'all',
                    from_datetime: Optional[datetime] = None,
                    to_datetime: Optional[datetime] = None) -> Dict[str, Any]:
        """
        Get the list of legislative subjects on a specific bill.
        
        Args:
            bill_type: Type of bill (hr, s, hjres, sjres, hconres, sconres, hres, or sres)
            bill_number: Bill number (e.g., 3076)
            congress: Congress number (defaults to current congress from config)
            format: Response format ('xml' or 'json')
            offset: Starting record number (0-based)
            limit: Number of records to return (max 250, or 'all' for all records)
            from_datetime: Start of update date filter
            to_datetime: End of update date filter
            
        Returns:
            API response data containing list of subjects for the specified bill
        """
        self._validate_bill_type(bill_type)
        
        params = {
            'format': format,
            'offset': offset,
            'fromDateTime': from_datetime.isoformat() if from_datetime else None,
            'toDateTime': to_datetime.isoformat() if to_datetime else None
        }
        
        congress = congress or self.client.config.default_congress
        endpoint = f"{self.base_path}/{congress}/{bill_type.lower()}/{bill_number}/subjects"
        return self._get(endpoint, params=params, limit=limit)

    def get_summaries(self,
                     bill_type: str,
                     bill_number: int,
                     congress: Optional[int] = None,
                     format: Optional[str] = "json",
                     offset: Optional[int] = 0,
                     limit: Union[int, Literal['all']] = 'all') -> Dict[str, Any]:
        """
        Get the list of summaries for a specific bill.
        
        Args:
            bill_type: Type of bill (hr, s, hjres, sjres, hconres, sconres, hres, or sres)
            bill_number: Bill number (e.g., 3076)
            congress: Congress number (defaults to current congress from config)
            format: Response format ('xml' or 'json')
            offset: Starting record number (0-based)
            limit: Number of records to return (max 250, or 'all' for all records)
            
        Returns:
            API response data containing list of summaries for the specified bill
        """
        self._validate_bill_type(bill_type)
        
        params = {
            'format': format,
            'offset': offset
        }
        
        congress = congress or self.client.config.default_congress
        endpoint = f"{self.base_path}/{congress}/{bill_type.lower()}/{bill_number}/summaries"
        return self._get(endpoint, params=params, limit=limit)

    def get_text(self,
                bill_type: str,
                bill_number: int,
                congress: Optional[int] = None,
                format: Optional[str] = "json",
                offset: Optional[int] = 0,
                limit: Union[int, Literal['all']] = 'all') -> Dict[str, Any]:
        """
        Get the list of text versions for a specific bill.
        
        Args:
            bill_type: Type of bill (hr, s, hjres, sjres, hconres, sconres, hres, or sres)
            bill_number: Bill number (e.g., 3076)
            congress: Congress number (defaults to current congress from config)
            format: Response format ('xml' or 'json')
            offset: Starting record number (0-based)
            limit: Number of records to return (max 250, or 'all' for all records)
            
        Returns:
            API response data containing list of text versions for the specified bill
        """
        self._validate_bill_type(bill_type)
        
        params = {
            'format': format,
            'offset': offset
        }
        
        congress = congress or self.client.config.default_congress
        endpoint = f"{self.base_path}/{congress}/{bill_type.lower()}/{bill_number}/text"
        return self._get(endpoint, params=params, limit=limit)

    def get_titles(self,
                  bill_type: str,
                  bill_number: int,
                  congress: Optional[int] = None,
                  format: Optional[str] = "json",
                  offset: Optional[int] = 0,
                  limit: Union[int, Literal['all']] = 'all',
                  from_datetime: Optional[datetime] = None,
                  to_datetime: Optional[datetime] = None) -> Dict[str, Any]:
        """
        Get the list of titles for a specific bill.
        
        Args:
            bill_type: Type of bill (hr, s, hjres, sjres, hconres, sconres, hres, or sres)
            bill_number: Bill number (e.g., 3076)
            congress: Congress number (defaults to current congress from config)
            format: Response format ('xml' or 'json')
            offset: Starting record number (0-based)
            limit: Number of records to return (max 250, or 'all' for all records)
            from_datetime: Start of update date filter
            to_datetime: End of update date filter
            
        Returns:
            API response data containing list of titles for the specified bill
        """
        self._validate_bill_type(bill_type)
        
        params = {
            'format': format,
            'offset': offset,
            'fromDateTime': from_datetime.isoformat() if from_datetime else None,
            'toDateTime': to_datetime.isoformat() if to_datetime else None
        }
        
        congress = congress or self.client.config.default_congress
        endpoint = f"{self.base_path}/{congress}/{bill_type.lower()}/{bill_number}/titles"
        return self._get(endpoint, params=params, limit=limit)