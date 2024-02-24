#!/usr/bin/env python\3
# -*- coding:utf-8 -*-
import json
import pprint
from ArticutAPI import Articut

with open("account.info", encoding="utf-8") as f:
    accountDICT = json.load(f)
articut = Articut(username=accountDICT["username"], apikey=accountDICT["api_key"])

with open ("../purged_corpus/中研院_須_purged.txt", mode="r", encoding="utf-8") as p:
    inputSTR = p.read()
    resultDICT = articut.parse(inputSTR, level='lv1')
    verbStemLIST = articut.getVerbStemLIST(resultDICT)
    pprint(verbStemLIST)    