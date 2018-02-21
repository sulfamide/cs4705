import os,sys
from decoder import *
import train
import torch
from torch.autograd import Variable

class DepModel:
    def __init__(self,model,dict):
        '''
            You can add more arguments for examples actions and model paths.
            You need to load your model here.
            actions: provides indices for actions.
            it has the same order as the data/vocabs.actions file.
        '''
        # if you prefer to have your own index for actions, change this.
        self.actions = ['SHIFT', 'LEFT-ARC:rroot', 'LEFT-ARC:cc', 'LEFT-ARC:number', 'LEFT-ARC:ccomp', 'LEFT-ARC:possessive', 'LEFT-ARC:prt', 'LEFT-ARC:num', 'LEFT-ARC:nsubjpass', 'LEFT-ARC:csubj', 'LEFT-ARC:conj', 'LEFT-ARC:dobj', 'LEFT-ARC:nn', 'LEFT-ARC:neg', 'LEFT-ARC:discourse', 'LEFT-ARC:mark', 'LEFT-ARC:auxpass', 'LEFT-ARC:infmod', 'LEFT-ARC:mwe', 'LEFT-ARC:advcl', 'LEFT-ARC:aux', 'LEFT-ARC:prep', 'LEFT-ARC:parataxis', 'LEFT-ARC:nsubj', 'LEFT-ARC:<null>', 'LEFT-ARC:rcmod', 'LEFT-ARC:advmod', 'LEFT-ARC:punct', 'LEFT-ARC:quantmod', 'LEFT-ARC:tmod', 'LEFT-ARC:acomp', 'LEFT-ARC:pcomp', 'LEFT-ARC:poss', 'LEFT-ARC:npadvmod', 'LEFT-ARC:xcomp', 'LEFT-ARC:cop', 'LEFT-ARC:partmod', 'LEFT-ARC:dep', 'LEFT-ARC:appos', 'LEFT-ARC:det', 'LEFT-ARC:amod', 'LEFT-ARC:pobj', 'LEFT-ARC:iobj', 'LEFT-ARC:expl', 'LEFT-ARC:predet', 'LEFT-ARC:preconj', 'LEFT-ARC:root', 'RIGHT-ARC:rroot', 'RIGHT-ARC:cc', 'RIGHT-ARC:number', 'RIGHT-ARC:ccomp', 'RIGHT-ARC:possessive', 'RIGHT-ARC:prt', 'RIGHT-ARC:num', 'RIGHT-ARC:nsubjpass', 'RIGHT-ARC:csubj', 'RIGHT-ARC:conj', 'RIGHT-ARC:dobj', 'RIGHT-ARC:nn', 'RIGHT-ARC:neg', 'RIGHT-ARC:discourse', 'RIGHT-ARC:mark', 'RIGHT-ARC:auxpass', 'RIGHT-ARC:infmod', 'RIGHT-ARC:mwe', 'RIGHT-ARC:advcl', 'RIGHT-ARC:aux', 'RIGHT-ARC:prep', 'RIGHT-ARC:parataxis', 'RIGHT-ARC:nsubj', 'RIGHT-ARC:<null>', 'RIGHT-ARC:rcmod', 'RIGHT-ARC:advmod', 'RIGHT-ARC:punct', 'RIGHT-ARC:quantmod', 'RIGHT-ARC:tmod', 'RIGHT-ARC:acomp', 'RIGHT-ARC:pcomp', 'RIGHT-ARC:poss', 'RIGHT-ARC:npadvmod', 'RIGHT-ARC:xcomp', 'RIGHT-ARC:cop', 'RIGHT-ARC:partmod', 'RIGHT-ARC:dep', 'RIGHT-ARC:appos', 'RIGHT-ARC:det', 'RIGHT-ARC:amod', 'RIGHT-ARC:pobj', 'RIGHT-ARC:iobj', 'RIGHT-ARC:expl', 'RIGHT-ARC:predet', 'RIGHT-ARC:preconj', 'RIGHT-ARC:root']
        self.model = model
        self.dict = dict
        # write your code here for additional parameters.
        # feel free to add more arguments to the initializer.

    def score(self, str_features):
        '''
        :param str_features: String features
        20 first: words, next 20: pos, next 12: dependency labels.
        DO NOT ADD ANY ARGUMENTS TO THIS FUNCTION.
        :return: list of scores
        '''
        # change this part of the code.
        feature=[]
        for i in range(0,20):
            if str_features[i] not in dict['word'][0]:
                feature.append(dict['word'][0]['<unk>'])
            else:
                feature.append(dict['word'][0][str_features[i]])
        for i in range(20, 40):
            if str_features[i] not in dict['pos'][0]:
                feature.append(dict['pos'][0]['<null>'])
            else:
                feature.append(dict['pos'][0][str_features[i]])
        for i in range(40, 52):
            if str_features[i] not in dict['labels'][0]:
                feature.append(dict['labels'][0]['<null>'])
            else:
                feature.append(dict['labels'][0][str_features[i]])
        feature = map(int,feature)
        feature = Variable(torch.LongTensor(feature).unsqueeze(0))
        scores = model(feature)
        scores = scores.data.numpy()
        #print scores
        return scores

if __name__=='__main__':
    model = train.model
    dict = train.vocab_dict
    m = DepModel(model,dict)
    input_p = "../trees/dev.conll"
    output_p = "../outputs/dev.out"
    #input_p = os.path.abspath(sys.argv[1])
    #output_p = os.path.abspath(sys.argv[2])


    Decoder(m.score, m.actions).parse(input_p, output_p)