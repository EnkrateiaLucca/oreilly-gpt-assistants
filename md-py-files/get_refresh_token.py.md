# get_refresh_token.py

## Overview

This script is a utility for obtaining Gmail API refresh tokens through the OAuth 2.0 authentication flow. It's designed to be run locally once to generate the long-lived refresh token that can be used in production environments without requiring repeated user authentication.

## Purpose

The script handles the OAuth 2.0 authorization flow for Gmail API access, allowing users to:
- Authenticate with their Google account
- Grant permission to read and send emails
- Generate a refresh token for persistent API access

## Dependencies

```python
from google_auth_oauthlib.flow import InstalledAppFlow
import json
import os
import logging
```

## Configuration

### OAuth Scopes

The script requests the following Gmail API scopes:

```python
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly',
          'https://www.googleapis.com/auth/gmail.send']
```

- `gmail.readonly`: Allows reading email messages and metadata
- `gmail.send`: Allows sending email on behalf of the authenticated user

## Main Functionality

### get_refresh_token() Function

```python
def get_refresh_token():
    """
    Get a refresh token using the credentials.json file.
    This should be run locally once to generate the refresh token.
    """
```

This function performs the following steps:

1. **Credential File Validation**
   - Checks if `credentials.json` exists
   - Provides detailed instructions if missing
   - Validates the JSON structure

2. **OAuth Flow Initialization**
   - Creates an `InstalledAppFlow` from the credentials file
   - Configures it with the required Gmail scopes

3. **Authentication Process**
   - Opens a browser window for user authentication
   - Runs a local server to receive the OAuth callback
   - Captures the authentication credentials

4. **Credential Output**
   - Displays the client ID, client secret, and refresh token
   - Provides instructions for adding them to the `.env` file

## Error Handling

The script includes comprehensive error handling:

```python
try:
    # OAuth flow logic
except Exception as e:
    print(f"\nError: {str(e)}")
    logger.exception("Detailed error:")
    print("\nTroubleshooting steps:")
    print("1. Make sure you have the correct credentials.json file")
    print("2. Verify that the Gmail API is enabled in Google Cloud Console")
    print("3. Check that your OAuth consent screen is properly configured")
    print("4. Ensure you're using a Desktop app type OAuth client")
```

## Usage Instructions

1. **Prerequisites**:
   - Enable Gmail API in Google Cloud Console
   - Create OAuth 2.0 credentials (Desktop application type)
   - Download credentials as `credentials.json`

2. **Running the Script**:
   ```bash
   python get_refresh_token.py
   ```

3. **Authentication Flow**:
   - A browser window will open
   - Log in to your Google account
   - Grant the requested permissions
   - The script will capture the refresh token

4. **Save Credentials**:
   - Copy the displayed credentials
   - Add them to your `.env` file:
     ```
     GMAIL_CLIENT_ID=your_client_id
     GMAIL_CLIENT_SECRET=your_client_secret
     GMAIL_REFRESH_TOKEN=your_refresh_token
     ```

## Security Considerations

- The refresh token provides long-term access to the Gmail account
- Store credentials securely and never commit them to version control
- Refresh tokens can be revoked through Google Account settings
- Use environment variables or secure credential management systems

## Troubleshooting

Common issues and solutions:

1. **Missing credentials.json**:
   - Download from Google Cloud Console
   - Ensure it's a Desktop app OAuth client

2. **Invalid credentials format**:
   - Verify the JSON structure contains an "installed" key
   - Re-download if necessary

3. **Authentication errors**:
   - Check Gmail API is enabled
   - Verify OAuth consent screen configuration
   - Ensure correct scopes are requested

## Complete Code

```python
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
```