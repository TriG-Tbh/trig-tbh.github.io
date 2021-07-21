def send(name, recipient, message):
    import smtplib
    import datetime
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login("[REDACTED]", '[REDACTED]')
    message = "Subject: Custom Feed (pulled from {}.feed at {})\n\n{}".format(name, datetime.datetime.now(), message)
    try:
        s.sendmail("sender_email_id", recipient, message.encode('utf-8'))
    except:
        raise ValueError
    s.quit()
