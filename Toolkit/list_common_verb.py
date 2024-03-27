#!/usr/bin/env python3
# -*- coding:utf-8 -*-

with open ("../purged_corpus/中研院_須_intent.txt", mode="r", encoding="utf-8") as a:
    deonticLIST = a.readlines()
    
with open ("../purged_corpus/中研院_需_intent.txt", mode="r", encoding="utf-8") as b:
    epistemicLIST = b.readlines()

common_intentLIST = []

for intent in deonticLIST:
    if (intent in epistemicLIST) and (intent not in common_intentLIST):
        common_intentLIST.append(intent)
    else:
        pass
        
with open('../purged_corpus/common_intent.txt','w',encoding="utf-8") as n:
    for entry in common_intentLIST:
        n.write(entry)
