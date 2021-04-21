import smtplib, ssl, sys
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

emails = sys.argv[1].split(',')

print("Input e-mails: " + str(emails))

port = 465  # For starttls
smtp_server = "smtp.gmail.com" #smtp server
sender_email = "abc@gmail.com" #e-mail address (from)
password = "" #password auth

message = MIMEMultipart("alternative")
message['Subject'] = sys.argv[2]
message['From'] = sender_email

# Create the plain-text and HTML version of your message
text = sys.argv[3]
html = sys.argv[3]

# Turn these into plain/html MIMEText objects
part1 = MIMEText(text, "plain")
part2 = MIMEText(html, "html")

# Add HTML/plain-text parts to MIMEMultipart message
# The email client will try to render the last part first
message.attach(part1)
message.attach(part2)

# Create secure connection with server and send email
context = ssl.create_default_context()

with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
  for email in emails:
    print("Sending e-mail to: " + email)
    message['To'] = email

    server.login(sender_email, password)
    server.sendmail(
      sender_email, email, message.as_string()
    )

print("Done")
