class BinaryConfusionMatrix:
    def __init__(self, pos_tag, neg_tag):
        self.tag_positive = pos_tag
        self.tag_negative = neg_tag
        self.tp = 0
        self.tn = 0
        self.fp = 0
        self.fn = 0

    def compute_from_dicts(self, truth_dict, pred_dict):
        for key, value in truth_dict.items():
            self.update(value, pred_dict[key])

    def update(self, truth, pred):
        if truth == self.tag_positive and pred == self.tag_positive:
            self.tp += 1
        elif truth == self.tag_positive and pred == self.tag_negative:
            self.fn += 1
        elif truth == self.tag_negative and pred == self.tag_positive:
            self.fp += 1
        elif truth == self.tag_negative and pred == self.tag_negative:
            self.tn += 1
        else:
            raise ValueError

    def as_dict(self):
        d = {"tp": self.tp, "tn": self.tn, "fp": self.fp, "fn": self.fn}
        return d
