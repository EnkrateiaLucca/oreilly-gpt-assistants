# Slack API App Setup

Here’s a full tutorial in Markdown for getting started with the Slack API to create agents using Slack + LangChain, including setup, scopes, tokens, and Socket Mode.

⸻

This guide walks you through setting up a Slack App for building an intelligent agent using LangChain, including scopes, tokens, and event handling.

⸻

✅ 1. Set Up Your Slack App

Follow the Slack API Quickstart Guide to create your app.

Steps:
1.	Go to https://api.slack.com/apps and click “Create New App.”
2.	Choose “From scratch” and give your app a name.
3.	Select your Slack workspace.
4.	After creation, configure the following:
  - Basic Information → Add a description and app icon if desired.
  - App Home:
  - Enable Allow users to send Slash commands and messages from the messages tab.

⸻

✅ 2. Set Up OAuth Scopes and Tokens

🔑 Bot Token (SLACK_BOT_TOKEN)

This allows your bot to send messages, read conversations, and respond to users.

Add these Bot Token Scopes under OAuth & Permissions → Scopes:

Scope Description
chat:write	Send messages as the bot
im:history	Read direct messages the bot gets
im:write	Start conversations with users
app_mentions:read	Read messages mentioning your bot

After setting scopes, click Install to Workspace to get your SLACK_BOT_TOKEN.

⸻

🔑 App-Level Token (SLACK_APP_TOKEN)

This is needed to use Socket Mode.

Steps:
1. Go to App-Level Tokens (left-hand menu).
2. Click Generate Token and Scopes.
3. Give it a name (e.g., socket-mode-token).
4. Add this scope:

Scope	Description
connections:write	Allows Socket Mode usage


	5.	Generate the token and save it as SLACK_APP_TOKEN.

⸻

✅ 3. Enable Socket Mode

Socket Mode allows your app to receive events through a WebSocket.

Steps:
	•	Go to Socket Mode in the sidebar.
	•	Toggle Enabled.
	•	Select your App-Level Token.

⸻

✅ 4. Subscribe to Events

To respond to messages, subscribe to the following events:

In Event Subscriptions:
	•	Turn On.
	•	Add your Socket Mode handler endpoint (or none if using the socket-mode package).

Under Subscribe to Bot Events:

Event	Description
message.im	Get DMs sent to your bot
app_mention	Get messages where the bot is mentioned



⸻

✅ 5. Invite the Bot to Channels (Optional)

To let the bot operate in channels:

/invite @your_bot_name



⸻

✅ 6. Set Up Your Environment Variables

`SLACK_BOT_TOKEN=xoxb-XXXXXXXXXXXX`
`SLACK_APP_TOKEN=xapp-XXXXXXXXXXXX`

⸻

✅ 7. Example Python Implementation

Ensure you have:

`pip install slack_bolt python-dotenv slack_sdk`

Example code snippet to handle DMs:
```python
@app.event("message")
def handle_message_events(event, say):
    if event.get("channel_type") == "im":
        user_query = event.get('text')
        response = execute_agent(assistant, tools, {"content": user_query})
        ai_response = response.return_values.get("output", "Sorry, I couldn't process your request.")
        say(ai_response)

Then start the bot with:

if __name__ == "__main__":
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()
```


⸻

✅ 8. Common Pitfalls

Problem	Solution
Bot not replying to DMs	Ensure message.im event is added and im:history scope is present.
App not receiving events, Check Socket Mode is enabled and app is running.
Missing token errors, Verify .env is loaded correctly.



⸻

✅ 9. Useful Links
- [Slack API Quickstart](https://api.slack.com/quickstart)
- [Slack Token Types](https://api.slack.com/concepts/token-types)
- [Slack Event Subscriptions](https://api.slack.com/apis/events-api)
- [Socket Mode Docs](https://api.slack.com/apis/socket-mode)

⸻