import nltk
import requests
from nltk.tokenize import word_tokenize
from collections import Counter

# 文章を定義

url = ["Hello, how are you today?","we are UoA student"]
combined_sentence = ' '.join(url)
count_Token = 0

wordlist = []
# 各文章のトークンとタイプを分析
    # 文章をトークン化
tokens = word_tokenize(combined_sentence)
count_Token = Counter(tokens)
count_Type = len(tokens)
    # 結果を表示
for token in tokens:
      print(f"Token: {token}")
     
print()  # 文章ごとに改行するための空行の出力

print("Total Token",count_Type)    
print("Total Type",len(count_Token))
print("Type-Token ratio",(len(count_Token)/count_Type))
