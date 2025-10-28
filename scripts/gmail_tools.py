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
