
from HW5_2 import viterbiAlgorithm
from HW4_2 import tagger
from computeCounnts import tagArr
from computeCounnts import initCount
import re


def subcategorize(word):

    if not re.search(r'\w', word):
        return '_PUNCS_'
    #elif re.search(r'[A-Z]{1}[a-z]+', word):
    #    return '_CAPITAL_'
    elif re.search(r'\d(\.\d)*', word):
        return '_NUM_'
    elif re.search(r'[A-Z]+[a-z]*\.{1}', word):
        return '_ABBR_'
    #elif re.search(r'\w+\d+',word):
    #    return '_CODE_'
    elif re.search(r'(ion\b|ty\b|ics\b|ment\b|ence\b|ance\b|ness\b|ist\b|ism\b)', word):
        return '_NOUNLIKE_'
    elif re.search(r'(ate\b|fy\b|ize\b|\ben|\bem)', word):
        return '_VERBLIKE_'
    elif re.search(r'(\bun|\bin|ble\b|ry\b|ish\b|ious\b|ical\b|\bnon)', word):
        return '_JJLIKE_'
    else:
        return '_RARE_'

    """
    if re.search(r'\d+\.{1}\d+',word):
        return '_NUM_'
    elif re.search(r'\d+(-\d)+',word):
        return '_NUM_'
    elif re.search(r'[A-Z]+[a-z]*\.{1}',word):
        return '_ABBR_'
    elif re.search(r'[A-Z]+',word):
        return '_ALLCAP_'
    else:
        return '_RARE_'
    
    """

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
                word = subcategorize(wordList[0])
            bos=1
            output_file.write("%s %s\n" % (word,wordList[1]))
        else:
            bos=0
            pass
            output_file.write(l+"\n")

def cleanSent(sent,type):
    wordList=sent.strip().split();
    sentence=''
    for k,word in enumerate(wordList):
        #word=classifyRareWord(word,k)
        if word not in tagArr:
            if type==1:
                word="_RARE_"
            else:
                word=subcategorize(word)
        sentence=sentence+' '+word
    return sentence.strip()



def trigramTagger(input_file, output_file, tagSet, type):
    l = input_file.readline()
    sent = ""
    while (l):
        line = l.strip()
        if len(line) <= 0:
            # do tagging
            cleanedSent = cleanSent(sent, type)
            # print sent
            if len(sent.split()) >= 2:
                probList, tagList = viterbiAlgorithm(cleanedSent, tagSet)
            else:
                cmax, tag = tagger(cleanedSent)
                tagList = [tag]
            for k, word in enumerate(sent.split()):
                output_file.write("%s %s %f\n" % (word, tagList[k], probList[k]))
            output_file.write('\n')
            sent = ""
        else:
            sent = sent + ' ' + line
        l = input_file.readline()
    pass




#input=file("ner_train.dat","r")
#output=file("ner_srare_train.dat","w")
#output=file("ner_rare_train.dat","w")
#output=file("ner_rare_group7_train.dat","w")
#rareTagger(input,output)
def main():
    input = file("ner_rare_group1_train.counts", "r")
    tagList = initCount(input)
    input = file("ner_dev.dat", "r")
    output = file("6.txt", "w")
    trigramTagger(input, output, tagList, 2)



if __name__ == "__main__":
    main()
    #pass
#trigramTagger
