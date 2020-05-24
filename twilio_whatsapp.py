from twilio.rest import Client
import smtplib
import settings
 
def send_whatsapp(message):
    client = Client(settings.ACCOUNT_SID, settings.AUTH_TOKEN)
    message = client.messages.create(
                                  from_=settings.WHATSAPP_FROM,
                                  body=message,
                                  to=settings.WHATSAPP_TO
                              )
    print(f'Sent message: {message.sid}')
