import os.path
from corpus import Corpus
from utils import read_classification_from_file, make_a_dict_from_body, dict_plus_dict, \
    number_of_received, return_subject_as_dict_from_body

SPAM_TAG = 'SPAM'
HAM_TAG = 'OK'


class Training:
    def __init__(self, path):
        self.path = path
        self.classification = read_classification_from_file(
            os.path.join(self.path, "!truth.txt"))
        self.sum_received_spams = 0
        self.sum_spams = 0
        self.sum_hams = 0
        self.sum_received_hams = 0
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
            if self.classification[name] == SPAM_TAG:
                self.sum_spams += 1
                self.sum_received_spams += number_of_received(body)
                self.add_to_spam_subject_dict(body)
                self.searchForKeyWordsInSpams(body)
            else:
                self.sum_hams += 1
                self.sum_received_hams += number_of_received(body)
                self.add_to_ham_subject_dict(body)
                self.searchForKeyWordsInHams(body)

    def add_to_spam_subject_dict(self, body):
        words = return_subject_as_dict_from_body(body)
        self.dict_keywords_spam_subjects = dict_plus_dict(self.dict_keywords_spam_subjects, words)

    def add_to_ham_subject_dict(self, body):
        words = return_subject_as_dict_from_body(body)
        self.dict_keywords_ham_subjects = dict_plus_dict(self.dict_keywords_ham_subjects, words)

    def searchForKeyWordsInSpams(self, body):
        words = make_a_dict_from_body(body)
        self.dict_keywords_spam_text = dict_plus_dict(self.dict_keywords_spam_text, words)

    def searchForKeyWordsInHams(self, body):
        words = make_a_dict_from_body(body)
        self.dict_keywords_ham_text = dict_plus_dict(self.dict_keywords_ham_text, words)

    def calculate_final_key_words_text(self):
        pass

    def calculate_final_key_words_subject(self):
        pass

    def export(self):
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


if __name__ == "__main__":
    t = Training("C:\\Users\\vojta\\Desktop\\PG\\SpamFilter\\2")
    t.train()
    t.export()
    print("Number of hams: ", t.sum_hams)
    print("Average number of resends: ", t.sum_received_hams / t.sum_hams)
    print("Subjects:")
    print(dict(sorted(t.dict_keywords_ham_subjects.items(), key=lambda item: item[1], reverse=True)))
    print("Average length of subject: ", t.average_length_ham_subject)
    print("Texts:")
    print(dict(sorted(t.dict_keywords_ham_text.items(), key=lambda item: item[1], reverse=True)))
    print("Average length of text:", t.average_length_ham_text)
    print("----------------------------")
    print("Number of spams: ", t.sum_spams)
    print("Average number of resend: ", t.sum_received_spams / t.sum_hams)
    print("Subjects:")
    print(dict(sorted(t.dict_keywords_spam_subjects.items(), key=lambda item: item[1], reverse=True)))
    print("Average length of subject: ", t.average_length_spam_subject)
    print("Texts:")
    print(dict(sorted(t.dict_keywords_spam_text.items(), key=lambda item: item[1], reverse=True)))
    print("Average length of text:", t.average_length_spam_text)
