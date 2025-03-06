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
