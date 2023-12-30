import time

import pandas as pd
import requests
from trading_ig.config import config

IG_BASE_URL = "https://demo-api.ig.com/gateway/deal"


class IG:
    def __init__(
        self,
        username,
        password,
        api_key,
        base_url="https://api.ig.com/gateway/deal",
    ):
        self.session_init(username, password, api_key, base_url)
        self.markets = []

    def session_init(self, username, password, api_key, base_url):
        self.base_url = base_url
        self.headers = {
            "Content-Type": "application/json; charset=UTF-8",
            "Accept": "application/json; charset=UTF-8",
            "VERSION": "2",
        }
        self.headers["X-IG-API-KEY"] = api_key
        self.session = requests.post(
            f"{self.base_url}/session",
            json={
                "identifier": username,
                "password": password,
                "encryptedPassword": False,
            },
            headers=self.headers,
        )
        self.headers["CST"] = self.session.headers["CST"]
        self.headers["X-SECURITY-TOKEN"] = self.session.headers[
            "X-SECURITY-TOKEN"
        ]
        self.headers_v1 = dict(self.headers)
        self.headers_v1["VERSION"] = "1"

    def navigation(self, node_id):
        return requests.get(
            f"{self.base_url}/marketnavigation/{node_id}",
            headers=self.headers_v1,
        ).json()

    def traverse(self, node_id, delay=2):
        level = self.navigation(node_id)
        time.sleep(delay)
        if "nodes" in level and isinstance(level["nodes"], list):
            for node in level["nodes"]:
                self.traverse(node["id"])
        if "markets" in level and isinstance(level["markets"], list):
            for market in level["markets"]:
                self.markets.append(market)

        return self.markets

    def get_instruments(self, epics=(), filt="ALL"):
        return requests.get(
            f"{self.base_url}/markets",
            params={"epics": ",".join(epics), "filter": filt},
            headers=self.headers,
        ).json()


config.get


ig = IG(config.username, config.password, config.api_key, base_url=IG_BASE_URL)

markets = ig.traverse(".")

data = pd.DataFrame(markets)

data.to_csv("./ig-markets.csv", index=False)
