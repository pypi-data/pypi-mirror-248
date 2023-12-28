from ttxt.base import baseFuturesExchange, baseSpotExchange
from ttxt.exchanges.gateFutures import gateFutures
from ttxt.exchanges.bybitFutures import bybitFutures
from ttxt.exchanges.bingx import bingx
from ttxt.exchanges.biconomy import biconomy

exchanges = [
    "gateFutures",
    "bybitFutures",
    "bingx",
    "biconomy"
]

base = [
    "baseFuturesExchange",
    "baseSpotExchange"
]

_all__ =  exchanges + base