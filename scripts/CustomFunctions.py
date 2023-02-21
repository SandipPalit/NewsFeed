from datetime import date
from gnewsclient import gnewsclient
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def generateNewsFeed(topics, language, location, receivers):
    with open("data/newsTemplate.html", "r") as header:
        feed = header.read()
        news = getNewsFeed(topics, language, location)
        feed = feed.replace('{{CURRENT_DATE}}', f"{date.today().strftime('%d %B, %Y')}")
        feed = feed.replace('{{NEWS_FEED}}', f"{news}")
        sendEmail(feed, receivers)

def getNewsFeed(topics, language, location):
    newsItem = ""
    for topic in topics:
        client = gnewsclient.NewsClient(language=language,
                                        topic=topic, location=location, max_results=5)
        for news in client.get_news():
            title, source = news['title'].rsplit(" - ", 1)
            link = news['link']
            newsItem += f"""<tr>
                                <td style='width: 14%;'>{topic}</td>
                                <td style='width: 58%;'>{title}</td>
                                <td style='width: 9%;'><a href='{link}'>Click here</a></td>
                                <td style='width: 14%;'>{source}</td>
                            </tr>"""
    return newsItem

def sendEmail(emailBody, receivers):
    password = os.getenv("emailpassword")
    message = MIMEMultipart()
    message['Subject'] = "Your NewsFeed  is here."
    message['From'] = "newsfeed.sandippalit@gmail.com"
    message['To'] = ", ".join(receivers)
    message.attach(MIMEText(emailBody, "html"))
    msg_body = message.as_string()
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.ehlo()
    server.login("newsfeed.sandippalit@gmail.com", password)
    server.sendmail("newsfeed.sandippalit@gmail.com", receivers, msg_body)
    server.close()