#!/usr/bin/env python
# coding: utf-8

# In[1]:


#description: This is a 'smart' chat bot program


# In[25]:


get_ipython().system('pip install nltk')


# In[26]:


get_ipython().system('pip install newspaper3k')


# In[27]:


from newspaper import Article 
import random
import string
import nltk
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import warnings
warnings.filterwarnings('ignore')


# In[28]:


#Download the punkt package
nltk.download('punkt',quiet=True)


# In[29]:


#Get the article
article=Article('https://www.mayoclinic.org/diseases-conditions/chronic-kidney-disease/symptoms-causes/syc-20354521')
article.download()
article.parse()
article.nlp()
corpus=article.text


# In[8]:


#print the articles text
print(corpus)


# In[30]:


#Tokenization 
text=corpus
sentence_list= nltk.sent_tokenize(text) # a list of sentence


# In[31]:


#print the list of Sentences 
print(sentence_list)


# In[32]:


# A function to return a random greeting response to a users greeting
def greeting_response(text):
    text= text.lower()
    
    #both greeting response
    bot_greetings=['howdy','hi','hey','hello','hola']
    #user greeting
    user_greetings=['hi','hey','hello','hola','greetings','wassup']
    
    
    for word in text.split():
        if word in user_greetings:
            return random.choice(bot_greetings)
    


# In[13]:


def index_sort(list_var):
    length = len(list_var)
    list_index=list(range(0, length))
    
    x = list_var
    for i in range(length):
        for j in range(length):
            if x[list_index[i]]> x[list_index[j]]:
                #swap
                temp = list_index[i]
                list_index[i] = list_index[j]
                list_index[j] = temp
    return list_index


# In[38]:


#create the bots response
def bot_response(user_input):
    user = user_input.lower()
    sentence_list.append(user_input)
    bot_response=''
    cm = CountVectorizer().fit_transform(sentence_list)
    similarity_scores = cosine_similarity(cm[-1],cm)
    similarity_scores_list = similarity_scores.flatten()
    index = index_sort(similarity_scores_list)
    index=index[1:]
    response_flag = 0
    
    j=0
    for i in range(len(index)):
        if similarity_scores_list[index[i]]>0.0:
            bot_response = bot_response+' '+sentence_list[index[i]]
            response_flag=1
            j = j+1
        if j>2:
            break
    if response_flag==0:
        bot_response=bot_response+' '+"I apologize, I don't understand what you say."
    sentence_list.remove(user_input)
    
    return bot_response


# In[39]:


#Start the Chat
print('Doc Bot: I am doctor Bot for short period of time to help you. I will answer all your query regarding Chronic Kidney Diseases. If you want to exit, type bye.')

exit_list = ['exit','see you later','bye','quit','break']

while(True):
    user_input= input()
    if user_input.lower() in exit_list:
        print('Doc Bot: Chat with you later!')
        break
    else:
        if greeting_response(user_input) != None:
            print('Doc Bot: '+greeting_response(user_input))
        else:
            print('Doc Bot: '+bot_response(user_input))


# In[ ]:




