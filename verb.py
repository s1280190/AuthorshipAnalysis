import nltk
nltk.download('all')

#f = open('****.txt','r')
#input_text = f.read()

input_text = "I was going there last year. I was going there yesterday. I'm going there now. I'm going there tomorrow. I'm going to go there tomorrow. I'm going to go there next week."
## input text for testing code

counts = [0, 0, 0]                             ## count the number of vbg, arranged_future, and planned_future
future_vocabs1 = ['tonight', 'tomorrow', 'weekend']
future_vocabs2 = ['next', 'week', 'month', 'year']


def verb(text, counts):
  sents = nltk.sent_tokenize(text)             ## tokenize input_text as sentences
  verb_analysis(sents, counts)
  print("Number of VBG: ", counts[0])
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
              print('"' + s + '"' + ' is arranged future.')
            else:                              ## if "going to" + noun, "going to" + "the" + noun, etc.
              counts[2] += 1
              print('"' + s + '"' + ' is planned future.')
          else:                                ## if "**ing" except "going to"
            counts[2] += 1
            print('"' + s + '"' + ' is planned future.')
  return counts


def judge_future(tokens):                      ## the sentence is future tense or not
  for w in future_vocabs1:                     ## judge the sentence includes "tonight", "tomorrow", or "weekend" or not
    if(w in tokens):
      return True

  if(not(len(set(tokens) & set(future_vocabs2)) < 2)): ## judge the sentence includes "next week", "next month", or "next year" or not
    return True
