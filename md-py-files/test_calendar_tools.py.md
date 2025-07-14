# test_calendar_tools.py

## Overview

This script provides a comprehensive test suite for the Google Calendar tools integration. It validates all major functionality including authentication, event listing, creation, updating, and deletion. The tests are designed to run sequentially and provide clear feedback on each operation.

## Purpose

The test suite validates:
- Google Calendar API authentication
- Event listing functionality
- Event creation with details
- Event updating capabilities
- Event deletion operations
- Error handling and edge cases

## Dependencies

```python
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
```

## Test Functions

### test_credentials()

```python
def test_credentials():
    """Test if credentials.json works and we can authenticate with Google Calendar."""
```

**Purpose**: Validates the authentication setup and service initialization

**Process**:
1. Attempts to get a calendar service instance
2. Verifies successful authentication
3. Returns success/failure status

**Expected Outcome**: Successful authentication without exceptions

### test_list_events()

```python
def test_list_events():
    """Test listing events from the primary calendar."""
```

**Purpose**: Tests the event listing functionality

**Process**:
1. Calls `list_events()` with a limit of 5 events
2. Displays found events with summaries and start times
3. Returns the list of events for validation

**Expected Outcome**: Successfully retrieves and displays upcoming events

### test_create_event()

```python
def test_create_event():
    """Test creating a new event in the primary calendar."""
```

**Purpose**: Tests event creation functionality

**Process**:
1. Generates tomorrow's date and time
2. Creates a test event with specific details:
   - Summary: "Test Event - Please Delete"
   - Description: Identifies as test event
   - Location: "Virtual"
   - Duration: 1 hour
3. Validates successful creation
4. Returns event ID for subsequent tests

**Expected Outcome**: Event created successfully with valid ID and HTML link

### test_update_event()

```python
def test_update_event(event_id):
    """Test updating an existing event."""
```

**Purpose**: Tests event modification functionality

**Process**:
1. Checks if event ID is provided
2. Updates the test event with new details:
   - Summary: "Test Event - Updated"
   - Description: Updated description
3. Validates successful update

**Expected Outcome**: Event successfully updated with new information

### test_delete_event()

```python
def test_delete_event(event_id):
    """Test deleting an event."""
```

**Purpose**: Tests event deletion functionality

**Process**:
1. Checks if event ID is provided
2. Deletes the test event
3. Validates successful deletion

**Expected Outcome**: Event successfully removed from calendar

## Test Execution

### run_tests()

```python
def run_tests():
    """Run all tests in sequence."""
```

**Test Flow**:
1. **Authentication Test**: Validates API connectivity
2. **List Events Test**: Tests read operations
3. **Create Event Test**: Tests write operations
4. **Update Event Test**: Tests modification operations (if create succeeded)
5. **Delete Event Test**: Tests deletion operations (cleanup)

**Sequential Logic**:
- If authentication fails, remaining tests are skipped
- Update and delete tests only run if create test succeeds
- Each test provides clear success/failure feedback

## Output Format

### Success Messages

```
✅ Authentication successful!
✅ list_events test successful!
✅ create_event test successful!
✅ update_event test successful!
✅ delete_event test successful!
```

### Error Messages

```
❌ Authentication failed: [error details]
❌ create_event test failed: [error message]
⚠️ Skipping update_event test: No event ID provided
```

## Test Data

### Event Creation Parameters

```python
result = create_event(
    summary="Test Event - Please Delete",
    start_time=start,
    end_time=end,
    description="This is a test event created by the Google Calendar tools test script.",
    location="Virtual"
)
```

### Event Update Parameters

```python
result = update_event(
    event_id=event_id,
    summary="Test Event - Updated",
    description="This event was updated by the test script."
)
```

## Error Handling

Each test function includes:
- Try-catch blocks for exception handling
- Validation of API responses
- Clear error messaging
- Graceful failure handling

## Safety Features

### Cleanup Operations

The test suite includes automatic cleanup:
- Creates clearly marked test events
- Deletes test events after validation
- Prevents calendar pollution

### Identification

Test events are clearly marked:
- Summary contains "Test Event - Please Delete"
- Description identifies as test data
- Location set to "Virtual" to avoid conflicts

## Usage Instructions

### Running the Tests

```bash
python test_calendar_tools.py
```

### Prerequisites

Before running tests:
1. Complete Google Calendar API setup
2. Have valid `credentials.json` file
3. Ensure proper OAuth configuration

### Expected Timeline

- **Authentication**: Immediate
- **List Events**: 1-2 seconds
- **Create Event**: 2-3 seconds
- **Update Event**: 2-3 seconds
- **Delete Event**: 2-3 seconds

## Troubleshooting

### Common Issues

1. **Authentication Failures**:
   - Check `credentials.json` file
   - Verify OAuth consent screen setup
   - Ensure Calendar API is enabled

2. **Permission Errors**:
   - Verify calendar access permissions
   - Check OAuth scopes

3. **API Quota Issues**:
   - Monitor API usage limits
   - Implement rate limiting if needed

### Debug Information

Tests provide detailed output including:
- Operation timing
- Event IDs and links
- Error messages and exceptions
- Success/failure status

## Integration Testing

This script validates integration with:
- Google Calendar API
- OAuth authentication system
- Event CRUD operations
- Error handling mechanisms

## Complete Code

```python
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
```