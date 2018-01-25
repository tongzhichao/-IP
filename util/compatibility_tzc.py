#coding:utf-8

import sys
PY3 = sys.version_info[0] == 3

if PY3:
	text_type = str
	binary_type = bytes

else:
	print('Python版本不对，该代码支持Python3')
	text_type = unicode
	binary_type = str  


def text_(s,encoding='utf-8',errors = 'strict'):
	if isinstance(s,binary_type):
		return s.decode(encoding,errors)

	return s 

def bytes_(s,encoding='utf-8',errors = 'strict'):
	if isinstance(s,text_type):
		return s.encode(encoding,errors)

	return s 


if __name__ == '__main__':
	a = text_('省')
	print(a)