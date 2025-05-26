# src/clean_data.py
import pandas as pd

def clean_contacts(df):
    """
    Clean and enrich contacts dataset with:
    - Booking flag
    - Response and acceptance times (Timedelta and hours)
    """

    # Safe datetime parsing
    datetime_cols = [
        'ts_booking_at',
        'ts_reply_at_first',
        'ts_interaction_first',
        'ts_accepted_at_first',
    ]
    for col in datetime_cols:
        df[col] = pd.to_datetime(df[col], errors='coerce')

    # Booking flag
    df['booking_happened'] = df['ts_booking_at'].notna()

    # Compute Timedelta safely: result is NaT if any input is NaT
    def compute_timedelta(row, later_col, earlier_col):
        if pd.isna(row[later_col]) or pd.isna(row[earlier_col]):
            return pd.NaT
        else :
            return row[later_col] - row[earlier_col]

    df['response_time'] = df.apply(
        lambda row: compute_timedelta(row, 'ts_reply_at_first', 'ts_interaction_first'),
        axis=1
    )

    df['accept_time'] = df.apply(
        lambda row: compute_timedelta(row, 'ts_accepted_at_first', 'ts_interaction_first'),
        axis=1
    )

    # Compute hours directly during the same process
    def compute_hours(td):
        return pd.NaT if pd.isna(td) else td.total_seconds() / 3600

    df['response_time_hours'] = df['response_time'].apply(compute_hours)
    df['accept_time_hours'] = df['accept_time'].apply(compute_hours)

    # Booking funnel stage
    def determine_stage(row):
        if pd.notna(row['ts_booking_at']):
            return 'booked'
        elif pd.notna(row['ts_accepted_at_first']):
            return 'accepted'
        elif pd.notna(row['ts_reply_at_first']):
            return 'replied'
        else:
            return 'no_reply'

    df['funnel_stage'] = df.apply(determine_stage, axis=1)

    return df


def clean_users(df):
    """
    Handle missing values in users dataset (e.g., profile text).
    Adds a binary flag: has_profile.
    """
    df['words_in_user_profile'] = df['words_in_user_profile'].fillna(0)
    df['has_profile'] = df['words_in_user_profile'] > 0
    return df


def clean_listings(df):
    """
    Basic cleanup for listings dataset.
    """
    df['room_type'] = df['room_type'].str.strip().str.lower()
    df = df[df['room_type'].isin(['entire home', 'private room', 'shared room'])]
    df['total_reviews'] = df['total_reviews'].fillna(0).astype(int)
    return df
