from urlextract import URLExtract
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import pandas as pd

def fetch_stats(selected_user,df):
    
    if selected_user != "Overall":
        df = df[df['user'] == selected_user]
    
    #fetch the number =of message
    num_messages = df.shape[0]

    #fetch the number of words
    words = []
    for message in df['message']:
        words.extend(message.split())

    #fetch the number of media sent
    num_media = df[df['message'] == '<Media omitted>\n'].shape[0]

    #fetch the number of links
    links=[]
    ext = URLExtract()

    for message in df['message']:
        links.extend(ext.find_urls(message))

    return num_messages,len(words),num_media,len(links)

def fetch_most_active_user(df):
    x = df['user'].value_counts().head()
    df = round((df['user'].value_counts()/df.shape[0])*100,2).to_frame().rename(columns={'count':'percentage'})
    return x,df

def create_Wordcloud(selscted_user,df):

    if selscted_user != 'Overall':
        df = df[df['user'] == selscted_user]

    words = []
    for word in df['message']:
        if word != '<Media omitted>\n':
            words.append(word)
    df = pd.DataFrame(words, columns=['words'])
    
    wc = WordCloud(width=500,height=500,min_font_size=10,background_color='white')
    df_wc = wc.generate(df['words'].str.cat(sep=" "))
    return df_wc




