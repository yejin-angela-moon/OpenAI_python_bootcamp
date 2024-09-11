#!/usr/bin/env python
# coding: utf-8

# In[2]:


get_ipython().system('pip3 install openai')
import pandas as pd
import os 
from openai import OpenAI


# In[3]:


pip3 install --upgrade pip


# In[ ]:


get_ipython().system('pip3 install --upgrade pip')


# In[9]:


df = pd.read_excel("adidas_sales_dataset.xlsx")
df.head(5)


# In[10]:


get_ipython().system('pip3 install openpyxl')


# In[11]:


df = pd.read_excel("adidas_sales_dataset.xlsx")
df.head(5)


# In[ ]:





# In[ ]:


df.rows


# In[ ]:


df.columns


# In[12]:


df.columns = [col.replace(' ', '_') for col in df.columns]


# In[13]:


df.columns


# In[ ]:


# It is basic for data analysis to use 'groupby' to check the data
# sum of sales by region
df.groupby("Region").sum(numeric_only=True)['Total_Sales'].sort_values(ascending=False)


# In[ ]:





# In[14]:


get_ipython().system('pip3 install sqlalchemy')


# In[15]:


from sqlalchemy import create_engine #임시 데이터베이스 만듦
from sqlalchemy import text


# In[16]:


temp_db = create_engine('sqlite:///:memory:', echo=True) # in-house db, or temp db


# In[17]:


#tabluate df (data frame)
data = df.to_sql(name='Sales', con=temp_db)


# In[18]:


with temp_db.connect() as conn:
    result = conn.execute(text("SELECT Retailer, City, State, Total_Sales, Operating_Profit from Sales ORDER BY Total_Sales DESC LIMIT 1"))
# Inside the text goes the SQL query


# In[19]:


result.all()
# To see the result


# In[ ]:


# To process natural language commands to SQL statement, we need processing functions
# 1. Function to let us know the table structure when using OpenAI API
# 2. Function to bring the natural language commands inputted from the user
# 3. Function to bring the prompt result for API call


# In[20]:


os.environ['OPENAI_API_KEY'] = 'sk-U1OIvrznf-vTSQIfoqzHoAmwKxQJu2LURge2SdIT6zT3BlbkFJUrQuElM8oqUCNClAcH18yexa1LZFnk_Mvpjta-KLsA'
client = OpenAI()


# In[21]:


# GPT 한테 우리가 다루는 데이터, 테이블이 어떤 구조인지 알려주는 함수
def table_definition_prompt(df):
    prompt = '''Given following sqlite SQL definition,
                write queries based on the request
                \n### sqlite SQL table, with its properties:
    #
    # Sales({})
    #
    '''.format(",".join(str(x) for x in df.columns))

    return prompt


# In[22]:


print(table_definition_prompt(df))


# In[23]:


# 사용자로부터 어떤 걸 확인하고 싶은지 받는 내용의 함수

def prompt_input():
    nlp_text = input("질의 하고자 하는 내용을 입력해주세요: ")
    return nlp_text


# In[24]:


nlp_text = prompt_input()


# In[29]:


full_prompt = str(table_definition_prompt(df)) + str(nlp_text)
full_prompt


# In[35]:


response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are an assisntant that generates SQL queries based on the given SQLite table definition and a natural language request. The query should start with 'SELECT' and end with a semicolon(;)"},
        {"role": "user", "content": f"A query to answer: {full_prompt}"},
    ],
    max_tokens=200,
    temperature=1.0, #생성되는 응답의 창의성(0-1)
    stop=None
)


# In[36]:


response


# In[39]:


# response에서 필요한 부분만 추출해보자
response.choices[0].message.content
# print해가면서 찾아가기 


# In[42]:


def handle_response(response):
    query = response.choices[0].message.content.strip()

    if not query.upper().startswith("SELECT"):
        query = "SELECT " + query

    if not query.endswith(";"):
        query += ";"

    return query


# In[43]:


print(handle_response(response))


# In[44]:


with temp_db.connect() as conn:
    result = conn.execute(text(handle_response(response)))


# In[45]:


result.all()


# In[ ]:




