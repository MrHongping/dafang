# coding=utf-8

"""
@version: 1.0
@author: chaowei
@file: shelltest.py
@time: 2018/2/18 21:08
"""
s='->|str123|<-'
s=s[s.find('->|')+3:s.find('|<-')]
print s
