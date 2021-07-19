import os, sys

from dotenv import load_dotenv
load_dotenv()

email = os.getenv("EMAIL")
password = os.getenv("PASSWORD")
passwordi = input("Password: ")
if passwordi != password:
	sys.exit("Invalid passcode")
os.system("cls")

import smtplib	

smtpObj = smtplib.SMTP("smtp.gmail.com", 587)
smtpObj.starttls()
smtpObj.login(email, password)
print("Successfully logged in")

import newspaper as np

'''recipient = input("Recipient: ")
subject = input("Subject: ")
msg = input("Message: ")
try:
	smtpObj.sendmail(email, recipient, "Subject: " + subject + "\n" + msg)
except:
	print("Error sending email, check the recipient's address")
else:
	print("Successfully sent message to " + recipient + ": \n" + "Subject: " + subject + "\n" + msg + "\n")
'''
cnn_paper = np.build('http://cnn.com')
for article in cnn_paper.articles:
        print(article.text)
