import re
import json
from requests import post
from time import sleep
from pprint import pprint
from ArticutAPI import Articut

with open("account.info", encoding="utf-8") as f:
    accountDICT = json.load(f)
articut = Articut(username=accountDICT["username"], apikey=accountDICT["api_key"])

#讀取擷取片段用re
with open("corpus_chunk_re.json","r",encoding="utf-8") as c:
    corpus_chunk_re = json.load(c)
chunk_regexLIST = dict(corpus_chunk_re.items())

def chunker(targetSTR, mode):
    try:
        chunked_list = []
        userDefined = "./UserDefinedFile.json"
        
        with open('../purged_corpus/中研院_{}_chunked.txt'.format(targetSTR),'w',encoding="utf-8") as n: # 開啟一份空白_chunked.txt
            pass
        
        with open('../purged_corpus/中研院_{}_purged.txt'.format(targetSTR),'r',encoding="utf-8") as g:  #讀取_purged.txt
            print("Working {}_{}...".format(targetSTR, mode))
            s_list = g.readlines()
            pat = chunk_regexLIST["{}".format(mode)]  #根據mode讀取片段用re建立pattern
            for sentence in s_list:
                resultDICT = articut.parse(sentence, level='lv2', userDefinedDictFILE=userDefined)  #articut斷詞
                m = re.search(pat, resultDICT["result_pos"][0])  
                    
                if m == None:
                    pass
                else:
                    chunked_string = ""
                    if mode == "front":
                        chunked_string += re.sub("<.+?>", "", m.group(0))  #拔掉POS tag
                    else:
                        chunked_string += re.sub("<.+?>", "", m.group(0))  #拔掉POS tag
                    chunked_list.append(chunked_string)  #暫存於chunked_list
                    sleep(0.5)
                    
             
        with open('../purged_corpus/中研院_{}_chunked_{}.txt'.format(targetSTR, mode),'w',encoding="utf-8") as n: # 將 chunked_list 中的句子寫入 _chunked.txt 檔
            n.write("\n".join(chunked_list))
            print("Success!")
            print("======================================================================================================")                        
            
    except Exception as e:
        print("Encountered Error: {}".format(e))

def insert_utterance(targetSTR, mode):
    with open('../purged_corpus/中研院_{}_chunked_{}.txt'.format(targetSTR, mode),'r',encoding="utf-8") as n: # 將 chunked_list 中的句子讀入
        lines = n.readlines()
        
    print("insert_utterance: {}_{}".format(targetSTR, mode))
    print("======================================================================================================")                            
    
    if targetSTR == "須":
        intent = "must_adv"
    else:
        intent = "need_adv"
    for utterance in lines:   
        url = "https://api.droidtown.co/Loki/Call/" #LokiCall Docker 版請自訂 URL
        payload = {
            "username" : accountDICT["username"], # 這裡填入您在 https://api.droidtown.co 使用的帳號 email。     Docker 版不需要此參數！
            "loki_key" : accountDICT["loki_key_{}".format(mode)], # 這裡填入您在 https://api.droidtown.co 登入後取得的 loki_key。 Docker 版不需要此參數！
            "project": "need_must_{}".format(mode), #專案名稱
            "intent": intent, #意圖名稱
            "func": "insert_utterance",
            "data": {
                "utterance": [ #新增的句子
                    utterance.strip("\n")
                ],
                "checked_list": [ #所有詞性全勾選。你可以把不要勾的項目註解掉。
                    #"ENTITY_noun", #包含所有名詞
                    #"UserDefined", 
                    "ENTITY_num",
                    "DegreeP",
                    "MODIFIER_color",
                    "LOCATION",
                    "KNOWLEDGE_addTW",
                    "KNOWLEDGE_routeTW",
                    "KNOWLEDGE_lawTW",
                    "KNOWLEDGE_url",
                    "KNOWLEDGE_place",
                    "KNOWLEDGE_wikiData",
                    "KNOWLEDGE_currency"
                ]
            }
        }
    
        response = post(url, json=payload).json()
        pprint(response['msg'])
        
    print("======================================================================================================\n")                        
    
    
if __name__ == "__main__":
    chunker("須", "front")
    chunker("須", "aft")
    chunker("需", "front")
    chunker("需", "aft")
    
    insert_utterance("須", "front")
    insert_utterance("須", "aft")
    insert_utterance("需", "front")
    insert_utterance("需", "aft")
