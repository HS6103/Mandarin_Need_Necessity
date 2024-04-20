import re
import json
from time import sleep
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
                        chunked_string += re.sub("<.+?>", "", m.group(1))  #拔掉POS tag
                    chunked_list.append(chunked_string)  #暫存於chunked_list
                    sleep(0.5)
                        
        with open('../purged_corpus/中研院_{}_chunked.txt'.format(targetSTR),'w',encoding="utf-8") as n: # 將 chunked_list 中的句子寫入 _chunked.txt 檔
            n.write("\n".join(chunked_list))
            print("Success!")
            print("======================================================================================================\n")                        
            
    except Exception as e:
        print("Encountered Error: {}".format(e))


if __name__ == "__main__":
    chunker("須", "front")
    chunker("須", "aft")
    chunker("需", "front")
    chunker("需", "aft")
