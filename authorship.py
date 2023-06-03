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
  #print("Number of VBG in future sentence: ", counts[0])
  #print("arranged future: ", counts[1])
  #print("planned future:  ", counts[2])
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

          #print("-------" + file_path + "------")
          counts[i][0] = file_path
          counts[i][1:4] = verb_pre(input_text, counts[i][1:4])
          #print()
          i += 1
  return counts

print()
n_Files = sum(file.endswith(".txt") for file in files)
n_Files2 = sum(file.endswith(".txt") for file in files2)
counts = [ ["", 0, 0, 0] for i in range(n_Files) ]      ## [file number][File name, number of VBG, number of arranged future, number of planned future]
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
      print("It couldn't analyse similarity of using VBG in future sentence")
      print()
  else:
    print("Cosine Similarity of " + counts2[i][0] + " couldn't compute")
    print()

################ VERB ANALYSIS END ################

################## ADJECTIVE ANALYSIS START ##################

class AA_adjectives :
  def __init__(self) :
    self.words_all = [] # 全ての単語
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

  def judge(self) : # 判定
    for word, tag in self.words_adjectives :
      if (tag == 'JJS') or (tag == 'JJR') :
        self.gradable += 1
      elif word in self.NonGradableAdjectiveWordList :
        self.non_gradable += 1
      else :
        self.gradable += 1

  def result_print(self) : # 結果の出力
    print("-------" + file_path + "------")
    print('  gradable adjective   : ', self.gradable)
    print('non-gradable adjective : ', self.non_gradable)
    print()

def execution(sentence) : # 実行するメソッド
  test = AA_adjectives()
  test.words_all = word_tokenize(sentence) # txtの文章を読み込む
  test.get_tag()                             # 英単語にタグをつける
  test.get_adjective()                       # 形容詞だけを抽出する
  test.judge()                               # gradable, non-gradable の判断
  test.result_print()                         # 結果を出力

def adjective(files, folder_path) :
  for file in files :
    if file.endswith(".txt") :
      file_path = os.path.join(folder_path, file)
      f = open(file_path, 'r')
      input_txt = f.read()
      execution(input_txt)

print()
adjective(files, folder_path)
adjective(files2, folder_path2)
################ ADJECTIVE ANALYSIS END ################
