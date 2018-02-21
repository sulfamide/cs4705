import argparse
import torch
import random
import torch.optim as O
from get_data import preProcess
from get_data import vocab_dict
from model import *
import glove

parser = argparse.ArgumentParser(description='train.py')

parser.add_argument('-config', help="Read options from this file")
parser.add_argument('-batch_size', type=int, default=1000,
                    help="Maximum batch size")
parser.add_argument('-word_embed_size', type=int, default=64,
                    help="Maximum batch size")
parser.add_argument('-pos_embed_size', type=int, default=32,
                    help="Maximum batch size")
parser.add_argument('-labels_embed_size', type=int, default=32,
                    help="Maximum batch size")
parser.add_argument('-lr', type=float, default=0.001,
                    help="Learning rate")
parser.add_argument('-d_hidden1', type=int, default=200,
                    help="Maximum batch size")
parser.add_argument('-d_hidden2', type=int, default=200,
                    help="Maximum batch size")
parser.add_argument('-log_every', type=int, default=10,
                    help="Log_every")
parser.add_argument('-dev_every', type=int, default=1,
                    help="Dev_every")
parser.add_argument('-clip', type=float, default=0.25)

opt = parser.parse_args()

def batchify(data):
    n_batch = len(data) // opt.batch_size

    batched_X, batched_Y = [], []
    for idx_batch in range(0, n_batch):
        # Batch
        X, Y = [], []
        tmp_data=data[idx_batch * opt.batch_size:(idx_batch + 1) * opt.batch_size]
        for sample in tmp_data:
            x = map(int,sample[0])
            y = int(sample[1])
            #print len(x)
            X.append(x)
            Y.append(y)
        batched_X.append(X)
        batched_Y.append(Y)
    return batched_X,batched_Y


train_data,dev_data=preProcess()
opt.word_size=len(vocab_dict['word'][0])
opt.pos_size=len(vocab_dict['pos'][0])
opt.labels_size=len(vocab_dict['labels'][0])
opt.d_input=20*opt.word_embed_size+20*opt.pos_embed_size+12*opt.labels_embed_size
opt.d_out=len(vocab_dict['actions'][0])

print 'out',opt.d_out,'input',opt.d_input
#print opt.word_size,opt.pos_size,opt.labels_size


[X, Y]=batchify(train_data)
[dev_X,dev_Y]=batchify(dev_data)
B=len(X)
d_B=len(dev_X)


model=Decoder(opt)
criterion=nn.CrossEntropyLoss()
optimizer=O.Adam(model.parameters(),lr=opt.lr)

num_epoch=7

for epoch in range(0,num_epoch):
    iterations=0
    n_correct,n_total=0,0
    seq=range(0,B)

    random.shuffle(seq)

    """
    if (epoch) % opt.dev_every == 0:
        dev_correct,dev_total=0,0
        for iter in range(0,d_B):
            d_x,d_y=dev_X[iter],dev_Y[iter]

            d_t_X = Variable(torch.LongTensor(d_x))
            d_t_Y = Variable(torch.LongTensor(d_y))

            d_answer=model(d_t_X)
            dev_correct += (torch.max(d_answer, 1)[1].view(d_t_Y.size()).data == d_t_Y.data).sum()
            dev_total += len(d_answer)

        print ('Epoch [%d/%d], Precision [%d/%d]'
               %(epoch+1, num_epoch,dev_correct,dev_total))
    """

    for iter in seq:
        x,y=X[iter],Y[iter]
        t_X= Variable(torch.LongTensor(x))
        t_Y= Variable(torch.LongTensor(y))

        model.train()
        model.zero_grad()

        answer=model(t_X)
        loss=criterion(answer,t_Y)
        loss.backward()
        torch.nn.utils.clip_grad_norm(model.parameters(), opt.clip)
        optimizer.step()

        #print torch.max(answer,1)[1].size()
        #print torch.max(answer,1)
        #print t_Y.size()
        n_correct += (torch.max(answer, 1)[1].data == t_Y.data).sum()
        n_total += len(answer)

        #print n_correct,n_total
        iterations+=1

        if (iterations+1) % opt.log_every == 0:
            print ('Epoch [%d/%d], Step [%d/%d], Loss: %.4f'
                   %(epoch+1, num_epoch, iterations+1, B, loss.data[0]))

    #print ('Epoch [%d/%d], Training Precision [%d/%d]'
    #       % (epoch + 1, num_epoch, n_correct, n_total))


#if torch.cuda.is_available():
#   torch.cuda.set_device(opt.gpu)
