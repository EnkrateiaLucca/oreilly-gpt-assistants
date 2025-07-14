# setup_gmail.py

## Overview

This script provides a comprehensive setup guide and automated authentication flow for the Gmail API. It walks users through the entire process of configuring Google Cloud Console, enabling APIs, and obtaining the necessary credentials for Gmail integration.

## Purpose

The script serves as a complete setup assistant for:
- Gmail API project configuration
- OAuth 2.0 credential generation
- Authentication flow completion
- Token file creation and management

## Dependencies

```python
import os
import json
import logging
from google_auth_oauthlib.flow import InstalledAppFlow
```

## Configuration

### OAuth Scopes

```python
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly',
          'https://www.googleapis.com/auth/gmail.send']
```

These scopes provide:
- `gmail.readonly`: Read access to Gmail messages and metadata
- `gmail.send`: Permission to send emails on behalf of the user

### Logging Setup

```python
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
```

## Main Function

### setup_gmail()

```python
def setup_gmail():
    """
    Set up Gmail API credentials.
    """
```

This function provides a step-by-step guided setup process:

#### Step 1: Google Cloud Console Setup

The script guides users through:
1. Creating a new OAuth client ID
2. Selecting the correct application type (Desktop app)
3. Downloading the credentials file
4. Saving it as `credentials.json`

Detailed instructions include:
- Navigating to Google Cloud Console
- Finding the Credentials section
- Creating the OAuth client ID
- Proper file naming and location

#### Step 2: Gmail API Enablement

Instructions for enabling the Gmail API:
1. Accessing the APIs & Services Library
2. Finding the Gmail API
3. Enabling the API for the project

#### Step 3: OAuth Consent Screen Configuration

Complete setup of the OAuth consent screen:
- Choosing External user type
- Required app information
- User support email configuration
- Developer contact information
- Test user addition

#### Step 4: Authentication Flow

Automated authentication process:
```python
# Run the OAuth flow
flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
creds = flow.run_local_server(port=0)

# Save the credentials
with open('token.json', 'w') as token:
    token.write(creds.to_json())
```

## Validation Features

### Credentials File Validation

The script validates the credentials file:
```python
with open('credentials.json', 'r') as f:
    creds_data = json.load(f)
    if 'installed' not in creds_data:
        print("\nError: Invalid credentials.json format!")
        print("Make sure you downloaded the correct credentials file.")
        return
```

This ensures:
- File exists and is readable
- JSON format is valid
- Contains required "installed" key
- Proper structure for Desktop app credentials

### Error Handling

Comprehensive error handling includes:
- File existence checks
- JSON parsing validation
- OAuth flow error capture
- Detailed troubleshooting guidance

## Setup Process Flow

1. **Pre-flight Check**:
   - Verifies `credentials.json` exists
   - Validates file format and structure

2. **Guided Instructions**:
   - Displays step-by-step setup instructions
   - Provides specific URLs and navigation paths
   - Explains each configuration step

3. **Automated Authentication**:
   - Initiates OAuth flow
   - Opens browser for user consent
   - Captures authorization code
   - Exchanges for access/refresh tokens

4. **Token Storage**:
   - Saves credentials to `token.json`
   - Provides security recommendations
   - Explains file management best practices

## Security Recommendations

The script emphasizes security best practices:
- Keep credential files secure
- Add files to `.gitignore`
- Protect refresh tokens
- Understand token lifecycle

## Troubleshooting Support

Built-in troubleshooting guidance:
- Common error scenarios
- Step-by-step resolution
- Verification checkpoints
- Alternative solutions

## Usage Instructions

### Running the Setup

```bash
python setup_gmail.py
```

### Prerequisites

Before running:
1. Have a Google Cloud project created
2. Access to Google Cloud Console
3. Valid Google account for authentication

### Expected Outputs

Successful completion produces:
- `token.json` file with refresh token
- Confirmation messages
- Security reminders
- Next steps guidance

## Integration with Other Tools

This setup script prepares the environment for:
- `gmail_tools.py` functionality
- OpenAI Assistant integrations
- Automated email processing
- Production deployments

## Complete Code

```python
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
```