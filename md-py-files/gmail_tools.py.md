# gmail_tools.py

## Overview

This module provides Gmail API integration tools for reading and sending emails programmatically. It handles OAuth 2.0 authentication, manages API credentials, and provides simple interfaces for common email operations.

## Purpose

The module enables:
- Reading emails from Gmail with flexible search queries
- Sending emails with optional attachments
- Automatic handling of OAuth authentication and token management
- Integration with OpenAI Assistants for email-based automation

## Dependencies

```python
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import os
from datetime import datetime
from typing import List, Dict, Optional
import base64
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import json
```

## Configuration

### OAuth Scopes

```python
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly',
          'https://www.googleapis.com/auth/gmail.send']
```

These scopes allow:
- Reading email messages and metadata
- Sending emails on behalf of the authenticated user

## Core Functions

### get_gmail_service()

```python
def get_gmail_service():
    """
    Get or create Gmail API service with proper authentication.
    """
```

This function handles the authentication flow:
1. Checks for existing `token.json` file
2. Validates and refreshes credentials if needed
3. Initiates OAuth flow if no valid credentials exist
4. Saves credentials for future use
5. Returns an authenticated Gmail API service object

### read_emails()

```python
def read_emails(query: str = "in:inbox", max_results: int = 10) -> List[Dict]:
    """
    Read emails from Gmail using Gmail API.
    
    Args:
        query (str): Gmail search query
        max_results (int): Maximum number of results to return
        
    Returns:
        List[Dict]: List of email messages with their details
    """
```

Features:
- **Flexible querying**: Uses Gmail's search syntax (e.g., "from:sender@email.com", "is:unread")
- **Message parsing**: Extracts subject, sender, date, and body
- **Body decoding**: Handles both simple and multipart messages
- **Error handling**: Returns error information if API calls fail

Return format:
```python
{
    'id': 'message_id',
    'subject': 'Email subject',
    'sender': 'sender@email.com',
    'date': 'Thu, 1 Jan 2024 12:00:00 +0000',
    'body': 'Email body content'
}
```

### send_email()

```python
def send_email(to: str, subject: str, body: str, 
               attachments: Optional[List[Dict]] = None) -> Dict:
    """
    Send an email using Gmail API.
    
    Args:
        to (str): Recipient email address
        subject (str): Email subject
        body (str): Email body content
        attachments (Optional[List[Dict]]): List of attachments with filename and content
        
    Returns:
        Dict: Response containing success status and message
    """
```

Features:
- **MIME message creation**: Properly formats emails with headers
- **Attachment support**: Can include multiple file attachments
- **Base64 encoding**: Encodes message for Gmail API transmission
- **Error handling**: Returns success/failure status with messages

Attachment format:
```python
{
    'filename': 'document.pdf',
    'content': b'file_content_bytes'
}
```

## Usage Examples

### Reading Emails

```python
# Read latest 5 emails from inbox
emails = read_emails(query="in:inbox", max_results=5)

# Read unread emails from specific sender
emails = read_emails(query="is:unread from:boss@company.com", max_results=10)

# Search for emails with specific subject
emails = read_emails(query="subject:'Meeting Request'", max_results=20)
```

### Sending Emails

```python
# Send simple text email
result = send_email(
    to="recipient@example.com",
    subject="Test Email",
    body="This is a test email from the Gmail tools."
)

# Send email with attachments
result = send_email(
    to="recipient@example.com",
    subject="Report Attached",
    body="Please find the report attached.",
    attachments=[
        {
            'filename': 'report.pdf',
            'content': pdf_content_bytes
        }
    ]
)
```

## Authentication Flow

1. **First Run**:
   - Requires `credentials.json` from Google Cloud Console
   - Opens browser for user authentication
   - Saves refresh token in `token.json`

2. **Subsequent Runs**:
   - Uses saved `token.json`
   - Automatically refreshes expired tokens
   - No user interaction required

## Error Handling

The module includes comprehensive error handling:
- Returns error dictionaries instead of raising exceptions
- Provides detailed error messages for debugging
- Handles common issues like expired tokens and API limits

## Security Considerations

- Store `credentials.json` and `token.json` securely
- Never commit these files to version control
- Use `.gitignore` to exclude credential files
- Consider using environment variables for production

## Integration with OpenAI Assistants

This module is designed to work as a function tool for OpenAI Assistants:
- Functions return JSON-serializable results
- Error handling prevents assistant crashes
- Simple interfaces for common operations

## Complete Code

```python
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import os
from datetime import datetime
from typing import List, Dict, Optional
import base64
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import json

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly',
          'https://www.googleapis.com/auth/gmail.send']

def get_gmail_service():
    """
    Get or create Gmail API service with proper authentication.
    """
    creds = None
    if os.path.exists('token.json'):
        with open('token.json') as token:
            creds = Credentials.from_authorized_user_info(json.load(token), SCOPES)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    return build('gmail', 'v1', credentials=creds)

def read_emails(query: str = "in:inbox", max_results: int = 10) -> List[Dict]:
    """
    Read emails from Gmail using Gmail API.
    
    Args:
        query (str): Gmail search query
        max_results (int): Maximum number of results to return
        
    Returns:
        List[Dict]: List of email messages with their details
    """
    try:
        service = get_gmail_service()
        results = service.users().messages().list(
            userId='me', q=query, maxResults=max_results).execute()
        messages = results.get('messages', [])

        emails = []
        for message in messages:
            msg = service.users().messages().get(
                userId='me', id=message['id']).execute()
            
            headers = msg['payload']['headers']
            subject = next(h['value'] for h in headers if h['name'] == 'Subject')
            sender = next(h['value'] for h in headers if h['name'] == 'From')
            date = next(h['value'] for h in headers if h['name'] == 'Date')
            
            # Get email body
            if 'parts' in msg['payload']:
                parts = msg['payload']['parts']
                body = ""
                for part in parts:
                    if part['mimeType'] == 'text/plain':
                        if 'data' in part['body']:
                            body = base64.urlsafe_b64decode(
                                part['body']['data']).decode()
                        break
            else:
                body = base64.urlsafe_b64decode(
                    msg['payload']['body']['data']).decode()

            emails.append({
                'id': message['id'],
                'subject': subject,
                'sender': sender,
                'date': date,
                'body': body
            })

        return emails
    except Exception as e:
        return [{'error': str(e)}]

def send_email(to: str, subject: str, body: str, 
               attachments: Optional[List[Dict]] = None) -> Dict:
    """
    Send an email using Gmail API.
    
    Args:
        to (str): Recipient email address
        subject (str): Email subject
        body (str): Email body content
        attachments (Optional[List[Dict]]): List of attachments with filename and content
        
    Returns:
        Dict: Response containing success status and message
    """
    try:
        service = get_gmail_service()
        
        message = MIMEMultipart()
        message['to'] = to
        message['from'] = "me"
        message['subject'] = subject
        
        msg = MIMEText(body)
        message.attach(msg)
        
        if attachments:
            for attachment in attachments:
                part = MIMEApplication(attachment['content'])
                part.add_header(
                    'Content-Disposition', 'attachment', 
                    filename=attachment['filename'])
                message.attach(part)
        
        raw = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')
        service.users().messages().send(
            userId='me', body={'raw': raw}).execute()
        
        return {
            "success": True,
            "message": "Email sent successfully!"
        }
    except Exception as e:
        return {
            "success": False,
            "message": f"Error: {str(e)}"
        }

# Example usage
if __name__ == "__main__":
    # Example of reading emails
    emails = read_emails(query="in:inbox", max_results=5)
    print("Read emails:", emails)
    
    # Example of sending an email
    result = send_email(
        to="recipient@example.com",
        subject="Test Email",
        body="This is a test email from the Gmail tools."
    )
    print("Send email result:", result)
```