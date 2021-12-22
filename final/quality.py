import os.path

from utils import read_classification_from_file
from confmat import BinaryConfusionMatrix


def quality_score(tp, tn, fp, fn):
    value = (tp + tn) / (tp + tn + 10 * fp + fn)
    return value


def compute_quality_for_corpus(corpus_dir):
    truth = read_classification_from_file(os.path.join(corpus_dir, "!truth.txt"))
    pred = read_classification_from_file(os.path.join(corpus_dir, "!prediction.txt"))
    b = BinaryConfusionMatrix("SPAM", "OK")
    b.compute_from_dicts(truth, pred)
    matrix = b.as_dict()
    return quality_score(matrix['tp'], matrix['tn'], matrix['fp'], matrix['fn'])


if __name__ == "__main__":
    print(quality_score(1, 1, 1, 1))
