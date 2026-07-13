from twilio.rest import Client

account_sid = 'YOUR_ACCOUNT_SID'
auth_token = 'YOUR_AUTH_TOKEN'
client = Client(account_sid, auth_token)

message = client.messages.create(
    from_='whatsapp:+14155238886',
    body='Hello! Welcome to GrowBot 🌱 Your farming assistant is ready!',
    to='whatsapp:+2349039705988'
)

print(message.sid)