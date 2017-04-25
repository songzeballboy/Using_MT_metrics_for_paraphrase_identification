#coding=utf-8

import sys,os

def _getNISTScore(strInfo):
	b_pos = strInfo.find("=")
	return strInfo[b_pos+1:]

def main():
	for line in sys.stdin:
		fields = line.replace('\n','').replace('\r','').split("\t")
		toWrite = _getNISTScore(fields[0])
		for i in range(1,len(fields)):
			toWrite = toWrite + "," + _getNISTScore(fields[i])
		print toWrite
	return 0

if __name__ == '__main__':
	main()
