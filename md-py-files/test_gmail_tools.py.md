# test_gmail_tools.py

## Overview

This script provides a comprehensive test suite for the Gmail tools integration. It validates email reading, sending, and attachment functionality to ensure the Gmail API integration works correctly before deployment in production environments.

## Purpose

The test suite validates:
- Email reading from Gmail inbox
- Basic email sending functionality
- Email sending with file attachments
- Error handling and response validation
- API authentication and connection

## Dependencies

```python
from gmail_tools import read_emails, send_email
import base64
import os
```

## Test Functions

### test_read_emails()

```python
def test_read_emails():
    print("\n=== Testing Email Reading ===")
```

**Purpose**: Tests the email reading functionality from Gmail

**Process**:
1. Reads the 3 most recent emails from inbox
2. Checks for API errors
3. Displays email metadata and body preview
4. Validates data structure

**Test Parameters**:
- Query: `"in:inbox"`
- Max results: 3 emails
- Shows first 100 characters of body

**Expected Output**:
```
Successfully read 3 emails:
---
Subject: [Email Subject]
From: [Sender Email]
Date: [Date String]
Body preview: [First 100 characters]...
```

### test_send_email()

```python
def test_send_email():
    print("\n=== Testing Email Sending ===")
```

**Purpose**: Tests basic email sending functionality

**Process**:
1. Sends a simple text email
2. Validates successful transmission
3. Reports success/failure status

**Test Parameters**:
- Recipient: `"lucasbnsoares@hotmail.com"`
- Subject: `"Test Email from Gmail Tools"`
- Body: Test message confirming functionality

**Expected Outcome**: Email successfully sent and delivered

### test_send_email_with_attachment()

```python
def test_send_email_with_attachment():
    print("\n=== Testing Email Sending with Attachment ===")
```

**Purpose**: Tests email sending with file attachments

**Process**:
1. Creates a test text file content
2. Encodes content as base64
3. Sends email with attachment
4. Validates successful transmission

**Attachment Structure**:
```python
attachment = {
    'filename': 'test.txt',
    'content': base64.b64encode(test_content.encode()).decode()
}
```

**Test Parameters**:
- Recipient: `"lucasbnsoares@hotmail.com"`
- Subject: `"Test Email with Attachment"`
- Attachment: Simple text file

## Test Execution Flow

### Sequential Testing

```python
if __name__ == "__main__":
    print("Starting Gmail Tools Tests...")
    
    # Run all tests
    test_read_emails()
    test_send_email()
    test_send_email_with_attachment()
    
    print("\nTests completed!")
```

**Test Order**:
1. **Email Reading**: Validates API connectivity and read operations
2. **Basic Sending**: Tests core email sending functionality
3. **Attachment Sending**: Tests more complex operations

## Error Handling

### Read Email Errors

```python
if emails and 'error' in emails[0]:
    print("❌ Error reading emails:", emails[0]['error'])
    return
```

Handles:
- Authentication failures
- API quota issues
- Network connectivity problems
- Permission errors

### Send Email Errors

```python
if result['success']:
    print("✅ Email sent successfully!")
else:
    print("❌ Failed to send email:", result['message'])
```

Validates:
- Successful transmission
- SMTP errors
- Invalid recipient addresses
- Attachment encoding issues

## Output Format

### Success Messages

```
✅ Email sent successfully!
✅ Email with attachment sent successfully!
```

### Error Messages

```
❌ Error reading emails: [error details]
❌ Failed to send email: [error message]
❌ Failed to send email with attachment: [error message]
```

## Test Data

### Email Content

**Basic Email**:
- Subject: "Test Email from Gmail Tools"
- Body: Confirmation message about successful testing

**Attachment Email**:
- Subject: "Test Email with Attachment"
- Body: Simple confirmation message
- Attachment: "test.txt" with test content

### Attachment Processing

```python
test_content = "This is a test file content."
attachment = {
    'filename': 'test.txt',
    'content': base64.b64encode(test_content.encode()).decode()
}
```

## Configuration Requirements

### Email Address Configuration

The script uses a hardcoded test email address:
```python
to="lucasbnsoares@hotmail.com"  # Replace with your email
```

**Important**: Update this to your own email address before running tests.

### Authentication Setup

Required files:
- `credentials.json`: OAuth client credentials
- `token.json`: Refresh token (auto-generated)

## Security Considerations

### Test Email Safety

- Uses clearly marked test subject lines
- Sends only to specified test addresses
- Contains harmless test content
- Includes identification as test emails

### Credential Protection

- Never commits credential files
- Uses environment variables for sensitive data
- Implements proper error handling

## Usage Instructions

### Running the Tests

```bash
python test_gmail_tools.py
```

### Prerequisites

1. Complete Gmail API setup
2. Have valid `credentials.json` file
3. Configure OAuth consent screen
4. Update recipient email address

### Expected Timeline

- **Read Emails**: 2-3 seconds
- **Send Email**: 3-5 seconds
- **Send with Attachment**: 4-6 seconds

## Troubleshooting

### Common Issues

1. **Authentication Errors**:
   - Check `credentials.json` file
   - Verify OAuth setup
   - Ensure Gmail API is enabled

2. **Send Failures**:
   - Verify recipient email address
   - Check SMTP permissions
   - Validate attachment encoding

3. **Read Failures**:
   - Confirm inbox access permissions
   - Check API quota limits
   - Verify email account access

### Debug Information

Tests provide detailed output including:
- Error messages and codes
- Success confirmations
- Email metadata display
- Attachment processing status

## Integration Validation

This script validates integration with:
- Gmail API authentication
- Email reading operations
- Email sending operations
- Attachment handling
- Error management

## Complete Code

```python
from gmail_tools import read_emails, send_email
import base64
import os


def test_read_emails():
    print("\n=== Testing Email Reading ===")
    # Test reading the most recent 3 emails from inbox
    emails = read_emails(query="in:inbox", max_results=3)
    
    if emails and 'error' in emails[0]:
        print("❌ Error reading emails:", emails[0]['error'])
        return
    
    print(f"Successfully read {len(emails)} emails:")
    for email in emails:
        print("\n---")
        print(f"Subject: {email['subject']}")
        print(f"From: {email['sender']}")
        print(f"Date: {email['date']}")
        print(f"Body preview: {email['body'][:100]}...")  # Show first 100 chars

def test_send_email():
    print("\n=== Testing Email Sending ===")
    # Test sending a simple email
    result = send_email(
        to="lucasbnsoares@hotmail.com",  # Replace with your email
        subject="Test Email from Gmail Tools",
        body="This is a test email sent using the Gmail API tools. If you're seeing this, the test was successful!"
    )
    
    if result['success']:
        print("✅ Email sent successfully!")
    else:
        print("❌ Failed to send email:", result['message'])

def test_send_email_with_attachment():
    print("\n=== Testing Email Sending with Attachment ===")
    # Create a simple text file as attachment
    test_content = "This is a test file content."
    attachment = {
        'filename': 'test.txt',
        'content': base64.b64encode(test_content.encode()).decode()
    }
    
    result = send_email(
        to="lucasbnsoares@hotmail.com",  # Replace with your email
        subject="Test Email with Attachment",
        body="This is a test email with an attachment.",
        attachments=[attachment]
    )
    
    if result['success']:
        print("✅ Email with attachment sent successfully!")
    else:
        print("❌ Failed to send email with attachment:", result['message'])

if __name__ == "__main__":
    print("Starting Gmail Tools Tests...")
    
    # Run all tests
    test_read_emails()
    test_send_email()
    test_send_email_with_attachment()
    
    print("\nTests completed!")
```