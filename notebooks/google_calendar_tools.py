import os
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Any
import json
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar']  # Full access to Google Calendar

def get_calendar_service():
    """
    Get or create Google Calendar API service with proper authentication.
    """
    creds = None
    if os.path.exists('token.json'):
        with open('token.json', 'r') as token:
            token_data = json.load(token)
            # Check if calendar scope is included in the token
            token_scopes = token_data.get('scopes', [])
            if 'https://www.googleapis.com/auth/calendar' not in token_scopes:
                # Force re-authentication with the correct scopes
                print("Calendar scope missing, need to re-authenticate")
                creds = None
            else:
                creds = Credentials.from_authorized_user_info(token_data, SCOPES)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            # Remove the existing token.json to force re-authentication
            if os.path.exists('token.json'):
                os.rename('token.json', 'token.json.bak')
                print("Renamed existing token.json to token.json.bak")
            
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('calendar', 'v3', credentials=creds)
    return service

def list_events(max_results: int = 10, time_min: Optional[str] = None, 
                time_max: Optional[str] = None, calendar_id: str = 'primary') -> List[Dict]:
    """
    List events from Google Calendar.
    
    Args:
        max_results (int): Maximum number of events to return
        time_min (str): Start time in ISO format (default: now)
        time_max (str): End time in ISO format (default: 7 days from now)
        calendar_id (str): Calendar ID (default: primary)
        
    Returns:
        List[Dict]: List of events with their details
    """
    try:
        service = get_calendar_service()
        
        # Default time range if not specified
        if not time_min:
            time_min = datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
        if not time_max:
            time_max = (datetime.utcnow() + timedelta(days=7)).isoformat() + 'Z'
            
        events_result = service.events().list(
            calendarId=calendar_id, 
            timeMin=time_min,
            timeMax=time_max, 
            maxResults=max_results,
            singleEvents=True,
            orderBy='startTime'
        ).execute()
        
        events = events_result.get('items', [])
        
        formatted_events = []
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            end = event['end'].get('dateTime', event['end'].get('date'))
            
            formatted_event = {
                'id': event['id'],
                'summary': event.get('summary', 'No title'),
                'start': start,
                'end': end,
                'location': event.get('location', ''),
                'description': event.get('description', ''),
                'attendees': [attendee.get('email') for attendee in event.get('attendees', [])]
            }
            formatted_events.append(formatted_event)
            
        return formatted_events
        
    except Exception as e:
        return [{'error': str(e)}]

def create_event(summary: str, start_time: str, end_time: str, description: str = '',
                location: str = '', attendees: Optional[List[str]] = None, 
                calendar_id: str = 'primary') -> Dict:
    """
    Create a new event in Google Calendar.
    
    Args:
        summary (str): Event title
        start_time (str): Start time in ISO format
        end_time (str): End time in ISO format
        description (str): Event description
        location (str): Event location
        attendees (List[str]): List of attendee email addresses
        calendar_id (str): Calendar ID (default: primary)
        
    Returns:
        Dict: Response containing the created event details or error
    """
    try:
        service = get_calendar_service()
        
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
            
        event = service.events().insert(calendarId=calendar_id, body=event).execute()
        
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
    
    Args:
        event_id (str): ID of the event to update
        summary (str): Event title
        start_time (str): Start time in ISO format
        end_time (str): End time in ISO format
        description (str): Event description
        location (str): Event location
        attendees (List[str]): List of attendee email addresses
        calendar_id (str): Calendar ID (default: primary)
        
    Returns:
        Dict: Response containing the updated event details or error
    """
    try:
        service = get_calendar_service()
        
        # Get the existing event
        event = service.events().get(calendarId=calendar_id, eventId=event_id).execute()
        
        # Update fields if provided
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
    
    Args:
        event_id (str): ID of the event to delete
        calendar_id (str): Calendar ID (default: primary)
        
    Returns:
        Dict: Response containing success status and message
    """
    try:
        service = get_calendar_service()
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
    # Example of listing events
    events = list_events(max_results=5)
    print("Events:", events)
    
    # Example of creating an event
    start = (datetime.utcnow() + timedelta(days=1)).isoformat() + 'Z'
    end = (datetime.utcnow() + timedelta(days=1, hours=1)).isoformat() + 'Z'
    
    result = create_event(
        summary="Test Event",
        start_time=start,
        end_time=end,
        description="This is a test event created by Google Calendar tools.",
        attendees=["test@example.com"]
    )
    print("Create event result:", result)