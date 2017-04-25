#!/bin/bash
#######################
# config information
#######################
_code="../code"
_ETL="../ETL-data"
_feature="../feature"
_out="../result"

if [ ! -d "${_code}" ]; then
    mkdir ${_code}
fi

if [ ! -d "${_ETL}" ]; then
    mkdir ${_ETL}
fi

if [ ! -d "${_feature}" ]; then
    mkdir ${_feature}
fi

if [ ! -d "${_out}" ]; then
    mkdir ${_out}
fi

code_path="../code/data-pre"
data_path="../data"
ETL_path="../ETL-data/MSRP"
fea_path="../feature/MSRP"
output="../result/MSRP"

tercom_path="../Tools/tercom-0.7.25"
meteor_path="../Tools/meteor-1.5"

if [ ! -d "${code_path}" ]; then
    mkdir ${code_path}
fi

if [ ! -d "${ETL_path}" ]; then
    mkdir ${ETL_path}
fi

if [ ! -d "${fea_path}" ]; then
    mkdir ${fea_path}
fi

if [ ! -d "${output}" ]; then
    mkdir ${output}
fi

##################################################
## 1. get bleu score #############################
##################################################
echo "get bleu score"
cat ${ETL_path}/out.train.dat | python ${code_path}/Bleu-feature.py > ${fea_path}/bleu.train.in
cat ${ETL_path}/out.test.dat | python ${code_path}/Bleu-feature.py > ${fea_path}/bleu.test.in

##################################################
## 2. get nist score #############################
##################################################
echo "get nist score"
cat ${ETL_path}/out.train.dat | python ${code_path}/NIST-feature.py > ${fea_path}/nist.train.in
cat ${ETL_path}/out.test.dat | python ${code_path}/NIST-feature.py > ${fea_path}/nist.test.in

##################################################
## 3. get ter score #############################
##################################################
echo "get ter score"
cat ${ETL_path}/out.train.dat | python ${code_path}/processNISTformatDATA.py ${ETL_path}/refData.train.dat ${ETL_path}/hypData.train.dat
cat ${ETL_path}/out.test.dat | python ${code_path}/processNISTformatDATA.py ${ETL_path}/refData.test.dat ${ETL_path}/hypData.test.dat

cat ${ETL_path}/hypData.train.dat | python ${code_path}/deal-ter-data.py > ${ETL_path}/hypData-ter.train.dat
cat ${ETL_path}/hypData.test.dat | python ${code_path}/deal-ter-data.py > ${ETL_path}/hypData-ter.test.dat

cat ${ETL_path}/refData.train.dat | python ${code_path}/deal-ter-data.py > ${ETL_path}/refData-ter.train.dat
cat ${ETL_path}/refData.test.dat | python ${code_path}/deal-ter-data.py > ${ETL_path}/refData-ter.test.dat

java -jar ${tercom_path}/tercom.7.25.jar -r ${ETL_path}/refData-ter.train.dat -h ${ETL_path}/hypData-ter.train.dat -o ter -n ${ETL_path}/ter-sc.train > log1.del
java -jar ${tercom_path}/tercom.7.25.jar -r ${ETL_path}/refData-ter.test.dat -h ${ETL_path}/hypData-ter.test.dat -o ter -n ${ETL_path}/ter-sc.test > log2.del

rm ./log1.del
rm ./log2.del

cat ${ETL_path}/ter-sc.train.ter | python ${code_path}/reshapeTER.py > ${fea_path}/ter-sc.train.fea
cat ${ETL_path}/ter-sc.test.ter | python ${code_path}/reshapeTER.py > ${fea_path}/ter-sc.test.fea


##################################################
## 4. get tfidf score #############################
##################################################
echo "Solve tfidf"
cat ${ETL_path}/out.train.dat | python ${code_path}/deal-tfidf-data.py > ${ETL_path}/tfidf.train.dat
cat ${ETL_path}/out.test.dat | python ${code_path}/deal-tfidf-data.py > ${ETL_path}/tfidf.test.dat

python ${code_path}/tfidf-feature.py ${ETL_path}/tfidf.train.dat ${fea_path}/tfidf.train.fea
python ${code_path}/tfidf-feature.py ${ETL_path}/tfidf.test.dat ${fea_path}/tfidf.test.fea

python ${code_path}/my-tfidf-cal.py ${ETL_path}/tfidf.train.dat ${fea_path}/my-tfidf.train.fea
python ${code_path}/my-tfidf-cal.py ${ETL_path}/tfidf.test.dat ${fea_path}/my-tfidf.test.fea


##################################################
## 4. get meteor score ###########################
##################################################
java -Xmx2G -jar ${meteor_path}/meteor-1.5.jar ${ETL_path}/hypData-ter.train.dat ${ETL_path}/refData-ter.train.dat -norm > ${fea_path}/meteor_sc.train.fea
java -Xmx2G -jar ${meteor_path}/meteor-1.5.jar ${ETL_path}/hypData-ter.test.dat ${ETL_path}/refData-ter.test.dat -norm > ${fea_path}/meteor_sc.test.fea

##################################################
## 6. get data prepare ###########################
##################################################
echo "get tfidf feature"
python ${code_path}/get-two-source-together.py ${fea_path}/tfidf.train.fea ${fea_path}/bleu.train.in ${fea_path}/tfidf-bleu.train.tmp
python ${code_path}/get-two-source-together.py ${fea_path}/tfidf.test.fea ${fea_path}/bleu.test.in ${fea_path}/tfidf-bleu.test.tmp

python ${code_path}/get-two-source-together.py ${fea_path}/my-tfidf.train.fea ${fea_path}/bleu.train.in ${fea_path}/my-tfidf-bleu.train.tmp
python ${code_path}/get-two-source-together.py ${fea_path}/my-tfidf.test.fea ${fea_path}/bleu.test.in ${fea_path}/my-tfidf-bleu.test.tmp

cat ${fea_path}/nist.train.in | awk -F ',' 'BEGIN{OFS=","}{print $1,$2,$3,$4,$5}' > ${fea_path}/nist-sc.train.fea
cat ${fea_path}/nist.test.in | awk -F ',' 'BEGIN{OFS=","}{print $1,$2,$3,$4,$5}' > ${fea_path}/nist-sc.test.fea

echo "get nist-bleu comb feature"
python ${code_path}/get-two-source-together.py ${fea_path}/nist-sc.train.fea ${fea_path}/bleu.train.in ${fea_path}/nist-bleu.train.in
python ${code_path}/get-two-source-together.py ${fea_path}/nist-sc.test.fea ${fea_path}/bleu.test.in ${fea_path}/nist-bleu.test.in

echo "get ter-nist-bleu comb feature"
python ${code_path}/get-two-source-together.py ${fea_path}/ter-sc.train.fea ${fea_path}/nist-bleu.train.in ${fea_path}/ter-nist-bleu.train.in
python ${code_path}/get-two-source-together.py ${fea_path}/ter-sc.test.fea ${fea_path}/nist-bleu.test.in ${fea_path}/ter-nist-bleu.test.in

cat ${fea_path}/tfidf-bleu.train.tmp | awk -F ',' 'BEGIN{OFS=","}{print $1,$6}' > ${fea_path}/tfidf.train.in
cat ${fea_path}/tfidf-bleu.test.tmp | awk -F ',' 'BEGIN{OFS=","}{print $1,$6}' > ${fea_path}/tfidf.test.in

cat ${fea_path}/my-tfidf-bleu.train.tmp | awk -F ',' 'BEGIN{OFS=","}{print $1,$6}' > ${fea_path}/my-tfidf.train.in
cat ${fea_path}/my-tfidf-bleu.test.tmp | awk -F ',' 'BEGIN{OFS=","}{print $1,$6}' > ${fea_path}/my-tfidf.test.in


cat ${fea_path}/ter-nist-bleu.train.in | awk -F ',' 'BEGIN{OFS=","}{print $1,$11}' > ${fea_path}/ter.train.in
cat ${fea_path}/ter-nist-bleu.test.in | awk -F ',' 'BEGIN{OFS=","}{print $1,$11}' > ${fea_path}/ter.test.in
