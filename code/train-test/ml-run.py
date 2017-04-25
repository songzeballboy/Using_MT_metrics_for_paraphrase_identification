# coding=utf-8
 
import time  
from sklearn import metrics
from sklearn import preprocessing
from sklearn.externals import joblib
import sys,os
import numpy as np

import pickle as pickle
import pandas as pd

  
# Multinomial Naive Bayes Classifier  
def naive_bayes_classifier(train_x, train_y):  
    from sklearn.naive_bayes import MultinomialNB  
    model = MultinomialNB(alpha=0.01)  
    model.fit(train_x, train_y)  
    return model  
  
  
# KNN Classifier  
def knn_classifier(train_x, train_y):  
    from sklearn.neighbors import KNeighborsClassifier  
    model = KNeighborsClassifier()  
    model.fit(train_x, train_y)
    return model  
  
  
# Logistic Regression Classifier  
def logistic_regression_classifier(train_x, train_y):  
    from sklearn.linear_model import LogisticRegression  
    model = LogisticRegression(penalty='l2')  
    model.fit(train_x, train_y)  
    return model  
  
# Random Forest Classifier  
def random_forest_classifier(train_x, train_y):  
    from sklearn.ensemble import RandomForestClassifier  
    model = RandomForestClassifier(n_estimators=8)  
    model.fit(train_x, train_y)  
    return model  
  
  
# Decision Tree Classifier  
def decision_tree_classifier(train_x, train_y):  
    from sklearn import tree  
    model = tree.DecisionTreeClassifier()  
    model.fit(train_x, train_y)  
    return model  
  
  
# GBDT(Gradient Boosting Decision Tree) Classifier  
def gradient_boosting_classifier(train_x, train_y):  
    from sklearn.ensemble import GradientBoostingClassifier  
    model = GradientBoostingClassifier(n_estimators=200)  
    model.fit(train_x, train_y)  
    return model
  
# SVM Classifier  
def svm_classifier(train_x, train_y):  
    from sklearn.svm import SVC  
    model = SVC(kernel='rbf')  
    model.fit(train_x, train_y)  
    return model  
  
# SVM Classifier using cross validation  
def svm_cross_validation(train_x, train_y):  
    from sklearn.grid_search import GridSearchCV  
    from sklearn.svm import SVC  
    model = SVC(kernel='rbf')  
    param_grid = {'C': [1e-3, 1e-2, 1e-1, 1, 10, 100, 1000], 'gamma': [0.001, 0.0001]}  
    grid_search = GridSearchCV(model, param_grid, n_jobs = 1, verbose=1)  
    grid_search.fit(train_x, train_y)  
    best_parameters = grid_search.best_estimator_.get_params()  
    for para, val in list(best_parameters.items()):  
        print(para, val)  
    model = SVC(kernel='rbf', C=best_parameters['C'], gamma=best_parameters['gamma'])  
    model.fit(train_x, train_y)  
    return model 

# LinearSVC
def svm_linearSVC_classifier(train_x, train_y):
    from sklearn.svm import LinearSVC
    model = LinearSVC()
    model.fit(train_x,train_y)
    return model

def main(trainset_path,testset_path,out_path,save_result=False):
    '''
    1. get data path config info
    2. get train data & test data
    3. model training
    4. evalution
    ''' 
    # 1. data path
    # trainset_path = "../../feature/chinese-2/ter-nist-bleu.train.in"
    # testset_path = "../../feature/chinese-2/ter-nist-bleu.test.in"
    
    # fea_fit_path = "../result/LR-info.m"
    # model_path = "../model-info/LogisticModel.m"

    # other paramter
    thresh = 0.5  
    model_save_file = None
    model_save = {}

    ### predict result save
    fea_info_list = trainset_path.split("/")
    fea_info_path_list = fea_info_list[-1].split(".")
    fea_info = fea_info_path_list[0]

    # cur_time = time.strftime("%Y-%m-%d-%H-%M")
    model_pre_result_LR = out_path + fea_info + ".LR.test"
    model_pre_result_SVM = out_path + fea_info + ".SVM.test"

    model_train_result_LR = out_path + fea_info + ".LR.train"
    model_train_result_SVM = out_path + fea_info + ".SVM.train"

#    model_save_file = "../../model-info/newQuora/" + fea_info + ".model"

    #### classifier setting info

    # test_classifiers = ['NB', 'KNN', 'LR', 'RF', 'DT', 'SVM','SVMCV', 'GBDT']
    test_classifiers = ['LR', 'SVM', 'KNN','LSVM']
    # test_classifiers = ['LR','SVM']
    # test_classifiers = ['LR']
    classifiers = {'NB':naive_bayes_classifier,
                  'KNN':knn_classifier,
                   'LR':logistic_regression_classifier,
                   'RF':random_forest_classifier,
                   'DT':decision_tree_classifier,
                  'SVM':svm_classifier,
                'SVMCV':svm_cross_validation,
                 'GBDT':gradient_boosting_classifier,
                 'LSVM':svm_linearSVC_classifier
    }

    # 2. read training data & test data
    # read training data
    dataset = np.loadtxt(trainset_path, delimiter=",")
    np.set_printoptions(suppress=True)
    len = np.shape(dataset)
    len_col = len[1]
    x_train = dataset[:, 0:len_col-1]
    y_train = dataset[:, len_col-1]

    min_max_scaler = preprocessing.MinMaxScaler()
    x_train_minMax = min_max_scaler.fit_transform(x_train)

    # read test data
    testset = np.loadtxt(testset_path, delimiter=",")
    len = np.shape(testset)
    len_col = len[1]
    x_test = testset[:, 0:len_col-1]
    y_test = testset[:, len_col-1]

    x_test_minMax = min_max_scaler.transform(x_test)
    # predict = clf.predict(x_test_minMax)

    print "training set path = " + trainset_path
    print "testing set path = " + testset_path

    for classifier in test_classifiers:
        print('******************* %s ********************' % classifier)
        # 3. model training
        model = classifiers[classifier](x_train_minMax, y_train)
        predict = model.predict(x_test_minMax)

        # record the model prdict information
        if save_result == True:
            if classifier == 'LR':
                predict_pro = model.predict_proba(x_test_minMax)[:,1].tolist()
                fp_w_LR = open(model_pre_result_LR,"w")
                for i in predict_pro:
                    fp_w_LR.write(str(i)+"\n")
                fp_w_LR.close()
            elif classifier == 'SVM':
                fp_w_SVM = open(model_pre_result_SVM,"w")
                predict_list = predict.tolist()
                for i in predict_list:
                    fp_w_SVM.write(str(i)+"\n")
                fp_w_SVM.close()

        if model_save_file != None:  
            model_save[classifier] = model  
        
        # 4. evalution
        precision = metrics.precision_score(y_test, predict)  
        recall = metrics.recall_score(y_test, predict)  
        print('precision: %.2f%%, recall: %.2f%%' % (100 * precision, 100 * recall))  
        
        accuracy = metrics.accuracy_score(y_test, predict)  
        print('accuracy: %.2f%%' % (100 * accuracy))   
        
        f1score = metrics.f1_score(y_test,predict)
        print('f1 score: %.2f%%' % (100 * f1score))

        ### save training information
        if save_result == True:
            if classifier == 'LR':
                predict_pro = model.predict_proba(x_train_minMax)[:,1].tolist()
                fp_w_LR = open(model_train_result_LR,"w")
                for i in predict_pro:
                    fp_w_LR.write(str(i)+"\n")
                fp_w_LR.close()
            elif classifier == 'SVM':
                fp_w_SVM = open(model_train_result_SVM,"w")
                train_predict = model.predict(x_train_minMax).tolist()
                for i in train_predict:
                    fp_w_SVM.write(str(i)+"\n")
                fp_w_SVM.close()    
  
    if model_save_file != None:
        pickle.dump(model_save, open(model_save_file, 'wb'))

    return 0

if __name__ == '__main__':
    train_path_list = [
                    "../../feature/MSRP/meteor.train.in"
                    #"../../feature/newQuora/bleu.train.in",
                    #"../../feature/newQuora/nist.train.in",
                    #"../../feature/newQuora/ter.train.in",
                    #"../../feature/newQuora/tfidf.train.in",
                    #"../../feature/newQuora/my-tfidf.train.in",
                    #"../../feature/newQuora/nist-bleu.train.in",
                    #"../../feature/newQuora/ter-nist-bleu.train.in"
    ]
    test_path_list = [
                    "../../feature/MSRP/meteor.test.in"
                    #"../../feature/newQuora/bleu.test.in",
                    #"../../feature/newQuora/nist.test.in",
                    #"../../feature/newQuora/ter.test.in",
                    #"../../feature/newQuora/tfidf.test.in",
                    #"../../feature/newQuora/my-tfidf.test.in",
                    #"../../feature/newQuora/nist-bleu.test.in",
                    #"../../feature/newQuora/ter-nist-bleu.test.in"
    ]

    out_path = "../../result/re-seg-zhihu/"
    
    for i in range(len(train_path_list)):
        trainset_path = train_path_list[i]
        testset_path = test_path_list[i]
        main(trainset_path,testset_path,out_path,False)
        print "###############################################"
        print "###############################################\n"

    print "over ------------------------ over"
