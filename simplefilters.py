import os.path
import random
from quality import compute_quality_for_corpus, quality_score
from corpus import Corpus
from utils import write_classification_to_file, HAM_TAG, SPAM_TAG

from basefilter import BaseFilter


class NaiveFilter(BaseFilter):
    def decide(self):
        return HAM_TAG


class ParanoidFilter(BaseFilter):
    def decide(self):
        return SPAM_TAG


class RandomFilter(BaseFilter):
    def decide(self):
        return random.choice([HAM_TAG, SPAM_TAG])


if __name__ == "__main__":
    naive = ParanoidFilter()
    naive.test("1")
    print(compute_quality_for_corpus("1"))
