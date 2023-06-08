import nltk
import os
import string
import requests
from collections import Counter
from nltk import pos_tag, word_tokenize
from nltk.tokenize import word_tokenize

folder_path = "DataSet"  # フォルダのパスを指定してください
folder_path2 = "Dataset2"  # 追加のデータセットフォルダのパスを指定してください
# フォルダ内のファイルを取得
files = os.listdir(folder_path)
files2 = os.listdir(folder_path2)

verb_counts = Counter()
noun_counts = Counter()

# 抽出する単語のリストを作成
target_words = ["Adamas"]

################## ADJECTIVE ANALYSIS START ##################

result = [] # dataset1の結果
adamas_result = [] # dataset2の結果
closest_file = [1000, 'non'] # 最も近い

class AA_adjectives :
  def __init__(self, sentence) :
    self.words_all = word_tokenize(sentence) # txtの文章を読み込む, 全ての単語
    self.words_adjectives = [] # 形容詞のみ
    self.gradable = 0 # gradable adjective
    self.non_gradable = 0 # non-gradable adjective
    self.AdjectivesTagsName = ['JJ', 'JJR', 'JJS'] # 形容詞のタグ
    # non-gradable の形容詞リスト
    self.NonGradableAdjectiveWordList = ['furious', 'terrible', 'awful', 'stunning', 'enormous',
                                         'huge', 'freezing', 'sure', 'insane', 'adrable',
                                         'impossible', 'filthy', 'devastated', 'hilarious', 'amazing',
                                         'perfect', 'incredible', 'fabulous', 'brilliant', 'fantastic',
                                         'marvellous', 'outstanding', 'bolling', 'starving', 'essential',
                                         'critical', 'crucial', 'vital', 'spectacular', 'remarkable',
                                         'magnificent', 'fascinating', 'certain', 'horrible', 'wonderful',
                                         'gorgeous', 'delightful', 'delighted', 'silent', 'outrageous',
                                         'terrified', 'terrifying', 'ridiculous', 'bizarre', 'stunned',
                                         'amazed', 'delicious', 'exhausted', 'appalled', 'disgusting',
                                         'priceless', 'dead']

  def get_tag(self) : # タグつけ
    self.words_all = pos_tag(self.words_all)

  def get_adjective(self) : # 形容詞の抽出
    for word, tag in self.words_all :
      for name in self.AdjectivesTagsName :
        if tag == name :
          self.words_adjectives.append((word, tag))

  def judge(self, file) : # 判定
    for word, tag in self.words_adjectives :
      if (tag == 'JJS') or (tag == 'JJR') :
        self.gradable += 1
      elif word in self.NonGradableAdjectiveWordList :
        self.non_gradable += 1
      else :
        self.gradable += 1
    
    result.append([self.gradable, self.non_gradable, file])

def result_print() :
    for temp in result :
        value = abs((temp[0] * 100 / (temp[0]+temp[1])) - (adamas_result[0] * 100 / (adamas_result[0] + adamas_result[1]))) + abs((temp[1] * 100 / (temp[0]+temp[1])) - (adamas_result[1] * 100 / (adamas_result[0] + adamas_result[1])))
        if value < closest_file[0] :
            closest_file[0] = value
            closest_file[1] = temp[2]
            
    print('---File closest to "Dataset/Adamas.txt"---')
    print('File name', closest_file[1])
    print('Difference : ' + str(closest_file[0]) + ' %')

def execution(sentence, file_path) : # 実行するメソッド
    test = AA_adjectives(sentence)
    test.get_tag()                             # 英単語にタグをつける
    test.get_adjective()                       # 形容詞だけを抽出する
    test.judge(file_path)                               # gradable, non-gradable の判断

def adjective(files, folder_path) :
  for file in files :
    if file.endswith(".txt") :
      file_path = os.path.join(folder_path, file)
      f = open(file_path, 'r')
      input_txt = f.read()
      execution(input_txt, file_path)

print()
print('dataset1')
adjective(files, folder_path)
print('dataset2')
adjective(files2, folder_path2)
adamas_result = result.pop(len(result)-1)
result_print()
################ ADJECTIVE ANALYSIS END ################
