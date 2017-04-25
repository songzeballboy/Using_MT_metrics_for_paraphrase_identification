#encoding=utf-8

import sys,os
import numpy as np
from sklearn import feature_extraction
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
import math

reload(sys)
sys.setdefaultencoding('utf8')

def main(input_path,output_path):
	# cropus = ["Amrozi accused his brother whom he called the witness of deliberately distorting his evidence",
	# "Yucaipa owned Dominick's before selling the chain to Safeway in 1998 for $25 billion",
	# "They had published an advertisement on the Internet on June 10 offering the cargo for sale he added"
	# ]

	# fp = open("../ETL-data/chineseData/tfidf-format-ch.dat")
	fp = open(input_path)
	fp_read = fp.readlines()

	fp.close()
	cropus = []
	for i in range(len(fp_read)):
		if len(fp_read[i]) < 1:
			continue
		cropus.append(fp_read[i].decode("utf-8"))

	# vectorizer = CountVectorizer(stop_words=None)
	tfidf_vectorizer = TfidfVectorizer(stop_words=None)
	transformer = TfidfTransformer()
	# tfidf = transformer.fit_transform(vectorizer.fit_transform(cropus))
	tfidf = transformer.fit_transform(tfidf_vectorizer.fit_transform(cropus))
	# word = tfidf_vectorizer.get_feature_names()
	# word = vectorizer.get_feature_names()

	# for wd in word:
	# 	print wd.encode("utf-8")
	# print str(word)
	# print str(tfidf.toarray())

	simMatrix = (tfidf * tfidf.T).A

	# print str(simMatrix)

	ret = []

	fea_len = len(tfidf.toarray())
	for i in xrange(0,fea_len,2):
		# print str(simMatrix[i,i+1])
		ret.append(simMatrix[i,i+1])

	# fw = open("../feature/chineseData/tfidf-ch.fea","w")
	fw = open(output_path,"w")
	for i in range(len(ret)):
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