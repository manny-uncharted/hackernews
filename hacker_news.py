from email.mime import text
import requests # For performing http requests

from bs4 import BeautifulSoup # Web Scraping

#To Send the mail
import smtplib

# Email body
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Importing secrets file
from my_secrets import sent_from, to, key_pass

#system date and time manipulation
import datetime
now = datetime.datetime.now()

# Email content placeholder

content = ''

# Extracting Hacker News Stories

def extract_news(url):
    print('Extracting Hacker News Stories...')
    cnt = ''
    cnt +=('<b>HN Top Stories:</b>\n'+'<br>'+'-'*50+'<br>')
    response = requests.get(url)
    content = response.content
    soup = BeautifulSoup(content, 'html.parser')
    for i, tag in enumerate(soup.find_all('td',attrs={'class': 'title', 'valign': ''})):
        cnt += ((str(i+1)+' :: '+tag.text + "\n" + '<br>') if tag.text!='More' else '')
    return(cnt)

cnt = extract_news('https://news.ycombinator.com/')
content += cnt
content += ('<br>------<br>')
content +=('<br><br>End of Message')

#Sending the mail

print('Composing Email')

#Update your email details

SERVER = 'smtp.gmail.com' # your smtp server
PORT = 587 # Your port number
FROM = sent_from # Your email id
TO = to # Your to email ids # Can be a list
PASS = key_pass # Your email id's password

# Create a text/plain message
msg = MIMEMultipart()

# msg.add_header('Content-Disposition', 'attachment', filename='empty.txt')
msg['Subject'] = 'Top News Stories HN [Automated Email]' + ' ' + str(now.day) + '-' + str(now.month) + '-' + str(now.year)
msg['From'] = FROM
msg['To'] = TO

msg.attach(MIMEText(content, 'html'))

print('Initiating Server....')

server = smtplib.SMTP(SERVER, PORT)
server.set_debuglevel(1)
server.ehlo()
server.starttls()
server.login(FROM, PASS)
server.sendmail(FROM, TO, msg.as_string())

print('Email Sent.....')

server.quit()
