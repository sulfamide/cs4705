

def classifyRareWord(word,pos):
    if pos==0:
        return 'firstWord'
    if word.islower():
        return 'lowercase'
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
                word='_RARE_'
            bos=1
            output_file.write("%s %s\n" % (word,wordList[1]))
        else:
            bos=0
            pass
            output_file.write(l+"\n")

    #print len(wordCount)

def main():
    # do rare
    input=file("ner_train.dat","r")
    #output=file("ner_srare_train.dat","w")
    output=file("ner_train.dat.rare_processed","w")
    rareTagger(input,output)

if __name__ == "__main__":
    main()


