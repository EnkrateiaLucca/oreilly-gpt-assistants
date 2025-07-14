# tools.py

## Overview

This module provides a unified interface for Google Services integration, combining Gmail and Google Calendar functionality in a single, optimized package. It uses the Singleton pattern to manage service instances efficiently and provides comprehensive tools for email and calendar operations.

## Purpose

The module serves as a:
- Unified Google Services interface
- Optimized service management with singleton pattern
- Comprehensive Gmail and Calendar API wrapper
- Function calling toolkit for OpenAI Assistants
- Production-ready integration solution

## Dependencies

```python
import os
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Any
import json
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import base64
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
```

## Configuration

### OAuth Scopes

```python
SCOPES = [
    'https://www.googleapis.com/auth/gmail.readonly',  # For reading emails
    'https://www.googleapis.com/auth/gmail.send',      # For sending emails
    'https://www.googleapis.com/auth/gmail.modify',    # For modifying emails
    'https://www.googleapis.com/auth/calendar'  # Calendar scope
]
```

These scopes provide comprehensive access to:
- Gmail read operations
- Gmail send operations
- Gmail modification operations
- Google Calendar full access

## Core Architecture

### GoogleServices Class (Singleton)

```python
class GoogleServices:
    _instance = None
    _gmail = None
    _calendar = None
    _credentials = None
```

**Design Pattern**: Singleton pattern ensures only one instance exists

**Benefits**:
- Reduces authentication overhead
- Maintains persistent connections
- Optimizes resource usage
- Prevents credential conflicts

#### Key Methods

##### __new__()

```python
def __new__(cls):
    if cls._instance is None:
        cls._instance = super(GoogleServices, cls).__new__(cls)
        cls._instance._initialize()
    return cls._instance
```

Implements singleton pattern with lazy initialization.

##### _initialize()

```python
def _initialize(self):
    """Initialize credentials and services"""
    self._credentials = self._get_credentials()
    self._gmail = build('gmail', 'v1', credentials=self._credentials)
    self._calendar = build('calendar', 'v3', credentials=self._credentials)
```

Sets up both Gmail and Calendar services with shared credentials.

##### _get_credentials()

```python
def _get_credentials(self):
    """Get and refresh credentials if needed"""
```

Handles comprehensive credential management:
- Loads existing tokens
- Refreshes expired credentials
- Initiates OAuth flow if needed
- Saves credentials for future use

## Gmail Functions

### read_emails()

```python
def read_emails(query: str = "in:inbox", max_results: int = 10) -> List[Dict]:
    """Read emails from Gmail using Gmail API."""
```

**Features**:
- Flexible Gmail search queries
- Handles both simple and multipart messages
- Extracts all relevant metadata
- Base64 decoding for message bodies

**Return Format**:
```python
{
    'id': 'message_id',
    'subject': 'Email subject',
    'sender': 'sender@email.com',
    'date': 'Date string',
    'body': 'Decoded email body'
}
```

### send_email()

```python
def send_email(to: str, subject: str, body: str, 
               attachments: Optional[List[Dict]] = None) -> Dict:
    """Send an email using Gmail API."""
```

**Features**:
- MIME message construction
- Attachment support
- Base64 encoding for API
- Comprehensive error handling

**Attachment Format**:
```python
{
    'filename': 'document.pdf',
    'content': b'file_content_bytes'
}
```

## Calendar Functions

### list_events()

```python
def list_events(max_results: int = 10, time_min: Optional[str] = None, 
                time_max: Optional[str] = None, calendar_id: str = 'primary') -> List[Dict]:
    """List events from Google Calendar."""
```

**Features**:
- Default 7-day time range
- Chronological ordering
- Complete event metadata
- Attendee extraction

**Default Time Range**:
- Start: Current time
- End: 7 days from now

### create_event()

```python
def create_event(summary: str, start_time: str, end_time: str, description: str = '',
                location: str = '', attendees: Optional[List[str]] = None, 
                calendar_id: str = 'primary') -> Dict:
    """Create a new event in Google Calendar."""
```

**Features**:
- ISO format time handling
- Attendee invitations
- UTC timezone standardization
- HTML link generation

### update_event()

```python
def update_event(event_id: str, summary: Optional[str] = None, start_time: Optional[str] = None,
                end_time: Optional[str] = None, description: Optional[str] = None,
                location: Optional[str] = None, attendees: Optional[List[str]] = None, 
                calendar_id: str = 'primary') -> Dict:
    """Update an existing event in Google Calendar."""
```

**Features**:
- Partial updates (only specified fields)
- Preserves existing data
- Flexible parameter handling

### delete_event()

```python
def delete_event(event_id: str, calendar_id: str = 'primary') -> Dict:
    """Delete an event from Google Calendar."""
```

**Features**:
- Simple interface
- Confirmation response
- Error handling

## Usage Examples

### Service Initialization

```python
# Global instance automatically created
services = GoogleServices()

# Access Gmail service
gmail_service = services.gmail

# Access Calendar service
calendar_service = services.calendar
```

### Email Operations

```python
# Read recent emails
emails = read_emails(query="is:unread", max_results=5)

# Send email
result = send_email(
    to="user@example.com",
    subject="Meeting Reminder",
    body="Don't forget about our meeting at 2 PM."
)

# Send with attachment
result = send_email(
    to="user@example.com",
    subject="Report Attached",
    body="Please find the report attached.",
    attachments=[{
        'filename': 'report.pdf',
        'content': pdf_bytes
    }]
)
```

### Calendar Operations

```python
# List upcoming events
events = list_events(max_results=10)

# Create event
result = create_event(
    summary="Team Meeting",
    start_time="2024-01-15T14:00:00Z",
    end_time="2024-01-15T15:00:00Z",
    description="Weekly team sync",
    attendees=["team@company.com"]
)

# Update event
result = update_event(
    event_id="event_123",
    summary="Updated Meeting Title",
    location="Conference Room B"
)

# Delete event
result = delete_event(event_id="event_123")
```

## Error Handling

All functions implement consistent error handling:
- Try-catch blocks for all operations
- Structured error responses
- Detailed error messages
- Graceful degradation

**Error Response Format**:
```python
{
    'success': False,
    'message': 'Error: detailed error description'
}
```

## Performance Optimizations

### Singleton Pattern Benefits

- **Reduced Authentication**: Single credential setup
- **Connection Reuse**: Persistent service instances
- **Memory Efficiency**: Single instance per application
- **Faster Operations**: No repeated initialization

### Credential Management

- **Token Caching**: Persistent token storage
- **Auto-refresh**: Automatic token renewal
- **Scope Validation**: Comprehensive permission checking

## Security Considerations

### Credential Protection

- Store tokens securely
- Use environment variables
- Implement proper access controls
- Regular credential rotation

### API Security

- Input validation
- Rate limiting awareness
- Proper error handling
- Secure token transmission

## Integration with OpenAI Assistants

This module is optimized for OpenAI Assistants:
- JSON-serializable responses
- Consistent error formats
- Clear function signatures
- Comprehensive documentation

## Production Deployment

### Environment Setup

Required files:
- `credentials.json`: OAuth client credentials
- `token.json`: Auto-generated refresh token

### Monitoring

- API quota usage
- Error rates
- Performance metrics
- Authentication failures

## Complete Code

```python
import os
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Any
import json
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import base64
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

# If modifying these scopes, delete the file token.json.
SCOPES = [
    'https://www.googleapis.com/auth/gmail.readonly',  # For reading emails
    'https://www.googleapis.com/auth/gmail.send',      # For sending emails
    'https://www.googleapis.com/auth/gmail.modify',    # For modifying emails
    'https://www.googleapis.com/auth/calendar'  # Calendar scope
]

class GoogleServices:
    _instance = None
    _gmail = None
    _calendar = None
    _credentials = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(GoogleServices, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        """Initialize credentials and services"""
        self._credentials = self._get_credentials()
        self._gmail = build('gmail', 'v1', credentials=self._credentials)
        self._calendar = build('calendar', 'v3', credentials=self._credentials)

    def _get_credentials(self):
        """Get and refresh credentials if needed"""
        creds = None
        if os.path.exists('token.json'):
            with open('token.json', 'r') as token:
                creds = Credentials.from_authorized_user_info(json.load(token), SCOPES)
        
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            with open('token.json', 'w') as token:
                token.write(creds.to_json())
        
        return creds

    @property
    def gmail(self):
        """Get Gmail service"""
        return self._gmail

    @property
    def calendar(self):
        """Get Calendar service"""
        return self._calendar

# Create a global instance
services = GoogleServices()

# Gmail Functions
def read_emails(query: str = "in:inbox", max_results: int = 10) -> List[Dict]:
    """Read emails from Gmail using Gmail API."""
    try:
        results = services.gmail.users().messages().list(
            userId='me', q=query, maxResults=max_results).execute()
        messages = results.get('messages', [])

        emails = []
        for message in messages:
            msg = services.gmail.users().messages().get(
                userId='me', id=message['id']).execute()
            
            headers = msg['payload']['headers']
            subject = next(h['value'] for h in headers if h['name'] == 'Subject')
            sender = next(h['value'] for h in headers if h['name'] == 'From')
            date = next(h['value'] for h in headers if h['name'] == 'Date')
            
            if 'parts' in msg['payload']:
                parts = msg['payload']['parts']
                body = ""
                for part in parts:
                    if part['mimeType'] == 'text/plain':
                        if 'data' in part['body']:
                            body = base64.urlsafe_b64decode(part['body']['data']).decode()
                        break
            else:
                body = base64.urlsafe_b64decode(msg['payload']['body']['data']).decode()

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
    """Send an email using Gmail API."""
    try:
        message = MIMEMultipart()
        message['to'] = to
        message['from'] = "me"
        message['subject'] = subject
        
        msg = MIMEText(body)
        message.attach(msg)
        
        if attachments:
            for attachment in attachments:
                part = MIMEApplication(attachment['content'])
                part.add_header('Content-Disposition', 'attachment', 
                              filename=attachment['filename'])
                message.attach(part)
        
        raw = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')
        services.gmail.users().messages().send(
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

# Calendar Functions
def list_events(max_results: int = 10, time_min: Optional[str] = None, 
                time_max: Optional[str] = None, calendar_id: str = 'primary') -> List[Dict]:
    """List events from Google Calendar."""
    try:
        if not time_min:
            time_min = datetime.utcnow().isoformat() + 'Z'
        if not time_max:
            time_max = (datetime.utcnow() + timedelta(days=7)).isoformat() + 'Z'
            
        events_result = services.calendar.events().list(
            calendarId=calendar_id, 
            timeMin=time_min,
            timeMax=time_max, 
            maxResults=max_results,
            singleEvents=True,
            orderBy='startTime'
        ).execute()
        
        events = events_result.get('items', [])
        
        return [{
            'id': event['id'],
            'summary': event.get('summary', 'No title'),
            'start': event['start'].get('dateTime', event['start'].get('date')),
            'end': event['end'].get('dateTime', event['end'].get('date')),
            'location': event.get('location', ''),
            'description': event.get('description', ''),
            'attendees': [attendee.get('email') for attendee in event.get('attendees', [])]
        } for event in events]
        
    except Exception as e:
        return [{'error': str(e)}]

def create_event(summary: str, start_time: str, end_time: str, description: str = '',
                location: str = '', attendees: Optional[List[str]] = None, 
                calendar_id: str = 'primary') -> Dict:
    """Create a new event in Google Calendar."""
    try:
        event = {
            'summary': summary,
            'location': location,
            'description': description,
            'start': {
                'dateTime': start_time,
                'timeZone': 'UTC',
            },
            'end': {
                'dateTime': end_time,
                'timeZone': 'UTC',
            }
        }
        
        if attendees:
            event['attendees'] = [{'email': email} for email in attendees]
            
        event = services.calendar.events().insert(calendarId=calendar_id, body=event).execute()
        
        return {
            'success': True,
            'event_id': event['id'],
            'html_link': event['htmlLink'],
            'message': 'Event created successfully!'
        }
        
    except Exception as e:
        return {
            'success': False,
            'message': f'Error: {str(e)}'
        }

def update_event(event_id: str, summary: Optional[str] = None, start_time: Optional[str] = None,
                end_time: Optional[str] = None, description: Optional[str] = None,
                location: Optional[str] = None, attendees: Optional[List[str]] = None, 
                calendar_id: str = 'primary') -> Dict:
    """
    Update an existing event in Google Calendar.
    """
    try:
        service = services.calendar
        
        event = service.events().get(calendarId=calendar_id, eventId=event_id).execute()
        
        if summary:
            event['summary'] = summary
        if location:
            event['location'] = location
        if description:
            event['description'] = description
        if start_time:
            event['start']['dateTime'] = start_time
        if end_time:
            event['end']['dateTime'] = end_time
        if attendees:
            event['attendees'] = [{'email': email} for email in attendees]
            
        updated_event = service.events().update(
            calendarId=calendar_id, eventId=event_id, body=event).execute()
        
        return {
            'success': True,
            'event_id': updated_event['id'],
            'html_link': updated_event['htmlLink'],
            'message': 'Event updated successfully!'
        }
        
    except Exception as e:
        return {
            'success': False,
            'message': f'Error: {str(e)}'
        }

def delete_event(event_id: str, calendar_id: str = 'primary') -> Dict:
    """
    Delete an event from Google Calendar.
    """
    try:
        service = services.calendar
        service.events().delete(calendarId=calendar_id, eventId=event_id).execute()
        
        return {
            'success': True,
            'message': 'Event deleted successfully!'
        }
        
    except Exception as e:
        return {
            'success': False,
            'message': f'Error: {str(e)}'
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