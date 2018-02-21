from __future__ import division
import json
import re

from count_cfg_freq import Counts
from pretty_print_tree import pretty_print_tree


class CKY:
    def __init__(self):
        self.binary_q={}
        self.unary_q={}
        self.counter=Counts()
        self.counter_n=Counts()
        self.pi=[]
        self.bp=[]
        self.parser={}
        self.use_vert= False
        #0.95 curr best
        self.beta=0
        self.vm="\^\<[A-Z]+[+A-Z]*\>"
        self.vocab = {}

    def loadData(self,corpus_file):

        l = corpus_file.readline()
        while(l):
            t = json.loads(l)
            self.counter.count(t)
            wordList = [y for x, y in self.extract_tag(t)]
            for word in wordList:
                if word not in self.vocab:
                    self.vocab[word] = 0
                self.vocab[word] += 1

            l_n = re.sub(self.vm,"", l)
            t_n =json.loads(l_n)
            self.counter_n.count(t_n)
            l = corpus_file.readline()

    def extract_tag(self, t):
        if len(t) == 3:
            return self.extract_tag(t[1]) + self.extract_tag(t[2])
        if len(t) == 2:
            return [(t[0], t[1])]

    def compute(self):
        #discounting method
        self.unary_a={}
        self.unary_dict={}
        self.binary_a={}
        self.binary_dict={}

        for (sym,word),count in self.counter.unary.iteritems():
            #self.unary_q[(sym,word)]=count/self.counter.nonterm[sym]
            self.unary_q[(sym,word)]=(count-self.beta) / self.counter.nonterm[sym]

            #hyper_sym= re.sub(self.vm,"",sym)
            #if hyper_sym not in self.unary_dict:
            #    self.unary_dict[hyper_sym]=[]
            #self.unary_dict[hyper_sym].append(sym)

            #if sym not in self.unary_a.keys():
            #    self.unary_a[sym]=1
            #self.unary_a[sym] -= self.unary_q[sym,word]

        #for (sym,word),count in self.counter_n.unary.iteritems():
        #    for hypo in self.unary_dict[sym]:
        #        self.unary_q[(hypo,word)] = self.unary_a[hypo]*count/self.counter_n.nonterm[sym]

        for (sym, y1, y2),count in self.counter.binary.iteritems():
            self.binary_q[(sym,y1,y2)]= count/self.counter.nonterm[sym]

            #self.binary_q[(sym, y1, y2)] = (count-self.beta) / self.counter.nonterm[sym]
            #hyper_sym = re.sub(self.vm, "", sym)
            #if hyper_sym not in self.binary_dict:
            #    self.binary_dict[hyper_sym] = []
            #self.binary_dict[hyper_sym].append(sym)

            #if sym not in self.binary_a.keys():
            #    self.binary_a[sym] = 1
            #self.binary_a[sym] -= self.binary_q[(sym, y1, y2)]

        #for (sym, y1, y2), count in self.counter_n.binary.iteritems():
        #    for hypo in self.binary_dict[sym]:
        #        self.binary_q[(hypo,y1,y2)] = self.binary_a[hypo]*count/self.counter_n.nonterm[sym]


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
        #vocabDict=[v for s,v in self.counter.unary.keys()]
        for i,word in enumerate(wordList):
            if word not in self.vocab:
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
            #print start,end,root,self.bp[start][end][root]
            #print self.pi[0][end]
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
input=file("parse_rare_train_vert.dat","r")

cky_model.loadData(input)
cky_model.compute()
cky_model.buildNTDict()
output='HW6.txt'
dev_corpus='parse_dev.dat'
cky_model.dev(dev_corpus,output)


#print len(cky_model.binary_q.keys())


#sent='The above represents a triumph of either apathy or civility .'
#sent='Congress previously cut six airports this year .'
#sent='Average shares outstanding dropped to 75.8 million from 82.1 million .'
#cky_model.cky_algorithm(sent)
#print cky_model.parse_res


#my_res='["S", ["NP", ["DET", "The"], ["NP", ["NOUN", "_RARE_"], ["NOUN", "_RARE_"]]], ["S", ["NP", ["NP", ["DET", "a"], ["NOUN", "_RARE_"]], ["PP", ["ADP", "of"], ["ADVP+ADV", "either"]]], ["S", ["VP", ["VERB", "_RARE_"], ["ADJP", ["CONJ", "or"], ["ADJ", "_RARE_"]]], [".", "."]]]]'
#my_res_vert='["S", ["NP^<S>", ["DET", "The"], ["NOUN", "_RARE_"]], ["S", ["VP^<S>", ["VERB", "_RARE_"], ["VP", ["ADVP^<VP>", ["NP^<ADVP>", ["DET", "a"], ["NOUN", "_RARE_"]], ["ADP", "of"]], ["VP", ["ADVP^<VP>+ADV", "either"], ["ADJP^<VP>", ["ADJ", "_RARE_"], ["ADJP", ["CONJ", "or"], ["ADJ", "_RARE_"]]]]]], [".", "."]]]'
#ans='["S", ["NP", ["DET", "The"], ["ADJ", "above"]], ["S", ["VP", ["VERB", "represents"], ["NP", ["NP", ["DET", "a"], ["NOUN", "triumph"]], ["PP", ["ADP", "of"], ["NP", ["DET", "either"], ["NP", ["NOUN", "apathy"], ["NP", ["CONJ", "or"], ["NOUN", "civility"]]]]]]], [".", "."]]]'
#t='["S", ["ADVP+ADV", "Thus"], ["S", [".", ","], ["S", ["NP", ["ADJ", "higher"], ["NOUN", "bidding"]], ["S", ["NP", ["NOUN", "narrows"], ["NP", ["DET", "the"], ["NP", ["NOUN", "investor"], ["PRT", "s"]]]], ["S", ["NP", ["NP+NOUN", "return"], ["PP", ["ADP", "while"], ["NP", ["ADJ", "lower"], ["NOUN", "bidding"]]]], ["S", ["VP", ["VERB", "widens"], ["NP+PRON", "it"]], [".", "."]]]]]]]'
#ta='["S", ["ADVP+ADV", "Thus"], ["S", [".", ","], ["S", ["NP", ["ADJ", "higher"], ["NOUN", "bidding"]], ["S", ["VP", ["VERB", "narrows"], ["VP", ["NP", ["NP", ["DET", "the"], ["NP", ["NOUN", "investor"], ["PRT", "s"]]], ["NOUN", "return"]], ["SBAR", ["ADP", "while"], ["S", ["NP", ["ADJ", "lower"], ["NOUN", "bidding"]], ["VP", ["VERB", "widens"], ["NP+PRON", "it"]]]]]], [".", "."]]]]]'
#t_vert='["S", ["ADVP^<S>+ADV", "Thus"], ["S", [".", ","], ["S", ["NP^<S>", ["ADJ", "higher"], ["NOUN", "bidding"]], ["S", ["VP^<S>", ["VERB", "narrows"], ["VP", ["NP^<VP>", ["NP^<NP>", ["DET", "the"], ["NOUN", "investor"]], ["PP^<NP>", ["PRT", "s"], ["NP^<PP>+NOUN", "return"]]], ["SBAR^<VP>", ["ADP", "while"], ["S^<SBAR>", ["NP^<S>", ["ADJ", "lower"], ["NOUN", "bidding"]], ["VP^<S>", ["VERB", "widens"], ["NP^<VP>+PRON", "it"]]]]]], [".", "."]]]]]'
#pretty_print_tree(json.loads(ta))
#pretty_print_tree(json.loads(t_vert))
#pretty_print_tree(json.loads(t))