from typing import List
from dcentrapi.Base import Base
from dcentrapi.requests_dappi import requests_get


class TokenPrices(Base):

    def get_token_price(self, match_string: str):
        url = self.arbitrage_url + "tokenPrices"
        data = {"match_strings": [match_string]}
        response = requests_get(url, params=data, headers=self.headers)
        return response.json()

    def get_token_prices(self, match_strings: List[str]):
        url = self.arbitrage_url + "tokenPrices"
        data = {"match_strings": match_strings}
        response = requests_get(url, params=data, headers=self.headers)
        return response.json()

    def get_token_prices_by_network_and_address(self, networks: List[str], token_addresses: List[str]):
        url = self.arbitrage_url + "tokenPricesByNetworkAndAddress"
        data = {
            "networks": networks,
            "token_addresses": token_addresses,
        }
        response = requests_get(url, params=data, headers=self.headers)
        return response.json()
