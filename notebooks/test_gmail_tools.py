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