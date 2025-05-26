# src/metrics.py

import pandas as pd

def booking_rate(df):
    """
    Overall percentage of inquiries that result in a booking.
    """
    return df['booking_happened'].mean()


def response_rate(df):
    """
    Percentage of inquiries that received a host reply.
    """
    return df['ts_reply_at_first'].notna().mean()


def acceptance_rate(df):
    """
    Percentage of inquiries that were accepted by the host.
    """
    return df['ts_accepted_at_first'].notna().mean()


def avg_response_time(df):
    """
    Average host response time in hours (excluding missing values).
    """
    return df['response_time_hours'].dropna().mean()


def avg_accept_time(df):
    """
    Average time to acceptance in hours (excluding missing values).
    """
    return df['accept_time_hours'].dropna().mean()


def conversion_by_contact_channel(df):
    """
    Booking conversion rate by contact method: contact_me, book_it, instant_book.
    """
    return df.groupby('contact_channel_first')['booking_happened'].mean().sort_values(ascending=False)


def conversion_by_user_stage(df):
    """
    Booking conversion rate for new users vs past bookers.
    """
    return df.groupby('guest_user_stage_first')['booking_happened'].mean().sort_values(ascending=False)
