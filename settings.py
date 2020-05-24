import os
from dotenv import load_dotenv
load_dotenv(verbose=True)

MAX_COUNT=6

URL=os.getenv('url')
GMAIL_USER=os.getenv('gmail_user')
GMAIL_PASSWORD=os.getenv('gmail_password')
GMAIL_TO=[os.getenv('gmail_to')]

ACCOUNT_SID=os.getenv('account_sid')
AUTH_TOKEN=os.getenv('auth_token')
WHATSAPP_FROM=os.getenv('whatsapp_from')
WHATSAPP_TO=os.getenv('whatsapp_to')

