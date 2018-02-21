Problem 4


Problem 5

      Type       Total   Precision      Recall     F1 Score
===============================================================
         .         370     1.000        1.000        1.000
       ADJ         164     0.827        0.555        0.664
      ADJP          29     0.333        0.241        0.280
  ADJP+ADJ          22     0.542        0.591        0.565
       ADP         204     0.955        0.946        0.951
       ADV          64     0.694        0.531        0.602
      ADVP          30     0.333        0.133        0.190
  ADVP+ADV          53     0.756        0.642        0.694
      CONJ          53     1.000        1.000        1.000
       DET         167     0.988        0.976        0.982
      NOUN         671     0.753        0.842        0.795
        NP         884     0.627        0.525        0.571
    NP+ADJ           2     0.286        1.000        0.444
    NP+DET          21     0.783        0.857        0.818
   NP+NOUN         131     0.641        0.573        0.605
    NP+NUM          13     0.214        0.231        0.222
   NP+PRON          50     0.980        0.980        0.980
     NP+QP          11     0.750        0.273        0.400
       NUM          93     0.984        0.656        0.787
        PP         208     0.597        0.635        0.615
      PRON          14     1.000        0.929        0.963
       PRT          45     0.957        0.978        0.967
   PRT+PRT           2     0.400        1.000        0.571
        QP          26     0.647        0.423        0.512
         S         587     0.626        0.782        0.695
      SBAR          25     0.091        0.040        0.056
      VERB         283     0.683        0.799        0.736
        VP         399     0.559        0.594        0.576
   VP+VERB          15     0.250        0.267        0.258

     total        4664     0.714        0.714        0.714

I do some preprocess by building a derivation rules dict which significantly reduce the running time.This cky model is very robust in parsing NOUN,VERB,DET,PRON and it get relatively much lower correction rate with SBAR and ADVP.

Problem 6

      Type       Total   Precision      Recall     F1 Score
===============================================================
         .         370     1.000        1.000        1.000
       ADJ         164     0.689        0.622        0.654
      ADJP          29     0.324        0.414        0.364
  ADJP+ADJ          22     0.591        0.591        0.591
       ADP         204     0.960        0.951        0.956
       ADV          64     0.759        0.641        0.695
      ADVP          30     0.417        0.167        0.238
  ADVP+ADV          53     0.700        0.660        0.680
      CONJ          53     1.000        1.000        1.000
       DET         167     0.988        0.994        0.991
      NOUN         671     0.797        0.851        0.823
        NP         884     0.618        0.550        0.582
    NP+ADJ           2     0.333        0.500        0.400
    NP+DET          21     0.944        0.810        0.872
   NP+NOUN         131     0.610        0.656        0.632
    NP+NUM          13     0.375        0.231        0.286
   NP+PRON          50     0.980        0.980        0.980
     NP+QP          11     0.800        0.364        0.500
       NUM          93     0.970        0.699        0.812
        PP         208     0.623        0.635        0.629
      PRON          14     1.000        0.929        0.963
       PRT          45     1.000        0.933        0.966
   PRT+PRT           2     0.286        1.000        0.444
        QP          26     0.722        0.500        0.591
         S         587     0.704        0.814        0.755
      SBAR          25     0.667        0.400        0.500
      VERB         283     0.790        0.813        0.801
        VP         399     0.663        0.677        0.670
   VP+VERB          15     0.294        0.333        0.312

     total        4664     0.744        0.744        0.744


We can see significant improvement from Question 5 to Question 6 due to vertical markovization. Compared with problem 5, the F1 score of SBAR increase from 5.6% to 50.0%.The bad thing is that the running time doubles since there are 1576 non terminals now while there are only 876 NTs in the simple CKY.


Take sentence No.144 in dev_set as an example:
Thus , higher bidding narrows the investor 's return while lower bidding widens it .

Gold Standard
[S,
 [ADVP+ADV, Thus],
 [S,
  [., ,],
  [S,
   [NP, [ADJ, higher], [NOUN, bidding]],
   [S,
    [VP,
     [VERB, narrows],
     [VP,
      [NP,
       [NP, [DET, the], [NP, [NOUN, investor], [PRT, s]]],
       [NOUN, return]],
      [SBAR,
       [ADP, while],
       [S,
        [NP, [ADJ, lower], [NOUN, bidding]],
        [VP, [VERB, widens], [NP+PRON, it]]]]]],
    [., .]]]]]

CKY with vertical markovization
[S,
 [ADVP^<S>+ADV, Thus],
 [S,
  [., ,],
  [S,
   [NP^<S>, [ADJ, higher], [NOUN, bidding]],
   [S,
    [VP^<S>,
     [VERB, narrows],
     [VP,
      [NP^<VP>,
       [NP^<NP>, [DET, the], [NOUN, investor]],
       [PP^<NP>, [PRT, s], [NP^<PP>+NOUN, return]]],
      [SBAR^<VP>,
       [ADP, while],
       [S^<SBAR>,
        [NP^<S>, [ADJ, lower], [NOUN, bidding]],
        [VP^<S>, [VERB, widens], [NP^<VP>+PRON, it]]]]]],
    [., .]]]]]

Simple CKY
[S,
 [ADVP+ADV, Thus],
 [S,
  [., ,],
  [S,
   [NP, [ADJ, higher], [NOUN, bidding]],
   [S,
    [NP,
     [NOUN, narrows],
     [NP, [DET, the], [NP, [NOUN, investor], [PRT, s]]]],
    [S,
     [NP,
      [NP+NOUN, return],
      [PP, [ADP, while], [NP, [ADJ, lower], [NOUN, bidding]]]],
     [S, [VP, [VERB, widens], [NP+PRON, it]], [., .]]]]]]]


The simple CKY doesn’t recognize the SBAR at all while vm-CKY do.Also,the simple CKY misunderstood the word narrows and the part of speech after it. Generally,NP can be the subject or the object, and it’s more likely to be a subject if it’s under a VP, or an object when it’s under an S.By using Markovization,we have more contexts when parsing and the parser knows that ‘the investor’ is an object rather than a subject.


