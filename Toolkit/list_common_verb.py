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
    cnt = len(common_intentLIST)
    for entry in common_intentLIST:
        n.write(entry)
    n.write("Total Count: {}".format(cnt))

#with open('../purged_corpus/deontic_unique_intent.txt','a',encoding="utf-8") as deontic_u:
    #written_list = []
    #cnt = 0
    #for verb in deonticLIST:
        #if verb not in common_intentLIST and verb not in written_list:
            #deontic_u.write(verb)
            #written_list.append(verb)
            #cnt += 1
    #deontic_u.write("Total Count: {}".format(cnt))
            
#with open('../purged_corpus/epistemic_unique_intent.txt','a',encoding="utf-8") as epistemic_u:
    #written_list = []
    #cnt = 0    
    #for verb in epistemicLIST:
        #if verb not in common_intentLIST and verb not in written_list:
            #epistemic_u.write(verb)
            #written_list.append(verb)
            #cnt += 1
    #epistemic_u.write("Total Count: {}".format(cnt))
