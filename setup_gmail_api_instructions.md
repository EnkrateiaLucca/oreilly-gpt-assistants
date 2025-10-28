# Gmail API Setup Tutorial

This tutorial walks you through setting up the Gmail API in order to allow an assistant (or any Python script) to programmatically access Gmail features.

---

## Step 1: Get `credentials.json` from Google Cloud Console

1. Go to [Google Cloud Console](https://console.cloud.google.com).
2. Select your existing project or create a new one.
3. Navigate to **APIs & Services** > **Credentials**.
4. Click **Create Credentials** > **OAuth client ID**.
5. Under **Application type**, choose **Desktop app**.
6. For **Name**, enter: **Gmail API Client**.
7. Click **Create**.
8. In the list of OAuth 2.0 Client IDs, click the **download** icon for your newly created credentials.
9. Save this file as `credentials.json` in the same directory as your script.

**Important:** Make sure the file is named exactly `credentials.json`.

If you do not see a file named `credentials.json`, verify you are downloading the correct type of credentials (Desktop app OAuth client).

---

## Step 2: Enable Gmail API

1. Go back to [Google Cloud Console](https://console.cloud.google.com).
2. Select your project.
3. Navigate to **APIs & Services** > **Library**.
4. Search for **Gmail API**.
5. Click **Enable**.

---

## Step 3: Configure the OAuth Consent Screen

1. In [Google Cloud Console](https://console.cloud.google.com), again select your project.
2. Go to **APIs & Services** > **OAuth consent screen**.
3. Choose **External** as the user type.
4. Fill in the required information:
   - **App name**: `Gmail API Client`
   - **User support email**: your email address
   - **Developer contact information**: your email address
5. Click **Save and Continue**.
6. Click **Save and Continue** again (no need to add additional scopes for basic Gmail API usage).
7. Add your email under **Test users**.
8. Click **Save and Continue**.

---

When you run the script:
1. It will check for credentials.json.
2. If valid, you will be prompted to authenticate in a browser window.
3. Once authenticated, the script will create a token.json file. This file holds your OAuth tokens so that you won’t need to re-authenticate every time.

Important Notes
• Secure Your Credentials: Both credentials.json and token.json contain sensitive information. Add them to your .gitignore and do not commit them to version control.
• Refresh Tokens: The token.json file contains your refresh token; keep this file safe. If it is compromised, revoke the credentials in the Google Cloud Console.
• API Quotas and Limits: Be mindful of your usage so you don’t exceed Google API rate limits.