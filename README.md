# Congress API

A Python wrapper for the Congress.gov API that provides easy access to congressional data including bills, amendments, and member information.

## Features

- Full support for Congress.gov API v3
- Simple and intuitive interface for accessing congressional data
- Built-in pagination handling
- Comprehensive endpoint coverage:
  - Bills and resolutions
  - Amendments
  - Congressional members
- Type hints for better IDE support
- Automatic rate limiting and retry handling
- Configurable through environment variables

## Note

- I currently only have support for Amendments, Bills, and Members
- Currently only supports JSON output because XML isn't any good
- Use with caution, I am not a wonderful coder.

## Quick Start

```python
from congress_api import CongressClient, APIConfig
import os

# Configure the client
config = APIConfig(
    api_key=os.getenv('CONGRESS_API_KEY'),
    base_url='https://api.congress.gov/v3/',
    default_format='json',
    max_retries=3,
    timeout=30,
    max_limit=250,
    default_congress=118
)

# Initialize the client
client = CongressClient(config)

# Get all bills from the current congress
bills = client.bill.list_by_congress()

# Get a specific bill's details
bill = client.bill.get_bill(bill_type='SRES', bill_number=928)

# Get all amendments for a bill
amendments = client.bill.get_amendments(bill_type='SRES', bill_number=928)

# Get member information
member = client.member.get_member_by_id('R000618')  # An example member from Nebraska
```

## Configuration

The library can be configured using environment variables:

- `CONGRESS_API_KEY` (required): Your Congress.gov API key
- `CONGRESS_API_BASE_URL` (optional): API base URL (default: https://api.congress.gov/v3/)
- `CONGRESS_API_FORMAT` (optional): Response format (default: json)
- `CONGRESS_API_MAX_RETRIES` (optional): Maximum retry attempts (default: 3)
- `CONGRESS_API_TIMEOUT` (optional): Request timeout in seconds (default: 30)

## Features in Detail

### Bills

Access bill information with various filters and details:

```python
# List all bills
bills = client.bill.list_all()

# Get bills from a specific congress
bills = client.bill.list_by_congress(congress=118)

# Get a specific bill's details
bill = client.bill.get_bill(bill_type='SRES', bill_number=928, congress=118)

# Get bill actions
actions = client.bill.get_actions(bill_type='SRES', bill_number=928)

# Get bill cosponsors
cosponsors = client.bill.get_cosponsors(bill_type='SRES', bill_number=928)
```

### Amendments

Work with amendment data:

```python
# List all amendments
amendments = client.amendment.list_all()

# Get specific amendment details
amendment = client.amendment.get_amendment(
    amendment_type='SAMDT',
    amendment_number=3362
)

# Get amendment actions
actions = client.amendment.get_actions(
    amendment_type='SAMDT',
    amendment_number=3362
)
```

### Members

Access congressional member information:

```python
# List all members
members = client.member.list_members()

# Get member by Bioguide ID
member = client.member.get_member_by_id('R000618')

# Get member's sponsored legislation
sponsored = client.member.list_sponsored_legislation_by_member_id('R000618')

# Get members by state
state_members = client.member.list_members_by_state('NE')
```

## Pagination

The library handles pagination automatically. You can specify a limit parameter in most list methods:

```python
# Get first 20 results
results = client.bill.list_all(limit=20)

# Get all results (automatically handles pagination)
all_results = client.bill.list_all(limit='all')
```

## Development

To contribute to this project:

1. Clone the repository
2. Install development dependencies:
   ```bash
   pip install -e ".[dev]"
   ```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Getting Help

- For bugs and feature requests, please [open an issue](https://github.com/prolsen/congress_api/issues)

## Credits

Created by Patrick Olsen