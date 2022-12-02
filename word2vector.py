from gensim.test.utils import common_texts
from gensim.models import Word2Vec
from gensim.models.keyedvectors import KeyedVectors
import matplotlib.pyplot as plt
import re
import pandas as pd
from sklearn.manifold import TSNE

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
print("Loading Word2Vec model, please wait.")
model = KeyedVectors.load_word2vec_format('GoogleNews-vectors-negative300.bin', binary=True)
# model = Word2Vec.load("GoogleNews-vectors-negative300.bin")
# model.train([["hello", "world"]], total_examples=1, epochs=1) 

print("Word2Vec loading complete!")
#vector = model['yes']  # get numpy vector of a word
#sims = model.most_similar('yes', topn=10)  # get other similar words
#print(sims)

# get a list of word and simularity
result = model.most_similar(positive=['yes', 'absolutely'], negative=['no'], topn=100)
print(result)

result_words = [s[0] for s in result]
print(result_words)

# vocab = list(model.key_to_index)[:10]
X = model[result_words]
print(X)

tsne = TSNE(n_components=2)
X_tsne = tsne.fit_transform(X)

df = pd.DataFrame(X_tsne, index=result_words, columns=['x', 'y'])

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)

ax.scatter(df['x'], df['y'])

for word, pos in df.iterrows():
   ax.annotate(word, pos)
   
plt.show()


yes_ok_sim = model.similarity('king', 'prince')
print(yes_ok_sim)

#result = model.most_similar(negative=['man'])
#print(result)

#vocab = list(model.index_to_key)

#while True:
   #user_input = input("Input the words:")
   #splited = re.split('\W', user_input)
   #splited = list(filter(None, splited))
   #yes_score = 0
   #no_score = 0
   #for word in splited:
      #if word in vocab:
         #yes_score += model.similarity('king', word)
         #no_score += model.similarity('queen', word)
   #print("Similarities Percentage: King: " + str(yes_score) + ", Queen: " + str(no_score))

# print(vector)

