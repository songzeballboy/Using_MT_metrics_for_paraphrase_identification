#coding=utf-8
import random
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def main():
	cnt = 1
	for str_line in sys.stdin:
		line = str_line.decode("utf-8").replace('\n','').replace('\r','')
		#print line
		line = line + " ( " + str(cnt) + " )"
		print(line.encode('utf-8'))
		cnt += 1

if __name__ == '__main__':
	main()

