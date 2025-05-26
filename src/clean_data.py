# src/clean_data.py

import pandas as pd

def clean_contacts(df):
    """
    Clean and enrich contacts dataset with new derived columns:
    - Booking flag
    - Response/acceptance times
    - Funnel stage (categorical)
    """
    # Booking flag
    df['booking_happened'] = df['ts_booking_at'].notna()

    # Time deltas (in hours)
    df['response_time_hours'] = (
        df['ts_reply_at_first'] - df['ts_interaction_first']
    ).dt.total_seconds() / 3600

    df['accept_time_hours'] = (
        df['ts_accepted_at_first'] - df['ts_interaction_first']
    ).dt.total_seconds() / 3600

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
