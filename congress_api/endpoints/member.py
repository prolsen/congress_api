# congress_api/endpoints/member.py
from typing import Optional, Dict, Any, List, Union, Literal
from .base import BaseEndpoint


class MemberEndpoint(BaseEndpoint):
    """Handles member-related API endpoints."""

    def list_members(self, 
                    format: Optional[str] = "json",
                    offset: Optional[int] = 0,
                    limit: Union[int, Literal['all']] = 20,
                    from_datetime: Optional[str] = None,
                    to_datetime: Optional[str] = None,
                    current_member: Optional[bool] = None) -> Dict[str, Any]:
        """
        Returns a list of congressional members.

        Args:
            format: The data format (xml or json)
            offset: The starting record returned (0 is first)
            limit: Number of records to return (max 250, or 'all' for all records)
            from_datetime: Start timestamp filter (YYYY-MM-DDT00:00:00Z)
            to_datetime: End timestamp filter (YYYY-MM-DDT00:00:00Z)
            current_member: Filter by current member status (true/false)
        """
        params = {
            'format': format,
            'offset': offset,
            'fromDateTime': from_datetime,
            'toDateTime': to_datetime,
            'currentMember': str(current_member).lower() if current_member is not None else None
        }
        return self._get('member', params=params, limit=limit)

    def get_member_by_id(self, bioguide_id: str, format: Optional[str] = "json") -> Dict[str, Any]:
        """
        Returns detailed information for a specified congressional member.

        Args:
            bioguide_id: The bioguide identifier for the member
            format: The data format (xml or json)
        """
        return self._get(f'member/{bioguide_id}', params={'format': format})

    def list_sponsored_legislation_by_member_id(self,
                                 bioguide_id: str,
                                 format: Optional[str] = "json",
                                 offset: Optional[int] = 0,
                                 limit: Union[int, Literal['all']] = 'all') -> Dict[str, Any]:
        """
        Returns the list of legislation sponsored by a specified congressional member.

        Args:
            bioguide_id: The bioguide identifier for the member
            format: The data format (xml or json)
            offset: The starting record returned (0 is first)
            limit: Number of records to return (max 250, or 'all' for all records)
        """
        params = {
            'format': format,
            'offset': offset
        }
        return self._get(f'member/{bioguide_id}/sponsored-legislation', params=params, limit=limit)

    def list_cosponsored_legislation_by_member_id(self,
                                   bioguide_id: str,
                                   format: Optional[str] = "json",
                                   offset: Optional[int] = 0,
                                   limit: Union[int, Literal['all']] = 'all') -> Dict[str, Any]:
        """
        Returns the list of legislation cosponsored by a specified congressional member.

        Args:
            bioguide_id: The bioguide identifier for the member
            format: The data format (xml or json)
            offset: The starting record returned (0 is first)
            limit: Number of records to return (max 250, or 'all' for all records)
        """
        params = {
            'format': format,
            'offset': offset
        }
        return self._get(f'member/{bioguide_id}/cosponsored-legislation', params=params, limit=limit)

    def list_members_by_congress(self,
                               congress: int,
                               format: Optional[str] = "json",
                               offset: Optional[int] = 0,
                               limit: Union[int, Literal['all']] = 20,
                               current_member: Optional[bool] = None) -> Dict[str, Any]:
        """
        Returns the list of members for a specified Congress.

        Args:
            congress: The congress number
            format: The data format (xml or json)
            offset: The starting record returned (0 is first)
            limit: Number of records to return (max 250, or 'all' for all records)
            current_member: Filter by current member status (true/false)
        """
        params = {
            'format': format,
            'offset': offset,
            'currentMember': str(current_member).lower() if current_member is not None else None
        }
        return self._get(f'member/congress/{congress}', params=params, limit=limit)

    def list_members_by_state(self,
                            state_code: str,
                            format: Optional[str] = "json",
                            current_member: Optional[bool] = None) -> Dict[str, Any]:
        """
        Returns a list of members filtered by state.

        Args:
            state_code: Two letter state identifier (e.g., 'CA')
            format: The data format (xml or json)
            current_member: Filter by current member status (true/false)
        """
        params = {
            'format': format,
            'currentMember': str(current_member).lower() if current_member is not None else None
        }
        return self._get(f'member/{state_code}', params=params)

    def list_members_by_state_district(self,
                                     state_code: str,
                                     district: int,
                                     format: Optional[str] = "json",
                                     current_member: Optional[bool] = None) -> Dict[str, Any]:
        """
        Returns a list of members filtered by state and district.

        Args:
            state_code: Two letter state identifier (e.g., 'CA')
            district: The district number
            format: The data format (xml or json)
            current_member: Filter by current member status (true/false)
        """
        params = {
            'format': format,
            'currentMember': str(current_member).lower() if current_member is not None else None
        }
        return self._get(f'member/{state_code}/{district}', params=params)

    def list_members_by_congress_state_district(self,
                                              congress: int,
                                              state_code: str,
                                              district: int,
                                              format: Optional[str] = "json",
                                              current_member: Optional[bool] = None) -> Dict[str, Any]:
        """
        Returns a list of members filtered by congress, state and district.

        Args:
            congress: The congress number
            state_code: Two letter state identifier (e.g., 'CA')
            district: The district number
            format: The data format (xml or json)
            current_member: Filter by current member status (true/false)
        """
        params = {
            'format': format,
            'currentMember': str(current_member).lower() if current_member is not None else None
        }
        return self._get(f'member/congress/{congress}/{state_code}/{district}', params=params)