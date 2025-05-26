# src/funnel_analysis.py

import pandas as pd

def get_funnel_stage_distribution(df, normalize=True):
    """
    Returns the distribution of users across funnel stages.
    """
    return df['funnel_stage'].value_counts(normalize=normalize)


def funnel_by_contact_channel(df):
    """
    Shows how each contact channel performs across funnel stages.
    Returns a dataframe showing % of inquiries by stage.
    """
    funnel = pd.crosstab(df['contact_channel_first'], df['funnel_stage'], normalize='index')
    return funnel


def funnel_by_guest_user_stage(df):
    """
    Booking conversion by guest user stage (new vs past booker).
    """
    return df.groupby('guest_user_stage_first')['booking_happened'].mean().sort_values(ascending=False)


def funnel_by_room_type(df_contacts, df_listings):
    """
    Join contacts with listings to see how room types convert.
    """
    df = df_contacts.merge(df_listings, on='id_listing_anon', how='left')
    return df.groupby('room_type')['booking_happened'].mean().sort_values(ascending=False)


def funnel_by_neighborhood(df_contacts, df_listings, min_inquiries=50):
    """
    Shows booking rate by neighborhood (filtering out neighborhoods with very few inquiries).
    """
    df = df_contacts.merge(df_listings, on='id_listing_anon', how='left')
    grouped = df.groupby('listing_neighborhood')['booking_happened'].agg(['mean', 'count'])
    grouped = grouped[grouped['count'] >= min_inquiries]
    return grouped.sort_values(by='mean', ascending=False)
