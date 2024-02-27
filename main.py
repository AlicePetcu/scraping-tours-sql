import requests
import selectorlib

URL = "https://programmer100.pythonanywhere.com/tours/"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 '
                  'Safari/537.36'}


def scrape(url):
    """Scrape the page source from de URL"""
    response = requests.get(url, headers=HEADERS, verify=False)
    text = response.text
    print(text)


scrape(URL)
