import copy
import math
from statistics import mode, StatisticsError

from Projects.Project_3.models import DataRow, TreeNode, DataColumn

indexed_attributes = []


def load_data(data_set=1):
    path = 'data/project3_dataset{}.txt'.format(data_set)

    array = []
    with open(path) as file:
        for row in file:
            data = row.split('\t')

            # Check for the nominal attributes in Dataset2
            # TODO: Handle Nominal Attributes
            if data_set == 2:
                data[4] = 1 if data[4] == 'Present' else 0

            # As everything is in string, type cast to Float
            data = [float(x) for x in data]

            # Making it an object here as it will be easier ahead.
            data_row = DataRow(data[-1], data[:-1])

            array.append(data_row)

    return array


def split_data(data, split_value=0.85):
    training_set = math.floor(split_value * len(data))

    return data[:training_set], data[training_set:]


# TODO: Check if absolutely necessary
def normalize_data(inputs):
    for j in range(len(inputs[0].data)):

        min_elem, max_elem = None, None
        for i in range(len(inputs)):
            if min_elem is None:
                min_elem = min(list(zip(*[x.data for x in inputs]))[j])
                max_elem = max(list(zip(*[x.data for x in inputs]))[j])
            # http://stats.stackexchange.com/a/70807
            inputs[i].data[j] = (inputs[i].data[j] - min_elem) / (max_elem - min_elem)

    pass


# Using Classification Error to split. ( Because it is easiest, atm )
def get_split_index(input_data, attributes):
    index = -1

    # 1 because it is higher than maximum value possible.
    # So regardless of our calculated error, it will be assigned to min_error
    min_error = 1

    total_class_values = len(input_data)

    for i in range(len(attributes)):

        if i not in indexed_attributes:
            inputs_lt = [x.truth for x in input_data if x.data[i] < attributes[i].mean]
            inputs_gte = [x.truth for x in input_data if x.data[i] >= attributes[i].mean]

            positives_in_inputs_lt = inputs_lt.count(1.0)
            positives_in_inputs_gte = inputs_gte.count(1.0)

            classification_error_for_lt = 1 - max(positives_in_inputs_lt,
                                                  total_class_values - positives_in_inputs_lt) / total_class_values

            classification_error_for_gte = 1 - max(positives_in_inputs_gte,
                                                   total_class_values - positives_in_inputs_gte) / total_class_values

            classification_error = min(classification_error_for_lt, classification_error_for_gte)

            if classification_error < min_error:
                min_error = classification_error
                index = i

    if index >= 0:
        indexed_attributes.append(index)
    return index


def buildTree(input_data, attributes, pruning_size=5, variance_check=False):
    classes = set([x.truth for x in input_data])

    node = TreeNode()

    # Pruning
    if len(classes) == 1:
        node.label = classes.pop()
        return node
    elif len(input_data) < pruning_size:
        if len(input_data) != 0:
            try:
                node.label = mode([x.truth for x in input_data])
            except StatisticsError:
                node.label = [x.truth for x in input_data].pop()
            return node
        else:
            return None

    else:

        # Because we don't have column headings. Keeping track of attributes by their column index
        # If index is not None, means that the node is not a leaf node. Compare on the index when classifying.
        index = get_split_index(input_data, attributes)

        if index < 0:
            if len(input_data) != 0:
                try:
                    node.label = mode([x.truth for x in input_data])
                except StatisticsError:
                    node.label = [x.truth for x in input_data].pop()
                return node
            else:
                return None
        else:
            node.index = index

            # Get data less than attribute at index
            data_lt = [x for x in input_data if x.data[node.index] < attributes[node.index].mean]
            # Get data greater than or equal to attribute at index
            data_gte = [x for x in input_data if x.data[node.index] >= attributes[node.index].mean]

            if len(data_lt) == 0:
                try:
                    node.label = mode([x.truth for x in data_gte])
                except StatisticsError:
                    node.label = [x.truth for x in data_gte].pop()
                return node
            elif len(data_gte) == 0:
                try:
                    node.label = mode([x.truth for x in data_lt])
                except StatisticsError:
                    node.label = [x.truth for x in data_lt].pop()
                return node

            node.left = buildTree(data_lt, get_attributes(data_lt),
                                  pruning_size)  # TODO: Check if attributes need to be regenerated
            node.right = buildTree(data_gte, get_attributes(data_gte),
                                   pruning_size)  # Important now, because bugging out if not being regenerated

    return node


def get_attributes(inputs):
    array = []
    for i in range(len(inputs[0].data)):
        array.append(DataColumn(list(zip(*[x.data for x in inputs]))[i]))

    return array


def classifyData(root, input_data, attributes):
    a, b, c, d = 0, 0, 0, 0

    for input in input_data:
        node = copy.deepcopy(root)
        while node.label is None:
            index = node.index

            if input.data[index] < attributes[index].mean:
                node = node.left
            else:
                node = node.right

        if input.truth == node.label:

            if node.label == 1.0:
                a += 1
            else:
                d += 1
        else:

            if node.label == 1.0:
                c += 1
            else:
                b += 1

    return a, b, c, d


def calculateStatistics(a, b, c, d):
    accuracy = (a + d) / (a + b + c + d)
    precision = a / (a + c)
    recall = a / (a + b)
    f_measure = 2 * a / (2 * a + b + c)

    print('Accuracy : {}'.format(accuracy))
    print('Precision : {}'.format(precision))
    print('Recall : {}'.format(recall))
    print('F-Measure : {}'.format(f_measure))


def run_algorithm(data_set=1, normalization=True, split_value=0.80, variance_check=False):
    data = load_data(data_set)
    # random.shuffle(data)
    if normalization:
        normalize_data(data)

    attributes = get_attributes(data)
    training_data, testing_data = split_data(data, split_value=split_value)

    root = buildTree(training_data, attributes=attributes, variance_check=variance_check)

    a, b, c, d = classifyData(root=copy.deepcopy(root), input_data=testing_data, attributes=attributes)

    calculateStatistics(a, b, c, d)


run_algorithm(data_set=1,
              normalization=False)
