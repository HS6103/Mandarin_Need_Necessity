#!/usr/bin/env python\3
# -*- coding:utf-8 -*-
import json
import pprint
from ArticutAPI import Articut

with open("account.info", encoding="utf-8") as f:
    accountDICT = json.load(f)
articut = Articut(username=accountDICT["username"], apikey=accountDICT["api_key"])

def listVerb(targetSTR):
    
    with open ("../purged_corpus/中研院_{}_purged.txt".format(targetSTR), mode="r", encoding="utf-8") as p:
        print("Generating verbStemLIST...\n" + "="*60)        
        inputSTR = p.read()
        resultDICT = articut.parse(inputSTR)
        verbStemLIST = articut.getVerbStemLIST(resultDICT)
        print("\nFinished loading verbStemLIST...\n" + "="*60)
    
    with open('../purged_corpus/中研院_{}_intent.txt'.format(targetSTR),'a',encoding="utf-8") as g: # 將 corpusLIST 中的句子寫入 _purged.txt 檔
        try:
            for content in verbStemLIST:
                if content != []:
                    for entry in content:
                        g.write(entry[2] + "\n")
                else:
                    pass
            print("\nFinished")
            
        except Exception as e:
            print("\nFailed!\n" + "The following error occurred: {}".format(e))
    


#entry_point
if __name__ == "__main__":
        
    targetSTR = input("Enter target character: ")
    print("\nRunning...")
    
    listVerb(targetSTR)
    
