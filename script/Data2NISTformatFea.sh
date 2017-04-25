#!/bin/bash
data_path=~/mycode/re-examining/data
ETL_path=~/mycode/re-examining/ETL-data
mt_eval_path=~/mteval-master
input_path=~/mycode/re-examining/data/new-test.dat
output_path=test-NISTFea.dat
cat ${input_path} | python ${ETL_path}/processNISTformatDATA.py
cd ${mt_eval_path}
mteval-sentence.exe -e NIST:ngram=1 NIST:ngram=2 NIST:ngram=3 NIST:ngram=4 NIST:ngram=5 -r ~/mycode/re-examining/data/refNIST.dat -h ~/mycode/re-examining/data/hpyNIST.dat > ~/mycode/re-examining/data/NIST-score.dat
cat ${data_path}/train-NIST-score.dat | python ${ETL_path}/NISTdata2fea.py > ${data_path}/${output_path}
rm ${data_path}/hpyNIST.dat
rm ${data_path}/refNIST.dat
rm train-NIST-score.dat