from random import randint

from Projects.Project_3.decision_trees import *


def split_len(a, n):
    k, m = divmod(len(a), n)
    return [len(a[i * k + min(i, m):(i + 1) * k + min(i + 1, m)]) for i in range(n)]


def split(a, n):
    k, m = divmod(len(a), n)
    return [a[i * k + min(i, m):(i + 1) * k + min(i + 1, m)] for i in range(n)]


def classify_forest(forest, input_data):
    tp = fn = fp = tn = 0
    predictions = []

    for record in input_data:

        record_predictions = []
        for tree in forest:
            root = copy.deepcopy(tree)
            node = copy.deepcopy(root)
            record_predictions.append(classify_record(root=node, record=record))

        predictions.append(mode(record_predictions))

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


def run_random_forests(data_set=1, number_of_bins=5, num_of_trees=5, num_of_folds=10):
    data = get_standardized_data(data_set=data_set, num_of_bins=number_of_bins)

    all_splits = split(data, num_of_folds)

    tp = fn = fp = tn = 0
    # K-Folds
    for i in range(num_of_folds):
        testing_data, training_data = all_splits[i], []
        for sub_list in all_splits:
            if sub_list != testing_data:
                training_data += sub_list

        split_lens = split_len(training_data, num_of_trees)

        forest_trees = []
        for j in range(num_of_trees):

            forest_training_data = []
            len_td = len(training_data)
            while split_lens[j] != 0:
                forest_training_data.append(training_data[randint(0, len_td - 1)])
                split_lens[j] -= 1

            total_attributes = len(columns)

            num_of_attributes_to_be_selected = math.ceil(total_attributes * 0.2)

            selected_attributes = []
            while num_of_attributes_to_be_selected != 0:

                p = randint(0, total_attributes - 1)

                if p not in selected_attributes:
                    selected_attributes.append(p)
                    num_of_attributes_to_be_selected -= 1

            forest_trees.append(build_tree(forest_training_data, selected_attributes, prune=False))

        a, b, c, d = classify_forest(forest_trees, testing_data)

        tp += a
        fn += b
        fp += c
        tn += d

    calculate_statistics(tp / num_of_folds, fn / num_of_folds, fp / num_of_folds, tn / num_of_folds)

    pass


if __name__ == '__main__':
    run_random_forests(data_set=2,
                       number_of_bins=5,
                       num_of_trees=5,
                       num_of_folds=10)
