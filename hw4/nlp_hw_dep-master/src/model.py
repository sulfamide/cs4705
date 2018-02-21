import torch
import torch.nn as nn
from torch.autograd import Variable
import torch.nn.functional as F
import torch.nn.init as init

class Decoder(nn.Module):
    def __init__(self, opt):
        super(Decoder, self).__init__()
        self.opt=opt
        self.embedding_w=nn.Embedding(opt.word_size, opt.word_embed_size)
        self.embedding_p=nn.Embedding(opt.pos_size,opt.pos_embed_size)
        self.embedding_l=nn.Embedding(opt.labels_size,opt.labels_embed_size)
        self.dropout = nn.Dropout(0.2)
        self.relu = nn.ReLU()
        self.leaky_relu = nn.LeakyReLU()
        self.hid1=nn.Linear(opt.d_input,opt.d_hidden1)
        self.hid2= nn.Linear(opt.d_hidden1, opt.d_hidden2)
        self.out=nn.Linear(opt.d_hidden2, opt.d_out)
        self.init_weights()



    def init_weights(self):
        self.embedding_w.weight.data.uniform_(-0.1, 0.1)
        self.embedding_p.weight.data.uniform_(-0.1, 0.1)
        self.embedding_l.weight.data.uniform_(-0.1, 0.1)

        self.hid1.bias.data.fill_(0)
        self.hid1.weight.data.uniform_(-0.1, 0.1)
        self.hid2.bias.data.fill_(0)
        self.hid2.weight.data.uniform_(-0.1, 0.1)
        self.out.bias.data.fill_(0)
        self.out.weight.data.uniform_(-0.1, 0.1)

        # leaky+dropout dev3 uniform

        #init.xavier_uniform(self.hid1.weight)
        #init.xavier_uniform(self.hid2.weight)
        #init.kaiming_normal(self.out.weight, mode='fan_in')


    def forward(self,input):
        embed_w=self.embedding_w(input[:,0:20]).view(input.size(0),-1)
        embed_p=self.embedding_p(input[:,20:40]).view(input.size(0),-1)
        embed_l=self.embedding_l(input[:,40:52]).view(input.size(0),-1)

        #print embed_w.size()
        #print embed_p.size()
        #print embed_l.size()

        embed=torch.cat((embed_w,embed_p,embed_l),1)

        hidden1=self.hid1(embed)
        hidden1=self.relu(hidden1)
        hidden2=self.hid2(hidden1)
        hidden2=self.relu(hidden2)

        #hidden1 = self.leaky_relu(self.hid1(embed))
        #hidden2 = self.leaky_relu(self.hid2(self.dropout(hidden1)))

        out=self.out(hidden2)

        return out