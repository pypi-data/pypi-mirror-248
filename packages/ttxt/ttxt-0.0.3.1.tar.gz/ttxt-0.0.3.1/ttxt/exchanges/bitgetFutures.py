import hmac
import base64
import hashlib
import json
import time
import requests
from ttxt.base import baseFuturesExchange
from ttxt.types import baseTypes
# Example of an exchange requiring a password
'''
Sample 
kwargs = {
    "productType": "",
    "marginMode": "",
    "marginCoin": ""
}
'''
class bitgetFutures(baseFuturesExchange.BaseFuturesExchange):
    def __init__(self, key, secret, password, **kwargs):
        super().__init__(key, secret, **kwargs)
        self.password = password
        self.domain_url = ""
        self.productType =  kwargs["productType"] if "productType" in kwargs else "USDT-FUTURES"
        self.marginMode = kwargs["marginMode"] if "marginMode" in kwargs else "isolated"
        self.marginCoin = kwargs["marginCoin"] if "marginCoin" in kwargs else "USDT"

    def sign(self, message):
        mac = hmac.new(bytes(self.secret, encoding='utf8'), bytes(message, encoding='utf-8'), digestmod='sha256')
        d = mac.digest()
        return base64.b64encode(d)

    def pre_hash(self, timestamp, method, request_path, queryString, body):
        if not body:
            return str(timestamp) + str.upper(method) + request_path + queryString
        return str(timestamp) + str.upper(method) + request_path + body

    def _signedRequest(self, method, request_path, queryString, body):
        timeMs = int(time.time()) *1000
        body = json.dumps(body)
        queryString = json.dumps(queryString)
        signature = self.sign(self.pre_hash(timeMs, method, request_path, queryString ,body))
        headers = {"ACCESS-KEY": self.key, "ACCESS-SIGN": signature, "ACCESS-PASSPHRASE": self.password, "ACCESS-TIMESTAMP": str(timeMs), "locale": "en-US","Content-Type": "application/json"}
        if method == "GET":
            try:
                url = self.domain_url+request_path+queryString
                response = requests.get(url, headers=headers)
                return response.json()
            except Exception as e:
                raise e
        if method == "POST":
            url = self.domain_url+request_path
            try:
                response = requests.post(url, headers=headers, data=body)
                return response.json()
            except Exception as e:
                raise e
    
    def _unsignedRequest(self, method, apiUrl, params):
        url = self.domain_url + apiUrl
        if method == 'GET':
            try:
                response = requests.request('get', url, params=params)
                return response.json()
            except Exception as e:
                raise e
        else:
            raise Exception(f"{method} Method not supported for unsigned calls")

    ## Exchange functions 
    def fetch_ticker(self, symbol):
        print(f"Fetching ticker for {symbol} with password {self.password}")
        
    def create_order(self, symbol, type, side, amount, price=None, params={}):
        try:
            if type == "market":
                body = {
                    "symbol": symbol,
                    "productType": self.productType,
                    "marginMode": self.marginMode,
                    "marginCoin":self.marginCoin,
                    "size": amount,
                    "side": side,
                    "tradeSide": params["tradeSide"] if "tradeSide" in params else "",
                    "orderType": "market",
                    "force": params["force"] if "force" in params else "",
                    "reduceOnly": params["reduceOnly"] if "reduceOnly" in params else "NO",
                    "presetStopSurplusPrice": params["tpPrice"] if "tpPrice" in params else "",
                    "presetStopLossPrice": params["slPrice"] if "slPrice" in params else "",
                }
            elif type == "limit":
                body = {
                    "symbol": symbol,
                    "productType": self.productType,
                    "marginMode": self.marginMode,
                    "marginCoin":self.marginCoin,
                    "size": amount,
                    "price": price,
                    "side": side,
                    "tradeSide": params["tradeSide"] if "tradeSide" in params else "",
                    "orderType": "market",
                    "force": params["force"] if "force" in params else "",
                    "reduceOnly": params["reduceOnly"] if "reduceOnly" in params else "NO",
                    "presetStopSurplusPrice": params["tpPrice"] if "tpPrice" in params else "",
                    "presetStopLossPrice": params["slPrice"] if "slPrice" in params else "",
                }
            # body = '{"symbol":' + '\"' + demoSymbol + '",' + '\"marginCoin":"SUSDT","side":"open_long","orderType":"market","size":' + '\"' + str(quantity) + '\"}'
            apiUrl = "/api/v2/mix/order/place-order"
            response = self._signedRequest('POST', apiUrl, None, body)
            return response
        except Exception as e:
            raise e
        
    def fetch_ticker(self, symbol: str, params={}) -> baseTypes.Ticker:
        apiUrl = "/api/v2/mix/market/ticker"
        params = {
            "symbol": symbol,
            "productType": self.productType
        }
        resp = self._unsignedRequest('GET', apiUrl, params=params)
        return resp # parse this response into Ticker
    
    def fetch_balance(self, params={}) -> baseTypes.Balances:
        pass