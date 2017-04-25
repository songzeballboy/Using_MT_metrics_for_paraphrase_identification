#coding=utf-8

import sys,os

def main(inpath1,inpath2,outpath):
	f_nist = open(inpath1)
	nist_list = []
	while 1:
		line = f_nist.readline()
		if not line:
			break
		nist_list.append(line)
	f_nist.close()

	f_bleu = open(inpath2)
	bleu_list = []
	while 1:
		line = f_bleu.readline()
		if not line:
			break
		bleu_list.append(line)
	f_bleu.close()

	f_w = open(outpath,"w")

	if len(bleu_list) != len(nist_list):
		print "error line is not the same"
		f_w.close()
		return -1
	
	for i in range(len(bleu_list)):
		line = nist_list[i].strip() + "," + bleu_list[i].strip()
		f_w.write(line+"\n")

	f_w.close()

	return 0

if __name__ == '__main__':
	inpath1 = sys.argv[1]
	inpath2 = sys.argv[2]
	outpath = sys.argv[3]
	main(inpath1,inpath2,outpath)
