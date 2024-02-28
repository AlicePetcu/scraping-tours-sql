import time
import requests
import selectorlib
import smtplib
import ssl
import os
import sqlite3

URL = "https://programmer100.pythonanywhere.com/tours/"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 '
                  'Safari/537.36'}

# Establish a connection and a cursor
connection = sqlite3.connect("data.db")
cursor = connection.cursor()


def scrape(url):
    """Scrape the page source from de URL"""
    response = requests.get(url, headers=HEADERS, verify=False)
    text = response.text
    return text


def extract(source):
    extractor = selectorlib.Extractor.from_yaml_file("extract.yaml")
    value = extractor.extract(source)["tours"]
    return value


def send_email(message):
    host = "smtp.gmail.com"
    port = 465
    username = "alice.petcu93@gmail.com"
    password = os.getenv("PASSWORD")
    receiver = "alice.petcu93@gmail.com"
    context = ssl.create_default_context()

    message = f"""\
Subject: New EVENT!!!
    
{message}"""

    with smtplib.SMTP_SSL(host, port, context=context) as server:
        server.login(username, password)
        server.sendmail(username, receiver, message)

    print("Email was sent!")


def store(extracted):
    row = extracted.split(',')
    row = [item.strip() for item in row]

    cursor = connection.cursor()
    cursor.execute("INSERT INTO events VALUES(?,?,?)", row)
    connection.commit()


def read(extracted):
    row = extracted.split(',')
    row = [item.strip() for item in row]
    band, city, date = row
    cursor.execute("SELECT * FROM events WHERE band=? AND city=? AND date=?",
                   (band, city, date))
    result = cursor.fetchall()
    print(result)
    return result


if __name__ == "__main__":
    while True:
        scraped = scrape(URL)
        extracted = extract(scraped)
        print(extracted)
        if extracted != "No upcoming tours":
            row = read(extracted)
            if not row:
                send_email("Hey! New event was found!")
                store(extracted)
        time.sleep(2)
