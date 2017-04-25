#coding=utf-8

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def getScoreInfo(base_path,LR_score_path,SVM_score_path,out_path):
	fp_LR_score = open(LR_score_path)
	fp_SVM_score = open(SVM_score_path)
	fp_base_info = open(base_path)
	fw = open(out_path,"w")

	LR_sc_ls = fp_LR_score.readlines()
	SVM_sc_ls = fp_SVM_score.readlines()
	base_info_ls = fp_base_info.readlines()

	fp_LR_score.close()
	fp_SVM_score.close()
	fp_base_info.close()

	if len(LR_sc_ls) != len(SVM_sc_ls) or len(base_info_ls) != len(LR_sc_ls) :
		print "#2 error"
		fw.close()
		return -1

	for i in range(len(LR_sc_ls)):
		base_info = base_info_ls[i].replace('\n','').replace('\r','').decode("utf-8")
		LR_sc = LR_sc_ls[i].replace('\n','').replace('\r','').decode("utf-8")
		SVM_sc = SVM_sc_ls[i].replace('\n','').replace('\r','').decode("utf-8")

		OFS = "\t"
		toWrite = base_info + OFS + LR_sc + OFS + SVM_sc
		fw.write(toWrite.encode("utf-8")+"\n")

	fw.close()
	return 0

def getBaseInfo(original_data_path,seg_data_path,out_path):
	fp_original_data = open(original_data_path)
	fp_seg_data =open(seg_data_path)
	fw = open(out_path,"w")

	original_data_ls = fp_original_data.readlines()
	seg_data_ls = fp_seg_data.readlines()
	
	fp_original_data.close()
	fp_seg_data.close()


	if len(original_data_ls) != len(seg_data_ls):
		print "#1 error"
		fw.close()
		return -1

	for i in range(len(original_data_ls)):
		original_data = original_data_ls[i].replace('\n','').replace('\r','').decode("utf-8")
		seg_data = seg_data_ls[i].replace('\n','').replace('\r','').decode("utf-8")

		feilds = original_data.split("\t")
		_hpy = feilds[1]
		_ref = feilds[2]
		label = feilds[0]

		seg_feilds = seg_data.split("\t")
		_seg_hpy = seg_feilds[1]
		_seg_ref = seg_feilds[2]

		OFS = "\t"
		toWrite = _hpy + OFS + _ref + OFS + _seg_hpy + OFS + _seg_ref + OFS + label
		fw.write(toWrite.encode("utf-8")+"\n")

	fw.close()
	return 0

def deal_train_set():
	original_data_path = "../ETL-data/newQuora/out.train.dat"
	seg_data_path = "../ETL-data/newQuora/out.train.dat"
	base_tmp_out_path = "../debug-info/newQuora/train-info.dat"

	LR_score_path_list = [
				"../result/newQuora/bleu.LR.train",
				"../result/newQuora/nist.LR.train",
				"../result/newQuora/ter.LR.train",
				"../result/newQuora/nist-bleu.LR.train",
				"../result/newQuora/ter-nist-bleu.LR.train",
				"../result/newQuora/tfidf.LR.train"
	]
	SVM_score_path_list = [
				"../result/newQuora/bleu.SVM.train",
				"../result/newQuora/nist.SVM.train",
				"../result/newQuora/ter.SVM.train",
				"../result/newQuora/nist-bleu.SVM.train",
				"../result/newQuora/ter-nist-bleu.SVM.train",
				"../result/newQuora/tfidf.SVM.train"
	]
	final_out_path_list = [
				"../debug-info/newQuora/bleu.LR.train",
				"../debug-info/newQuora/nist.LR.train",
				"../debug-info/newQuora/ter.LR.train",
				"../debug-info/newQuora/nist-bleu.LR.train",
				"../debug-info/newQuora/ter-nist-bleu.LR.train",
				"../debug-info/newQuora/tfidf.LR.train"
	]
	
	getBaseInfo(original_data_path,seg_data_path,base_tmp_out_path)

	for i in range(len(LR_score_path_list)):
		LR_score_path = LR_score_path_list[i]
		SVM_score_path = SVM_score_path_list[i]
		final_out_path = final_out_path_list[i]

		getScoreInfo(base_tmp_out_path,LR_score_path,SVM_score_path,final_out_path)

	return 0

def deal_test_set():
	original_data_path = "../ETL-data/newQuora/out.test.dat"
	seg_data_path = "../ETL-data/newQuora/out.test.dat"
	base_tmp_out_path = "../debug-info/newQuora/test-info.dat"

	LR_score_path_list = [
				"../result/newQuora/bleu.LR.test",
				"../result/newQuora/nist.LR.test",
				"../result/newQuora/ter.LR.test",
				"../result/newQuora/nist-bleu.LR.test",
				"../result/newQuora/ter-nist-bleu.LR.test",
				"../result/newQuora/tfidf.LR.test"
	]
	SVM_score_path_list = [
				"../result/newQuora/bleu.SVM.test",
				"../result/newQuora/nist.SVM.test",
				"../result/newQuora/ter.SVM.test",
				"../result/newQuora/nist-bleu.SVM.test",
				"../result/newQuora/ter-nist-bleu.SVM.test",
				"../result/newQuora/tfidf.SVM.test"
	]
	final_out_path_list = [
				"../debug-info/newQuora/bleu.LR.test",
				"../debug-info/newQuora/nist.LR.test",
				"../debug-info/newQuora/ter.LR.test",
				"../debug-info/newQuora/nist-bleu.LR.test",
				"../debug-info/newQuora/ter-nist-bleu.LR.test",
				"../debug-info/newQuora/tfidf.LR.test"
	]
	
	getBaseInfo(original_data_path,seg_data_path,base_tmp_out_path)

	for i in range(len(LR_score_path_list)):
		LR_score_path = LR_score_path_list[i]
		SVM_score_path = SVM_score_path_list[i]
		final_out_path = final_out_path_list[i]

		getScoreInfo(base_tmp_out_path,LR_score_path,SVM_score_path,final_out_path)

	return 0

def deal_train_set1():
	original_data_path = "../ETL-data/check-data/gouzao/train-ch.dat"
	seg_data_path = "../ETL-data/check-data/gouzao/out-train.dat"
	base_tmp_out_path = "../debug-info/re-seg-chinese2/train-info.dat"

	LR_score_path_list = [
				"../result/re-seg-chinese2/bleu.LR.train",
				"../result/re-seg-chinese2/nist.LR.train",
				"../result/re-seg-chinese2/ter.LR.train",
				"../result/re-seg-chinese2/nist-bleu.LR.train",
				"../result/re-seg-chinese2/ter-nist-bleu.LR.train",
				"../result/re-seg-chinese2/tfidf.LR.train"
	]
	SVM_score_path_list = [
				"../result/re-seg-chinese2/bleu.SVM.train",
				"../result/re-seg-chinese2/nist.SVM.train",
				"../result/re-seg-chinese2/ter.SVM.train",
				"../result/re-seg-chinese2/nist-bleu.SVM.train",
				"../result/re-seg-chinese2/ter-nist-bleu.SVM.train",
				"../result/re-seg-chinese2/tfidf.SVM.train"
	]
	final_out_path_list = [
				"../debug-info/re-seg-chinese2/bleu.LR.train",
				"../debug-info/re-seg-chinese2/nist.LR.train",
				"../debug-info/re-seg-chinese2/ter.LR.train",
				"../debug-info/re-seg-chinese2/nist-bleu.LR.train",
				"../debug-info/re-seg-chinese2/ter-nist-bleu.LR.train",
				"../debug-info/re-seg-chinese2/tfidf.LR.train"
	]
	
	getBaseInfo(original_data_path,seg_data_path,base_tmp_out_path)

	for i in range(len(LR_score_path_list)):
		LR_score_path = LR_score_path_list[i]
		SVM_score_path = SVM_score_path_list[i]
		final_out_path = final_out_path_list[i]

		getScoreInfo(base_tmp_out_path,LR_score_path,SVM_score_path,final_out_path)

	return 0

def deal_test_set1():
	original_data_path = "../ETL-data/check-data/gouzao/test-ch.dat"
	seg_data_path = "../ETL-data/check-data/gouzao/out-test.dat"
	base_tmp_out_path = "../debug-info/re-seg-chinese2/test-info.dat"

	LR_score_path_list = [
				"../result/re-seg-chinese2/bleu.LR.test",
				"../result/re-seg-chinese2/nist.LR.test",
				"../result/re-seg-chinese2/ter.LR.test",
				"../result/re-seg-chinese2/nist-bleu.LR.test",
				"../result/re-seg-chinese2/ter-nist-bleu.LR.test",
				"../result/re-seg-chinese2/tfidf.LR.test"
	]
	SVM_score_path_list = [
				"../result/re-seg-chinese2/bleu.SVM.test",
				"../result/re-seg-chinese2/nist.SVM.test",
				"../result/re-seg-chinese2/ter.SVM.test",
				"../result/re-seg-chinese2/nist-bleu.SVM.test",
				"../result/re-seg-chinese2/ter-nist-bleu.SVM.test",
				"../result/re-seg-chinese2/tfidf.SVM.test"
	]
	final_out_path_list = [
				"../debug-info/re-seg-chinese2/bleu.LR.test",
				"../debug-info/re-seg-chinese2/nist.LR.test",
				"../debug-info/re-seg-chinese2/ter.LR.test",
				"../debug-info/re-seg-chinese2/nist-bleu.LR.test",
				"../debug-info/re-seg-chinese2/ter-nist-bleu.LR.test",
				"../debug-info/re-seg-chinese2/tfidf.LR.test"
	]
	
	getBaseInfo(original_data_path,seg_data_path,base_tmp_out_path)

	for i in range(len(LR_score_path_list)):
		LR_score_path = LR_score_path_list[i]
		SVM_score_path = SVM_score_path_list[i]
		final_out_path = final_out_path_list[i]

		getScoreInfo(base_tmp_out_path,LR_score_path,SVM_score_path,final_out_path)

	return 0

def main():
	deal_train_set()
	deal_test_set()

	# deal_train_set1()
	# deal_test_set1()

if __name__ == '__main__':
	main()