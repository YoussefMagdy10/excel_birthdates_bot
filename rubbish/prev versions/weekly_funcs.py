def select_rows_last(data):
    today = datetime.now().date()
    seven_days_earlier = pd.Timestamp(today - timedelta(days=7))
    today = pd.Timestamp(today)
    selected_rows = pd.date_range(start=seven_days_earlier, end=today, freq='D')

    selected_rows_1 = data[
        (data['birthdate'].dt.month == today.month) &  # Check month
        (data['birthdate'].dt.day < today.day)
    ]  # Check day < today
    # Apply additional filtering only if the previous condition is met (day < today)
    if today.day > seven_days_earlier.day:
        selected_rows_1 = selected_rows_1[
            selected_rows_1['birthdate'].dt.day > seven_days_earlier.day
        ]

    selected_rows_2 = pd.DataFrame(columns=data.columns)
    
    if seven_days_earlier.month == today.month - 1:
        selected_rows_2 = data[
            (data['birthdate'].dt.month == today.month - 1) & 
            (data['birthdate'].dt.day <= calendar.monthrange(today.year, today.month - 1)[1]) & 
            (data['birthdate'].dt.day > seven_days_earlier.day)
        ]

    # Concatenate selected rows
    selected_rows = pd.concat([selected_rows_1, selected_rows_2])

    # Ensure 'birthdate' is in datetime format

    selected_rows['birthdate'] = pd.to_datetime(selected_rows['birthdate'])

    # Extract month and day
    selected_rows['month'] = selected_rows['birthdate'].dt.month
    selected_rows['day'] = selected_rows['birthdate'].dt.day

    selected_rows = selected_rows.sort_values(by=['month', 'day'], ascending=[True, True])
    return selected_rows, today


def select_rows_next(data):
    today = datetime.now().date()
    seven_days_later = today + timedelta(days=7)  # Calculate date 7 days later
    seven_days_later = pd.Timestamp(seven_days_later)
    today = pd.Timestamp(today)

    # Filter rows for birthdays within the next 7 days (inclusive)
    data['birthdate'] = pd.to_datetime(data['birthdate'])

    # Get today's date
    today = datetime.now().date()
    tomorrow = today + timedelta(days=1)
    seven_days_later = today + timedelta(days=7)

    # Filter birthdays occurring within the next 7 days
    selected_rows = data[
        ((data['birthdate'].dt.month == tomorrow.month) & (data['birthdate'].dt.day >= tomorrow.day)) |
        ((data['birthdate'].dt.month == seven_days_later.month) & (data['birthdate'].dt.day <= seven_days_later.day))
    ]

    # Extract month and day
    selected_rows['month'] = selected_rows['birthdate'].dt.month
    selected_rows['day'] = selected_rows['birthdate'].dt.day

    # Sort by month and day
    selected_rows = selected_rows.sort_values(by=['month', 'day'], ascending=[True, True])

    # Drop the temporary columns if you don't need them anymore
    selected_rows = selected_rows.drop(columns=['month', 'day'])
    return selected_rows, today
