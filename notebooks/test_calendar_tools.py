import os
import json
from datetime import datetime, timedelta
from google_calendar_tools import (
    get_calendar_service,
    list_events,
    create_event,
    update_event,
    delete_event
)

def test_credentials():
    """Test if credentials.json works and we can authenticate with Google Calendar."""
    try:
        print("Testing credentials and authentication...")
        service = get_calendar_service()
        print("✅ Authentication successful!")
        return True
    except Exception as e:
        print(f"❌ Authentication failed: {str(e)}")
        return False

def test_list_events():
    """Test listing events from the primary calendar."""
    try:
        print("\nTesting list_events...")
        events = list_events(max_results=5)
        print(f"Found {len(events)} upcoming events:")
        for i, event in enumerate(events):
            print(f"{i+1}. {event.get('summary')} - {event.get('start')}")
        print("✅ list_events test successful!")
        return events
    except Exception as e:
        print(f"❌ list_events test failed: {str(e)}")
        return []

def test_create_event():
    """Test creating a new event in the primary calendar."""
    try:
        print("\nTesting create_event...")
        # Create an event tomorrow
        start = (datetime.utcnow() + timedelta(days=1)).isoformat() + 'Z'
        end = (datetime.utcnow() + timedelta(days=1, hours=1)).isoformat() + 'Z'
        
        result = create_event(
            summary="Test Event - Please Delete",
            start_time=start,
            end_time=end,
            description="This is a test event created by the Google Calendar tools test script.",
            location="Virtual"
        )
        
        if result.get('success'):
            print(f"✅ create_event test successful!")
            print(f"Event created with ID: {result.get('event_id')}")
            print(f"View event at: {result.get('html_link')}")
            return result.get('event_id')
        else:
            print(f"❌ create_event test failed: {result.get('message')}")
            return None
    except Exception as e:
        print(f"❌ create_event test failed with exception: {str(e)}")
        return None

def test_update_event(event_id):
    """Test updating an existing event."""
    if not event_id:
        print("\n⚠️ Skipping update_event test: No event ID provided")
        return False
        
    try:
        print("\nTesting update_event...")
        result = update_event(
            event_id=event_id,
            summary="Test Event - Updated",
            description="This event was updated by the test script."
        )
        
        if result.get('success'):
            print(f"✅ update_event test successful!")
            print(f"Updated event: {result.get('html_link')}")
            return True
        else:
            print(f"❌ update_event test failed: {result.get('message')}")
            return False
    except Exception as e:
        print(f"❌ update_event test failed with exception: {str(e)}")
        return False

def test_delete_event(event_id):
    """Test deleting an event."""
    if not event_id:
        print("\n⚠️ Skipping delete_event test: No event ID provided")
        return False
        
    try:
        print("\nTesting delete_event...")
        result = delete_event(event_id=event_id)
        
        if result.get('success'):
            print(f"✅ delete_event test successful!")
            return True
        else:
            print(f"❌ delete_event test failed: {result.get('message')}")
            return False
    except Exception as e:
        print(f"❌ delete_event test failed with exception: {str(e)}")
        return False

def run_tests():
    """Run all tests in sequence."""
    print("=== Google Calendar Tools Test ===")
    
    # Test authentication first
    if not test_credentials():
        print("\n⚠️ Authentication failed, skipping remaining tests.")
        return
    
    # Test list_events
    test_list_events()
    
    # Test create_event
    event_id = test_create_event()
    
    if event_id:
        # Test update_event if create was successful
        test_update_event(event_id)
        
        # Test delete_event to clean up
        test_delete_event(event_id)
    
    print("\n=== Test Summary ===")
    print("All tests completed. Check the output above for results.")

if __name__ == "__main__":
    run_tests()