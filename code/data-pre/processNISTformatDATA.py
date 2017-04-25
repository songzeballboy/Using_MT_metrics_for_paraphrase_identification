#coding=utf-8

import sys,os
reload(sys)
sys.setdefaultencoding('utf-8')

def main(ref_path,hpy_path):
	f_ref = open(ref_path,"w")
	f_hpy = open(hpy_path,"w")

	for line in sys.stdin:
		fields = line.replace('\n','').replace('\r','').decode("utf-8").split("\t")
		
		if(len(fields) != 3) :
			continue
		data_label = fields[0]
		data_reference = fields[2]
		data_hypothesis = fields[1]

		L_reference = data_reference.replace(',','').replace('.','').replace('"','').replace(':','')
		L_hypothesis = data_hypothesis.replace(',','').replace('.','').replace('"','').replace(':','')

		hypothesis = L_hypothesis.encode("utf-8")
		reference = L_reference.encode("utf-8")
		
		f_ref.write(reference+"\n")
		f_hpy.write(hypothesis+"\n")

	f_ref.close()
	f_hpy.close()
	return 0

if __name__ == '__main__':
	ref_path = sys.argv[1]
	hpy_path = sys.argv[2]
	main(ref_path,hpy_path)
