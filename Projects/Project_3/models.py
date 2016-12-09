class TreeNode:
    def __init__(self):
        self.left = None  # Left Node
        self.right = None  # Right Node
        self.label = None  # If a node has a label, it is a root node.
        self.index = None  # Index of the attribute being split on.
        self.choice = None  # The attribute being split on. E.g 'hot' or 'rain'


class DataRow:
    def __init__(self, truth, data):
        self.truth = truth  # The truth value for that sample
        self.data = data  # The sample data itself


class Column:
    def __init__(self, data):
        self.choices = list(set(data))


class ImpurityMeasure:
    GINI = 'GINI'
    CL_ERROR = 'Classification Error'
    ENTROPY = 'Entropy & Information Gain'
