#データセットをかく
########




#########
import nltk
import urllib.request
import os
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist
from nltk.corpus import stopwords

nltk.download('stopwords') #stopwordの機能をダウンロード
nltk.download('punkt') #分かち書きの機能をダウンロード
##nltk.download('all') #すべての機能をダウンロード

urls = [
    'file://' + os.path.abspath('/Ghahramani-2015-Nature.txt'),
    'file://' + os.path.abspath('/2009.11087.txt')
]  
texts = []
freqdists = []

stop_words = set(stopwords.words('english')) #stopword を適応して is am のような最頻出語句を摘出する

for data in urls: #　texts　に　urls　の内容を入れる
    response = urllib.request.urlopen(data)
    textdata = response.read().decode('utf-8')
    texts.append(textdata)
    
for text in texts: #texts で使われている語句の回数をカウント
    tokens = word_tokenize(text)
    words = [word.lower() for word in tokens if word.isalpha() and word.lower() not in stop_words]
    freqdists.append(FreqDist(words))

errors = [] #分析精度の計算
for i in range(len(freqdists)):
    for j in range(i+1, len(freqdists)):
        error = 0
        for word, count in freqdists[i].items():
            error += abs(count - freqdists[j].get(word, 0))
        errors.append(error)

avg_error = sum(errors) / len(errors)

if avg_error < 100:
    print("These authors have similar writing styles.")
else:
    print("These authors have distinct writing styles.")
