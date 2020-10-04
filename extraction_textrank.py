import math
import re
import numpy as np
import networkx as nx

#Input: Txt name.
#Function: 
# - constructs a similarity matrix using cosine similarity
# - use TextRank algorithm based on page ranking 

#splits the sentences in the article into individual words
def read_article(doc, fromFile):
    temp = ['']
    if fromFile:
        file = open(doc, "r", encoding='utf-8')
        filedata = file.readlines()
        for index in range(len(filedata)):
            temp[0] = temp[0] + filedata[index].rstrip("\n") + " "
    else:
        temp = [doc]
    article = re.split('[.?!] ', temp[0])
    sentences = []
    for sentence in article:
        sentences.append(sentence.replace("[^a-zA-Z]", " ").split(" "))
    return sentences

#returns angle between two sentence vectors
def sentence_similarity(sent1, sent2, stopwords=None):
    if stopwords is None:
        stopwords = []
    
    #converts all words to lowercase
    sent1 = [w.lower() for w in sent1]
    sent2 = [w.lower() for w in sent2]
 
    #combines all words from two different sentences
    all_words = list(set(sent1 + sent2))
 
    #create empty vectors
    vector1 = [0] * len(all_words)
    vector2 = [0] * len(all_words)
 
    # build the vector for the first sentence
    for w in sent1:
        if w in stopwords: #stopwords to eliminate words like "the", "a" which are irrelevant
            continue
        vector1[all_words.index(w)] += 1 #fill in 1 if not stopword
 
    # build the vector for the second sentence
    for w in sent2:
        if w in stopwords:
            continue
        vector2[all_words.index(w)] += 1
    
    # at this point, vector1 and vector2 are filled with 1s and 0s 

    #calculate angle between two vectors (similiarity)
    angle = np.dot(vector1, vector2)/(math.sqrt(np.dot(vector1, vector1))) * (math.sqrt(np.dot(vector2, vector2)))
    return angle

#returns a similarity matrix of all sentences
def build_similarity_matrix(sentences, stop_words):
    # Create an empty similarity matrix
    similarity_matrix = np.zeros((len(sentences), len(sentences)))
 
    #builds a matrix of degree of similiarity values
    for i in range(len(sentences)):
        for j in range(len(sentences)):
            if i != j: #ignore if both are same sentences
                similarity_matrix[i][j] = sentence_similarity(sentences[i], sentences[j], stop_words)
    return similarity_matrix

#converts matrix to graph and uses page rank method to rank sentences
def generate_extract_summary(doc, fromFile):
    
    with open("stopwords.txt", 'r') as file:
        stop_words = file.readlines()

    summarize_text = []

    # Step 1 - Read text anc split it
    sentences =  read_article(doc, fromFile)

    top_n = math.ceil(len(sentences) / 5)

    # Step 2 - Generate Similary Martix across sentences
    sentence_similarity_martix = build_similarity_matrix(sentences, stop_words)

    # Step 3 - Rank sentences in similarity martix
    #converts to adjacency matrix
    sentence_similarity_graph = nx.from_numpy_array(sentence_similarity_martix)
    #ranks sentences using page rank method
    scores = nx.pagerank(sentence_similarity_graph)

    # Step 4 - Sort the rank and pick top sentences
    ranked_sentence = sorted(((scores[i],s) for i,s in enumerate(sentences)), reverse=True)      

    for i in range(top_n):
        summarize_text.append(" ".join(ranked_sentence[i][1]))
    
    summary = ". ".join(summarize_text)

    return summary

#print(generate_extract_summary("President Trump’s performance at the first presidential debate was so petulant and disgusting that it has taken me this long to put my thoughts to pixels. It’s not like I was surprised by what he did. Trump has been barking lies and obscenities at the American people since June 16, 2015. What was breathtaking on Tuesday was the ferocity of his bullying. It was a Brett Kavanaugh-like performance that reeked of desperation.\n\nThe chaos in Cleveland reinforced my belief that Trump will do everything to win. He’ll do anything to maintain his shield from criminal prosecution and to continue monetizing the presidency — perhaps to make enough money to pay the $421 million in debts and loans that are coming due within the next four years, according to the New York Times. Trump is as pathetic as he is dangerous.", False))