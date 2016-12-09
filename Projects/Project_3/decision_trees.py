import copy
import math
import random
from statistics import mode, StatisticsError

from Projects.Project_3.models import DataRow, TreeNode, DataColumn, SplitAlgo

indexed_attributes = []

depth = 0


def load_data(data_set=1):
    path = 'data/project3_dataset{}.txt'.format(data_set)

    array = []

    def is_number(s):
        try:
            float(s)
            return True
        except ValueError:
            return False

    with open(path) as file:
        for row in file:
            data = row.split('\t')

            # As everything is in string, type cast to Float
            data = [float(x) if is_number(x) else x for x in data]

            # Making it an object here as it will be easier ahead.
            data_row = DataRow(data[-1], data[:-1])

            array.append(data_row)

    return array


def split_data(data, split_value=0.85):
    training_set = math.floor(split_value * len(data))

    return data[:training_set], data[training_set:]


# TODO: Check if absolutely necessary
def normalize_data(inputs, attributes):
    for j in range(len(inputs[0].data)):

        if attributes[j].type == 'Continuous':
            min_elem, max_elem = None, None
            for i in range(len(inputs)):
                if min_elem is None:
                    min_elem = min(list(zip(*[x.data for x in inputs]))[j])
                    max_elem = max(list(zip(*[x.data for x in inputs]))[j])
                # http://stats.stackexchange.com/a/70807
                inputs[i].data[j] = (inputs[i].data[j] - min_elem) / (max_elem - min_elem)

    pass


def get_classification_error(inputs):
    positives = inputs.count(1.0)
    negatives = len(inputs) - positives
    classification_error = 1 - max(positives, negatives) / len(inputs)

    return classification_error


def get_classification_error_for_split(inputs_left, inputs_right):
    return min(get_classification_error(inputs_left),
               get_classification_error(inputs_right))


def get_gini_error_for_split(inputs_left, inputs_right, total):
    return 0


def get_split_index(input_data, attributes, split_on=SplitAlgo.CLERROR):
    index = -1

    # 1 because it is higher than maximum value possible.
    # So regardless of our calculated error, it will be assigned to min_error
    min_measure = 1
    nominal_choice = None

    for i in range(len(attributes)):

        if i not in indexed_attributes:
            temp_choice = None

            if attributes[i].type == 'Continuous':
                inputs_left = [x.truth for x in input_data if x.data[i] < attributes[i].median]
                inputs_right = [x.truth for x in input_data if x.data[i] >= attributes[i].median]

                if len(inputs_right) == 0 or len(inputs_left) == 0:
                    index = i
                    nominal_choice = temp_choice
                    break

                elif split_on == SplitAlgo.CLERROR:
                    split_measure = get_classification_error_for_split(inputs_left, inputs_right)
                elif split_on == SplitAlgo.GINI:
                    split_measure = get_gini_error_for_split(inputs_left, inputs_right)
            else:
                choices = attributes[i].choices

                temp_min_measure = 1
                for choice in choices:
                    inputs_left = [x.truth for x in input_data if x.data[i] != choice]
                    inputs_right = [x.truth for x in input_data if x.data[i] == choice]

                    if split_on == SplitAlgo.CLERROR:
                        split_measure = get_classification_error_for_split(inputs_left, inputs_right)
                    elif split_on == SplitAlgo.GINI:
                        split_measure = get_gini_error_for_split(inputs_left, inputs_right)

                    if split_measure < temp_min_measure:
                        temp_min_measure = split_measure
                        temp_choice = choice

                split_measure = temp_min_measure

            if split_measure < min_measure:
                min_measure = split_measure
                nominal_choice = temp_choice
                index = i

                if nominal_choice is not None:
                    attributes[index].choices.remove(nominal_choice)

    indexed_attributes.append(index)

    if attributes[index].choices is not None:
        if len(attributes[index].choices) > 1:
            indexed_attributes.remove(index)

    return index, nominal_choice


def get_mode_label(input_data):
    try:
        return mode([x.truth for x in input_data])
    except StatisticsError:
        return [x.truth for x in input_data].pop()


def build_tree(input_data, attributes, split_on, pruning_size=5):
    classes = set([x.truth for x in input_data])

    node = TreeNode()
    node.count = len(input_data)
    # Pruning

    # Stop if all instances belong to the same class
    if len(classes) == 1:
        node.label = classes.pop()

    # Stop if number of instances is less than some user specified threshold
    elif len(input_data) < pruning_size:
        node.label = get_mode_label(input_data)

    else:

        # Because we don't have column headings. Keeping track of attributes by their column index
        # If index is not None, means that the node is not a leaf node. Compare on the index when classifying.
        index, choice = get_split_index(input_data, attributes, split_on)

        if index < 0:
            node.label = get_mode_label(input_data)
        else:
            node.index = index
            node.choice = choice

            if choice is None:
                data_left = [x for x in input_data if x.data[node.index] < attributes[node.index].median]
                data_right = [x for x in input_data if x.data[node.index] >= attributes[node.index].median]
            else:
                data_left = [x for x in input_data if x.data[node.index] != choice]
                data_right = [x for x in input_data if x.data[node.index] == choice]

            if len(data_left) == 0:
                node.label = get_mode_label(data_right)
            elif len(data_right) == 0:
                node.label = get_mode_label(data_left)
            else:
                node.left = build_tree(input_data=data_left,
                                       attributes=attributes,
                                       pruning_size=pruning_size,
                                       split_on=split_on)  # TODO: Check if attributes need to be regenerated
                node.right = build_tree(input_data=data_right,
                                        attributes=attributes,
                                        pruning_size=pruning_size,
                                        split_on=split_on)

    return node


def get_attributes(inputs):
    array = []
    for i in range(len(inputs[0].data)):
        array.append(DataColumn(list(zip(*[x.data for x in inputs]))[i]))

    return array


def classify_testing_data(root, input_data, attributes):
    a, b, c, d = 0, 0, 0, 0

    for input in input_data:
        node = copy.deepcopy(root)
        while node.label is None:
            index, choice = node.index, node.choice

            if choice is None:
                if input.data[index] < attributes[index].median:
                    node = node.left
                else:
                    node = node.right
            else:
                if input.data[index] != choice:
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


def calculate_statistics(a, b, c, d):
    accuracy = (a + d) / (a + b + c + d)

    if (a + c) != 0:
        precision = a / (a + c)
    else:
        precision = 'No Positives Classified'
    recall = a / (a + b)
    f_measure = 2 * a / (2 * a + b + c)

    print('Accuracy : {}'.format(accuracy))
    print('Precision : {}'.format(precision))
    print('Recall : {}'.format(recall))
    print('F-Measure : {}'.format(f_measure))


def run_algorithm(data_set=1, normalization=True, split_value=0.85, shuffle=True, split_on=SplitAlgo.CLERROR):
    data = load_data(data_set)

    if shuffle:
        random.shuffle(data)
    if normalization:
        attributes = get_attributes(data)
        normalize_data(data, attributes)

    attributes = get_attributes(data)
    training_data, testing_data = split_data(data, split_value=split_value)

    root = build_tree(input_data=training_data,
                      attributes=attributes,
                      split_on=split_on)

    a, b, c, d = classify_testing_data(root=copy.deepcopy(root), input_data=testing_data, attributes=attributes)

    calculate_statistics(a, b, c, d)


run_algorithm(data_set=1,
              normalization=False,
              shuffle=False,
              split_value=0.80,
              split_on=SplitAlgo.CLERROR)
