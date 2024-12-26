from OrderType import *

class OrderNode:
    def __init__(self, volume=0):
        self.volume = volume
        self.next = None

    def __str__(self):
        return f"Volume: {self.volume}"
    
class OrderList:
    def __init__(self):
        self.root = None

    def addOrderNode(self, node: OrderNode):
        if self.root == None:
            self.root = node
            return node
        pointer = self.root
        while pointer.next!=None:
            pointer = pointer.next
        pointer.next = node
        return node
  
    def orderFill(self, opp_order: Order):
        if self.root == None:
            return opp_order
        
        while True:
            if self.root.volume > opp_order.quantity:
                self.root.volume -= opp_order.quantity
                opp_order.quantity = 0
                return opp_order
            elif self.root.volume == opp_order.quantity:
                self.root.volume = 0
                opp_order.quantity = 0
                self.root = self.root.next
                return opp_order
            else:
                opp_order.quantity -= self.root.volume
                self.root.volume = 0
                self.root = self.root.next


    def getOrderVolume(self):
        volume = 0
        
        if self.root == None:
            return volume

        pointer = self.root
        while pointer != None:
            volume += pointer.volume 
            pointer = pointer.next

        return volume
    

    def __str__(self):
        output = []
        pointer = self.root
        while True:
            output.append(pointer.volume)
            if pointer.next == None:
                break
            pointer = pointer.next
        return str(output)

class PriceNode:
    def __init__(self, price:float):
        self.right = None
        self.left = None
        self.orderlist = OrderList()
        self.price = price

class PriceTree:
    def __init__(self):
        self.root = None
    
    def limitOrderAdd(self, order:LimitOrder):
        validnode = self.addPriceNode(PriceNode(order.limit_price))
        validnode.orderlist.addOrderNode(OrderNode(order.quantity))
        return True
    def orderFill(self, order: Order):
        if isinstance(order, LimitOrder):    
            self.limitOrderAdd(order)
            return True
    def getBestBid(self):
        if self.root == None:
            return False

        pointer = self.root

        while True:
            if pointer.right == None:
                break
            pointer = pointer.right
            
        return pointer
    def getBestAsk(self):
        if self.root == None:
            return False

        pointer = self.root

        while True:
            if pointer.left == None:
                break
            pointer = pointer.left
            
        return pointer
    def getValidPriceNode(self, price:float):
        if self.root == None:
            return None
        if self.root.price == price:
            return self.root
        
        pointer = self.root

        while True:
            if price > pointer.price:
                if pointer.right == None:
                    return pointer
                pointer = pointer.right
            elif price < pointer.price:
                if pointer.left == None:
                    return pointer
                pointer = pointer.left
            else:
                return pointer
    def addPriceNode(self, node:PriceNode):
        pricenode = self.getValidPriceNode(node.price)

        if pricenode != None:
            if node.price < pricenode.price:
                pricenode.left = node
                return pricenode.left
            elif node.price > pricenode.price:
                pricenode.right = node
                return pricenode.right
            else:
                return pricenode

        self.root = node
        return self.root

class OrderBook:
    def __init__(self, symbol: str):
        self.symbol = symbol
        self.long_limit = PriceTree()
        self.short_limit = PriceTree()

    def bk_trade(self, order: Order):
        if isinstance(order, LimitOrder):
            if isinstance(order, LimitLong):
                self.long_limit.orderFill(order)
                return True
            elif isinstance(order, LimitShort):
                self.short_limit.orderFill(order)
                return True
            else:
                return False
        return False
    
class Exchange:
    def __init__(self):
        self.__assets = {}

    def addAsset(self, symbol: str):
        self.__assets[symbol] = OrderBook(symbol)
        return True
    
    def deleteAsset(self, symbol: str):
        self.__assets.pop(symbol)
        return True
    
    def getAssets(self):
        return self.__assets
    
    def checkAsset(self, symbol: str):
        if symbol in self.__assets:
            return True
        return False
    
    def getOrderBook(self, symbol: str):
        return self.__assets[symbol]
    
    def ex_trade(self, order: Order):
        if self.checkAsset(order.symbol):
            if self.getOrderBook(order.symbol).bk_trade(order):
                return True
        return False
        