from computeCounnts import tagArr,tagSumArr
from computeCounnts import initCount
import math


def computeEmission(str,tag):
    if not tagArr.has_key(str):
        return 0
    if not tagArr[str].has_key(tag):
        return 0
    tagCount=tagArr[str][tag]
    emi=float(tagCount)/(tagSumArr[tag])
    #emi=math.log(emi,2)
    return emi

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

def main():
    #test dev
    input = file("4_1.txt", "r")
    initCount(input)
    input=file("ner_dev.dat","r")
    output=file("4_2.txt","w")
    tagDev(input,output)

if __name__ == "__main__":
    main()