import copy
import math
import random
from statistics import mode, StatisticsError

from Projects.Project_3.models import DataRow, TreeNode, Column, ImpurityMeasure

indexed_attributes = []

depth = 0


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
    Using this function to split our data into training and testing data-sets
    :param data: The input data
    :param split_value: The % of data to use as testing data
    :return: Training data and Testing Data
    """
    training_set = math.floor(split_value * len(data))

    return data[:training_set], data[training_set:]


def normalize_data(inputs):
    """
    Normalize the data into a 0-1 range.
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

    pass


def get_classification_error(inputs):
    """
    Get error using the Classification Error Measure for a given dataset
    :param inputs: The dataset
    :return: Classification Error
    """
    positives = inputs.count(1.0)
    negatives = len(inputs) - positives
    total = len(inputs)

    if total:
        classification_error = 1 - max(positives, negatives) / total
        return classification_error
    else:
        return 1


def get_classification_error_for_split(inputs_left, inputs_right):
    """
    Return the minimum classification error for a split.
    :param inputs_left: Left Dataset
    :param inputs_right: Right Dataset
    :return:
    """
    return min(get_classification_error(inputs_left), get_classification_error(inputs_right))


def get_gini_error(inputs):
    """
    Get error using the GINI Error measure for a given dataset
    :param inputs: the dataset
    :return: GINI Error
    """
    positives = inputs.count(1.0)
    negatives = len(inputs) - positives
    total = len(inputs)

    if total:
        gini_error = 1 - (positives / total) ** 2 - (negatives / total) ** 2
        return gini_error
    else:
        return 0


def get_gini_error_for_split(inputs_left, inputs_right):
    """
    Return the minimum GINI error value for a split.
    :param inputs_left: Left Dataset
    :param inputs_right: Right Dataset
    :return:
    """

    return min(get_gini_error(inputs_left), get_gini_error(inputs_right))


def get_split_index(input_data, attributes, measure=ImpurityMeasure.CL_ERROR, expand=False):
    """
    Returns the index of the attribute to split on. We're using indexes as we don't have labels.
    :param input_data: The input dataset
    :param attributes: Array of Column objects
    :param measure: The measure to use while calculating error
    :param expand: Whether to expand on the remaining attributes once one of them is already selected
    :return: Index of the attribute to split on
    """

    index, nominal_choice = -1, None

    # 1 because it is higher than maximum value possible.
    # So regardless of our calculated error, it will be assigned to min_error
    min_measure = 1

    for i in range(len(attributes)):

        if i not in indexed_attributes:
            temp_choice, temp_min_measure = None, 1

            choices = attributes[i].choices

            for choice in choices:
                inputs_left = [x.truth for x in input_data if x.data[i] != choice]
                inputs_right = [x.truth for x in input_data if x.data[i] == choice]

                if measure == ImpurityMeasure.CL_ERROR:
                    split_measure = get_classification_error_for_split(inputs_left, inputs_right)
                elif measure == ImpurityMeasure.GINI:
                    split_measure = get_gini_error_for_split(inputs_left, inputs_right)

                if split_measure < temp_min_measure:
                    temp_min_measure = split_measure
                    temp_choice = choice

            if temp_min_measure < min_measure:
                min_measure = temp_min_measure
                nominal_choice = temp_choice
                index = i

    if len(indexed_attributes) < len(attributes):
        indexed_attributes.append(index)

        if expand:
            attributes[index].choices.remove(nominal_choice)
            if len(attributes[index].choices) != 1:
                indexed_attributes.remove(index)

    return index, nominal_choice


def get_mode_label(input_data):
    try:
        return mode([x.truth for x in input_data])
    except StatisticsError:
        return [x.truth for x in input_data].pop()


def build_tree(input_data, attributes, split_on, expand, pruning_size=5):
    classes = set([x.truth for x in input_data])

    node = TreeNode()

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
        index, choice = get_split_index(input_data, attributes, split_on, expand)

        if index < 0:
            node.label = get_mode_label(input_data)
        else:
            node.index = index
            node.choice = choice

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
                                       split_on=split_on,
                                       expand=expand)
                node.right = build_tree(input_data=data_right,
                                        attributes=attributes,
                                        pruning_size=pruning_size,
                                        split_on=split_on,
                                        expand=expand)

    return node


def get_attributes(inputs):
    """
    Find column properties and append Column object to an array.
    :param inputs: The input dataset
    :return: Array of Column objects
    """
    array = []
    for i in range(len(inputs[0].data)):
        array.append(Column(list(zip(*[x.data for x in inputs]))[i]))

    return array


def classify_testing_data(root, input_data):
    """
    Classify the testing data using the Decision Tree we built
    :param root: The root of the decision tree
    :param input_data: The testing data-set
    :return: Estimation measures
    """

    true_positives, false_negatives, false_positives, true_negatives = 0, 0, 0, 0

    for row in input_data:
        node = copy.deepcopy(root)
        while node.label is None:
            index, choice = node.index, node.choice

            if row.data[index] != choice:
                node = node.left
            else:
                node = node.right

        if row.truth == node.label:

            if node.label == 1.0:
                true_positives += 1
            else:
                true_negatives += 1
        else:

            if node.label == 1.0:
                false_positives += 1
            else:
                false_negatives += 1

    return true_positives, false_negatives, false_positives, true_negatives


def calculate_statistics(a, b, c, d):
    """
    Calculate the metrics for Performance Evaluation
    :param a: True Positives
    :param b: False Negatives
    :param c: False Positives
    :param d: True Negatives
    :return: None
    """
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


def run_algorithm(data_set=1, split_value=0.85, shuffle=True, measure=ImpurityMeasure.CL_ERROR, no_of_bins=5,
                  expand=False):
    """

    :param data_set: The input data file
    :param split_value: The percentage of data to use as training data and testing data
    :param shuffle: Whether to shuffle the data or not.
    :param measure: The Impurity Measure to use
    :param expand: Whether to furthur split nominal attributes until no choices are left.
                    ( ABC ) -> ( A,BC) -> (B,C)
    :param no_of_bins: The number of partitions to make of the data while discretizing
    :return: None
    """

    assert no_of_bins > 1, "Number of Bins should be greater than 1"
    assert split_value > 0.5, "Testing data cannot be larger than training data"
    assert data_set in [1, 2, 4], "No such data-set exists"

    data = read_file(data_set)

    if shuffle:
        random.shuffle(data)

    normalize_data(data)
    discretize_data(data, no_of_bins)

    attributes = get_attributes(data)
    training_data, testing_data = split_data(data, split_value=split_value)

    root = build_tree(input_data=training_data,
                      attributes=attributes,
                      split_on=measure,
                      expand=expand)

    true_positives, false_negatives, false_positives, true_negatives = classify_testing_data(root=copy.deepcopy(root),
                                                                                             input_data=testing_data)

    calculate_statistics(true_positives, false_negatives, false_positives, true_negatives)


if __name__ == '__main__':
    run_algorithm(data_set=1,
                  shuffle=False,
                  split_value=0.80,
                  no_of_bins=10,
                  expand=True,
                  measure=ImpurityMeasure.GINI)
