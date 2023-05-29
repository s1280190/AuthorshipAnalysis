import nltk
import requests
from nltk.tokenize import word_tokenize
from collections import Counter

# 文章を定義
def Type_rate():
 txt = [#txtdataをいれる]
 combined_sentence = ' '.join(txt)
 count_Type = 0

 wordlist = []
 # 各文章のトークンとタイプを分析
     # 文章をトークン化
 tokens = word_tokenize(combined_sentence)
 count_Type = Counter(tokens)
 count_Token = len(tokens)
     # 結果を表示
 for token in tokens:
       print(f"Token: {token}")
     
 print()  # 文章ごとに改行するための空行の出力 

 print("Total Token",count_Token)    
 print("Total Type",len(count_Type))
 print("Type-Token ratio",(len(count_Type)/count_Token))
