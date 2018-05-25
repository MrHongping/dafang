s='/root/usr/local/test/'.split('/')
s= [item for item in filter(lambda x:x != '', s)]
print s[1:]