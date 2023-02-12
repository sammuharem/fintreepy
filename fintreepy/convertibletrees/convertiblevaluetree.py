from ..valuetree import ValueTree

class ConvertibleValueTree(ValueTree):
    def get_rates(self):
        """
        Returns the value of the asset at each branch in the tree.
        
        Each list represents another branch

        Returns
        -------
        List
            Price of the asset at each node

        """
        vals = []
        for branch in self._tree:
            b = []
            for node in branch:
                b.append(node.get_rate())
            vals.append(b)
        return(vals)
    
    def get_probs(self):
        """
        Returns the value of the asset at each branch in the tree.
        
        Each list represents another branch

        Returns
        -------
        List
            Price of the asset at each node

        """
        vals = []
        for branch in self._tree:
            b = []
            for node in branch:
                b.append(node.get_prob())
            vals.append(b)
        return(vals)   