from computeCounnts import trigramCount
from computeCounnts import bigramCount
from computeCounnts import initCount
import math

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


def compute(input,output):
    input_file=file(input,'r')
    output_file=file(output,'w')
    l = input_file.readline()
    while (l):
        line = l.strip()
        pTri=computePTri(line)
        output_file.write("%f \n" % (pTri))
        l = input_file.readline()


def main():
    input=file("4_1.txt","r")
    initCount(input)
    input='trigrams.txt'
    output='5_1.txt'
    compute(input,output)

if __name__ == "__main__":
    main()