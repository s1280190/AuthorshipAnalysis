from nltk import pos_tag
from nltk import word_tokenize

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
