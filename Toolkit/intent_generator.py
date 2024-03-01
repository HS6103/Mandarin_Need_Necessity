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
        print("Generating verbStemLIST...\n" + "="*60)        
        inputSTR = p.read()
        resultDICT = articut.parse(inputSTR)
        verbStemLIST = articut.getVerbStemLIST(resultDICT)
        print("\nFinished loading verbStemLIST...\n" + "="*60)
    
    with open('../purged_corpus/中研院_{}_intent.txt'.format(targetSTR),'a',encoding="utf-8") as g: # 將選取檔案中utterance的動詞寫入{}_intent.txt
        try:
            for entry in verbStemLIST:
                if entry != []:
                    for subentry in entry:
                        g.write(subentry[2] + "\n")
                else:
                    pass
            print("\nFinished\n")
            
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
                    iLIST = articut.parse(word, level="lv3", pinyin="HANYU")["utterance"]
                    intentSTR = iLIST[0].replace("/", "").replace(" ", "").strip()
                    
                    url = "https://api.droidtown.co/Loki/Call/" #LokiCall Docker 版請自訂 URL
                    payload = {
                        "username" : accountDICT["username"], # 這裡填入您在 https://api.droidtown.co 使用的帳號 email。     Docker 版不需要此參數！
                        "loki_key" : accountDICT["loki_key_{}".format(project)], # 這裡填入您在 https://api.droidtown.co 登入後取得的 loki_key。 Docker 版不需要此參數！
                        "project": "{}_xu".format(project), #專案名稱 (請先在 Loki 的設定網頁裡建立一個 Project 以便取得它的專案金鑰 (loki_key)
                        "intent": "{}".format(intentSTR), #意圖名稱
                        "func": "create_intent",
                        "data": {
                            "type": "advance" #意圖類別
                        }
                    }
                    print("Creating {}...".format(intentSTR))
                    response = post(url, json=payload).json()
                    pprint(response)
                    sleep(0.3)
                    
            print("\nFinished\n")
            
        except Exception as e:
            print("\nFailed!\n" + "The following error occurred: {}".format(e))
            
#entry_point
if __name__ == "__main__":
        
    #targetSTR = input("Enter target character: ") #輸入要處理的字
    print("\nRunning...")
                    
    #listVerb("須")
    #listVerb("需")
    create_intent("須")
    create_intent("需")
    
    
    
