from statistics import mean, median


class TreeNode:
    def __init__(self):
        self.left = None
        self.count = None
        self.right = None
        self.label = None
        self.index = None  # Index of the attribute being split on.


class DataRow:
    def __init__(self, truth, data):
        self.truth = truth
        self.data = data
        self.prediction = None


class DataColumn:
    def __init__(self, data):
        self.mean = mean(data)
        self.median = median(data)
