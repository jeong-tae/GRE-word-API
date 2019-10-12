# encoding=utf-8
import random
import glob

class quiz_maker(object):
    def __init__(self, DATA_PATH):
        self.wordset = dict()
        for data_path in glob.glob("%s*" % DATA_PATH):
            with open(data_path) as f:
                for line in f.readlines():
                    word = line.rstrip().split("\t")[0]
                    if word in self.wordset:
                        self.wordset[word].append(line.rstrip().split("\t"))
                    else:
                        self.wordset[word] = [line.rstrip().split("\t")]
        self.word_list = list(self.wordset.keys())
        self.sample_size = 20
        self.question_type = ""
        self.field = 2

    def update_question_type(self, question_type):
        self.question_type = question_type
        if self.question_type == "cloze": 
            self.sample_size = 5
            self.field = 3
        elif self.question_type == "synonyms":
            self.sample_size = 5
            self.field = 4
        else:
            self.sample_size = 20
            self.field = 2

    def jaccard_sim(self, w1, w2):
        w1 = w1.replace(" ", "").replace(",", "").replace(";", "")
        w2 = w2.replace(" ", "").replace(",", "").replace(";", "")
        ch1 = list(filter(lambda x: x in w2, w1))
        ch2 = list(filter(lambda x: x in w1, w2))
        js1 = len(ch1)/len(w1)
        js2 = len(ch2)/len(w2)
        return js1*js2

    def select_candid(self, word):
        word_pool = self.word_list
        word_pool.remove(word) 
        return sorted(word_pool, key=lambda x: self.jaccard_sim(word, x), reverse=True)
    
    def filter_by_field(self, data):
        filtered = []
        for word in data:
            sample_list = self.wordset[word]
            for sample in sample_list:
                app = False
                if len(sample) < self.field: continue
                if sample[self.field-1] == "": continue
                app = True
            if app: filtered.append(word)
        return filtered

    def random_sampling(self):
        result = []
        if self.field >=3 :
            data = self.filter_by_field(self.word_list)
        else: 
            data = self.word_list
        for i, sample in enumerate(data):
            if i < self.sample_size: 
                result.append(sample)
            else:
                r = random.randint(0, i)
                if r < self.sample_size: 
                    result[r] = sample
                else:
                    pass
        return result

    def create_candid_pool(self):
        candidates_pool = dict()
        for sample in self.random_sampling():
            info = random.choice(self.wordset[sample])
            meaning = info[1]
            candidates = self.select_candid(sample)
            i = 0
            candidates_pool[sample] = []
            for candidate in candidates:
                meaning_cand = list(map(lambda x: x[1], self.wordset[candidate]))
#                s = max(map(lambda x: self.jaccard_sim(meaning.replace("하다",""), x.replace("하다","")), meaning_cand))
#               if s > 0.3: 
#                  pass
#               else:
                candidates_pool[sample].append(candidate)
                i += 1
                if i >= 4: break
        return candidates_pool

    def make_quiz_meaning(self, candidate_dict):
        word, candidates = candidate_dict
        meaning = ";".join(map(lambda x: x[1], self.wordset[word]))
        wrong_answer_list = list(map(lambda x: (x, random.choice(self.wordset[x])[1]), candidates))
        target_info = (word, meaning)
        return target_info, wrong_answer_list, ""

    def make_quiz_cloze(self, candidate_dict):
        word, candidates = candidate_dict
        meaning = ";".join(map(lambda x: x[1], self.wordset[word]))
        ex_sent = random.choice(self.wordset[word])[2].replace(word, "(    )")
        wrong_answer_list = list(map(lambda x: (x, random.choice(self.wordset[x])[1]), candidates))
        target_info = (word, meaning)
        return target_info, wrong_answer_list, ex_sent

    def make_quiz_synonyms(self, candidate_dict):
        word, candidates = candidate_dict
        meaning = ";".join(map(lambda x: x[1], self.wordset[word]))
        target_info = (word, meaning)
        synonyms = random.choice(self.wordset[word])[3]
        wrong_answer_list = list(map(lambda x: (x, random.choice(self.wordset[x])[1]), candidates))
        return target_info, wrong_answer_list, synonyms
