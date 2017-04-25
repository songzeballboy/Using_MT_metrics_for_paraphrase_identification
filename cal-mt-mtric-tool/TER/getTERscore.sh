#!/bin/bash
function main(){
	ref_path=$1
	hpy_path=$2
	out_path=$3

	cat ${ref_path} | python deal-ter-format.py > temp1.dat
	cat ${hpy_path} | python deal-ter-format.py > temp2.dat
	java -jar ./tercom-0.7.25/tercom.7.25.jar -r temp1.dat -h temp2.dat -o ter -n ${out_path}
	rm temp1.dat
	rm temp2.dat
}

main