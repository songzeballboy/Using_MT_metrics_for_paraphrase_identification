#coding=utf-8
import random
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def main():
	for str_line in sys.stdin:
		line = str_line.decode("utf-8").replace('\n','').replace('\r','')
		feilds = line.split("\t")
		ref = feilds[1]
		hpy = feilds[2]

		print ref.encode("utf-8")
		print hpy.encode("utf-8")

if __name__ == '__main__':
	main()
