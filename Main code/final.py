import pymysql
import pickle
from urllib.request import urlopen
from bs4 import BeautifulSoup
from goose3 import Goose
from textblob import TextBlob
from textblob.classifiers import NaiveBayesClassifier

#Connecting to the database
#Specify the name of the database in db field and password of your localhost in passwd field
db = pymysql.connect(db='',user='root',passwd='',host='localhost',port=3306)
cursor = db.cursor()
db.commit()

#Extracting the headline from the url
def headline(url):
	print(url)
	page = urlopen(url)
	page_read = page.read()
	page.close()
	soup = BeautifulSoup(page_read, "html.parser")
	str_soup = str(soup)
	number1 = int(str_soup.find("<h1")) + 1
	number2 = int(str_soup.find("</h1"))
	str_soup = str_soup[number1:number2]
	while(1):
		if((str_soup.count("<")>0) or (str_soup.count(">")>0)):
			number3 = int(str_soup.find(">")) + 1
			str_soup = str_soup[number3:]
			str_soup = str_soup.strip()
			str_soup = str(str_soup)
		else:
			break
	return str_soup

#Extracting the body from the url
def body(url):
	g = Goose()
	article = g.extract(url=url)
	article = str(article.cleaned_text)
	article = article.replace('"','')
	article = " ".join(article.split())
	article = str(article)
	return article

#Extracting the url from the database
while(1):
	#SELECT attribute from table_name
	url = "SELECT urlname from urldata"
	url = cursor.execute(url)
	db.commit()
	if(url!=0):
		break
url = cursor.fetchone()
url = url[0]
headlines = headline(url)
articles = body(url)

try:
	#Loading the pickle
	f1 = open('cl1.pickle','rb')
	f2 = open('cl2.pickle','rb')
	cl1 = pickle.load(f1)
	cl2 = pickle.load(f2)
	f1.close()
	f2.close()
	print("Pickle Loaded")
except:
	#Pickle file
	f1 = open('cl1.pickle','wb')
	f2 = open('cl2.pickle','wb')

	#Training the classifier on the headline dataset
	with open("dataset1.json", 'r', encoding="utf-8-sig") as fp1:
		cl1 = NaiveBayesClassifier(fp1, format="json")

	#Dumping inside pickle
	pickle.dump(cl1, f1)
	f1.close()

	#Training the classifier on the body dataset
	with open("dataset2.json", 'r', encoding="utf-8-sig") as fp2:
		cl2 = NaiveBayesClassifier(fp2, format="json")

	#Dumping inside pickle
	pickle.dump(cl2, f2)
	f2.close()
	print("Pickle created")


#Taking the string values
str1 = str(headlines)
headline = TextBlob(str1)
body = str(articles)
tb_body = TextBlob(body)
subjectivity = tb_body.sentiment.subjectivity
subjectivity = float(subjectivity) * 100
body_classify = str(cl2.classify(body))
body = body.lower()

#Finding the subjectivity
headline = headline.replace('Was', '')
headline = headline.replace('was', '')
headline = headline.replace('’','')

#Finding the tags in the sentence
array = headline.tags
array1 = []

#Finding the hot words
for ii in array:
	name, tag = ii
	name = str(name)
	name = name.lower()
	if(tag.count('NN')>0):
		name = TextBlob(name)
		array1.append(name)
true = 0
false = 0

#Finding the percent of relativity between the body and the headline
for j in range(0,len(array1)):
	count = body.count(str(array1[j]))
	if(count>0):
		true = true + 1
	else:
		false = false + 1

related = (true/(true+false))*100

#Predicting the result
if(related<=50 and subjectivity<50):
	print("Unrelated")
else:
	print("Related percent: "+str(related))
	print("Predicted class for Headline :"+str(cl1.classify(str1)))
	print("Predicted class for Body Text :"+body_classify)
