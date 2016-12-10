class TreeNode:
    def __init__(self):
        self.label = None  # If a node has a label, it is a leaf node.
        self.branches = []
        self.attribute_index = None
        self.attribute_value = None

    def add_child(self, obj):
        self.branches.append(obj)


class DataRow:
    def __init__(self, truth, data):
        self.truth = truth  # The truth value for that sample
        self.data = data  # The sample data itself
        self.weight = None


class Column:
    def __init__(self, data):
        self.choices = list(set(data))


class Classifier:
    def __init__(self, root=None, weight=None):
        self.root = root
        self.weight = weight
