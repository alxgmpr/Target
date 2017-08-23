import threading
from time import time, sleep
from json import load

from logger import Logger

import requests
from selenium import webdriver


class Target(threading.Thread):
    def __init__(self, tid):
        threading.Thread.__init__(self)
        self.start_time = time()
        self.tid = tid
        self.log = Logger(tid).log
        self.S = requests.Session()
        # self.driver = webdriver.Chrome('bin/chromedriver')
        with open('config.json') as config_file:
            self.C = load(config_file)
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36'
        }
        self.form_headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36',
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        self.json_headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36',
            'Content-Type': 'application/json'
        }

    def wait(self):
        sleep(self.C['sleep_time'])

    def login(self):
        self.log('logging into account')
        endpoint = 'https://www.target.com/gsp/authentications/v1/credential_validations?client_id=ecom-web-1.0.0'
        payload = {
            'email': self.C['checkout']['email'],
            'password': self.C['checkout']['password']
        }

    def add_to_cart(self):

        # NES: 52826093
        payload = {
            "products": [{
                "partnumber": "52826093",
                "quantity": "1"
            }]
        }
        endpoint = 'https://www-secure.target.com/api/cart/order-api/cart/v5/cartitems?responseGroup=cart'
        r = self.S.post(
            endpoint,
            headers=self.json_headers,
            json=payload
        )
        while True:
            try:
                r.raise_for_status()
                self.log('!!!!!!!!!!!!!!SUCCESFULLY ADDED. STOCK LIVE.!!!!!!!!!!!!!')

                break
            except requests.exceptions.HTTPError:
                self.log('still out of stock :(')
                print r.text
                sleep(5)
                self.add_to_cart()

    def open_checkout(self):
        self.log('opening checkout')
        # session_cookies = self.S.cookies.items()
        # print session_cookies
        # for c in session_cookies:
        #     self.driver.add_cookie({'name': c[0], 'value': c[1]})
        # sleep(1)
        # self.driver.get('https://www-secure.target.com/co-cart')
        # sleep(10)

    def submit_shipping(self):
        self.log('submitting shipping')

    def run(self):
        self.add_to_cart()
        self.open_checkout()
