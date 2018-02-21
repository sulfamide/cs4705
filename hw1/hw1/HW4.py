import math

import operator

tagSumArr = {}
tagArr = {}
countArr = []
bigramCount = {}
trigramCount = {}
unigramCount = {}


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



def computeEmission(str,tag):
    if not tagArr.has_key(str):
        return 0
    if not tagArr[str].has_key(tag):
        return 0
    tagCount=tagArr[str][tag]
    emi=float(tagCount)/(tagSumArr[tag])
    #emi=math.log(emi,2)
    return emi

def classifyRareWord(word,pos):
    if pos==0:
        return 'firstWord'
    if word.islower():
        return 'lowercase'
    #if word.isupper():
    #    return 'uppercase'
    if word[0].isupper():
        return 'initCap'


    pass
    return '_RARE_'

def rareTagger(corpus_file,output_file):
    l = corpus_file.readline()
    wordCount={}
    lineList=[]

    while (l):
        line = l.strip()
        lineList.append(line)
        if len(line)>0:
            wordList = line.split()
            if not wordCount.has_key(wordList[0]):
                wordCount[wordList[0]]=1
            else:
                wordCount[wordList[0]]+=1

        l = corpus_file.readline()

    bos = 0
    for l in lineList:
        if len(l)>0:
            wordList=l.split()
            if int(wordCount[wordList[0]])>=5:
                word=wordList[0]
            else:
                #word='_RARE_'
                word = classifyRareWord(wordList[0],bos)
            bos=1
            output_file.write("%s %s\n" % (word,wordList[1]))
        else:
            bos=0
            pass
            output_file.write(l+"\n")

    #print len(wordCount)
    #print wordCount['newcomers']


def tagger(inputStr):
    if inputStr not in tagArr:
        inputStr="_RARE_"

    cmax=0.0
    for key,value in tagArr[inputStr].iteritems():
        emis=float(computeEmission(inputStr,key))
        if emis>cmax:
            cmax=emis
            tag=key
    cmax=math.log(cmax,2)
    return cmax,tag


def tagDev(corpus_file,output_file):
    l = corpus_file.readline()
    while(l):
        line=l.strip()
        if len(line)>0:
            word=line
            #print word
            emax,tag=tagger(word)
            output_file.write("%s %s %f\n" % (word,tag,emax))
        else:
            output_file.write("\n")
        l = corpus_file.readline()

    pass


#compute P by count(Bigram)/count(Trigram)
def computePTri(tag):
    tagArr=tag.split(' ')
    triTag=tagArr[0]+' '+tagArr[1]+' '+tagArr[2]
    biTag=tagArr[0]+' '+tagArr[1]
    if not trigramCount.has_key(triTag):
        return 1
    if not bigramCount.has_key(biTag):
        return 1
    pTri=float(trigramCount[triTag])/float(bigramCount[biTag])
    #print trigramCount[triTag]
    #print bigramCount[biTag]
    pTri=math.log(pTri,2)
    return pTri


def viterbiAlgorithm(sentence,tagList):
    wordList=sentence.split()
    #print wordList
    tagDict={tag:key for key,tag in enumerate(tagList)}
    tagDict['*']=len(tagDict)
    tagDict['.']=len(tagDict)
    paiStatus=[{'* *':0}]
    probList = []
    bpForPai=[{}]
    #print len(wordList)
    for k,word in enumerate(wordList):
        k=k+1
        bpForPai.append({})
        paiStatus.append({})
        for tagV in tagList:
            emis = computeEmission(word, tagV);
            if emis==0:
                #print 'do'
                continue
            else:
                #using log or not
                emis=math.log(emis,2)
                #print emis
            if k==1 or k==2:
                tagListW=['*']
            else:
                tagListW=tagList
            if k==1:
                tagListU=['*']
            else:
                tagListU=tagList
            for tagU in tagListU:
                maxPai=0
                for tagW in tagListW:
                    triP=computePTri(tagW+' '+tagU+' '+tagV)
                    #print k
                    #print paiStatus[2]
                    if not paiStatus[k-1].has_key(tagW+' '+tagU):
                        continue
                    if triP>0:
                        continue
                    if paiStatus[k-1].has_key(tagW+' '+tagU)==0:
                        continue
                    else:
                        pai_status=paiStatus[k-1][tagW+' '+tagU]
                    curPai=float(pai_status+triP+emis)
                    if maxPai==0:
                        maxPai=curPai
                        maxTagW=tagW
                    elif curPai>maxPai:
                        maxPai=curPai
                        maxTagW=tagW
                if maxPai != 0:
                    #if len(paiStatus)!=k:
                    #    paiStatus.append({(tagU+' '+tagV):maxPai})
                    #    if k>2:
                    #        bpForPai.append({(tagU+' '+tagV):maxTagW})
                    #else:
                    paiStatus[k][tagU + ' ' + tagV] = maxPai
                    bpForPai[k][(tagU + ' ' + tagV)]= maxTagW


    #compute stop
    #print bpForPai
    #print len(bpForPai)
    #print len(wordList)
    #print len(paiStatus)

    k=len(wordList)
    maxPai=0
    paiStatus.append({})
    bpForPai.append({})
    for tagV in tagList:
        for tagU in tagList:
            triP=computePTri(tagU+' '+tagV+' STOP')

            if not paiStatus[k].has_key(tagU + ' ' + tagV):
                continue
            if triP > 0:
                continue
            if paiStatus[k].has_key(tagU + ' ' + tagV) == 0:
                continue
            else:
                pai_status = paiStatus[k][tagU + ' ' + tagV]
                #triP = math.log(triP, 2)
            curPai = float(pai_status + triP)
            if maxPai == 0:
                maxPai = curPai
                maxTagV = tagV
                maxTagU = tagU
            elif curPai > maxPai:
                maxPai = curPai
                maxTagV = tagV
                maxTagU = tagU
    if maxPai != 0:
        paiStatus[k+1][maxTagV + ' STOP'] = maxPai
        bpForPai[k+1][maxTagV+' STOP'] = maxTagU


    #print bpForPai
    tagV='STOP'
    tagU= maxTagV
    tagList = [maxTagV,'STOP']

    #print paiStatus[16]
    #print paiStatus[15]
    #print wordList[16]
    #print wordList[15]
    #print bpForPai

    k=len(bpForPai)-1
    while k>=1:
        tagUV=tagU+' '+tagV
        tagV = tagU
        #print tagUV,k
        prob = paiStatus[k][tagUV]
        probList.insert(0, prob)
        tagU=bpForPai[k][tagUV]
        tagList.insert(0,tagU)
        k-=1

    #print len(paiStatus)
    #print bpForPai
    #print probList
    #print len(probList)
    #print len(tagList)
    return probList[0:-1],tagList[2:-1]

def cleanSent(sent):
    wordList=sent.strip().split();
    sentence=''
    for k,word in enumerate(wordList):
        #word=classifyRareWord(word,k)
        if word not in tagArr:
            word="_RARE_"
        sentence=sentence+' '+word
    return sentence.strip()



def traigramTagger(input_file,output_file,tagSet):
    l = input_file.readline()
    sent=""
    while (l):
        line = l.strip()
        if len(line)<=0:
            #do tagging
            cleanedSent=cleanSent(sent)
            #print sent
            if len(sent.split())>=2:
                paiDict,tagList=viterbiAlgorithm(cleanedSent,tagSet)
            else:
                cmax,tag=tagger(cleanedSent)
                tagList=[tag]
            for k,word in enumerate(sent.split()):
                output_file.write("%s %s %f\n" % (word,tagList[k],1.0))
            output_file.write('\n')
            sent=""
        else:
            sent=sent+' '+line
        l = input_file.readline()
    pass


#do rare
#input=file("ner_train.dat","r")
#output=file("ner_srare_train.dat","w")
#output=file("ner_srare_withUpper_train.dat","w")
#rareTagger(input,output)




input=file("ner_rare_train.counts","r")
#input=file("ner_srare_train.counts","r")
#input=file("ner_train.counts","r")

computeCounts(input)
tagList=[tag for (tag,number) in tagSumArr.iteritems()]


#do computeEmission
#print computeEmission(str,tag)

#compute the maxEmission
#emax,tag=tagger(str)

#print emax,tag

#test dev
#input=file("ner_dev.dat","r")
#output=file("ner_dev.ans","w")
#tagDev(input,output)


#input=file("ner_train.counts","r")

#compute trigram possibility
#tag="* * O"
#pTri=computePTri(tag)
#print pTri

#viterbiAlgorithm
#sent="He said a proposal by EU Farm Commissioner Franz Fischler was a highly specific and precautionary move to protect human health ."
#sent="CRICKET - LEICESTERSHIRE TAKE OVER AT TOP AFTER INNINGS VICTORY ."

#sent="_RARE_ leaders in Chechnya have criticised Tim _RARE_ , the Swiss diplomat who heads the OSCE Chechnya mission , saying he was _RARE_ toward _RARE_ _RARE_ , president of the _RARE_ separatist government ."
#sent="LONDON 1996-08-30"
#sent="They said there was still demand for blue chips in engineering sector despite their persistent rise over the past several sessions ."
#sent=cleanSent(sent)
#print sent
#print len(sent.split())
#probList,tagList=viterbiAlgorithm(sent,tagList)

#print len(probList)
#print zip(tagList,sent.split())
#print paiDict

#trigramTagger
input=file("ner_dev.dat","r")
output=file("ner_dev_rare_tri.ans","w")
traigramTagger(input,output,tagList)