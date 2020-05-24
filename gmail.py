import smtplib
from settings import GMAIL_USER, GMAIL_TO, GMAIL_PASSWORD


def send_email(new_arrivals):
    subject = '[Canyon Outlet] New bikes'
    body = '\n\n'.join(map(str,new_arrivals))

    email_text = """\
    From: %s
    To: %s
    Subject: %s

    %s
    """ % (GMAIL_USER, ", ".join(GMAIL_TO), subject, body)

    print('Sending email...')

    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(GMAIL_USER, GMAIL_PASSWORD)
        server.sendmail(GMAIL_USER, GMAIL_TO, email_text)
        server.close()

        print('Email sent!')
    except Exception as e:
        print('Something went wrong...' + str(e))

