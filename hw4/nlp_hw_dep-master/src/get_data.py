import argparse

parser = argparse.ArgumentParser(description='get_data.py')

parser.add_argument('-config', help="Read options from this file")
parser.add_argument('-train_src', type=str, default='../data/train.data',
                    help="Path to the training source data")
parser.add_argument('-dev_src', type=str, default='../data/dev.data',
                    help="Path to the validation source data")

parser.add_argument('-train_dict', type=str, default='../data/vocabs.',
                    help="Path to the validation source data")

parser.add_argument('-dev_dict', type=str, default='../data/dev_vocabs.',
                    help="Path to the validation dict")


opt = parser.parse_args()
vocab_dict = {}
dev_vocab_dict = {}
def readDict(filename):
        dict={}
        idx={}
        dict_file=file(filename,'r')
        l = dict_file.readline()
        while (l):
            key,val=l.split(' ')
            dict[key]=val
            idx[val]=key
            l = dict_file.readline()
        return dict,idx

def getData(filename,dict):
    data_set=[]
    data_file=file(filename,'r')
    l = data_file.readline()
    while(l):
        l=l.replace('\n','')
        word_list=l.split(' ')
        _data=[]

        for i in range(0,20):
            if word_list[i] not in dict['word'][0]:
                _data.append(dict['word'][0]['<unk>'])
            else:
                _data.append(dict['word'][0][word_list[i]])
        for i in range(20,40):
            try:
                _data.append(dict['pos'][0][word_list[i]])
            except:
                print word_list
        for i in range(40,52):
            _data.append(dict['labels'][0][word_list[i]])
        _label=dict['actions'][0][word_list[-1]]

        data_set.append((_data,_label))
        l=data_file.readline()
    return data_set

def loadDict(dict,path):
    dict['actions'] = readDict(path + 'actions')
    dict['labels'] = readDict(path + 'labels')
    dict['pos'] = readDict(path + 'pos')
    dict['word'] = readDict(path + 'word')
    return dict

def preProcess():

    print('Loading dict')
    loadDict(vocab_dict,opt.train_dict)
    #loadDict(dev_vocab_dict,opt.dev_dict)

    print('Preparing training ...')
    train_data=getData(opt.train_src,vocab_dict)

    print('Preparing validation ...')
    #valid_data=getData(opt.dev_src,dev_vocab_dict)
    #valid_data = getData(opt.dev_src, vocab_dict)
    valid_data=[]
    return train_data,valid_data

def word2idx():
    pass

def idx2word():
    pass
