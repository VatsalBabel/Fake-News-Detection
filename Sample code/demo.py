from textblob import TextBlob
from textblob.classifiers import NaiveBayesClassifier

'''
Article Reference- 
http://www.thehindu.com/news/national/naidu-cancels-dinner-for-mps-over-frequent-disruptions-in-rajya-sabha/article23303375.ece?homepage=true

This sample code tests for the news article with-

Headline:
Venkaiah Naidu cancels dinner for MPs over frequent disruptions in Rajya Sabha

Body Content:
With the Rajya Sabha not functioning for the twelfth working day in a row, Chairman M. Venkaiah Naidu called off the dinner for the members of the Upper House on Wednesday. The Opposition parties also met at 10 a.m. on Tuesday to end the stalemate. However, protests by the AIADMK and TDP continued unabated. Efforts were made by the Opposition parties to end the stalemate. Their leaders met at 10 on Tuesday morning to discuss the floor strategy in the Rajya Sabha. It was the first Opposition meeting after Parliament reconvened for the second part of the Budget session. The meeting was attended by the Congress, Trinamool Congress, DMK, Left Front and the BSP, among other parties. According to sources, it was decided that Leader of Opposition Ghulam Nabi Azad would speak to put the Opposition’s willingness to run the House on record. They also reached out to the AIADMK requesting them for to halt their protests for a few minutes so that Mr. Azad could speak. But the AIADMK, despite its assurance, did not stick to its word. After the meeting, the leaders also met Mr. Naidu to convey that the Opposition wanted the House to run and said they specifically wanted to discuss three issues: bank scams, special package for Andhra Pradesh and the Cauvery Management Board. Minister of State for Parliamentary Affairs Vijay Goel assured them of the Government’s support. He also sought the Opposition’s help to pass the Prevention of Corruption (Amendment) Bill. Despite the talks, the protests by members of the AIAMDK, TDP and others continued unabated in the House and the Rajya Sabha could not transact any business. “Opposition wants Parliament to run. But it can’t run because a government on the run is running away, and deliberately not allowing the House to run. In fact the only thing the government is running is circles around democracy,” TMC floor leader Derek O’ Brien said. Congress leaders too rued that there have been back-channel talks by the Government to placate the AIADMK and TDP, whose protests have been stalling functioning of the Rajya Sabha. Mr. Naidu has repeatedly aired his anguish on the disruptions. Last week, he had refused to inaugurate a badminton tournament for MPs at the Constitution Club in protest.
'''

#headline
headline = "Venkaiah Naidu cancels dinner for MPs over frequent disruptions in Rajya Sabha"

#body
body = "With the Rajya Sabha not functioning for the twelfth working day in a row, Chairman M. Venkaiah Naidu called off the dinner for the members of the Upper House on Wednesday. The Opposition parties also met at 10 a.m. on Tuesday to end the stalemate. However, protests by the AIADMK and TDP continued unabated. Efforts were made by the Opposition parties to end the stalemate. Their leaders met at 10 on Tuesday morning to discuss the floor strategy in the Rajya Sabha. It was the first Opposition meeting after Parliament reconvened for the second part of the Budget session. The meeting was attended by the Congress, Trinamool Congress, DMK, Left Front and the BSP, among other parties. According to sources, it was decided that Leader of Opposition Ghulam Nabi Azad would speak to put the Opposition’s willingness to run the House on record. They also reached out to the AIADMK requesting them for to halt their protests for a few minutes so that Mr. Azad could speak. But the AIADMK, despite its assurance, did not stick to its word. After the meeting, the leaders also met Mr. Naidu to convey that the Opposition wanted the House to run and said they specifically wanted to discuss three issues: bank scams, special package for Andhra Pradesh and the Cauvery Management Board. Minister of State for Parliamentary Affairs Vijay Goel assured them of the Government’s support. He also sought the Opposition’s help to pass the Prevention of Corruption (Amendment) Bill. Despite the talks, the protests by members of the AIAMDK, TDP and others continued unabated in the House and the Rajya Sabha could not transact any business. “Opposition wants Parliament to run. But it can’t run because a government on the run is running away, and deliberately not allowing the House to run. In fact the only thing the government is running is circles around democracy,” TMC floor leader Derek O’ Brien said. Congress leaders too rued that there have been back-channel talks by the Government to placate the AIADMK and TDP, whose protests have been stalling functioning of the Rajya Sabha. Mr. Naidu has repeatedly aired his anguish on the disruptions. Last week, he had refused to inaugurate a badminton tournament for MPs at the Constitution Club in protest."

#Training the classifier on the headline dataset
with open("dataset1.json", 'r', encoding="utf-8-sig") as fp1:
	cl1 = NaiveBayesClassifier(fp1, format="json")

#Training the classifier on the body dataset
with open("dataset2.json", 'r', encoding="utf-8-sig") as fp2:
	cl2 = NaiveBayesClassifier(fp2, format="json")

#Taking the string values
str1 = str(headline)
headline = TextBlob(str1)
body = str(body)
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


#Related percent: 87.5
#Predicted class for Headline :discuss
#Predicted class for Body Text :discuss
