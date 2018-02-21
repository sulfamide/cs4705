Part 1
The performance of part one on development data is:
Unlabeled attachment score 83.05
Labeled attachment score 79.84

Part 2
The performance of part two on development data is:
Unlabeled attachment score 83.46
Labeled attachment score 80.2
Since we add the number of hidden layers, now there are more hidden neurons which represents the features of input embedding.Thus, the model is optimizer than part one’s model.

Part 3 
I change the activation function by using Leaky-RELU than the original RELU.Also a dropout layer is added in the second layer.The arguments of training-model is as follows:
word_embed_size: 128
pos_embed_size: 64
label_embed_size: 64
batch_size: 1000
learning_rate: 0.0015
d_hidden1: 400
d_hidden2: 400
The performance of development data is:
Unlabeled attachment score 84.85
Labeled attachment score 81.4

The function dropout is a form of regularization, it avoids the network becoming too smart in learning the input data; it thus helps to avoid overfitting.
The function Leaky ReLU helps to fix the dying ReLU problem, it has a small negative slope for negative neurons.
Also I increase the features size of embedding so the model can have more feature for the input.


 
