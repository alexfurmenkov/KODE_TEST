import smtplib


def send_email(subject, msg):
    try:
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.ehlo()
        server.starttls()
        server.login("alexeushka8@gmail.com", "a210c1755")
        message = 'Subject: {}\n\n{}'.format(subject, msg)
        from project import App
        server.sendmail("alexeushka8@gmail.com", App.email, message)
        server.quit()
        print("Success: Email sent!")
    except:
        print("Email failed to send.")
