# example.py
from congress_api import CongressClient
from congress_api.config import load_config
from congress_api.exceptions import CongressAPIError
from pprint import pprint

def main():
    """Main function demonstrating client usage."""       
    try:
        # Load the configuration
        config = load_config()
        
        # Initialize the client
        client = CongressClient(config)

        # Get all bills from the current congress
        bills = client.bill.list_by_congress(limit=5)
        pprint(bills)
        
        # Get a specific bill's details
        bill = client.bill.get_bill(bill_type='SRES', bill_number=928)
        pprint(bill)
        
    except CongressAPIError as e:
        print(f"\nAPI Error: {e.message}")
        if e.status_code:
            print(f"Status Code: {e.status_code}")
        if e.response:
            print(f"Response: {e.response}")
    except Exception as e:
        print(f"\nUnexpected error: {str(e)}")

if __name__ == "__main__":
    main()