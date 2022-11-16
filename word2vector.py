from gensim.test.utils import common_texts
from gensim.models import Word2Vec
from gensim.models.keyedvectors import KeyedVectors
import re

# lines = []
# with open("IMDB Dataset.csv", "r", encoding="UTF-8") as f:
#    lines = f.readlines()
# splitedSentences = []

# processeed = 0
# maxProcessCount = 5000

# for line in lines:
#    sentences = line.split(".")
#    for sentence in sentences:
#       splited = re.split('\W', sentence)
#       splited = list(filter(None, splited))
#       splitedSentences.append(splited)
#       processeed += 1
#       if processeed > maxProcessCount:
#          break
#    if processeed > maxProcessCount:
#       break
   
# print(splitedSentences[0])

# model = Word2Vec(sentences=splitedSentences, vector_size=100, window=5, min_count=1, workers=4)
# model.save("word2vec.model")
model = KeyedVectors.load_word2vec_format('GoogleNews-vectors-negative300.bin', binary=True)
# model = Word2Vec.load("GoogleNews-vectors-negative300.bin")
# model.train([["hello", "world"]], total_examples=1, epochs=1) 


#vector = model['yes']  # get numpy vector of a word
#sims = model.most_similar('yes', topn=10)  # get other similar words
#print(sims)
#yes_ok_sim = model.similarity('yes', 'sure')
#print(yes_ok_sim)
#result = model.most_similar(positive=['woman', 'king'], negative=['man'])
#print(result)
#result = model.most_similar(negative=['yes'])
#print(result)

vocab = list(model.index_to_key)

while True:
   user_input = input("Would youe like to have some cookies?")
   splited = re.split('\W', user_input)
   splited = list(filter(None, splited))
   yes_score = 0
   no_score = 0
   for word in splited:
      if word in vocab:
         yes_score += model.similarity('yes', word)
         no_score += model.similarity('no', word)
   print("Similarities: yes: " + str(yes_score) + ", no: " + str(no_score))

# print(vector)

