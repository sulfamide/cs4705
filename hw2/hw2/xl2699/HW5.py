from __future__ import division
import json
import re

from count_cfg_freq import Counts
import numpy as np


class CKY:
    def __init__(self):
        self.binary_q={}
        self.unary_q={}
        self.counter=Counts()
        self.pi=[]
        self.bp=[]
        self.parser={}
        self.use_vert= False


    def loadData(self,corpus_file):

        l = corpus_file.readline()
        while(l):
            t = json.loads(l)
            self.counter.count(t)
            l = corpus_file.readline()


    def compute(self):
        for (sym,word),count in self.counter.unary.iteritems():
            self.unary_q[(sym,word)]=count/self.counter.nonterm[sym]
        for (sym, y1, y2),count in self.counter.binary.iteritems():
            self.binary_q[(sym,y1,y2)]=count/self.counter.nonterm[sym]

    def buildNTDict(self):
        self.binary_rule={}
        for x, y1, y2 in self.binary_q.keys():
            if x not in self.binary_rule.keys():
                self.binary_rule[x]=[]
            self.binary_rule[x].append((y1, y2))



    def cky_init(self,wordList):
        self.pi = []
        self.bp = []
        sent_len=len(wordList)
        for i in range(0,sent_len):
            self.pi.append([])
            self.bp.append([])
            for j in range(0,sent_len):
                self.pi[i].append({})
                self.bp[i].append({})
            for (sym,word),q in self.unary_q.iteritems():
                if wordList[i]==word:
                    self.pi[i][i][sym]=q
                    self.bp[i][i][sym]=word
        pass

    def clean_sent(self,sentence):
        wordList=sentence.split()
        vocabDict=[v for s,v in self.counter.unary.keys()]
        for i,word in enumerate(wordList):
            if word not in vocabDict:
                wordList[i]='_RARE_'
        return wordList

    def cky_algorithm(self,sentence):
        self.inputWordList=sentence.split()
        wordList=self.clean_sent(sentence)
        sent_len=len(wordList)
        self.cky_init(wordList)

        #print self.pi[10][10]


        for l in range(1,sent_len):
            for i in range(0,sent_len-l):
                j=i+l
                #print i,j
                for sym in self.binary_rule.keys():
                    for s in range(i, j):
                        derivations=self.binary_rule[sym]
                        for y1,y2 in derivations:
                            if y1 not in self.pi[i][s].keys() or y2 not in self.pi[s+1][j].keys():
                                #if i == 0 and j == 4 :
                                #print s,'t'
                                #if sym=='S' and y1=='NP' and y2=='S':
                                #    print sym,y1,y2
                                #    print s
                                #    print self.pi[0][1].keys()
                                #    print self.pi[2][4].keys()
                                #    print y1 in self.pi[i][s].keys()
                                #    print y2 in self.pi[s+1][j].keys()
                                #    print (sym,y1,y2) not in self.binary_q.keys()
                                #pass
                                continue
                            #print i,j

                            temp=self.binary_q.get((sym,y1,y2))*self.pi[i][s].get(y1)*self.pi[s+1][j].get(y2)
                            self.bp[i][j][sym] = (s, y1, y2) if temp > self.pi[i][j].get(sym, 0) else self.bp[i][j].get(sym, 0)
                            self.pi[i][j][sym]=max(temp,self.pi[i][j].get(sym,0))


        #print self.pi[1][sent_len-1]
        #print self.pi[0][0]
        #print self.binary_q['S','NP^<S>+NOUN','S']
        #print self.bp
        #try:
        if 'S' in self.pi[0][sent_len-1].keys():
            root_score= 'S',self.pi[0][sent_len-1]['S']
        else:
            root_score=max(self.pi[0][sent_len-1].iteritems(),key=lambda x:x[1])
        self.parse_res = self.buildTreeHelper(0,sent_len-1,root_score[0])#,self.parser
        #except:
        #    self.parse_res = "cannot parse unk"
        pass
        #print 'start',root_score


    def buildTreeHelper(self,start,end,root):
        if start==end:
            #self.parser[root]= self.bp[start][end][root]
            #t=self.bp[start][end][root]
            return '["'+root+'", "'+self.inputWordList[start]+'"]'
        else:
            s,y1,y2=self.bp[start][end][root]
            r1=self.buildTreeHelper(start,s,y1)
            r2=self.buildTreeHelper(s+1,end,y2)
            return ('["'+root+'", '+r1 + ', '+r2  +']')

    def dev(self,dev_file,output_file):
        output=file(output_file,'w')
        for l in open(dev_file):
            print l.strip()
            self.parse_res=""
            self.cky_algorithm(l.strip())
            if self.use_vert:
                new_parse_res = re.sub("\^\[[A-Z]+\]","", self.parse_res)
                self.parse_res = new_parse_res
            output.write(self.parse_res)
            output.write('\n')




cky_model=CKY()
input=file("HW4.txt","r")
cky_model.loadData(input)
cky_model.compute()
cky_model.buildNTDict()
#print len(cky_model.unary_q)
#print len(cky_model.counter.unary)
#sent='This time , the firms were ready .'
#sent='The complicated language in the huge new law has muddied the fight .'
#sent='ARNOLD ADVERTISING :'
#cky_model.cky_algorithm(sent)

#print cky_model.pi[0][2]
#print cky_model.parse_res
#s='["S", ["NP", ["NOUN", "Ms."], ["NOUN", "Haag"]], ["S", ["VP", ["VERB", "plays"], ["NP+NOUN", "Elianti"]], [".", "."]]]'

output='HW5.txt'
dev_corpus='parse_dev.dat'
cky_model.dev(dev_corpus,output)


