from fwords import fwords
from collections import Counter
import re

def compare_lsm(preps1, preps2):
	return 1 - (abs(preps1 - preps2)/float(preps1 + preps2 + .0001))

def compare_lsm_obj(obj1, obj2):
	"""
	reduces two lsm objects to a float representing their alikeness
	higher return value means more alike
	"""
	total = []
	for k in obj1.percents.keys():
		weight = float(obj1.percents[k] + obj2.percents[k])/2
		diff = compare_lsm(obj1.percents[k], obj2.percents[k])
		total.append(compare_lsm(diff, weight))
	return float(sum(total)) / len(total)

def reduce_to_words(text):
	"""
	split a text into an array of lowercase words, 
	eliminating spaces, punctuation, etc.
	"""
	return [word.lower() for word in re.findall(r"\w+", text)]

class LSM(object):
	def __init__(self, text):
		self.text = text
		self.reduced = reduce_to_words(text)
		self.counter = Counter(self.reduced)
		self.fwords = {}
		self.percents = {}
		for function, wordlist in fwords.items():
			self.fwords[function] = 0
			for word in wordlist:
				self.fwords[function] += self.counter[word]
			self.percents[function] = float(self.fwords[function]) / len(self.reduced)
		self.percents['content'] = 1 - sum(self.percents.values())
	def compare_key(self, other, key):
		return compare_lsm(self.percents[key], other.percents[key])
	def compare(self, other):
		return compare_lsm_obj(self, other)
	def __add__(self, other):
		"""
		combines two LSM objects, returns a new one
		"""
		return LSM(self.text + other.text)
	def __radd__(self, other):
		# LSM: flawless victory
		return self