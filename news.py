import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime as dt
import time
from pandas import option_context

def news(OLD_NEWS):
    p = 'https://www.inn.co.il/flashes'
    r = requests.get(p)
    soup = BeautifulSoup(r.content)
    soup = soup.find_all('div', {'class':"accordeon-item__header"} )
    
    for div in soup:
        if div.text not in OLD_NEWS:
            OLD_NEWS = [div.text] + OLD_NEWS # i want the most new to be first
            #print (div.text)
    return OLD_NEWS

frequency = st.slider('How often do you want the news to be updated (in seconds):', 1, 60)

LAST_NEWS = []
while True:
    LAST_NEWS_TEST = news(LAST_NEWS)
    if LAST_NEWS != LAST_NEWS_TEST:
        LAST_NEWS = LAST_NEWS_TEST
        df = pd.DataFrame([ LAST_NEWS[i].split("\n")[0:2] for i in range(0,len(LAST_NEWS_TEST))],columns=['time','news'])
        reversed_df = df.iloc[::-1]

        st.dataframe( reversed_df.head(15) )

    time.sleep(frequency)

