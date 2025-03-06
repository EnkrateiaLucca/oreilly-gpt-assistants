import json
import os
import logging
from google.oauth2 import service_account
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly',
          'https://www.googleapis.com/auth/gmail.send']

def setup_service_account():
    """
    Set up a service account and generate the necessary credentials.
    """
    print("\n=== Gmail API Service Account Setup ===")
    print("\nStep 1: Create a Service Account in Google Cloud Console")
    print("1. Go to https://console.cloud.google.com")
    print("2. Select your project")
    print("3. Go to 'IAM & Admin' > 'Service Accounts'")
    print("4. Click 'Create Service Account'")
    print("5. Name: 'gmail-api-service'")
    print("6. Description: 'Service account for Gmail API access'")
    print("7. Click 'Create and Continue'")
    print("8. Click 'Continue' (no need to grant access)")
    print("9. Click 'Done'")
    print("\nStep 2: Create and Download Service Account Key")
    print("1. Find your new service account in the list")
    print("2. Click on the service account name")
    print("3. Go to the 'Keys' tab")
    print("4. Click 'Add Key' > 'Create new key'")
    print("5. Choose JSON format")
    print("6. Click 'Create'")
    print("7. Save the downloaded file as 'service-account.json'")
    
    if not os.path.exists('service-account.json'):
        print("\nError: service-account.json not found!")
        print("Please follow the steps above to create and download the service account key.")
        return
    
    try:
        # Load the service account credentials
        with open('service-account.json', 'r') as f:
            service_account_info = json.load(f)
        
        # Get the service account email
        service_account_email = service_account_info['client_email']
        print(f"\nFound service account: {service_account_email}")
        
        print("\nStep 3: Enable Domain-Wide Delegation")
        print("1. Go to Google Workspace Admin Console (admin.google.com)")
        print("2. Go to Security > API Controls")
        print("3. Click 'Manage Domain Wide Delegation'")
        print("4. Click 'Add new'")
        print("5. Client ID:", service_account_info['client_id'])
        print("6. OAuth Scopes (one per line):")
        for scope in SCOPES:
            print(f"   {scope}")
        print("7. Click 'Authorize'")
        
        print("\nStep 4: Generate Environment Variables")
        print("\nAdd these to your .env file:")
        print(f"GMAIL_SERVICE_ACCOUNT='{json.dumps(service_account_info)}'")
        print("GMAIL_USER_EMAIL=your-email@yourdomain.com")
        
        print("\nImportant Notes:")
        print("1. Replace 'your-email@yourdomain.com' with the email address you want to use")
        print("2. The service account needs to be granted access to the Gmail API")
        print("3. The user email needs to be in the same domain as your Google Workspace")
        print("4. The service account needs domain-wide delegation enabled")
        
    except Exception as e:
        print(f"\nError: {str(e)}")
        logger.exception("Detailed error:")
        print("\nTroubleshooting steps:")
        print("1. Make sure you have the correct service-account.json file")
        print("2. Verify that the Gmail API is enabled in Google Cloud Console")
        print("3. Check that domain-wide delegation is properly configured")
        print("4. Ensure the service account has the necessary permissions")

if __name__ == "__main__":
    setup_service_account() 