# src/clean_data.py
import pandas as pd

def clean_contacts(df):
    """
    Cleans and enriches a DataFrame containing Airbnb contact/booking data.
    This function performs the following operations:
    - Safely parses specified columns as datetimes, coercing errors to NaT.
    - Adds a boolean 'booking_happened' column indicating if a booking occurred.
    - Computes 'response_time' and 'accept_time' as timedeltas between relevant events.
    - Adds 'response_time_hours' and 'accept_time_hours' as the duration in hours.
    - Determines the booking funnel stage for each row and adds it as 'funnel_stage'.
    Parameters:
        df (pd.DataFrame): Input DataFrame with columns:
            - 'ts_booking_at'
            - 'ts_reply_at_first'
            - 'ts_interaction_first'
            - 'ts_accepted_at_first'
    Returns:
        pd.DataFrame: The cleaned and enriched DataFrame with new columns added.
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
        """
        Compute the time difference between two datetime columns in a DataFrame row.

        Parameters:
            row (pd.Series): A row from a pandas DataFrame.
            later_col (str): The name of the column containing the later datetime.
            earlier_col (str): The name of the column containing the earlier datetime.

        Returns:
            pd.Timedelta or pd.NaT: The time difference between the two columns, or pd.NaT if either value is missing.
        """
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
        """
        Converts a pandas Timedelta object to the total number of hours.

        Parameters:
            td (pandas.Timedelta or NaT): The time difference to convert.

        Returns:
            float or pandas.NaT: The total number of hours represented by the Timedelta,
            or pandas.NaT if the input is missing (NaT).
        """
        return pd.NaT if pd.isna(td) else td.total_seconds() / 3600

    df['response_time_hours'] = df['response_time'].apply(compute_hours)
    df['accept_time_hours'] = df['accept_time'].apply(compute_hours)

    # Booking funnel stage
    def determine_stage(row):
        """
        Determines the booking stage of a row based on timestamp columns.

        Parameters:
            row (pd.Series): A pandas Series representing a row of data with the following timestamp columns:
                - 'ts_booking_at'
                - 'ts_accepted_at_first'
                - 'ts_reply_at_first'

        Returns:
            str: The booking stage, which can be one of the following:
                - 'booked' if 'ts_booking_at' is not NaN
                - 'accepted' if 'ts_accepted_at_first' is not NaN
                - 'replied' if 'ts_reply_at_first' is not NaN
                - 'no_reply' if none of the above are present
        """
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
    Cleans the user DataFrame by handling missing values and adding a profile indicator.

    Parameters:
        df (pandas.DataFrame): The input DataFrame containing a 'words_in_user_profile' column.

    Returns:
        pandas.DataFrame: The cleaned DataFrame with missing 'words_in_user_profile' values filled with 0,
                          and a new boolean column 'has_profile' indicating if the user has a profile.
    """
    df['words_in_user_profile'] = df['words_in_user_profile'].fillna(0)
    df['has_profile'] = df['words_in_user_profile'] > 0
    return df


def clean_listings(df):
    """
    Cleans and filters the Airbnb listings DataFrame.

    This function performs the following operations:
    1. Strips whitespace and converts the 'room_type' column to lowercase.
    2. Filters the DataFrame to include only rows where 'room_type' is one of:
        'entire home', 'private room', or 'shared room'.
    3. Fills missing values in the 'total_reviews' column with 0 and converts the column to integer type.

    Parameters:
         df (pandas.DataFrame): The input DataFrame containing Airbnb listings data.

    Returns:
         pandas.DataFrame: The cleaned and filtered DataFrame.
    """
    df['room_type'] = df['room_type'].str.strip().str.lower()
    df = df[df['room_type'].isin(['entire home', 'private room', 'shared room'])]
    df['total_reviews'] = df['total_reviews'].fillna(0).astype(int)
    return df
