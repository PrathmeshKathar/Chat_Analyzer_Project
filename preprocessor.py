import re
import pandas as pd

def preprocess(data):
    pattern = '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}(?:\s?[apAP][mM])?\s*-\s'

    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern,data)

    df = pd.DataFrame({'user_message':messages,'message_date':dates})
    df['message_date'] = df['message_date'].str.replace('\u202f', ' ', regex=True).str.strip()
    df['message_date'] = pd.to_datetime(df['message_date'], format='%d/%m/%y, %I:%M %p -')

    users = []
    messages = []
    for message in df['user_message']:
        entry = re.split(r'^(.+?):\s', message)
        if entry[1:]:
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append('group_notification')
            messages.append(entry[0])

    df['user'] = users
    df['message'] = messages
    df.drop(columns=['user_message'],inplace=True)

    df['year'] = df['message_date'].dt.year
    df['month'] = df['message_date'].dt.month_name()
    df['day'] = df['message_date'].dt.day
    df['hour'] = df['message_date'].dt.hour
    df['miniutes'] = df['message_date'].dt.minute

    return df