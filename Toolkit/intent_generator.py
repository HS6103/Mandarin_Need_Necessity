#!/usr/bin/env python\3
# -*- coding:utf-8 -*-

import json
import pprint
from time import sleep
from requests import post
from pprint import pprint
from ArticutAPI import Articut

with open("account.info", encoding="utf-8") as f:
    accountDICT = json.load(f)
articut = Articut(username=accountDICT["username"], apikey=accountDICT["api_key"])

def listVerb(targetSTR):
    with open ("../purged_corpus/中研院_{}_purged.txt".format(targetSTR), mode="r", encoding="utf-8") as p:
        print("Generating verbStemLIST...")        
        inputSTR = p.read()
        resultDICT = articut.parse(inputSTR)
        verbStemLIST = articut.getVerbStemLIST(resultDICT)
        print("Finished creating verbStemLIST...\n")
    
    with open('../purged_corpus/中研院_{}_intent.txt'.format(targetSTR),'a',encoding="utf-8") as g: # 將選取檔案中utterance的所有verbStem寫入{}_intent.txt
        try:
            writtenLIST = []        #裝寫過的verbStem
            for entry in verbStemLIST:  #撥開第一層list
                if entry != []:  
                    for verb in entry:           #撥開第二層list
                        if (len(verb[2]) >= 2) and (verb[2] not in writtenLIST):     #將不是[]且沒寫過的verbStem寫入{}_intent.txt和writtenLIST
                            g.write(verb[2] + "\n")        
                            writtenLIST.append(verb[2])
                            break
                        else:
                            pass
                else:
                    pass
            print("Finished\n" + "="*60)
            
        except Exception as e:
            print("\nFailed!\n" + "The following error occurred: {}".format(e))
    

def create_intent(targetSTR):
        try:
            if targetSTR == '須':
                project = 'deontic'
            else:
                project = 'epistemic'
            
            with open('../purged_corpus/中研院_{}_intent.txt'.format(targetSTR),'r',encoding="utf-8") as g:
                print("Generating intent...\n" + "="*60)
                for word in g:
                    iLIST = articut.parse(word, level="lv3", pinyin="HANYU")["utterance"]  #將文件內容(動詞)轉成拼音
                    intentSTR = iLIST[0].replace("/", "").replace(" ", "").strip()
                    
                    url = "https://api.droidtown.co/Loki/Call/" 
                    payload = {
                        "username" : accountDICT["username"], 
                        "loki_key" : accountDICT["loki_key_{}".format(project)], 
                        "project": "{}_xu".format(project), 
                        "intent": "{}".format(intentSTR), #意圖名稱
                        "func": "create_intent",
                        "data": {
                            "type": "advance" #意圖類別
                        }
                    }
                    print("Creating {}...".format(intentSTR))  #建立意圖
                    response = post(url, json=payload).json()
                    pprint(response)
                    sleep(0.3)
            print("\nFinished\n")
            
        except Exception as e:
            print("\nFailed!\n" + "The following error occurred: {}".format(e))
            
#def insert_utterance(targetSTR):
        
            
            
#entry_point
if __name__ == "__main__":
        
    print("\nRunning...")
                    
    listVerb("須")
    create_intent("須")
    
    listVerb("需")
    create_intent("需")
    
    
    
