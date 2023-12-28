# -*- coding: utf-8 -*-

import hashlib
import hmac
import math
import time
from datetime import datetime

# from ccxt.base.errors import AuthenticationError
from ccxt.base.errors import ExchangeError, OrderNotFound, InvalidOrder
from ccxt.base.exchange import Exchange


class vinex(Exchange):

    def describe(self):
        return self.deep_extend(super(vinex, self).describe(), {
            'id': 'vinex',
            'name': 'Vinex',
            'countries': ['SG'],
            'rateLimit': 200,
            # 'has': {
            #     'fetchCurrencies': True,
            #     'fetchTickers': True,
            #     'fetchOpenOrders': True,
            #     'fetchMyTrades': True,
            #     'fetchDepositAddress': True,
            # },
            'urls': {
                'logo': 'https://storage.googleapis.com/vinex-images/mail-icons/vinex-logo.png',  # noqa
                'api': 'https://api.coinstore.com/api',
                'www': 'https://coinstore.com/',
                'doc': 'https://docs.coinstore.com/',
                # 'fees': 'https://vinex.network/fees',
            },
            'api': {
                'public': {
                    'get': [
                        #'markets',
                       # 'markets/{market_id}',
                        # 'currencies',
                        # 'tickers',
                        'v1/market/tickers',
                        'trade/order/orderInfo',
                        # 'get-orders',
                        # 'market/{market_id}/ohlcv/{interval}',
                    ],
                },
                'private': {
                    'get': [
                        'spot/accountList',
                        'trade/order/active',
                        'trade/match/accountMatches',
                        # 'user/order/{order_id}',
                        # 'user/market/{market_id}',
                        # 'user/withdraws',
                        # 'user/withdraw/{withdraw_id}',
                        # 'user/deposits',
                    ],
                    'post': [
                        'spot/accountList',
                        'trade/order/place',
                        'trade/order/cancel',
                    ],
                },
            },
            'fees': {
                'trading': {
                    'maker': 0.001,
                    'taker': 0.001,
                },
            },
        })

    def fetch_balance(self, params={}):
        self.load_markets()

        balances = self.privatePostSpotAccountList(params)

        result = {'info': balances}

        for balance in balances:
            currency = self.common_currency_code(balance['asset'])

            free_amount = float(balance['free'])
            used_amount = float(balance['locked'])

            account = {
                'free': free_amount,
                'used': used_amount,
                'total': free_amount + used_amount,
            }

            result[currency] = account

        return self.parse_balance(result)

    def create_order(self, symbol, type, side, amount, price=None, params={}):
        self.load_markets()
        market = self.market(symbol)

        request = dict()
        request['market'] = market['id']

        # request['price'] = self.price_to_precision(symbol, price)
        # request['amount'] = self.amount_to_precision(symbol, amount)

        request['price'] = float(self.price_to_precision(symbol, price))
        request['amount'] = float(self.amount_to_precision(symbol, amount))

        if side == 'buy':
            request['type'] = 'BUY'
        elif side == 'sell':
            request['type'] = 'SELL'

        data = self.privatePostTradeOrderPlace(self.extend(request, params))

        # if not data:
        #     raise InvalidOrder(self.id + ' ' + self.json(response))

        order_obj = data.copy()
        order_obj['info'] = data
        order = self.parse_order(order_obj)

        id = order['id']
        self.orders[id] = order

        return order

    def cancel_order(self, id, symbol=None, params={}):
        self.load_markets()
        market = self.market(symbol)

        request = dict()
        request['market'] = market['id']
        request['uid'] = id

        result = self.privatePostTradeOrderCancelAll(self.extend(request, params))
