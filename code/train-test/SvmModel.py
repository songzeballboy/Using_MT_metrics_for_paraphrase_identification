#coding=utf-8
import sys,os
import numpy as np
from sklearn import preprocessing
from sklearn.cross_validation import train_test_split   
from sklearn.cross_validation import cross_val_score    
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
from sklearn import metrics
from sklearn.svm import SVC

def main():
    
    #日志文件清空
    # fp_model = open("../result/SVM-1.model", "w")
    # fp_para = open("../result//SVM-1.para", "w")
    
    print "load dataset"
    #加载数据
    dataset = np.loadtxt("./../feature/train-1.fea", delimiter=",")
    np.set_printoptions(suppress=True)

    len = np.shape(dataset)           #获取数据集大小（row_len,col_len）
    len_col = len[1]
    x_train = dataset[:, 0:len_col-1]     #特征矩阵：x
    y_train = dataset[:, len_col-1]       #目标变量：y
    # fp_model.write("shape of dataset, x, y: "+str(dataset.shape)+"\t"+str(x_train.shape)+"\t"+str(y_train.shape) + "\n")

    # print "split dataset"
    # #数据切分：
    # x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.1)
    # fp_model.write("test_size = 0.1 \nshape of train, test: " + str(x_train.shape)+"\t"+str(y_train.shape)+"\t"+str(x_test.shape)+"\t"+str(y_test.shape)+"\n")

    print "proprocess dataset"
    #数据预处理：归一化
    min_max_scaler = preprocessing.MinMaxScaler()
    x_train_minMax = min_max_scaler.fit_transform(x_train)       #训练并转换特征矩阵： (x-min)/(max-min)
    # fp_model.write("\nx_train_min(parameters):\n" + str(x_train.min(axis = 0)) + "\n" )
    # fp_model.write("\nx_train_max(parameters):\n" + str(x_train.max(axis = 0)) + "\n")
    # fp_para.write(str(x_train.min(axis = 0).tolist()) + "\n")
    # fp_para.write(str(x_train.max(axis = 0).tolist())+"\n")

    print "train SVM"
    #SVM模型
    clf = SVC()
    clf.fit(x_train_minMax, y_train)
    # fp_model.write("\ncoefficient(parameters):\n" + str(clf.coef_) + "\n")   #系数矩阵
    # fp_model.write("intercept(parameters):" + str(clf.intercept_) + "\n")   #截距
    # fp_para.write(str(clf.coef_[0].tolist()) + "\n")
    # fp_para.write(str(clf.intercept_.tolist()) + "\n")
    print "SVM trianing  OK"

    print "load testset"
    testset = np.loadtxt("./../feature/test-1.fea", delimiter=",")
    len = np.shape(testset)           #获取数据集大小（row_len,col_len）
    len_col = len[1]
    x_test = testset[:, 0:len_col-1]     #特征矩阵：x
    y_test = testset[:, len_col-1]       #目标变量：y
    # fp_model.write("shape of dataset, x, y: "+str(testset.shape)+"\t"+str(x_test.shape)+"\t"+str(y_test.shape) + "\n")

    #指标计算: precision, recall, auc
    print "print zhibiao"
    x_test_minMax = min_max_scaler.transform(x_test)
    predict = clf.predict(x_test_minMax)
    # predict_pro = clf.predict_proba(x_test_minMax)[:,1] #clf模型给出预估的概率,predict_proba返回的是一个两列的矩阵，第一列代表该事件不会发生的概率，第二列代表的是该事件会发生的概率
    #report = predict_pro > 0.5
    # report = predict_pro > 0.7
    # fp_model.write("\ny_test: " + str(y_test) + "\n")
    # fp_model.write("report: " + str(report) + "\n")
    # neg_pos_zhibiao = classification_report(y_test, report, target_names = ['neg', 'pos'])  #正确率和召回率
    # fp_model.write("\n"+str(neg_pos_zhibiao) + "\n")
    precision = metrics.precision_score(y_test, predict)  
    recall = metrics.recall_score(y_test, predict)  
    print('precision: %.2f%%, recall: %.2f%%' % (100 * precision, 100 * recall))  
    accuracy = metrics.accuracy_score(y_test, predict)  
    print('accuracy: %.2f%%' % (100 * accuracy))   
    f1score = metrics.f1_score(y_test,predict)
    print('f1 score: %.2f%%' % (100 * f1score))
    # r = clf.score(x_test_minMax, y_test)
    # fp_model.write("模型准确率: " + str(r) + "\n")
    # auc = roc_auc_score(y_test, predict_pro)        #auc计算
    # fp_model.write("AUC: " + str(auc) + "\n")
    
    # fp_model.close()
    # fp_para.close()
    return 0

    #LR模型，交叉验证
    #t_min_max_scaler = preprocessing.MinMaxScaler()
    #x_minMax = t_min_max_scaler.fit_transform(x)       #训练并转换特征矩阵： (x-min)/(max-min)
    #scores = cross_val_score(LogisticRegression(), x_minMax, y, cv=10)
    #log_data = str(scores) + "\n"
    #log_data += "Accuracy: %0.2f (+/- %0.2f): " + str(scores.mean()) + "\t" + str(scores.std()*2) + "\n"  #平均精度，及模型稳定性
    #fprint(log_data)
    #return 0


if __name__ == "__main__":

    main()