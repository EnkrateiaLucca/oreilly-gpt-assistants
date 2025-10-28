from google_auth_oauthlib.flow import InstalledAppFlow
import json
import os
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly',
          'https://www.googleapis.com/auth/gmail.send']

def get_refresh_token():
    """
    Get a refresh token using the credentials.json file.
    This should be run locally once to generate the refresh token.
    """
    if not os.path.exists('credentials.json'):
        print("Error: credentials.json not found!")
        print("Please download your credentials.json from Google Cloud Console:")
        print("1. Go to https://console.cloud.google.com")
        print("2. Select your project")
        print("3. Go to 'APIs & Services' > 'Credentials'")
        print("4. Find your OAuth 2.0 Client ID")
        print("5. Click the download button (looks like a download arrow)")
        print("6. Save the file as 'credentials.json' in this directory")
        return
    
    try:
        # Load the credentials file to verify it's valid
        with open('credentials.json', 'r') as f:
            creds_data = json.load(f)
            if 'installed' not in creds_data:
                print("Error: Invalid credentials.json format!")
                print("Make sure you downloaded the correct credentials file.")
                return
            
            client_id = creds_data['installed']['client_id']
            client_secret = creds_data['installed']['client_secret']
            print(f"\nFound credentials for client ID: {client_id}")
        
        # Create the flow
        flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
        
        # Run the OAuth flow
        print("\nStarting OAuth flow...")
        print("A browser window will open. Please complete the authentication process.")
        creds = flow.run_local_server(port=0)
        
        # Print the credentials
        print("\n=== Your Credentials ===")
        print("\nAdd these to your .env file:")
        print(f"GMAIL_CLIENT_ID={creds.client_id}")
        print(f"GMAIL_CLIENT_SECRET={creds.client_secret}")
        print(f"GMAIL_REFRESH_TOKEN={creds.refresh_token}")
        
        print("\nImportant: Save these credentials securely!")
        print("The refresh token is long-lived but can be revoked if needed.")
        
    except Exception as e:
        print(f"\nError: {str(e)}")
        logger.exception("Detailed error:")
        print("\nTroubleshooting steps:")
        print("1. Make sure you have the correct credentials.json file")
        print("2. Verify that the Gmail API is enabled in Google Cloud Console")
        print("3. Check that your OAuth consent screen is properly configured")
        print("4. Ensure you're using a Desktop app type OAuth client")

if __name__ == "__main__":
    get_refresh_token() 