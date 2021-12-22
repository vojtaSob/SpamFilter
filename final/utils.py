import os
import re

SPAM_TAG = 'SPAM'
HAM_TAG = 'OK'


def write_to_file():
    f = open('text.txt', 'a', encoding='utf-8')
    f.write('WOW!\n')
    f.close()

    with open('text.txt', 'a', encoding='utf-8') as f:
        f.write('WOW!\n')

    print('All done!')


def load_from_file():
    with open('text.txt', 'r', encoding='utf-8') as f:
        data = f.readlines()
    return data


def read_classification_from_file(file):
    mail_statuses = {}
    with open(file, 'r', encoding='utf-8') as f:
        s = f.readlines()
        for i in s:
            params = i.split()
            mail_statuses[params[0]] = params[1]
    return mail_statuses


def write_classification_to_file(file, mail_statuses):
    with open(file, 'w', encoding='utf-8') as f:
        for mail, status in mail_statuses.items():
            s = "{} {}".format(mail, status)
            f.write(s)
            f.write('\n')


def return_subject_as_dict_from_body(body):
    """Method finds subject in body and returns it as a dict of worlds"""
    data = body.splitlines()
    subject = None
    for i in data:
        if i.startswith("Subject:"):
            subject = i
    if subject is None:
        return None
    data = subject.split()
    dict_out = {}
    for i in data:
        if dict_out.get(i):
            dict_out[i] += 1
        else:
            dict_out[i] = 1
    try:
        dict_out.pop('Subject:')
        return dict_out
    except KeyError:
        return dict_out


def make_a_dict_from_body(body):
    """Returns body as dict of worlds and counts, method cleans mail from headers"""
    lines = body.splitlines()
    for i in range(0, len(lines)):
        if lines[i] == '':
            i += 1
            del lines[:i]
            break
    text = []
    for i in lines:
        text.extend(re.split('<|>| |\n ', i))
    dict_output = {}
    while '' in text:
        text.remove('')
    for i in text:
        if dict_output.get(i):
            dict_output[i] += 1
        else:
            dict_output[i] = 1
    return dict_output


def dict_plus_dict(dict_a, dict_b):
    """Methods return dict made of two, if dicts got same keys, values are added"""
    dict_out = {}
    dict_out = dict_a.copy()
    try:
        for key in dict_b.keys():
            if dict_out.get(key):
                dict_out[key] += dict_b[key]
            else:
                dict_out[key] = dict_b[key]
        return dict_out
    except AttributeError:
        return dict_out


def number_of_received(body):
    """Methods return number of word received in mail"""
    received = 0
    lines = body.splitlines()
    text = []
    for i in lines:
        text.extend(re.split('<|>| |\n ', i))
    for i in text:
        if i == "Received:":
            received += 1
    return received


def sum_a_dict(dict_in):
    """Sum values in a dict"""
    dict_out = {}
    dict_out = dict_in.copy()
    suma = 0
    for i in dict_out.values():
        suma += i
    return suma


def remove_from_dict_items_below_limit(dict_in, limit):
    """Remove from dict keys with values below limit"""
    dict_out = {}
    for key, value in dict_in.items():
        if value >= limit:
            dict_out[key] = value

    return dict_out


def make_dict_percentage(dict_in, number):
    dict_out = dict_in.copy()
    for key, value in dict_out.items():
        dict_out[key] = value / number
    return dict_out


def make_dict_of_differences(dict_spam, dict_ham):
    dict_out = {}
    dict_out = dict_spam.copy()
    for key, value in dict_out.items():
        if dict_ham.get(key):
            if dict_ham[key] > dict_out[key]:
                dict_out[key] = -1 * dict_ham[key]
                dict_ham.pop(key)

    for key, value in dict_ham.items():
        dict_out[key] = -1 * dict_ham[key]

    return dict_out


def evaluate_dict_by_dict(dict_text, dict_ranks):
    score = 0
    try:
        for key, value in dict_text.items():
            if dict_ranks.get(key):
                score += dict_text[key] * dict_ranks[key]
        return score
    except AttributeError:
        return 0


def is_is_closer_to_a_ham_or_spam_number(number_spam, number_ham, number_to_decide):
    """Return 1 if number is closer to spam or 0 if closer to ham"""
    avg = (number_spam + number_ham) / 2
    if number_spam >= number_ham:
        if number_to_decide >= avg:
            return 1
        else:
            return 0
    else:
        if number_to_decide <= avg:
            return 1
        else:
            return 0
