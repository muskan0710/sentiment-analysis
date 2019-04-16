
import json
import csv
from nltk.tokenize import word_tokenize
import string
import re
import time
import pandas as pd


tweets_data = []
x = []
y = []
k = []
m = []

print("Starting Preprocess Function")
print("\n")

def getdata(dataurl):
    
    print("Retrieving the csv file")
    tweets_data_path = dataurl
    tweets_file = open(tweets_data_path, "r")
    for line in tweets_file:
        try:
            tweet = json.loads(line)
            tweets_data.append(tweet)
        except:
            continue

    print("Retrieving Successfull")
    print(" \n")
    #time.sleep(3)
    processdata()


def processdata():
   
    print("Recovering Data Tweets")
   
    #time.sleep(1)
    RE_EMOJI = re.compile('[\U00010000-\U0010ffff]', flags=re.UNICODE)
    for i in range(len(tweets_data)):
        q = tweets_data[i]['text']
        o = tweets_data[i]['id_str']
        q = RE_EMOJI.sub(r'', q)
        i = q.translate(str.maketrans('','',string.punctuation))
        x.append(i)
        k.append(o)

    print("Data Tweets Recovered")
    print("\n")
    
    
    
def readdict(dataurl):
    print("Reading Dictionary")
    with open(dataurl) as csvfile:
      reader = csv.reader(csvfile, delimiter='\t')
      for row in reader:
          i = []
          i.append(row[2])
          i.append(row[5])
          y.append(i)
    print("Dictionary Preparation Done")
    print("\n")  
    addpolarity()

def addpolarity():  
    start_time = time.time()
    counter = 0
  
    print("Processing please wait...")
    print("\n")
    
    
    
    for j in x:
 
            tweet_token = j
            token = word_tokenize(tweet_token)
            sumnum = 0
            sum_word = 0
            for t in token:
     
                for d in y:
                    if t == d[0]:
                        sentiment = d[1]
                        if sentiment == "positive":
                            sumnum += 1
                            sum_word += 1

                        elif sentiment == "negative":
                            sumnum += -1
                            sum_word += 1

                        else:
                            sumnum += 0
                            sum_word += 1


                        break
                 
            
            if sum_word != 0.0:
                sum_more = sumnum / sum_word
                if sum_more >= 0.2:
                    sum_more = 1
   
                elif (sum_more < 0.2) and (sum_more > -0.5):
                    sum_more = 0
                   
                elif sum_more <= -0.5:
                    sum_more = -1
                   
                else:
                    print("*")
                    
                
            sum_var = []    
            varid = k[counter]
            sum_var.append(varid)
            sum_var.append(sum_more)
            m.append(sum_var)
            counter += 1
            
    print("Processing time: ", round((time.time() - start_time),8), "Seconds \n\n")
    
   # time.sleep(3)
        
   
    print("Processing Finish")
   
    
    for i in m:
        print(i)
        print
    
    df = pd.DataFrame(m)
    df.columns=['id','sentiment']
    df.head()
    df.to_excel('output.xlsx', index=False)
    print("Data Saved!")
   
    

def runall():
    getdata('Extract.csv')
    readdict('dictionary.csv')
    


runall()