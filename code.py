import tweepy
import re
import csv
from textblob import TextBlob
import matplotlib.pyplot as plt
import tkMessageBox
from Tkinter import *

def clean_tweet(tweet):
	str1=tweet.split(" ")
	j=0
	for word in str1:
		fileName="data.csv"
		with open(fileName,"r") as my:
			data=csv.reader(my,delimiter=",")
			word=re.sub(r'(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)',"", word)	
			for row in data:
				if word.lower() == row[0]:
					str1[j]=row[1]
				else:
					continue
			my.close()
		j+=1
	tweet=' '.join(str1)
	return tweet

def extractsentiment():
  if((E1.get())=='' or (E2.get())==''):
    tkMessageBox.showerror("WARNING","Fill all the information properly")
  else:
    consumer_key='**********************************' 
    consumer_secret='*****************************************' 
    access_token='****************************************' 
    access_token_secret='******************************'

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    api = tweepy.API(auth)
    sentiment='' 
    p=n=ne=0
    pt=[]
    net=[]
    nt=[]
    query=E1.get()
    cnt=num.get()
    if(cnt==0):
      cnt=20
    public_tweets = api.search(q=query,count=cnt)
    for tweet in public_tweets:
        #data preprocessing
        str1=clean_tweet(tweet.text)        
	#Polarity determination and sentiment calculation
        analysis = TextBlob(str1)
        if analysis.sentiment.polarity > 0:
                sentiment='positive'
                p=p+1                
		pt.append(tweet.text)         
        elif analysis.sentiment.polarity == 0:
                sentiment='neutral'
                ne=ne+1
		net.append(tweet.text)
        else:
                sentiment='negative'
                n=n+1
                nt.append(tweet.text)
    print("\n***********************Positive Tweets***************************\n")
    for tweet in pt[:5]:
	print("#"+tweet)
	
    print("\n***********************Negative Tweets***************************\n")
    for tweet in nt[:5]:
	print("#"+tweet)

    print("\n***********************Neutral Tweets***************************\n")
    for tweet in net[:5]:
	print("#"+tweet)
	
    #data visualization
    plt.pie([p,ne,n],labels=['Positive','Neutral','Negative'],startangle=90,colors=['blue','green','red'],explode=[.1,0.1,0.1],autopct="%1.1f%%",shadow=True,pctdistance=0.5)
    plt.title("Twitter Sentiment Analysis");
    plt.show()
    exit()
   
   

root =Tk()
#label=Label(root, text="TWITTER SENTIMENT ANALYSIS")
#label.pack()
canvas=Canvas(root,width=1000,height=500)
canvas.pack()
my_image=PhotoImage(file='/home/prasanna/Downloads/images2.png')
canvas.create_image(400,150,anchor= NW,image=my_image)
canvas.create_text(550,80,text="TWITTER SENTIMENT ANALYSIS",font=('Times New Roman',25))
label1=Label(root, text="SEARCH QUERY")
E1=Entry(root,bd=5)
label2=Label(root,text="ENTER NO. OF TWEETS")
num=IntVar()
E2=Entry(root,bd=5,textvariable=num)
submit=Button(root,text="SUBMIT",command=extractsentiment)

label1.pack()
E1.pack()
label2.pack()
E2.pack()
submit.pack()

root.mainloop()


