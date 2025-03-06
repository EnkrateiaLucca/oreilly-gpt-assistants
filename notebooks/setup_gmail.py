import os
import json
import logging
from google_auth_oauthlib.flow import InstalledAppFlow

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly',
          'https://www.googleapis.com/auth/gmail.send']

def setup_gmail():
    """
    Set up Gmail API credentials.
    """
    print("\n=== Gmail API Setup ===")
    print("\nStep 1: Get credentials.json from Google Cloud Console")
    print("1. Go to https://console.cloud.google.com")
    print("2. Select your project")
    print("3. Go to 'APIs & Services' > 'Credentials'")
    print("4. Click 'Create Credentials' > 'OAuth client ID'")
    print("5. Choose 'Desktop app' as the application type")
    print("6. Name: 'Gmail API Client'")
    print("7. Click 'Create'")
    print("8. Click the download button (looks like a download arrow)")
    print("9. Save the file as 'credentials.json' in this directory")
    
    if not os.path.exists('credentials.json'):
        print("\nError: credentials.json not found!")
        print("Please follow the steps above to download your credentials.")
        return
    
    try:
        # Verify the credentials file is valid
        with open('credentials.json', 'r') as f:
            creds_data = json.load(f)
            if 'installed' not in creds_data:
                print("\nError: Invalid credentials.json format!")
                print("Make sure you downloaded the correct credentials file.")
                return
        
        print("\nFound valid credentials.json")
        
        print("\nStep 2: Enable Gmail API")
        print("1. Go to https://console.cloud.google.com")
        print("2. Select your project")
        print("3. Go to 'APIs & Services' > 'Library'")
        print("4. Search for 'Gmail API'")
        print("5. Click 'Enable'")
        
        print("\nStep 3: Configure OAuth Consent Screen")
        print("1. Go to https://console.cloud.google.com")
        print("2. Select your project")
        print("3. Go to 'APIs & Services' > 'OAuth consent screen'")
        print("4. Choose 'External' user type")
        print("5. Fill in the required information:")
        print("   - App name: 'Gmail API Client'")
        print("   - User support email: your email")
        print("   - Developer contact information: your email")
        print("6. Click 'Save and Continue'")
        print("7. Click 'Save and Continue' (no need to add scopes)")
        print("8. Add your email as a test user")
        print("9. Click 'Save and Continue'")
        
        print("\nStep 4: Run the authentication flow")
        print("A browser window will open. Please complete the authentication process.")
        
        # Run the OAuth flow
        flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
        
        # Save the credentials
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
        
        print("\n✅ Setup completed successfully!")
        print("\nImportant Notes:")
        print("1. Keep your credentials.json and token.json files secure")
        print("2. Add both files to your .gitignore")
        print("3. The token.json file contains your refresh token - keep it safe")
        
    except Exception as e:
        print(f"\nError: {str(e)}")
        logger.exception("Detailed error:")
        print("\nTroubleshooting steps:")
        print("1. Make sure you have the correct credentials.json file")
        print("2. Verify that the Gmail API is enabled")
        print("3. Check that your OAuth consent screen is properly configured")
        print("4. Ensure you're using a Desktop app type OAuth client")

if __name__ == "__main__":
    setup_gmail() 