import os

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

# def get_all_filenames(path):
#    files = os.listdir(path)
