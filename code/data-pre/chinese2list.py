#coding=utf-8

import sys,os
import jieba
reload(sys)
sys.setdefaultencoding('utf-8')

def main():
	for str_line in sys.stdin:
		try:
			line = str_line.replace('\n','').replace('\r','').decode("utf-8")
			fields = line.replace('#','').replace('?','').replace('。','').replace('.','').replace('N','').replace('《','').replace('》','').replace('“','').replace('”','').replace('（','').replace('）','').replace('「','').replace('」','').replace('、','').replace('？','').replace('/','').split("\t")

			# fields = line.split("\t")
			if(len(fields) != 3):
				continue

			# str_list1 = list(fields[1])
			# str1 = str_list1[0].encode("utf-8")
			# for i in range(1,len(str_list1)):
			# 	str1 = str1 + " " + str_list1[i].encode("utf-8")

			# str_list2 = list(fields[2])
			# if len(str_list2) < 1:
			# 	continue
			# str2 = str_list2[0].encode("utf-8")
			# for i in range(1,len(str_list2)):
			# 	str2 = str2 + " " + str_list2[i].encode("utf-8")

			str_list1 = jieba.cut(fields[0])
			str1 = " ".join(str_list1)

			str_list2 = jieba.cut(fields[1])
			str2 = " ".join(str_list2)
            id_class = fields[2]
			OFS = "\t"
			toWrite = id_class + OFS + str(str1) + OFS + str(str2)

			print toWrite.encode("utf-8")
		except Exception as e:
			raise e
	return 0

if __name__ == '__main__':
	main()
