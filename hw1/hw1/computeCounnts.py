import math

import operator

tagSumArr = {}
tagArr = {}
countArr = []
bigramCount = {}
trigramCount = {}
unigramCount = {}
#tagList=[]

def computeCounts(corpus_file):
    l = corpus_file.readline()
    while(l):
        line=l.strip()
        wordList=line.split()
        #print wo[1]=='WORDTAG'
        #print wordList

        if wordList[1]!='WORDTAG':
            if wordList[1] == '1-GRAM':
                unigramCount[wordList[2]] = wordList[0]
            if wordList[1] == '2-GRAM':
                bigramCount[wordList[2] + " " + wordList[3]] = wordList[0]
            elif wordList[1] == '3-GRAM':
                trigramCount[wordList[2] + " " + wordList[3] + " " + wordList[4]] = wordList[0]
        else:
            if not tagSumArr.has_key(wordList[2]):
                tagSumArr[wordList[2]]=len(countArr)
                countArr.append(0)
            if not tagArr.has_key(wordList[3]):
                tagArr[wordList[3]]={}
            tagArr[wordList[3]][wordList[2]]=wordList[0]
            countArr[tagSumArr[wordList[2]]]+=int(wordList[0])
        #print countArr
        #print l
        l = corpus_file.readline()

    for key,value in tagSumArr.iteritems():
        tagSumArr[key]=countArr[tagSumArr[key]]




#input=file("ner_srare_train.counts","r")
#input=file("ner_train.counts","r")

def initCount(input):
    computeCounts(input)
    tagList=[tag for (tag,number) in tagSumArr.iteritems()]
    return tagList




#trigramTagger
#input=file("ner_dev.dat","r")
#output=file("ner_dev_srare_tri.ans","w")
#traigramTagger(input,output,tagList)