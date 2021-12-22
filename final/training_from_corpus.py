import os.path
from corpus import Corpus
from utils import read_classification_from_file, make_a_dict_from_body, dict_plus_dict, \
    number_of_received, return_subject_as_dict_from_body, sum_a_dict, remove_from_dict_items_below_limit, \
    make_dict_percentage, make_dict_of_differences, evaluate_dict_by_dict

SPAM_TAG = 'SPAM'
HAM_TAG = 'OK'
LIMIT = 5


class Training:
    def __init__(self, path):
        self.path = path
        self.classification = read_classification_from_file(
            os.path.join(self.path, "!truth.txt"))
        self.sum_received_spams = 0
        self.sum_spams = 0
        self.sum_hams = 0
        self.average_number_receive_spams = 0
        self.average_number_receive_hams = 0
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
        self.average_score_subject_spam = 0
        self.average_score_subject_ham = 0
        self.average_score_text_spam = 0
        self.average_score_text_ham = 0

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
        self.export()
        self.evaluate_dicts()

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
        self.average_length_spam_subject = sum_a_dict(self.dict_keywords_spam_subjects)
        self.average_length_ham_subject = sum_a_dict(self.dict_keywords_ham_subjects)
        self.average_length_spam_subject = self.average_length_spam_subject / self.sum_spams
        self.average_length_ham_subject = self.average_length_ham_subject / self.sum_hams
        self.average_length_spam_text = sum_a_dict(self.dict_keywords_spam_text)
        self.average_length_ham_text = sum_a_dict(self.dict_keywords_ham_text)

        self.average_length_spam_text = self.average_length_spam_text / self.sum_spams
        self.average_length_ham_text = self.average_length_ham_text / self.sum_hams
        self.average_number_receive_hams = self.sum_received_hams / self.sum_hams
        self.average_number_receive_spams = self.sum_received_spams / self.sum_spams

        self.dict_keywords_ham_subjects = remove_from_dict_items_below_limit(self.dict_keywords_ham_subjects, LIMIT)
        self.dict_keywords_ham_text = remove_from_dict_items_below_limit(self.dict_keywords_ham_text, LIMIT)
        self.dict_keywords_spam_subjects = remove_from_dict_items_below_limit(self.dict_keywords_spam_subjects, LIMIT)
        self.dict_keywords_spam_text = remove_from_dict_items_below_limit(self.dict_keywords_spam_text, LIMIT)

        self.dict_keywords_ham_subjects = make_dict_percentage(self.dict_keywords_ham_subjects, self.sum_hams)
        self.dict_keywords_ham_text = make_dict_percentage(self.dict_keywords_ham_text, self.sum_hams)
        self.dict_keywords_spam_subjects = make_dict_percentage(self.dict_keywords_spam_subjects, self.sum_spams)
        self.dict_keywords_spam_text = make_dict_percentage(self.dict_keywords_spam_text, self.sum_spams)

        self.dict_key_words_final_subject = make_dict_of_differences(self.dict_keywords_spam_subjects,
                                                                     self.dict_keywords_ham_subjects)
        self.dict_key_words_final_text = make_dict_of_differences(self.dict_keywords_spam_text,
                                                                  self.dict_keywords_ham_text)

    def evaluate_dicts(self):
        c = Corpus(self.path)

        for name, body in c.emails():
            subject = make_a_dict_from_body(body)
            body = return_subject_as_dict_from_body(body)
            if self.classification[name] == SPAM_TAG:
                self.average_score_subject_spam += evaluate_dict_by_dict(subject, self.dict_key_words_final_subject)
                self.average_score_text_spam += evaluate_dict_by_dict(body, self.dict_key_words_final_text)
            else:
                self.average_score_subject_ham += evaluate_dict_by_dict(subject, self.dict_key_words_final_subject)
                self.average_score_text_ham += evaluate_dict_by_dict(body, self.dict_key_words_final_text)

        self.average_score_subject_spam = self.average_score_subject_spam / self.sum_spams
        self.average_score_text_spam = self.average_score_text_spam / self.sum_spams
        self.average_score_subject_ham = self.average_score_subject_ham / self.sum_hams
        self.average_score_text_ham = self.average_score_text_ham / self.sum_hams


if __name__ == "__main__":
    t = Training("C:\\Users\\vojta\\Desktop\\PG\\SpamFilter\\2")
    t.train()
    print("Subject Spam: ", t.average_score_subject_spam, " Ham: ", t.average_score_subject_ham)
    print("Text Spam: ", t.average_score_text_spam, " Ham: ", t.average_score_text_ham)
    """print("Number of hams: ", t.sum_hams)
    print("Average number of resends: ", t.sum_received_hams / t.sum_hams)
    print(t.average_number_receive_hams)
    print("Subjects:")
    # print(dict(sorted(t.dict_keywords_ham_subjects.items(), key=lambda item: item[1], reverse=True)))
    print("Average length of subject: ", t.average_length_ham_subject)
    print("Texts:")
    # print(dict(sorted(t.dict_keywords_ham_text.items(), key=lambda item: item[1], reverse=True)))
    print("Average length of text:", t.average_length_ham_text)
    print("----------------------------")
    print("Number of spams: ", t.sum_spams)
    print("Average number of resend: ", t.sum_received_spams / t.sum_spams)
    print(t.average_number_receive_spams)
    print("Subjects:")
    # print(dict(sorted(t.dict_keywords_spam_subjects.items(), key=lambda item: item[1], reverse=True)))
    print("Average length of subject: ", t.average_length_spam_subject)
    print("Texts:")
    # print(dict(sorted(t.dict_keywords_spam_text.items(), key=lambda item: item[1], reverse=True)))
    print("Average length of text:", t.average_length_spam_text)
    """
