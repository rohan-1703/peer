#!/usr/bin/env python
# coding: utf-8

# In[1]:


get_ipython().system('pip install yfinance')
get_ipython().system('pip install plotly')


# In[2]:


get_ipython().system('pip install yfinance')
#!pip install pandas
#!pip install requests
get_ipython().system('pip install bs4')
#!pip install plotly


# In[3]:


import yfinance as yf
import pandas as pd
import requests
from bs4 import BeautifulSoup
import plotly.graph_objects as go
from plotly.subplots import make_subplots


# In[4]:


def make_graph(stock_data, revenue_data, stock):
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, subplot_titles=("Historical Share Price", "Historical Revenue"), vertical_spacing = .3)
    fig.add_trace(go.Scatter(x=pd.to_datetime(stock_data.Date, infer_datetime_format=True), y=stock_data.Close.astype("float"), name="Share Price"), row=1, col=1)
    fig.add_trace(go.Scatter(x=pd.to_datetime(revenue_data.Date, infer_datetime_format=True), y=revenue_data.Revenue.astype("float"), name="Revenue"), row=2, col=1)
    fig.update_xaxes(title_text="Date", row=1, col=1)
    fig.update_xaxes(title_text="Date", row=2, col=1)
    fig.update_yaxes(title_text="Price ($US)", row=1, col=1)
    fig.update_yaxes(title_text="Revenue ($US Millions)", row=2, col=1)
    fig.update_layout(showlegend=False,
    height=900,
    title=stock,
    xaxis_rangeslider_visible=True)
    fig.show()


# In[5]:


tesla = yf.Ticker('TSLA')


# In[6]:


tesla_data = tesla.history(period="max")


# In[7]:


tesla_data.reset_index(inplace=True)
tesla_data.head()


# In[8]:


url = 'https://www.macrotrends.net/stocks/charts/TSLA/tesla/revenue'
html_data = requests.get(url).text


# In[9]:


soup = BeautifulSoup(html_data,"html5lib")


# In[10]:


tesla_revenue = pd.DataFrame(columns=['Date', 'Revenue'])

for table in soup.find_all('table'):

    if ('Tesla Quarterly Revenue' in table.find('th').text):
        rows = table.find_all('tr')
        
        for row in rows:
            col = row.find_all('td')
            
            if col != []:
                date = col[0].text
                revenue = col[1].text.replace(',','').replace('$','')

                tesla_revenue = tesla_revenue.append({"Date":date, "Revenue":revenue}, ignore_index=True)


# In[11]:


tesla_revenue


# In[12]:


tesla_revenue = tesla_revenue[tesla_revenue['Revenue'].astype(bool)]


# In[13]:


tesla_revenue.tail()


# In[14]:


gme = yf.Ticker('GME')


# In[16]:


gme_data = gme.history(period='max')


# In[17]:


gme_data.reset_index(inplace=True)
gme_data.head()


# In[18]:


url = 'https://www.macrotrends.net/stocks/charts/GME/gamestop/revenue'
html_data = requests.get(url).text


# In[19]:


soup = BeautifulSoup(html_data,"html5lib")


# In[20]:


gme_revenue = pd.DataFrame(columns=['Date', 'Revenue'])

for table in soup.find_all('table'):

    if ('GameStop Quarterly Revenue' in table.find('th').text):
        rows = table.find_all('tr')
        
        for row in rows:
            col = row.find_all('td')
            
            if col != []:
                date = col[0].text
                revenue = col[1].text.replace(',','').replace('$','')

                gme_revenue = gme_revenue.append({"Date":date, "Revenue":revenue}, ignore_index=True)


# In[21]:


gme_revenue.tail()


# In[22]:


make_graph(tesla_data[['Date','Close']], tesla_revenue, 'Tesla')


# In[23]:


make_graph(gme_data[['Date','Close']], gme_revenue, 'GameStop')


# In[ ]:




