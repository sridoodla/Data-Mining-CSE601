import copy
import math
from statistics import mode, StatisticsError

from Projects.Project_3.models import DataRow, TreeNode, Column

columns = []


def read_file(data_set=1):
    """
    Read and parse the data set
    :param data_set: File Number
    :type data_set: int
    :return: Array of DataRow (s)
    """
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

            # As everything is in string, type cast to Float if it is a number.
            # If it's a string, it's a nominal type
            data = [float(x) if is_number(x) else x for x in data]

            # Making it an object here as it will be easier ahead.
            data_row = DataRow(data[-1], data[:-1])

            array.append(data_row)

    return array


def split_data(data, split_value=0.85):
    """
    Splits the data into training and testing data-sets
    :param data: The input data
    :param split_value: The % of data to use as testing data
    :return: Training data and Testing Data
    """
    training_set = math.floor(split_value * len(data))

    return data[:training_set], data[training_set:]


def normalize_data(inputs):
    """
    Normalizes the data into a 0-1 range.
    :param inputs: The input data
    :type inputs : list
    :return:
    """
    for j in range(len(inputs[0].data)):

        if type(inputs[0].data[j]) is not str:
            min_elem, max_elem = None, None
            for i in range(len(inputs)):
                if min_elem is None:
                    min_elem = min(list(zip(*[x.data for x in inputs]))[j])
                    max_elem = max(list(zip(*[x.data for x in inputs]))[j])
                # http://stats.stackexchange.com/a/70807
                inputs[i].data[j] = (inputs[i].data[j] - min_elem) / (max_elem - min_elem)


def get_entropy(inputs):
    """
    Get error using the GINI Error measure for a given dataset
    :param inputs: the dataset
    :return: GINI Error
    """
    positives = inputs.count(1.0)
    negatives = len(inputs) - positives
    total = len(inputs)

    if positives == 0 or negatives == 0:
        return 0
    else:

        entropy = -(positives / total) * math.log(positives / total, 2) - (negatives / total) * math.log(
            negatives / total, 2)

        return entropy


def get_majority_label(input_data):
    try:
        return mode([x.truth for x in input_data])
    except StatisticsError:
        return [x.truth for x in input_data].pop()


def get_information_gain(input_data, attribute_index):
    subset_entropy = 0
    for choice in columns[attribute_index].choices:
        input_data_subset = [x.truth for x in input_data if x.data[attribute_index] == choice]

        subset_entropy += (len(input_data_subset) / len(input_data)) * get_entropy(input_data_subset)

    input_data = [x.truth for x in input_data]

    return get_entropy(input_data) - subset_entropy


def get_best_attribute_index(input_data, attribute_list):
    input_data = input_data[:]
    best_gain = -1
    best_attr = -1

    for attribute_index in attribute_list:
        temp_gain = get_information_gain(input_data, attribute_index)

        if temp_gain > best_gain:
            best_gain = temp_gain
            best_attr = attribute_index

    return best_attr


def build_tree(input_data, attributes_list, prune=True):
    classes = set([x.truth for x in input_data])

    root = TreeNode()

    if prune:
        pass

    # Stop if all instances belong to the same class
    if len(classes) == 1:
        root.label = classes.pop()
    elif len(attributes_list) == 0:
        root.label = get_majority_label(input_data)
    else:
        attribute_index = get_best_attribute_index(input_data, attributes_list)

        root.attribute_index = attribute_index

        for choice in columns[attribute_index].choices:
            branch = TreeNode()

            choice_subset = [x for x in input_data if x.data[attribute_index] == choice]

            if len(choice_subset) == 0:
                branch.label = get_majority_label(input_data)
                branch.attribute_value = choice
            else:
                branch = build_tree(choice_subset, [x for x in attributes_list if x != attribute_index])
                branch.attribute_value = choice
            root.add_child(branch)

    return root


def get_columns(inputs):
    """
    Find column properties and append Column object to an array.
    :param inputs: The input dataset
    :return: Array of Column objects
    """
    global columns
    for i in range(len(inputs[0].data)):
        columns.append(Column(list(zip(*[x.data for x in inputs]))[i]))


def classify_record(root, record):
    if root.label is not None:
        return root.label

    index = root.attribute_index

    branches = root.branches

    for branch in branches:
        if branch.attribute_value == record.data[index]:
            return classify_record(root=branch, record=record)


def classify_testing_data(root, input_data):
    """
    Classify the testing data using the Decision Tree we built
    :param root: The root of the decision tree
    :param input_data: The testing data-set
    :return: Estimation measures
    """

    tp, fn, fp, tn = 0, 0, 0, 0

    predictions = []
    for record in input_data:
        node = copy.deepcopy(root)
        predictions.append(classify_record(root=node, record=record))

    for prediction, record in zip(predictions, input_data):

        if prediction == record.truth:

            if prediction == 1:
                tp += 1
            else:
                tn += 1
        else:

            if prediction == 1:
                fp += 1
            else:
                fn += 1

    return tp, fn, fp, tn


def calculate_statistics(tp, fn, fp, tn):
    """
    Calculate the metrics for Performance Evaluation
    :param tp: True Positives
    :param fn: False Negatives
    :param fp: False Positives
    :param tn: True Negatives
    :return: None
    """
    accuracy = (tp + tn) / (tp + fn + fp + tn)

    if (tp + fp) != 0:
        precision = tp / (tp + fp)
    else:
        precision = 'No Positives Classified'
    recall = tp / (tp + fn)
    f_measure = 2 * tp / (2 * tp + fn + fp)

    print('Accuracy : {}'.format(accuracy))
    print('Precision : {}'.format(precision))
    print('Recall : {}'.format(recall))
    print('F-Measure : {}'.format(f_measure))


def discretize_data(inputs, no_of_bins):
    """
    This function converts our continuous data into "bins" based on the number of partitons
    :param inputs: The input dataset
    :param no_of_bins: The number of intervals
    :return: None
    """
    # Loop through columns
    for j in range(len(inputs[0].data)):

        if type(inputs[0].data[j]) is not str:
            min_elem, max_elem = None, None

            # Loop through rows
            for i in range(len(inputs)):

                # Calculate min and max of the column
                if min_elem is None:
                    min_elem = min(list(zip(*[x.data for x in inputs]))[j])
                    max_elem = max(list(zip(*[x.data for x in inputs]))[j])

                bin_width = (max_elem - min_elem) / no_of_bins

                for p in range(1, no_of_bins + 1):

                    if inputs[i].data[j] <= p * bin_width:
                        inputs[i].data[j] = p
                        break


def get_standardized_data(data_set, num_of_bins):
    data = read_file(data_set)
    normalize_data(data)
    discretize_data(data, num_of_bins)

    get_columns(data)

    return data


def run_algorithm(data_set=1, split_value=0.85, num_of_bins=5):
    """

    :param data_set: The input data file
    :param split_value: The percentage of data to use as training data and testing data
    :param num_of_bins: The number of partitions to make of the data while discretizing
    :return: None
    """

    assert num_of_bins > 1, "Number of Bins should be greater than 1"
    assert split_value > 0.5, "Testing data cannot be larger than training data"
    assert data_set in [1, 2, 4], "No such data-set exists"

    data = get_standardized_data(data_set, num_of_bins)

    training_data, testing_data = split_data(data, split_value=split_value)

    root = build_tree(training_data, range(len(columns)))
    tp, fn, fp, tn = classify_testing_data(root=root, input_data=testing_data)

    calculate_statistics(tp, fn, fp, tn)


if __name__ == '__main__':
    run_algorithm(data_set=4,
                  split_value=0.80,
                  num_of_bins=5)
