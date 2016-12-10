from Projects.Project_3.decision_trees import *


def split(a, n):
    k, m = divmod(len(a), n)
    return [a[i * k + min(i, m):(i + 1) * k + min(i + 1, m)] for i in range(n)]


def run_k_folds(data_set=1, number_of_bins=5, num_of_folds=10):
    data = get_standardized_data(data_set=data_set, num_of_bins=number_of_bins)

    all_splits = split(data, num_of_folds)

    tp = fn = fp = tn = 0
    for i in range(num_of_folds):
        testing_data = all_splits[i]
        training_data = []
        for sub_list in all_splits:
            if sub_list != testing_data:
                training_data += sub_list

        root = build_tree(training_data, range(len(columns)))
        a, b, c, d = classify_testing_data(root=root, input_data=testing_data)

        tp += a
        fn += b
        fp += c
        tn += d

    calculate_statistics(tp / num_of_folds, fn / num_of_folds, fp / num_of_folds, tn / num_of_folds)


if __name__ == '__main__':
    run_k_folds(data_set=2,
                number_of_bins=5,
                num_of_folds=10)
