import os


class Corpus:
    def __init__(self, path):
        self.path = path

    def emails(self):
        mails = {}
        files = os.listdir(self.path)
        for i in files:
            a = i[0]
            if a != '!':
                yield i, getBody(self.path, i)


def getBody(path, name):
    with open(path + '\\' + name, 'r', encoding='utf-8') as f:
        body = f.read(-1)
        return body


if __name__ == "__main__":
    c = Corpus("C:\\Users\\vojta\\Desktop\\PG\\SpamFilter\\1")

    print(c.emails())
    for fname, contents in c.emails():

        print(fname)
        print(contents)
