from .. import Node

class ConvertibleNode(Node):
    def __init__(self, assetprice, rate, prob, vbond):
        self.set_assetprice(assetprice)
        self.set_rate(rate)
        self.set_prob(prob)
        self.set_vbond(vbond)
        self.price = None
        
    def set_price(self, price):
        self.price = price
    
    def get_price(self):
        return self.price
    
    def set_assetprice(self, assetprice):
        """
        Sets the price of the underlying asset at a node.

        """
        self.assetprice = assetprice
        
    def get_assetprice(self):
        return self.assetprice
            
    def set_rate(self, rate):
        self.rate = rate
        
    def get_rate(self):
        return self.rate
    
    def set_prob(self, prob):
        self.convprob = prob
        
    def get_prob(self):
        return self.convprob
        
    def set_vbond(self, value):
        self.vbond = value
        
    def get_vbond(self):
        return self.vbond

    def __str__(self):
        if self.price is None:
            return f'Asset Price: {self.assetprice}; Discount Rate {self.rate}; Conversion Probability {self.convprob}; Vanilla Price {self.vbond}'
        else:
            return f'Price {self.price}; Asset Price: {self.assetprice}; Discount Rate {self.rate}; Conversion Probability {self.convprob}; Vanilla Price {self.vbond}'