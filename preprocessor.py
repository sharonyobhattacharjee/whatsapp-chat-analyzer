
import re
import pandas as pd


def preprocess(data):

    pattern = r'\[(\d{1,2}/\d{1,2}/\d{2,4}, \d{1,2}:\d{2}:\d{2} [AP]M)\] '

    raw_messages = re.split(pattern, data)[2::2]
    dates = re.findall(pattern, data)

    df = pd.DataFrame({
        'user_message': raw_messages,
        'date': pd.to_datetime(
            dates,
            format='%m/%d/%y, %I:%M:%S %p'
        )
    })

    users = []
    messages_list = []

    for message in df['user_message']:

        entry = re.split(
            r'^(.*?):\s',
            message,
            maxsplit=1
        )

        if len(entry) > 1:

            users.append(entry[1])
            messages_list.append(entry[2])

        else:

            users.append('group_notification')
            messages_list.append(entry[0])

    df['user'] = users
    df['message'] = messages_list

    # Remove original column
    df.drop(
        columns=['user_message'],
        inplace=True
    )

    # Date features
    df['only_date'] = df['date'].dt.date
    df['year'] = df['date'].dt.year
    df['month_num'] = df['date'].dt.month
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['day_name'] = df['date'].dt.day_name()
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute

    # Period
    period = []

    for hour in df['hour']:

        if hour == 0:

            period.append(
                '00-1'
            )

        elif hour == 23:

            period.append(
                '23-00'
            )

        else:

            period.append(
                str(hour) + "-" + str(hour + 1)
            )

    df['period'] = period

    return df