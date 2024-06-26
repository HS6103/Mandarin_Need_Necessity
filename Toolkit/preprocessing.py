#!/user/bin/env python
# -*- coding: utf-8 -*-

import re
import json
from ArticutAPI import Articut
from collections import OrderedDict

with open("account.info", encoding="utf-8") as f:
    accountDICT = json.load(f)
articut = Articut(username=accountDICT["username"], apikey=accountDICT["api_key"])

# 讀取 re
with open("corpus_op_re.json","r",encoding="utf-8") as e:
    corpus_op_re = json.load(e)
regexLIST = list(corpus_op_re.items())

with open("corpus_chunk_re.json","r",encoding="utf-8") as c:
    corpus_chunk_re = json.load(c)
chunk_regexLIST = dict(corpus_chunk_re.items())

# 處理無意義標點符號及空格
def rm_marks(inputLIST): 
    inputLIST = [item.replace("」", "", 1) if item.startswith("」") else item for item in inputLIST] 
    inputLIST = [item.replace("「", "", 1) if item.startswith("「") and "」" not in item[1:] else item for item in inputLIST]
    inputLIST = [item.replace("」", "", 1) if "」" in item and "「" not in item else item for item in inputLIST]
    inputLIST = [item.replace("「", "", 1) if "「" in item and "」" not in item else item for item in inputLIST]
    inputLIST = [item.replace("、", "", 1) if item.startswith("、") else item for item in inputLIST]
    inputLIST = [item.replace("\t","").replace("\s","").replace(" ","") for item in inputLIST]
    
    return inputLIST

# 依 re 處理語料並寫入 _purged.txt 檔
def sinica_purger(i, targetSTR):
    print('*** Now Processing："{}"... ***'.format(targetSTR)+"\n")
    with open('../purged_corpus/中研院_{}_purged.txt'.format(targetSTR), 'w') as g: # 新增空的 .txt 檔，若有相同檔案會將之清空
        pass    
    with open('../raw_corpus/sinica/中研院_{}.txt'.format(targetSTR),encoding="utf-8") as f: # 配合 sinica 格式將 raw 語料重新依 'more\n' 切分
        raw = ''.join(f.readlines())
        rawLIST = raw.split('more\n') 
        rawLIST = list(OrderedDict.fromkeys(rawLIST)) # 移除相同語料
    corpusLIST = [] 
    lineCount = 1 
    for j in rawLIST:  
        purgeLIST = re.findall(r'{}'.format(regexLIST[i][1]), j) # 抽取含有標的詞彙的句子
        purgeLIST = [item.replace('\n', '') for item in purgeLIST] # 處理句子被 "\n" 切開的情形
        purgeLIST = rm_marks(purgeLIST) # 處理無意義標點符號及空格
        corpusLIST.extend(purgeLIST) # 將批次處理切分後的句子放入 corpusLIST
        print("{}. {} ==> {}".format(lineCount, j, purgeLIST)) # 此處將顯示 {句數}. {raw 語料} ==> {取出部分}
        lineCount += 1
    corpusLIST = list(OrderedDict.fromkeys(corpusLIST)) # 移除相同句子 
    with open('../purged_corpus/中研院_{}_purged.txt'.format(targetSTR),'a',encoding="utf-8") as g: # 將 corpusLIST 中的句子寫入 _purged.txt 檔
        g.write("\n".join(corpusLIST))
        g.write("\n\n"+'"{}"：Total {} lines.'.format(targetSTR, len(corpusLIST))) # 計算總句數
        print("\n"+'"{}"：Total {} lines.'.format(targetSTR, len(corpusLIST)))
        print("======================================================================================================")
        
def chunker(targetSTR, mode):
    chunked_list = []
    userDefined = "./UserDefinedFile.json"
    
    with open('../purged_corpus/中研院_{}_chunked.txt'.format(targetSTR),'w',encoding="utf-8") as n: # 將 corpusLIST 中的句子寫入 _purged.txt 檔
        pass
    with open('../purged_corpus/中研院_{}_purged.txt'.format(targetSTR),'r',encoding="utf-8") as g:
        s_list = g.readlines()
        pat = chunk_regexLIST["{}".format(mode)]
        for sentence in s_list:
            resultDICT = articut.parse(sentence, level='lv2', userDefinedDictFILE=userDefined)
            m = re.search(pat, resultDICT["result_pos"][0])
            print(m)
                
            if m == None:
                pass
            else:
                chunked_string = ""
                chunked_string += re.sub("<.+?>", "", m.group(0))
                chunked_list.append(chunked_string)
                    
    with open('../purged_corpus/中研院_{}_chunked.txt'.format(targetSTR),'w',encoding="utf-8") as n: # 將 chunked_list 中的句子寫入 _chunked.txt 檔
        n.write("\n".join(chunked_list))
    
        
# 為了方便了解執行狀態，main() 中在執行 sinica_purger() 時，會同步顯示標的詞彙狀態。 
def main(i):
    targetSTR =  regexLIST[i][0]
    resultDICT = {
        "需_status":True, # 依標的詞彙為單位執行 sinica_purger()
        "須_status":True
    }
    try:
        sinica_purger(i, targetSTR)
        chunker(targetSTR, "front")
        chunker(targetSTR, "aft")
    except Exception as e: # 若遇到錯誤，會將錯誤訊息回傳。
        resultDICT["{}_status".format(regexLIST[i][0])] = False
        print(r"Error occurred when processing '{}': {}.".format(targetSTR, type(e).__name__))
        
    return resultDICT

# 執行
if __name__ == "__main__":
    for i in range(len(corpus_op_re)):
        main(i)
