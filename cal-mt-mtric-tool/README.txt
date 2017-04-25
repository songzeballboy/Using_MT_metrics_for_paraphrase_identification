############################################
1. BLEU
I recommend you to use Python 2.x version
And you need install the NLTK modul for python

usage:
python BLEU.py input_file_path output_file_path

The InputFormat:
1 file
data_id sentence1 sentence2
The data is split by "\t" perline

The OutputFormat:
data_id BLEU1 BLEU2 BLEU3 BLEU4
The data is split by "," perline

############################################
2. NIST
I recommend you to use Python 2.x version
And you need install the NLTK modul for python

usage:
python NIST.py input_file_path output_file_path

The InputFormat:
1 file
data_id sentence1 sentence2
The data is split by "\t" perline

The OutputFormat:
data_id NIST1_score NIST2_score NIST3_score NIST4_score NIST5_score
The data is split by "," perline

############################################
2. TER
I recommend you to use Python 2.x version
And You also need install jre & jdk 1.8 version or later

The tool is based on https://github.com/jhclark/tercom

usage:
python 
sh getTERscore.sh ref_path hpy_path outpath

The InputFormat:
2 file:
	ref_sentence_file:
		ref_sentence_1
		ref_snetence_2
		.....
		ref_sentence_n

	hpy_sentence_file:
		hpy_sentence_1
		hpy_sentence_2
		.....
		hpy_sentence_n

The OutputFormat:
TER_score per line

