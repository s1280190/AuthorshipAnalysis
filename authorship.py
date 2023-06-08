import os
import string
import requests
import nltk
from collections import Counter
from nltk import pos_tag, word_tokenize
from nltk.tokenize import word_tokenize
import numpy as np


folder_path = "DataSet"  # フォルダのパスを指定してください
folder_path2 = "DataSet2"  # 追加のデータセットフォルダのパスを指定してください
# フォルダ内のファイルを取得
files = os.listdir(folder_path)
files2 = os.listdir(folder_path2)

n_Files = sum(file.endswith(".txt") for file in files)
n_Files2 = sum(file.endswith(".txt") for file in files2)

verb_counts = Counter()
noun_counts = Counter()

# 抽出する単語のリストを作成
target_words = ["Adams"]


def Type_rate(file_path):
    with open(file_path, "r") as f:
        file_contents = f.read()
        tokens = word_tokenize(file_contents)
        count_Type = Counter(tokens)
        count_Token = len(tokens)
        if(file_path == os.path.join(folder_path2, file)):
            print(file_path)
            print("Total Token", count_Token)
            print("Total Type", len(count_Type))
            print("Type-Token ratio", (len(count_Type) / count_Token))
            print()
        return [(len(count_Type) / count_Token)]

# ファイルごとに単語のカウントを行う
for file in files:
    if file.endswith(".txt"):
        file_path = os.path.join(folder_path, file)
        with open(file_path, "r") as f:
            contents = f.read()
            contents = contents.lower()  # 大文字と小文字を区別しないように変換
            contents = contents.translate(str.maketrans("", "", string.punctuation))  # 句読点を削除
            words = word_tokenize(contents)  # 単語にトークン化
            tagged_words = pos_tag(words)  # 単語に品詞タグ付け

            for word, tag in tagged_words:
                if tag.startswith("V") and word not in target_words:  # 動詞かつ対象単語でない場合
                    verb_counts[word] += 1
                elif tag.startswith("N") and word not in target_words:  # 名詞かつ対象単語でない場合
                    noun_counts[word] += 1
            # 対象単語が含まれるファイルを抽出
            target_files = []
            for file in files:
                if file.endswith(".txt"):
                    file_path = os.path.join(folder_path, file)
                    with open(file_path, "r") as f:
                        contents = f.read()
                        if any(word in contents for word in target_words):
                            target_files.append(file)

# 追加のデータセットでの判別
adamas_probability = 0.0
adamas_file_path = os.path.join(folder_path2, "Adamas.txt")
if os.path.exists(adamas_file_path):
    with open(adamas_file_path, "r") as f:
        adamas_contents = f.read()
        adamas_contents = adamas_contents.lower()
        adamas_contents = adamas_contents.translate(str.maketrans("", "", string.punctuation))
        adamas_words = word_tokenize(adamas_contents)
        adamas_tagged_words = pos_tag(adamas_words)

        adamas_verb_count = 0
        adamas_noun_count = 0
        total_words = 0

        for word, tag in adamas_tagged_words:
            if tag.startswith("V") and word not in target_words:
                adamas_verb_count += 1
            elif tag.startswith("N") and word not in target_words:
                adamas_noun_count += 1
            total_words += 1

        verb_similarity = adamas_verb_count / (total_words + 1e-10)
        noun_similarity = adamas_noun_count / (total_words + 1e-10)

        adamas_probability = (verb_similarity + noun_similarity) / 2

print("Percentage of DataSet/Adams....txt & DataSet2/Adams.txt are same?")
print(adamas_probability)
if adamas_probability > 70:
    print("High Percent")
else:
    print("Low Percent")
print()

type_rate_1 = [ 0 for i in range(n_Files) ]
type_rate_1_name = [ "" for i in range(n_Files)]
type_rate_2 = [ 0 for i in range(n_Files2) ]
type_rate_2_name = [ "" for i in range(n_Files2)]

# folder_path2内の各ファイルに対してType_rate()を実行
i = 0
for file in files2:
    if file.endswith(".txt"):
        file_path = os.path.join(folder_path2, file)
        type_rate_2_name[i] = file_path
        type_rate_2[i] = Type_rate(file_path)
        i += 1

# folder_path内の各ファイルに対してType_rate()を実行
i = 0
for file in files:
    if file.endswith(".txt"):
        file_path = os.path.join(folder_path, file)
        type_rate_1_name[i] = file_path
        type_rate_1[i] = Type_rate(file_path)
        i += 1


for i in range(n_Files2):
    rate_2 = np.array(type_rate_2[i])
    for j in range(n_Files):
        rate_1 = np.array(type_rate_1[j])
        if abs(np.subtract(rate_2, rate_1)) < 0.005:
            print(type_rate_1_name[j], ": ", rate_1)
            print("\t" + type_rate_1_name[j] + " might be written by the same author as " + type_rate_2_name[i])
    print()

################## VERB ANALYSIS ##################

future_vocabs1 = ['tomorrow', 'weekend']
future_vocabs2 = ['next', 'week', 'month', 'year']

def verb_pre(text, counts):
  sents = nltk.sent_tokenize(text)             ## tokenize input_text as sentences
  verb_analysis(sents, counts)
  return counts

def verb_analysis(sents, counts):
  for s in sents:
    tokens = nltk.word_tokenize(s)             ## tokenize sentence as words
    tagged_tokens = nltk.pos_tag(tokens)       ## POS tagging
    if(judge_future(tokens)) == True:          ## if the sentence is future tense
      for n in range(len(tokens)-1):
        if(tagged_tokens[n][1]=='VBG'):        ## if "**ing"
          counts[0] += 1
          if(tokens[n] == 'going') and (tokens[n+1] == 'to'):
            if(tagged_tokens[n+2][1] == 'VB'): ## if "going to" + verb
              counts[1] += 1
              #print('"' + s + '"' + ' is arranged future.')
            else:                              ## if "going to" + noun, "going to" + "the" + noun, etc.(except verb)
              counts[2] += 1
              #print('"' + s + '"' + ' is planned future.')
          else:                                ## if "**ing" except "going to"
            counts[2] += 1
            #print('"' + s + '"' + ' is planned future.')
  return counts

def judge_future(tokens):                      ## the sentence is future tense or not
  for w in future_vocabs1:                     ## judge the sentence includes "tomorrow" or "weekend" or not
    if(w in tokens):
      return True

  if(not(len(set(tokens) & set(future_vocabs2)) < 2)): ## judge the sentence includes "next week", "next month", or "next year" or not
    return True

def verb(files, folder_path, counts):
  i = 0
  for file in files:
      if file.endswith(".txt"):
          file_path = os.path.join(folder_path, file)
          f = open(file_path,'r')
          input_text = f.read()

          counts[i][0] = file_path
          counts[i][1:4] = verb_pre(input_text, counts[i][1:4])

          if(counts[i][2] > 0):
            print("-------" + file_path + "------")
            print("Number of VBG in future sentence: ", counts[i][1])
            print("arranged future: ", counts[i][2])
            print("planned future:  ", counts[i][3])
            print()

          i += 1
  return counts

print()

counts = [ ["", 0, 0, 0] for i in range(n_Files) ]      
## [file number][File name, number of VBG, number of arranged future, number of planned future]
counts2 = [ ["", 0, 0, 0] for i in range(n_Files2) ]

counts = verb(files, folder_path, counts)
counts2 = verb(files2, folder_path2, counts2)
  

for i in range(n_Files2):                               ## analyse the similarity of using VBG of two texts
  vec_counts2 = np.array(counts2[i][1:4])
  if not(np.linalg.norm(vec_counts2) == 0):
    close_v_similarity_files = []
    far_v_similarity_files = []
    for j in range(n_Files):
      if not (counts[j][1] == 0):
        vec_counts = np.array(counts[j][1:4])
        if not(np.linalg.norm(vec_counts) * np.linalg.norm(vec_counts2) == 0):
          similarity_v = np.dot(vec_counts, vec_counts2)/(np.linalg.norm(vec_counts) * np.linalg.norm(vec_counts2))     ## compute Cosine Similarity of 2 texts
          if(similarity_v > 0.7): 
            close_v_similarity_files.append(counts[j][0])
          elif(similarity_v < -0.7):
            far_v_similarity_files.append(counts[j][0])

    if(close_v_similarity_files):
      print("These files have close Cosine Similarity of using VBG with " + counts2[i][0])
      for k in range(len(close_v_similarity_files)):
        print(" " + close_v_similarity_files[k])
      print()

    if(far_v_similarity_files):
      print("These files have far Cosine Similarity of using VBG with " + counts2[i][0])
      for k in range(len(far_v_similarity_files)):
        print(" " + far_v_similarity_files[k])
      print()

    if not(close_v_similarity_files) and not(far_v_similarity_files):
      print("It couldn't analyse similarity of using VBG in future sentence of " + counts2[i][0] + " and other file")
      print()
  else:
    print("Cosine Similarity of VBG of " + counts2[i][0] + " and other file couldn't compute")
    print()

################ VERB ANALYSIS END ################

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
