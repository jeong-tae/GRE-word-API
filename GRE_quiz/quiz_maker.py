# encoding=utf-8
import random
import glob

class quiz_maker(object):
	def __init__(self, DATA_PATH):
		self.wordset = dict()
		for data_path in glob.glob("%s/*" % DATA_PATH):
			with open(data_path) as f:
				for line in f.readlines():
					word = line.rstrip().split("\t")[0]
					if word in self.wordset:
						self.wordset[word].append(line.rstrip().split("\t"))
					else:
						self.wordset[word] = [line.rstrip().split("\t")]
		self.word_list = self.wordset.keys()
		self.sample_size = 5

	
	def jaccard_sim(self, w1, w2):
		w1 = w1.replace(" ", "").replace(",", "").replace(";", "")
		w2 = w2.replace(" ", "").replace(",", "").replace(";", "")
		ch1 = list(filter(lambda x: x in w2, w1))
		ch2 = list(filter(lambda x: x in w1, w2))
		js1 = len(ch1)/len(w1)
		js2 = len(ch2)/len(w2)
		return js1*js2

	def select_candid(self, word):
		return sorted(self.word_list, key=lambda x: self.jaccard_sim(word, x), reverse=True)

	def random_sampling(self, target_index=False):
		result = []
		if target_index: 
			data = filter(lambda a: a!=False, map(lambda x: x if target_index in x else False, self.wordset))
		else: 
			data = self.wordset
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
				s = max(map(lambda x: self.jaccard_sim(meaning.replace("하다",""), x.replace("하다","")), meaning_cand))
				if s > 0.3: 
					pass
				else:
					candidates_pool[sample].append(candidate)
					i += 1
				if i >= 4: break
		return candidates_pool

	def make_quiz_meaning(self, candidate_dict):
		answer, candidates = candidate_dict
		meaning = ";".join(map(lambda x: x[1], self.wordset[answer]))
		wrong_answer_list = list(map(lambda x: (x, random.choice(self.wordset[x])[1]), candidates))
		return answer, meaning, wrong_answer_list

	def make_quiz_cloze(self, candidate_dict):
		answer, candidates = candidate_dict
		meaning = ";".join(map(lambda x: x[1], self.wordset[answer]))
		if self.wordset[answer][2] == "": 
			return
		else:
			ex_sent = self.wordset[answer][2].replace(answer, "(	)")
			wrong_answer_list = list(map(lambda x: (x, random.choice(self.wordset[x])[1]), candidates))
			return answer, meaning, wrong_answer_list, ex_sent

	def make_quiz_synonym(self, candidate_dict):
		answer, candidates = candidate_dict
		meaning = ";".join(map(lambda x: x[1], self.wordset[answer]))
		if self.wordset[answer][3] == "": 
			return
		else:
			synonyms = self.wordset[answer][3]
			wrong_answer_list = list(map(lambda x: (x, random.choice(self.wordset[x])[1]), candidates))
			return answer, meaning, wrong_answer_list, synonyms
