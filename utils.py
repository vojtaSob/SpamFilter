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
    dict_out = {}
    dict_out = dict_a.copy()
    for key in dict_b.keys():
        if dict_out.get(key):
            dict_out[key] += dict_b[key]
        else:
            dict_out[key] = dict_b[key]
    return dict_out


def number_of_received(body):
    received = 0
    lines = body.splitlines()
    text = []
    for i in lines:
        text.extend(re.split('<|>| |\n ', i))
    for i in text:
        if i == "Received:":
            received += 1
    return received
