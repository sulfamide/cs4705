Problem 4
4.1
run HW4_1.py and get ner_train.dat.rare_processed

4.2
run HW4_2.py
	 precision 	recall 		F1-Score
Total:	 0.221961	0.525544	0.312106
PER:	 0.435451	0.231230	0.302061
ORG:	 0.475936	0.399103	0.434146
LOC:	 0.147750	0.870229	0.252612
MISC:	 0.491689	0.610206	0.544574
	
The unigram method has reached total precision at 22%.I notice that precision of PER,ORG and MISC are much higher than the total, which means that for the words of those tags, they have high probability to get such tags regardless the context arround.


Problem 5
5.1
put the trigrams txt into the same file directory and run HW5_1.py.

5.2
put the 4_1.txt in the same file directory and run HW5_2.py 

The performance of model is followed.

Found 4707 NEs. Expected 5931 NEs; Correct: 3648
	 precision 	recall 		F1-Score
Total:	 0.775016	0.615073	0.685843
PER:     0.763231	0.596300	0.669517
ORG:	 0.611855	0.478326	0.536913
LOC:	 0.874658	0.696292	0.775349
MISC:	 0.830065	0.689468	0.753262

The ORG tag has the lowest precision and many ORG words are mistagged as PER and LOC.So we need more precise features to separate those init Capital words.
The F1-score is lower because the model give fewer NER tagging results than the correct answer.So the recall has a very low value.


Problem 6
I have 6 testing groups and I choose the best one which is ner_rare_group1_train.counts.
Simply run HW6.py since the file ner_rare_group1_train.counts is also in the file.


In the first time, I use the features which professor mentioned in class to group the rare words.The features are:
	if pos==0:
    	return 'firstWord'
	if word.islower():
    	return 'lowercase'
	if word[0].isupper():
    	return 'initCap'
In this case, the total precision is quite good:

	 precision 	recall 		F1-Score
Total:	 0.724461	0.730568	0.727502
PER:	 0.779946	0.782916	0.781428
ORG:	 0.521812	0.697309	0.596929
LOC:	 0.837531	0.725191	0.777323
MISC:	 0.830263	0.685125	0.750744
	
It’s surprising that such simple group method can arrive a better outcome.
Then I tried those features mentioned in the homework pdf, which are:

	if re.search(r'\d+\.{1}\d+',word):
    	return '_NUM_'
	elif re.search(r'\d+(-\d)+',word):
    	return '_NUM_'
	elif re.search(r'[A-Z]+[a-z]*\.{1}',word):
    	return '_ABBR_'
	elif re.search(r'[A-Z]+',word):
    	return '_ALLCAP_'
	else:
    	return '_RARE_'
	
The precision is almost the same as above.

	 precision 	recall 		F1-Score
Total:	 0.727584	0.715562	0.721523
PER:	 0.777293	0.774755	0.776022
ORG:	 0.520540	0.662930	0.583169
LOC:	 0.847204	0.710469	0.772835
MISC:	 0.830040	0.684039	0.750000


Then,I tried the numbers and abbreviations as the features.

	if not re.search(r'\w', word):
    	return '_PUNCS_'
	elif re.search(r'\d(\.\d)*', word):
    	return '_NUM_'
	elif re.search(r'[A-Z]+[a-z]*\.{1}', word):
    	return '_ABBR_'
	else:
    	return '_RARE_'

Found 4816 NEs. Expected 5931 NEs; Correct: 3763
	 precision 	recall 		F1-Score
Total:	 0.781354	0.634463	0.700288
PER:	 0.754557	0.630577	0.687018
ORG:	 0.658168	0.520927	0.581560
LOC:	 0.875000	0.694656	0.774468
MISC:	 0.827451	0.687296	0.750890

Since it’s lower, we know that the detailed grouping strategy do work and I need to go more detailedly with the words.

Finally, I try to go detailedly with the feature of the words,I decide to group the words into 6 groups, based on the ending part of a word.I tag words ending with ion/ics/ment as NOUNLIKE words and words ending with ble/bin/ious as JJLIKE words.

	if not re.search(r'\w', word):
    	return '_PUNCS_'
	elif re.search(r'[A-Z]{1}[a-z]+', word):
    	return '_CAPITAL_'
	elif re.search(r'\d', word):
    	return '_NUM_'
	elif re.search(r'(ion\b|ty\b|ics\b|ment\b|ence\b|ance\b|ness\b|ist\b|	ism\b)', 	word):
    	return '_NOUNLIKE_'
	elif re.search(r'(ate\b|fy\b|ize\b|\ben|\bem)', word):
    	return '_VERBLIKE_'
	elif re.search(r'(\bun|\bin|ble\b|ry\b|ish\b|ious\b|ical\b|\bnon)', 	word):
    	return '_JJLIKE_'
	else:
    	return '_RARE_'

As I wished, I got the highest precision.

	 precision 	recall 		F1-Score
Total:	 0.755785	0.715900	0.735302
PER:	 0.809040	0.779108	0.793792
ORG:	 0.557604	0.633034	0.592930
LOC:	 0.845321	0.724100	0.780029
MISC:	 0.843008	0.693811	0.761167

Consequently, the correct grouping strategy will improve the correction rate.Maybe if we use the Pos as features, the f1-score will be higher.


