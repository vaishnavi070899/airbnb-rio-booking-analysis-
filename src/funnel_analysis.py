# src/funnel_analysis.py

import pandas as pd

def get_funnel_stage_distribution(df, normalize=True):
    """
    Calculates the distribution of values in the 'funnel_stage' column of a DataFrame.

    Parameters:
        df (pandas.DataFrame): The input DataFrame containing a 'funnel_stage' column.
        normalize (bool, optional): If True, returns the relative frequencies of the unique values.
                                    If False, returns the absolute counts. Default is True.

    Returns:
        pandas.Series: A Series containing the counts or relative frequencies of each unique value in 'funnel_stage'.
    """
    return df['funnel_stage'].value_counts(normalize=normalize)


def funnel_by_contact_channel(df):
    """
    Generates a funnel analysis table by contact channel and funnel stage.

    This function computes a normalized crosstab of the first contact channel versus the funnel stage,
    showing the proportion of entries in each funnel stage for every contact channel.

    Parameters:
        df (pandas.DataFrame): The input DataFrame containing at least the columns
            'contact_channel_first' and 'funnel_stage'.

    Returns:
        pandas.DataFrame: A DataFrame where each row corresponds to a contact channel,
            each column to a funnel stage, and values represent the proportion of entries
            in each stage for that channel.
    """
    funnel = pd.crosstab(df['contact_channel_first'], df['funnel_stage'], normalize='index')
    return funnel


def funnel_by_guest_user_stage(df):
    """
    Calculates the booking conversion rate for each guest user stage.

    Groups the input DataFrame by the 'guest_user_stage_first' column and computes the mean of the 'booking_happened' column for each group, representing the conversion rate (i.e., the proportion of bookings that happened) at each stage. The results are sorted in descending order of conversion rate.

    Parameters:
        df (pandas.DataFrame): DataFrame containing at least the columns 'guest_user_stage_first' and 'booking_happened'.

    Returns:
        pandas.Series: Conversion rates indexed by guest user stage, sorted in descending order.
    """
    return df.groupby('guest_user_stage_first')['booking_happened'].mean().sort_values(ascending=False)


def funnel_by_room_type(df_contacts, df_listings):
    """
    Calculates the booking conversion rate by room type.

    This function merges the contacts and listings DataFrames on the 'id_listing_anon' column,
    then groups the resulting DataFrame by 'room_type' and computes the mean of the 'booking_happened'
    column for each room type. The result is a Series with room types as the index and their corresponding
    booking conversion rates, sorted in descending order.

    Parameters:
        df_contacts (pd.DataFrame): DataFrame containing contact/booking information, must include 'id_listing_anon' and 'booking_happened' columns.
        df_listings (pd.DataFrame): DataFrame containing listing information, must include 'id_listing_anon' and 'room_type' columns.

    Returns:
        pd.Series: Booking conversion rates by room type, sorted in descending order.
    """
    df = df_contacts.merge(df_listings, on='id_listing_anon', how='left')
    return df.groupby('room_type')['booking_happened'].mean().sort_values(ascending=False)


def funnel_by_neighborhood(df_contacts, df_listings, min_inquiries=50):
    """
    Analyzes the booking funnel by neighborhood, calculating the booking conversion rate and inquiry count for each neighborhood.

    Parameters:
        df_contacts (pd.DataFrame): DataFrame containing contact/inquiry data, including 'id_listing_anon' and 'booking_happened' columns.
        df_listings (pd.DataFrame): DataFrame containing listing details, including 'id_listing_anon' and 'listing_neighborhood' columns.
        min_inquiries (int, optional): Minimum number of inquiries required for a neighborhood to be included in the results. Defaults to 50.

    Returns:
        pd.DataFrame: DataFrame indexed by 'listing_neighborhood', with columns:
            - 'mean': The mean booking conversion rate (fraction of inquiries resulting in bookings).
            - 'count': The number of inquiries in each neighborhood.
        The DataFrame is sorted by conversion rate in descending order.
    """
    df = df_contacts.merge(df_listings, on='id_listing_anon', how='left')
    grouped = df.groupby('listing_neighborhood')['booking_happened'].agg(['mean', 'count'])
    grouped = grouped[grouped['count'] >= min_inquiries]
    return grouped.sort_values(by='mean', ascending=False)
