import os
import string
import requests
import nltk
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


def Type_rate(file_path):
    with open(file_path, "r") as f:
        file_contents = f.read()
        tokens = word_tokenize(file_contents)
        count_Type = Counter(tokens)
        count_Token = len(tokens)
        print("Total Token", count_Token)
        print("Total Type", len(count_Type))
        print("Type-Token ratio", (len(count_Type) / count_Token))


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

# folder_path2内の各ファイルに対してType_rate()を実行
for file in files2:
    if file.endswith(".txt"):
        file_path = os.path.join(folder_path2, file)
        Type_rate(file_path)


################## VERB ANALYSIS ##################

future_vocabs1 = ['tomorrow', 'weekend']
future_vocabs2 = ['next', 'week', 'month', 'year']

def verb_pre(text, counts):
  sents = nltk.sent_tokenize(text)             ## tokenize input_text as sentences
  verb_analysis(sents, counts)
  print("Number of VBG in future sentence: ", counts[0])
  print("arranged future: ", counts[1])
  print("planned future:  ", counts[2])
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

def verb(files, folder_path):
  for file in files:
      if file.endswith(".txt"):
          counts = [0, 0, 0]
          file_path = os.path.join(folder_path, file)
          f = open(file_path,'r')
          input_text = f.read()

          print("-------" + file_path + "------")
          counts = verb_pre(input_text, counts)
          print()

print()
verb(files, folder_path)
verb(files2, folder_path2)

################ VERB ANALYSIS END ################
