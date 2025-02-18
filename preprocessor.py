import re
import pandas as pd


def preprocess(data):
    # Regex pattern for matching date, time, sender, and message
    pattern = r"(\d{1,2}/\d{1,2}/\d{2,4}),\s(\d{1,2}:\d{2}\s?[APMampm]{2})\s-\s([^:]+):\s(.*)"

    # Find all matches
    matches = re.findall(pattern, data)

    # Prepare a list to store the grouped data
    grouped_messages = []

    for match in matches:
        date, time, sender, message = match
        date_time = f"{date} {time}"

        # Append to the list (if sender is missing, use 'Group Notification')
        sender = sender if sender else "Group Notification"
        grouped_messages.append((date_time, sender, message))

    # Create DataFrame from the grouped messages
    df = pd.DataFrame(grouped_messages, columns=["DateTime", "Sender", "Message"])

    # Convert 'DateTime' to datetime object for further processing
    df['DateTime'] = pd.to_datetime(df['DateTime'])

    # Extract year, month, day, hour, minute
    df['only_date'] = df['DateTime'].dt.date
    df['Year'] = df['DateTime'].dt.year
    df['month_num'] = df['DateTime'].dt.month
    df['Month'] = df['DateTime'].dt.month_name()
    df['Day'] = df['DateTime'].dt.day
    df['day_name'] = df['DateTime'].dt.day_name()
    df['Hour'] = df['DateTime'].dt.hour
    df['Minute'] = df['DateTime'].dt.minute

    # Extracting the day name
    df['DayName'] = df['DateTime'].dt.day_name()

    # Adding period based on hour (e.g., 10-11, 23-00, etc.)
    period = []
    for hour in df['Hour']:
        if hour == 23:
            period.append(f"{hour}-00")
        elif hour == 0:
            period.append(f"00-{hour + 1}")
        else:
            period.append(f"{hour}-{hour + 1}")

    df['Period'] = period

    return df


