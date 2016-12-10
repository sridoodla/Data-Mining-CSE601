from random import randint

from Projects.Project_3.decision_trees import *
from Projects.Project_3.models import Classifier


def assign_initial_weights(input_data):
    for x in input_data:
        x.weight = 1 / len(input_data)


def get_random_sampling(data, split_value):
    split_index = math.floor(len(data) * split_value)

    res = []
    while split_index > 1:
        res.append(data[randint(0, len(data) - 1)])
        split_index -= 1

    return res


def get_error(root, input_data):
    predictions = []
    for record in input_data:
        node = copy.deepcopy(root)
        predictions.append(classify_record(root=node, record=record))

    error = 0
    for prediction, record in zip(predictions, input_data):

        if prediction != record.truth:
            error += record.weight

    return error, predictions


def classify_testing_data_on_boosters(classifiers, input_data):
    tp = fn = fp = tn = 0
    predictions = []
    for record in input_data:
        w0 = 0
        w1 = 0

        for classifier in classifiers:
            label = classify_record(root=copy.deepcopy(classifier.root), record=record)

            if label == 1:
                w1 += classifier.weight
            else:
                w0 += classifier.weight

        predictions.append(1 if w1 > w0 else 0)

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


def boost(data_set=1, num_of_bins=5, num_of_classifiers=5, split_value=0.6):
    data = get_standardized_data(data_set=data_set, num_of_bins=num_of_bins)

    assign_initial_weights(data)

    i = 0

    # Training Classifiers
    classifiers = []
    while i < num_of_classifiers:
        d1 = get_random_sampling(data=data, split_value=split_value)

        d2 = get_random_sampling(data=data, split_value=0.66)
        classifier = Classifier()

        classifier.root = build_tree(input_data=d1, attributes_list=range(len(columns)))

        error, predictions = get_error(root=classifier.root, input_data=d2)

        if error < 0.5:
            i += 1

            if error == 0:
                classifiers.append(classifier)
                break
            classifier.weight = math.log((1 - error) / error)

            for prediction, record in zip(predictions, d1):
                if prediction == record.truth:
                    record.weight *= math.exp(-classifier.weight)

            # Sum of Weights
            weight_sum = sum([x.weight for x in data])

            # Normalizing
            for record in data:
                record.weight /= weight_sum

            classifiers.append(classifier)

    testing_data = data[:]

    a, b, c, d = classify_testing_data_on_boosters(classifiers=classifiers, input_data=testing_data)

    calculate_statistics(a, b, c, d)


if __name__ == '__main__':
    boost(
        data_set=1,
        num_of_bins=5,
        num_of_classifiers=3,
        split_value=0.60
    )
