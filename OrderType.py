import time

class Order:
    def __init__(self, quantity: int, symbol: str):
        self.quantity = quantity
        self.symbol = symbol
        self.timestamp = time.time()  

class MarketOrder(Order):
    def __init__(self, quantity: int, symbol: str):
        super().__init__(quantity, symbol)

class MarketLong(MarketOrder):
    def __init__(self, quantity: int, symbol: str):
        super().__init__(quantity, symbol)
        self.order_type = 'MarketLong'

class MarketShort(MarketOrder):
    def __init__(self, quantity: int, symbol: str):
        super().__init__(quantity, symbol)
        self.order_type = 'MarketShort'

class LimitOrder(Order):
    def __init__(self, quantity: int, symbol: str, limit_price: float):
        super().__init__(quantity, symbol)
        self.limit_price = limit_price

class LimitLong(LimitOrder):
    def __init__(self, quantity: int, symbol: str, limit_price: float):
        super().__init__(quantity, symbol, limit_price)
        self.order_type = 'LimitLong'

class LimitShort(LimitOrder):
    def __init__(self, quantity: int, symbol: str, limit_price: float):
        super().__init__(quantity, symbol, limit_price)
        self.order_type = 'LimitShort'
