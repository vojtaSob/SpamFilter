import os.path

from corpus import Corpus
from utils import write_classification_to_file


class BaseFilter:
    def __init__(self):
        pass

    def train(self, path):
        pass

    def test(self, path):
        filename = os.path.join(path, '!prediction.txt')
        c = Corpus(path)
        classification = {}
        for email_name, content in c.emails():
            classification[email_name] = self.decide(content)
        write_classification_to_file(filename, classification)

    def decide(self, body):
        raise NotImplementedError
