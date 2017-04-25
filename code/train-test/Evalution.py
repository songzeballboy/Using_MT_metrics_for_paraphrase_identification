#coding=utf-8
import sys,os
import numpy as np
from sklearn import preprocessing
from sklearn.cross_validation import train_test_split   
from sklearn.cross_validation import cross_val_score    
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
from sklearn.metrics import roc_auc_score
from sklearn.externals import joblib

def work(output_path,model_path,fea_fit_path,testset_path):
    #log infomation set
    fp_model = open(output_path, "w")

    print "load testset"
    testset = np.loadtxt(testset_path, delimiter=",")
    len = np.shape(testset)           
    len_col = len[1]
    x_test = testset[:, 0:len_col-1]
    y_test = testset[:, len_col-1]
    fp_model.write("shape of dataset, x, y: "+str(testset.shape)+"\t"+str(x_test.shape)+"\t"+str(y_test.shape) + "\n")

    # model load
    clf = joblib.load(model_path)

    #get evalution infomation: precision, recall, F1 & Acc.
    print "print Evalution"
    min_max_scaler = joblib.load(fea_fit_path)
    x_test_minMax = min_max_scaler.transform(x_test)
    predict = clf.predict(x_test_minMax)
    predict_pro = clf.predict_proba(x_test_minMax)[:,1] #clf模型给出预估的概率,predict_proba返回的是一个两列的矩阵，第一列代表该事件不会发生的概率，第二列代表的是该事件会发生的概率
    #report = predict_pro > 0.5
    report = predict_pro > 0.6
    fp_model.write("\ny_test: " + str(y_test) + "\n")
    fp_model.write("report: " + str(report) + "\n")
    neg_pos_zhibiao = classification_report(y_test, report, target_names = ['neg', 'pos'])  #正确率和召回率
    fp_model.write("\n"+str(neg_pos_zhibiao) + "\n")
    r = clf.score(x_test_minMax, y_test)
    fp_model.write("模型准确率: " + str(r) + "\n")

    fp_model.close()
    return 0

def main():
    output_path = "../result/new-LR.log"
    model_path = "../model-info/LogisticModel.m"
    fea_fit_path = "../result/LR-info.m"
    testset_path = "../feature/test-1.fea"

    work(output_path,model_path,fea_fit_path,testset_path)

    return 0


if __name__ == "__main__":
    main()