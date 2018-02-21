import json
from count_cfg_freq import Counts

counter=Counts()
vocab={}

def loadData(corpus_file):
    l = corpus_file.readline()
    while(l):
        t = json.loads(l)
        counter.count(t)
        wordList = [y for x,y in extract_tag(t)]
        for word in wordList:
            if word not in vocab:
                vocab[word]=0
            vocab[word]+=1
        #for tag in tagList
        l = corpus_file.readline()


def extract_tag(t):
    if len(t)==3:
        return extract_tag(t[1])+extract_tag(t[2])
    if len(t)==2:
        return [(t[0],t[1])]


def tagRareWord(corpus_file,new_corpus_file):
    l = corpus_file.readline()
    while (l):
        tagList=extract_tag(json.loads(l))
        for tag in tagList:
            if vocab[tag[1]]<5:
                new_str='"'+tag[0]+ '", "_RARE_"'
                l=l.replace('"'+tag[0]+'", "'+tag[1]+'"',new_str)
        new_corpus_file.write(l)
        #print 1
        l = corpus_file.readline()


    #for (sym, word), count in counter.unary.iteritems():
    #print count, "UNARYRULE", sym, word
    #    pass


input=file("parse_train.dat","r")
output=file("HW4.txt","w")
loadData(input)

input=file("parse_train.dat","r")
tagRareWord(input,output)


