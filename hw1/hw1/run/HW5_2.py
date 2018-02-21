from HW5_1 import computePTri
from HW4_2 import computeEmission,tagger
from HW4_1 import classifyRareWord
from computeCounnts import tagArr
from computeCounnts import initCount

import math


def viterbiAlgorithm(sentence,tagList):
    #print sentence
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


def trigramTagger(input_file,output_file,tagSet):
    l = input_file.readline()
    sent=""
    while (l):
        line = l.strip()
        if len(line)<=0:
            #do tagging
            cleanedSent=cleanSent(sent)
            #print sent
            if len(sent.split())>=2:
                probList,tagList=viterbiAlgorithm(cleanedSent,tagSet)
            else:
                cmax,tag=tagger(cleanedSent)
                tagList=[tag]
            for k,word in enumerate(sent.split()):
                output_file.write("%s %s %f\n" % (word,tagList[k],probList[k]))
            output_file.write('\n')
            sent=""
        else:
            sent=sent+' '+line
        l = input_file.readline()
    pass


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

def main():
    #trigramTagger
    input=file("4_1.txt","r")
    tagList = initCount(input)
    input=file("ner_dev.dat","r")
    output=file("5_2.txt","w")
    trigramTagger(input,output,tagList)

if __name__ == "__main__":
    main()