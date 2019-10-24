# encoding=utf-8
import random
import glob
import numpy as np

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
        self.sim_map = self.similar_word_cluster()
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

    def similar_word_cluster(self):
        print("Build up Word Cluster...")
        sim_map = np.zeros([len(self.word_list), len(self.word_list)])
        k = 1
        for i, word in enumerate(self.word_list):
            meaning =";".join(map(lambda x: x[1], self.wordset[word]))
            for j in range(k, len(self.word_list)):
                cand_word = self.word_list[j]
                cand_meaning = ";".join(map(lambda x: x[1], self.wordset[cand_word]))
                jc = self.jaccard_sim(meaning, cand_meaning)
                sim_map[i][j] = jc
                sim_map[j][i] = jc
            k += 1
        return sim_map

    def jaccard_sim(self, w1, w2):
        w1 = w1.replace(" ", "").replace(",", "").replace(";", "")
        w2 = w2.replace(" ", "").replace(",", "").replace(";", "")
        ch1 = list(filter(lambda x: x in w2, w1))
        ch2 = list(filter(lambda x: x in w1, w2))
        js1 = len(ch1)/len(w1)
        js2 = len(ch2)/len(w2)
        return js1*js2

    def select_candid(self, word):
        word_pool = filter(lambda x: x!=word,self.word_list)
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
    
    def make_study_synonyms(self):
        while True:
            idx = random.randint(0, len(self.word_list))
            word = self.word_list[idx]
            sim_idx_list = np.argwhere(self.sim_map[idx] > 0.7)
            if sim_idx_list.shape[0] > 3: 
                break
        meaning = ";".join((map(lambda x: x[1], self.wordset[word])))
        sim_idx_list = map(lambda x: x[0], sim_idx_list.tolist())
        sim_word_list = list(map(lambda i: self.wordset[self.word_list[i]], sim_idx_list))
        return word, meaning, sim_word_list
