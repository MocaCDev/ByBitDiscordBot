from pybit.unified_trading import HTTP

class ByBitBackend:

    ACCOUNT_TYPES = {
        # UTA accounts.
        'UC': 'CONTRACT',
        'UU': 'UNIFIED',
        'UF': 'FUND',

        # Classic (standard) accounts.
        'SS': 'SPOT',
        'SC': 'CONTRACT',
        'SO': 'OPTION',
        'SF': 'FUND'
    }

    def __init__(self):

        # Assigned when certain bot commands are invoked.
        self.sessions = []

        # Change this as you need.
        self.testnet = False

        # Dev-related public/private API keys.
        self.dev_pub = "GlcBEvOWoM9zfPGn3K"
        self.dev_secret = "NO4QEEBBcKzxmzAD2n8UsVEDz28wLqXnpxKS"

    def init_session(self, user_id: int, public_key: str, private_key: str):

        # `get_user_public_key` and `get_user_private_key` can return `None`.
        # This is also just a safe measure.
        if public_key is None or private_key is None:
            return False
        
        try:
            self.sessions.append({
                'user_id': user_id,
                'session': HTTP(
                    testnet=self.testnet,
                    api_key=public_key,
                    api_secret=private_key
                )
            })

            return True
        except:
            return False

    def get_session(self, user_id: int):
        for i in range(len(self.sessions)):
            if self.sessions[i]['user_id'] == user_id:
                return self.sessions[i]['session']

        return None

    def get_users_api_key_information(self, user_id: int):
        try:
            session = self.get_session(user_id)
            api_key_information = session.get_api_key_information()

            return api_key_information
        except:
            return None

    # `from_session` appended to end to be clear this function comes from
    # the `ByBitBackend` class.
    def get_user_balance_from_session(self, user_id: int, account_type: str, coin: str):
        session = self.get_session(user_id)

        if session is None:
            return None

        try:
            return session.get_wallet_balance(
                accountType=ByBitBackend.ACCOUNT_TYPES[account_type],
                coin=coin
            ) #['result'][0]['totalWalletBalance']
        except Exception as e:
            print(f'\n`get_user_balance_from_session` error: {str(e)}')
            return None

    def get_total_bs_data_from_session(self, user_id: int):
        buy_total = 0
        sell_total = 0
        session = self.get_session(user_id)

        if session is None:
            return ['', ''] # The values should be decimal values, so if this is returned we know there was an error.

        try:
            executions = session.get_executions(category='linear')

            return executions

            #for x in executions:
            #    for l in x['result']['list']:
            #        if l['side'] == 'Buy':
            #            buy_total += l['orderPrice']
            #        if l['side'] == 'Sell':
            #            sell_total += l['orderPrice']

            #return [buy_total, sell_total]
        except Exception as e:
            print(f'\n`get_total_bs_data_from_session` error: {str(e)}')
            return ['', ''] # The values should be decimal values, so if this is returned we know there was an error.

    # `interval` is, by default, based on daily reports of the stock (`D`; see `calculate_gain_or_loss`).
    def get_total_stock_data_from_session(self, user_id: int, interval: str):
        session = self.get_session(user_id)

        if session is None:
            return ['', '', ''] # The values should be decimal values, so if this is returned we know there was an error.

        all_symbols = []
        order_quantity = {}
        total_sell = 0
        total_buy = 0
        stock_total = 0

        # In regards to the interval, if it is a number (which means the interval is in minutes),
        # the number will start with either a `1`, `3`, `5`, `6`, `2` or `7`.
        # See https://bybit-exchange.github.io/docs/v5/enum#interval
        if interval[0] >= '1' and interval[0] <= '7':
            interval = int(interval)

        try:
            executions = session.get_executions(category='linear')

            return executions

            '''for x in executions:
                for l in x['result']['list']:
                    if l['side'] == 'Buy':
                        all_symbols.append(l['symbol'])
                        order_quantity[l['symbol']] = [l['orderQty'], l['orderPrice']]

                    if l['side'] == 'Sell':
                        if l['symbol'] in order_quantity:
                            # If the order quantity for the sell of the stock minus the
                            # buy quantity is zero, that means the user sold all of the stock.
                            # If the user sold all of the stock, we want to make sure we remove
                            # the stocks symbol from `all_symbols` so we don't track the stocks
                            # price during `interval`.
                            if order_quantity[l['symbol']][0]-l['orderQty'] == 0:
                                del all_symbols[all_symbols.index(l['symbol'])]
                                del order_quantity[l['symbol']] # Delete order information.

                        total_sell += l['orderPrice']

            # Loop through all the symbols and get the stock data.
            # Takes the open price and subtracts it by the close price.
            for s in all_symbols:
                market_price_info = session.get_mark_price_kline(
                    category='linear',
                    symbol=s,
                    interval=interval
                )['result']['list']

                if market_price_info[1] > market_price_info[4]:
                    stock_total += -(market_price_info[1] - market_price_info[4])
                else:
                    stock_total += -1 * (market_price_info[1] - market_price_info[4])

            for _, v in order_quantity.items():
                total_buy += v[1]

            return [stock_total, total_sell, total_buy]'''
        except Exception as e:
            print(f'\n`get_total_stock_data_from_session` error: {str(e)}')
            return ['', '', ''] # The values should be decimal values, so if this is returned we know there was an error.

    def close_session(self, user_id: int):
        for i in range(len(self.sessions)):
            if self.sessions[i]['user_id'] == user_id:
                del self.sessions[i]
                return

    def close_all_sessions(self):
        del self.sessions[:]
