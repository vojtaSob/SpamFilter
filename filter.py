from basefilter import BaseFilter
from training_from_corpus import Training
from utils import *
from quality import compute_quality_for_corpus


class MyFilter(BaseFilter):

    def __init__(self):
        self.trained = False
        self.average_number_receive_spams = 0
        self.average_number_receive_hams = 0
        self.average_length_spam_text = 0
        self.average_length_ham_text = 0
        self.dict_key_words_final_text = {}
        self.dict_key_words_final_subject = {}
        self.average_score_subject_spam = 0
        self.average_score_subject_ham = 0
        self.average_score_text_spam = 0
        self.average_score_text_ham = 0

    def train(self, path):
        t = Training(path)
        t.train()
        self.trained = True
        self.average_number_receive_spams = t.average_number_receive_spams
        self.average_number_receive_hams = t.average_number_receive_hams
        self.average_length_spam_text = t.average_length_spam_text
        self.average_length_ham_text = t.average_length_ham_text
        self.dict_key_words_final_text = t.dict_key_words_final_text.copy()
        self.dict_key_words_final_subject = t.dict_key_words_final_subject.copy()
        self.average_score_subject_spam = t.average_score_subject_spam
        self.average_score_subject_ham = t.average_score_subject_ham
        self.average_score_text_spam = t.average_score_text_spam
        self.average_score_text_ham = t.average_score_text_ham

    def decide(self, body):
        if not self.trained:
            return HAM_TAG
        rank = 0
        subject = return_subject_as_dict_from_body(body)
        rank_subject = evaluate_dict_by_dict(subject, self.dict_key_words_final_subject)
        rank += is_is_closer_to_a_ham_or_spam_number(self.average_score_subject_spam, self.average_score_subject_ham,
                                                     rank_subject)
        text = make_a_dict_from_body(body)
        rank_text = evaluate_dict_by_dict(text, self.dict_key_words_final_text)
        rank += is_is_closer_to_a_ham_or_spam_number(self.average_score_text_spam, self.average_score_text_ham,
                                                     rank_text)
        length = sum_a_dict(text)
        rank += is_is_closer_to_a_ham_or_spam_number(self.average_length_spam_text, self.average_length_ham_text,
                                                     length)
        if rank >= 2:
            return SPAM_TAG
        else:
            return HAM_TAG


if __name__ == "__main__":
    f = MyFilter()
    f.train("C:\\Users\\vojta\\Desktop\\PG\\SpamFilter\\1")
    f.test("C:\\Users\\vojta\\Desktop\\PG\\SpamFilter\\2")
    print(compute_quality_for_corpus("C:\\Users\\vojta\\Desktop\\PG\\SpamFilter\\2"))
