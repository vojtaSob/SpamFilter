import os.path
import re
import operator
from corpus import Corpus
from utils import read_classification_from_file

SPAM_TAG = 'SPAM'
HAM_TAG = 'OK'


class Training:
    def __init__(self, path):
        self.path = path
        self.classification = read_classification_from_file(
            os.path.join(self.path, "!truth.txt"))
        self.sum_chain_spams = 0
        self.sum_spams = 0
        self.sum_hams = 0
        self.sum_chain_hams = 0
        self.dict_keywords_spam_subjects = {}
        self.dict_keywords_ham_subjects = {}
        self.average_length_spam_subject = 0
        self.average_length_ham_subject = 0
        self.dict_keywords_spam_text = {}
        self.dict_keywords_ham_text = {}
        self.average_length_spam_text = 0
        self.average_length_ham_text = 0
        self.dict_key_words_final_text = {}
        self.dict_key_words_final_subject = {}

    def train(self):
        corpus = Corpus(self.path)

        for name, body in corpus.emails():
            data = body.splitlines()
            lines = data
            subject = ""
            datas = []
            for i in data:
                if i.startswith("Subject:"):
                    subject = i
                datas.extend(re.split('<|>| |\n ', i))

            for i in range(0, len(lines)):
                if lines[i] == '':
                    i += 1
                    del lines[:i]
                    break

            if self.classification[name] == SPAM_TAG:
                self.sum_spams += 1
                self.checkForChain(datas, 'S')
                self.add_to_spam_subject_dict(subject)
                self.searchForKeyWordsInSpams(lines)
            else:
                self.sum_hams += 1
                self.checkForChain(datas, 'H')
                self.add_to_ham_subject_dict(subject)
                self.searchForKeyWordsInHams(lines)

    def export(self):
        self.dict_keywords_spam_subjects.pop('Subject:')
        self.dict_keywords_ham_subjects.pop('Subject:')
        for i in self.dict_keywords_spam_subjects.values():
            self.average_length_spam_subject += i
        for i in self.dict_keywords_ham_subjects.values():
            self.average_length_ham_subject += i
        self.average_length_spam_subject = self.average_length_spam_subject / self.sum_spams
        self.average_length_ham_subject = self.average_length_ham_subject / self.sum_hams
        for i in self.dict_keywords_spam_text.values():
            self.average_length_spam_text += 1
        for i in self.dict_keywords_ham_text.values():
            self.average_length_ham_text += 1
        self.average_length_spam_text = self.average_length_spam_text / self.sum_spams
        self.average_length_ham_text = self.average_length_ham_text / self.sum_hams
        remove = []
        for key, value in self.dict_keywords_ham_subjects.items():
            if value < 5:
                remove.append(key)
        for i in remove:
            self.dict_keywords_ham_subjects.pop(i)
        remove.clear()
        for key, value in self.dict_keywords_ham_text.items():
            if value < 5:
                remove.append(key)
        for i in remove:
            self.dict_keywords_ham_text.pop(i)
        remove.clear()
        for key, value in self.dict_keywords_spam_subjects.items():
            if value < 5:
                remove.append(key)
        for i in remove:
            self.dict_keywords_spam_subjects.pop(i)
        remove.clear()
        for key, value in self.dict_keywords_spam_text.items():
            if value < 5:
                remove.append(key)
        for i in remove:
            self.dict_keywords_spam_text.pop(i)

        self.calculate_final_key_words_text()
        self.calculate_final_key_words_subject()

    def checkForChain(self, datas, param):
        for i in datas:
            if i == "Received:":
                if param == 'S':
                    self.sum_chain_spams += 1
                else:
                    self.sum_chain_hams += 1

    def add_to_spam_subject_dict(self, subject):
        data = subject.split()
        for i in data:
            if self.dict_keywords_spam_subjects.get(i):
                self.dict_keywords_spam_subjects[i] += 1
            else:
                self.dict_keywords_spam_subjects[i] = 1

    def add_to_ham_subject_dict(self, subject):
        data = subject.split()
        for i in data:
            if self.dict_keywords_ham_subjects.get(i):
                self.dict_keywords_ham_subjects[i] += 1
            else:
                self.dict_keywords_ham_subjects[i] = 1

    def searchForKeyWordsInSpams(self, lines):
        text = []
        while '' in lines:
            lines.remove('')
        for i in lines:
            text.extend(re.split('<|>| |\n ', i))
        while '' in text:
            text.remove('')
        for i in text:
            if self.dict_keywords_spam_text.get(i):
                self.dict_keywords_spam_text[i] += 1
            else:
                self.dict_keywords_spam_text[i] = 1

    def searchForKeyWordsInHams(self, lines):
        text = []
        while '' in lines:
            lines.remove('')
        for i in lines:
            text.extend(re.split('<|>| |\n ', i))
        while '' in text:
            text.remove('')
        for i in text:
            if self.dict_keywords_ham_text.get(i):
                self.dict_keywords_ham_text[i] += 1
            else:
                self.dict_keywords_ham_text[i] = 1

    def calculate_final_key_words_text(self):
        pass

    def calculate_final_key_words_subject(self):
        pass


if __name__ == "__main__":
    t = Training("C:\\Users\\vojta\\Desktop\\PG\\SpamFilter\\2")
    t.train()
    t.export()
    print("Number of hams: ", t.sum_hams)
    print("Average number of resends: ", t.sum_chain_hams / t.sum_hams)
    print("Subjects:")
    print(dict(sorted(t.dict_keywords_ham_subjects.items(), key=lambda item: item[1], reverse=True)))
    print("Average length of subject: ", t.average_length_ham_subject)
    print("Texts:")
    print(dict(sorted(t.dict_keywords_ham_text.items(), key=lambda item: item[1], reverse=True)))
    print("Average length of text:", t.average_length_ham_text)
    print("----------------------------")
    print("Number of spams: ", t.sum_spams)
    print("Average number of resend: ", t.sum_chain_spams / t.sum_hams)
    print("Subjects:")
    print(dict(sorted(t.dict_keywords_spam_subjects.items(), key=lambda item: item[1], reverse=True)))
    print("Average length of subject: ", t.average_length_spam_subject)
    print("Texts:")
    print(dict(sorted(t.dict_keywords_spam_text.items(), key=lambda item: item[1], reverse=True)))
    print("Average length of text:", t.average_length_spam_text)
