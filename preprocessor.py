# import re
# import pandas as pd

# def preprocess(data):
#     pattern = r'\[(\d{2}/\d{2}/\d{2}, \d{2}:\d{2}:\d{2})\] (.*?): (.*)'

#     # Initialize empty lists to store extracted data
#     dates = []
#     users = []
#     messages = []

#     # Read the WhatsApp chat file line by line and extract the relevant information
#     with open('DS_chat.txt', 'r', encoding='utf-8') as file:
#         for line in file:
#             match = re.match(pattern, line)
#             if match:
#                 date, user, message = match.groups()
#                 dates.append(date)
#                 users.append(user)
#                 messages.append(message)

# # Create a DataFrame with 'Date', 'User', and 'Message' columns
#     df = pd.DataFrame({'date': dates, 'user': users, 'message': messages})

#     # Convert the 'Date' column to a pandas datetime object for easier analysis
#     df['date'] = pd.to_datetime(df['date'], format='%d/%m/%y, %H:%M:%S')
#     df['year'] = df['date'].dt.year
#     df['month'] = df['date'].dt.month_name()
#     df['day'] = df['date'].dt.day
#     df['hour'] = df['date'].dt.hour
#     df['minute'] = df['date'].dt.minute

#     return df

import re
import pandas as pd

def preprocess(data):
    pattern = r'\[(\d{2}/\d{2}/\d{2}, \d{2}:\d{2}:\d{2})\] (.*?): (.*)'

    # Initialize empty lists to store extracted data
    dates = []
    users = []
    messages = []

    # Read the WhatsApp chat data (provided as a string) line by line and extract the relevant information
    lines = data.split('\n')
    for line in lines:
        match = re.match(pattern, line)
        if match:
            date, user, message = match.groups()
            dates.append(date)
            users.append(user)
            messages.append(message)

    # Create a DataFrame with 'Date', 'User', and 'Message' columns
    df = pd.DataFrame({'date': dates, 'user': users, 'message': messages})

    # Convert the 'Date' column to a pandas datetime object for easier analysis
    df['date'] = pd.to_datetime(df['date'], format='%d/%m/%y, %H:%M:%S')

    df['day_date'] = df['date'].dt.date
    df['year'] = df['date'].dt.year
    df['month_num'] = df['date'].dt.month
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['day_name'] = df['date'].dt.day_name()
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute

    period = []
    for hour in df[['day_name', 'hour']]['hour']:
        if hour == 23:
            period.append(str(hour) + "-"+ str('00'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))
            
    df['period']=period
    return df

    return df