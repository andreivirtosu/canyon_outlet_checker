from contextlib import closing

from bs4 import BeautifulSoup
from requests import get
from requests.exceptions import RequestException

from dataclasses import dataclass
import pickle
import smtplib
from twilio_whatsapp import send_whatsapp
from gmail import send_email
import settings

@dataclass
class Bike:
    price: float
    name: str
    url: str

    def __str__(self):
        return f'{self.price} "{self.name}" canyon.com{self.url}'

    def __eq__(self, other):
        return self.url == other.url

    def __hash__(self):
        return hash(self.url)


def simple_get(url: str) -> str:
    """Attempts to get the content at `url` by making an HTTP GET request.
    If the content-type of response is some kind of HTML/XML, return the text content, otherwise return None."""
    try:
        with closing(get(url, stream=True)) as resp:
            if is_good_response(resp):
                return resp.text
            else:
                return "none"
    except RequestException as e:
        log_error('Error during requests to {0} : {1}'.format(url, str(e)))
        return "none"


def is_good_response(resp) -> bool:
    """Returns True if the response seems to be HTML, False otherwise."""
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200
            and content_type is not None
            and content_type.find('html') > -1)


def log_error(e) -> None:
    """TODO: do something else with a HTML requests error"""
    print(e)


def parseSearch(raw_html: str, max_count=5) -> list:
    html: BeautifulSoup
    try:
        html = BeautifulSoup(raw_html, 'html.parser')
    except TypeError as e:
        print("Type Error parsing raw html = " + e)
        exit(-1)

    bikes: list = []

    products = (html.find_all('div', class_='productTile__productSummary'))
    for p in products[:max_count]:
        #print(p)
        name = p.find('div', class_='productTile__productName').text.strip()
        url = p.find('meta', itemprop='url')['content']
        price =p.find('meta', itemprop='price')['content'] 

        bike = Bike(price, name, url)
        bikes.append(bike)

    return bikes

def save_bikes(bikes):
    open('bikes.dat', 'wb').write(pickle.dumps(bikes))

def load_bikes():
    try:
        return pickle.loads(open('bikes.dat', 'rb').read())
    except:
        return []

if __name__ == "__main__":
    test_data = False
    test_data = True
    if test_data:
        raw_html = open('test.html', 'r').read()
    else:
        url = settings.URL
        raw_html = simple_get(url)
        open('test.html', 'w').write(raw_html)

    bikes_old = load_bikes()
    bikes_now = parseSearch(raw_html, settings.MAX_COUNT)

    new_arrivals = []
    for bike in bikes_now:
        if bike not in bikes_old:
            new_arrivals.append(bike)
    
    if new_arrivals:
        print(f'Got {len(new_arrivals)} bikes')
        send_email(new_arrivals)

        for bike in new_arrivals:
            send_whatsapp(str(bike))

    else:
        print('No new bikes')

    save_bikes(bikes_now)


    

