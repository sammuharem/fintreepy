import numpy as np
import math
from ..trinomialpricetree import TrinomialPriceTree
from convertiblenode import ConvertibleNode
from convertiblevaluetree import ConvertibleValueTree

class ConvertibleTrinomialTree(TrinomialPriceTree):
    # CURRENTLY ASSUMES ON YEAR PER BRANCH, HAVE KEPT SAME INPUTS FOR CONSISTENCY
    def __init__(self, s, t, r, v):
        super().__init__(s, t, r, t, v)

    def vanillabond(self, fv, c, r, t):
        """
        Get the annual price of a vanilla bond at each time step

        Parameters
        ----------
        fv : float
            The face value of the covnertible bond
        c : float
            The coupon rate on the bond
        r : float
            The risky rate to discoutn bonds, includes credit spread
        t : int
            Periods to value bond for

        Returns
        -------
        list
            Price of a vanilla bond at each step

        """
        payments = np.full((t), c * fv)
        payments[-1] += fv
        payments = np.insert(payments, 0, 0)
        values = [0]
        for item in payments[::-1] + [0]:
            values.append(values[-1]/(1 + r) + item)
        return values[1:][::-1]
    
    def rate_tree(self, convprob_tree):
        """
        Calculates the discount rate for the convertible bond at each node.
        
        Using the probability of conversion, the discount rate is the chance
        the bond will be converted multiplied by the risk-free rate plus the
        probability the bond won't be converted multiplied by the risky-rate.

        Parameters
        ----------
        convprob_tree : TYPE
            DESCRIPTION.

        Returns
        -------
        rate_tree : TYPE
            DESCRIPTION.

        """
        rate_tree = []
        for branch in convprob_tree:
            row = []
            for prob in branch:
                row.append(prob * self.r + (1 - prob) * self.i)
            rate_tree.append(row)    
        return rate_tree
    
    def convprob_tree(self, vbond_price, mat_conv=True):
        """
        Calculates the probability that the convertible bond will be converted
        to equity at each node.        

        Parameters
        ----------
        vbond_price : List
            List of price of a vanilla bond at each branch
        mat_conv : TYPE, optional
            DESCRIPTION. The default is True.

        Returns
        -------
        List of List of Floats
            The discount rate to use for valuation tree at each node.

        """
        convtree = []
        row = []
        
        # At last branch, convertible will have either 1 or 0 
        for item in self.Tree[-1]:
            row.append([0, 1][self.conv_ratio * item > vbond_price[-1]])
        convtree.append(row)
        
        # TODO: Confirm early exercise practices
        for branch in self.Tree[:-1][::-1]:
            new_row = []
            for i in range(len(branch)):
                lower = convtree[-1][i]
                flat = convtree[-1][i + 1]
                upper = convtree[-1][i + 2]
                weighted_conv = lower * self.q + flat * self.m + upper * self.p
                new_row.append(weighted_conv)
            convtree.append(new_row)                 
        return convtree[::-1]
        
    def combine_trees(self, vbond_price, rate_tree, convprob_tree):
        """
        Combines earlier trees to create a tree of nodes to value convertible

        Parameters
        ----------
        vbond_price : List
            List of price of a vanilla bond at each branch
        rate_tree : List of List of Floats
            The discount rate to use for valuation tree at each node.
        convprob_tree : List of List of Floats
            The probability that the covnertible will be covnerted at each node

        Returns
        -------
        node_tree : List of List of ConvertibleNodes

        """
        node_tree = []
        for i in range(len(self.Tree)):
            row = []
            for j in range(len(self.Tree[i])):
                row.append(ConvertibleNode(self.Tree[i][j], rate_tree[i][j], 
                                           convprob_tree[i][j], vbond_price[i]))
            node_tree.append(row)
        return node_tree
    
    def value_tree(self, node_tree, c, fv):
        for i in range(len(node_tree))[::-1]:
            for j in range(len(node_tree[i])):
                node = node_tree[i][j]
                if node.get_prob() == 1:
                    node.set_price(node.assetprice * self.conv_ratio)
                    
                if node.get_prob() == 0:
                    node.set_price(node.vbond)
                    
                
                if 0 < node.get_prob() < 1:
                    lower = node_tree[i + 1][j].get_price()
                    flat = node_tree[i + 1][j + 1].get_price()
                    upper = node_tree[i + 1][j + 2].get_price()
                    node.set_price(math.e ** (-node.get_rate()) * (lower * self.q + flat * self.m + upper * self.p) + c * fv)
                
                
    def value_convertible(self, i, conv_ratio, c, fv=100):
        self.i = i
        self.conv_ratio = conv_ratio
    
        vbonds = self.vanillabond(fv, c, i, self.t)
        convtree = self.tree.convprob_tree(vbonds)
        rates = self.tree.rate_tree(convtree)
        nodes = self.tree.combine_trees(vbonds, rates, convtree)
        self.value_tree(nodes, c, fv)
        nodes = ConvertibleValueTree(nodes)
        nodes.save_vars(i, conv_ratio, c, fv, self.u, self.d, self.p, self.m, self.q)
        return nodes
            
        
