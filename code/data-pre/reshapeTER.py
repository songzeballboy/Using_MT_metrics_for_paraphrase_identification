#coding=utf-8
import random
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def main():
	cnt = 0
	for str_line in sys.stdin:
		cnt += 1
		if cnt == 1 or cnt == 2:
			continue
		line = str_line.decode("utf-8").replace('\n','').replace('\r','')
		# print line
		toWrite= line.split(" ")[5]
		print toWrite.encode("utf-8")

if __name__ == '__main__':
	main()
