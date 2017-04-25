#encoding=utf-8

import os,sys
from nltk.util import ngrams
import math
import nltk
reload(sys)
sys.setdefaultencoding('utf-8')

def _getBLEU_Score(reference_list,hypothesis):
	return

def _getNIST_Score(reference_list,hypothesis):
	'''
	get feature for NIST1 to NIST5
	'''	

	obj_op = nltk.translate.bleu_score
	chencherry = nltk.translate.bleu_score.SmoothingFunction()

	# get NIST1 feature
	weights = [1,0,0,0,0]
	val1 = obj_op.sentence_bleu(reference_list, hypothesis,weights,smoothing_function=chencherry.method3)

	# get NIST2 feature
	weights = [0,1,0,0,0]
	val2 = obj_op.sentence_bleu(reference_list, hypothesis,weights,smoothing_function=chencherry.method3)

	# get NIST3 feature
	weights = [0,0,1,0,0]
	val3 = obj_op.sentence_bleu(reference_list, hypothesis,weights,smoothing_function=chencherry.method3)

	# get NIST4 feature
	weights = [0,0,0,1,0]
	val4 = obj_op.sentence_bleu(reference_list, hypothesis,weights,smoothing_function=chencherry.method3)

	# get NIST5 feature
	weights = [0,0,0,0,1]
	val5 = obj_op.sentence_bleu(reference_list, hypothesis,weights,smoothing_function=chencherry.method3)

	return val1,val2,val3,val4,val5

def _getTER_Score(reference_list,hypothesis):

	return

def _getTERp_Score(reference_list,hypothesis):

	return

def _getMETEOR_Score(reference_list,hypothesis):

	return

def _getSEPIA_Score(reference_list,hypothesis):

	return

def  _getBADGER_Score(reference_list,hypothesis):
	
	return

def _getMAXSIM_Score(reference_list,hypothesis):

	return

def _getFeature_Sentence(reference_list,hypothesis):
	feature_ret = []

	# get the BLEU features
	# BLEU1,BLEU2,BLEU3,BLEU4 = _getBLEU_Score(reference_list,hypothesis)
	# feature_ret.append(BLEU1)
	# feature_ret.append(BLEU2)
	# feature_ret.append(BLEU3)
	# feature_ret.append(BLEU4)

	NIST1,NIST2,NIST3,NIST4,NIST5 = _getNIST_Score(reference_list,hypothesis)
	feature_ret.append(NIST1)
	feature_ret.append(NIST2)
	feature_ret.append(NIST3)
	feature_ret.append(NIST4)
	feature_ret.append(NIST5)

	# TER_Score = _getTER_Score(reference_list,hypothesis)
	# feature_ret.append(TER_Score)

	# TERp_Socre = _getTERp_Score(reference_list,hypothesis)
	# feature_ret.append(TERp_Socre)

	# METEOR_Score = _getMETEOR_Score(reference_list,hypothesis)
	# feature_ret.append(METEOR_Score)

	# SEPIA_Score = _getSEPIA_Score(reference_list,hypothesis)
	# feature_ret.append(SEPIA_Score)

	# BADGER_Score = _getBADGER_Score(reference_list,hypothesis)
	# feature_ret.append(BADGER_Score)

	# MAXSIM_Score = _getMAXSIM_Score(reference_list,hypothesis)
	# feature_ret.append(MAXSIM_Score)

	return feature_ret

def deal_with_perSentence(reference_list,hypothesis):
	fea_sentence = _getFeature_Sentence(reference_list,hypothesis)

	toWrite = str(fea_sentence[0])
	for i in range(1,len(fea_sentence)):
		toWrite = toWrite + "," + str(fea_sentence[i])
	return toWrite

def main(IN,OUT):
	fr = open(IN)
	fw = open(OUT,"w")

	allread = fr.readlines()

	for line in allread:
		fields = line.replace('\n','').split("\t")
		
		if(len(fields) != 3) :
			continue
		data_label = fields[0]
		data_reference = fields[2]
		data_hypothesis = fields[1]

		L_reference = data_reference.replace(',','').replace('.','').replace('"','').replace(':','').split(' ')
		L_hypothesis = data_hypothesis.replace(',','').replace('.','').replace('"','').replace(':','').split(' ')

		hypothesis = L_hypothesis
		reference = L_reference
		reference_list = [reference]

		fea_format = deal_with_perSentence(reference_list,hypothesis)
		toWrite = fea_format + "," + data_label
		# print toWrite
		fw.write(toWrite+"\n")

	fr.close()
	fw.close()

if __name__ == '__main__':
	IN = sys.argv[1]
	OUT = sys.argv[2]
	main(IN,OUT)