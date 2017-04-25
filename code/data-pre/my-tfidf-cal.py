#encoding=utf-8

import sys,os
import numpy as np
from sklearn import feature_extraction
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
import math

reload(sys)
sys.setdefaultencoding('utf8')

def cal_similarity(tfidfMat):
	sim_list = []
	for i in xrange(0,len(tfidfMat),2):
		j = i + 1
		_sc_1 = 0.0
		_sc_2 = 0.0
		_sc_3 = 0.0
		for p in range(len(tfidfMat[i])):
			_sc_1 += tfidfMat[i][p] * tfidfMat[j][p]
			_sc_2 += tfidfMat[i][p]**2
			_sc_3 += tfidfMat[j][p]**2
		_sc = _sc_1 / (math.sqrt(_sc_2) * math.sqrt(_sc_3))
		sim_list.append(_sc)
	return sim_list

def main(input_path,output_path):
	fp = open(input_path)
	fp_read = fp.readlines()
	fp.close()

	word_set = {}
	doc_contain = {}
	tf_list = []
	# cropus = []
	len_cropus = 0.0
	for i in range(len(fp_read)):
		if len(fp_read[i]) < 1:
			continue
		len_cropus += 1.0
		# cropus.append(fp_read[i].decode("utf-8"))
		word_ls = fp_read[i].decode("utf-8").replace('\r','').replace('\n','').split(" ")
		cur_wd_set = {}
		flag = True
		for wd in word_ls:
			if wd not in word_set.keys():
				word_set[wd] = 1
				doc_contain[wd] = 1.0
				flag = False
			else:
				if flag == True:
					doc_contain[wd] += 1.0
					flag = False

			if wd not in cur_wd_set.keys():
				cur_wd_set[wd] = 1.0
			else:
				cur_wd_set[wd] += 1.0

		per_len_doc = len(word_ls)
		for wd in cur_wd_set.keys():
			cur_wd_set[wd] = (cur_wd_set[wd] / per_len_doc)
		tf_list.append(cur_wd_set)

	# print word_set
	# print doc_contain
	# print tf_list

	idf_list = {}
	all_wd_ls = word_set.keys()
	wd_len = len(all_wd_ls)

	for wd in word_set.keys():
		idf_list[wd] = 1 + math.log(len_cropus / (doc_contain[wd] + 1) )
	
	# print idf_list

	tfidf_mat = []

	for cur_wd_set in tf_list:
		per_line_tfidf = []		
		for wd in all_wd_ls:
			if wd not in cur_wd_set.keys():
				per_line_tfidf.append(0.0)
			else:
				_sc = cur_wd_set[wd] * idf_list[wd]
				per_line_tfidf.append(_sc)

		tfidf_mat.append(per_line_tfidf)

	# print tfidf_mat
	ret = cal_similarity(tfidf_mat)
	# print ret
	fw = open(output_path,"w")
	for i in range(len(ret)):
		# print str(ret[i])
		fw.write(str(ret[i])+"\n")
	fw.close()

if __name__ == '__main__':
	input_path = sys.argv[1]
	output_path = sys.argv[2]

	main(input_path,output_path)

'''
吃 撑 了 应当 如何 缓解
吃 撑 到 了 怎么办
求 推荐 一款 男士 包
什么样 的 包 适合 IT 男 上班 用
'''
