import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

sns.set(style="whitegrid")

def plot_funnel_stage_distribution(df, save_path=None):
    """
    Plots the distribution of guest inquiries across different funnel stages.
    Parameters:
        df (pd.DataFrame): DataFrame containing at least a 'funnel_stage' column with stage labels.
        save_path (str, optional): If provided, the plot will be saved to this file path.
    The function creates a count plot of the number of inquiries at each funnel stage ('no_reply', 'replied', 'accepted', 'booked'),
    annotates each bar with its count, and displays the plot. Optionally saves the plot to the specified path.
    """
    order = ['no_reply', 'replied', 'accepted', 'booked']
    plt.figure(figsize=(8, 5))
    ax = sns.countplot(data=df, x='funnel_stage', order=order, palette="Blues_d")
    plt.title("Guest Inquiry Funnel Stages")
    plt.xlabel("Funnel Stage")
    plt.ylabel("Number of Inquiries")

    # Annotate each bar
    for container in ax.containers:
        ax.bar_label(container, fmt='%d', label_type='edge', padding=3)

    if save_path:
        plt.savefig(save_path, bbox_inches='tight')
    plt.show()


def plot_booking_rate_by_contact_channel(df, save_path=None):
    """
    Plots the booking rate by the first contact channel from the given DataFrame.
    This function groups the data by the 'contact_channel_first' column, calculates the mean booking rate
    ('booking_happened'), and visualizes the results as a horizontal bar chart. Each bar is annotated with
    the booking rate percentage. Optionally, the plot can be saved to a specified file path.
    Parameters:
        df (pd.DataFrame): DataFrame containing at least 'contact_channel_first' and 'booking_happened' columns.
        save_path (str, optional): File path to save the plot image. If None, the plot is not saved.
    Returns:
        None
    """
    booking_rates = df.groupby('contact_channel_first')['booking_happened'].mean().sort_values()
    plt.figure(figsize=(8, 5))
    ax = booking_rates.plot(kind='barh', color='skyblue')
    plt.title("Booking Rate by Contact Channel")
    plt.xlabel("Booking Rate")
    plt.ylabel("Contact Method")

    # Annotate bars with %
    for i, v in enumerate(booking_rates):
        ax.text(v + 0.01, i, f'{v:.1%}', va='center', fontsize=9)

    # Highlight top performer
    max_idx = booking_rates.idxmax()
    ax.bar_label(ax.containers[0], fmt='%.0f%%', label_type='edge')

    if save_path:
        plt.savefig(save_path, bbox_inches='tight')
    plt.show()


def plot_booking_rate_by_room_type(df_contacts, df_listings, save_path=None):
    """
    Plots the booking rate by room type using data from contacts and listings DataFrames.
    This function merges the contacts and listings DataFrames on the 'id_listing_anon' column,
    calculates the mean booking rate for each room type, and creates a horizontal bar plot
    showing the booking rate by room type. Optionally, the plot can be saved to a specified path.
    Parameters:
        df_contacts (pd.DataFrame): DataFrame containing booking/contact information, including 'id_listing_anon' and 'booking_happened' columns.
        df_listings (pd.DataFrame): DataFrame containing listing details, including 'id_listing_anon' and 'room_type' columns.
        save_path (str, optional): File path to save the plot image. If None, the plot is not saved.
    Returns:
        None
    """
    merged = df_contacts.merge(df_listings, on='id_listing_anon', how='left')
    rates = merged.groupby('room_type')['booking_happened'].mean().sort_values()
    plt.figure(figsize=(8, 5))
    ax = rates.plot(kind='barh', color='salmon')
    plt.title("Booking Rate by Room Type")
    plt.xlabel("Booking Rate")
    plt.ylabel("Room Type")

    for i, v in enumerate(rates):
        ax.text(v + 0.01, i, f'{v:.1%}', va='center', fontsize=9)

    if save_path:
        plt.savefig(save_path, bbox_inches='tight')
    plt.show()


def plot_trimmed_response_time_distribution(df, max_hours=72, save_path=None):
    """
    Plots the distribution of host response times, trimmed to a specified maximum number of hours.
    Parameters:
        df (pd.DataFrame): DataFrame containing a 'response_time_hours' column with host response times in hours.
        max_hours (float, optional): Maximum response time (in hours) to include in the plot. Defaults to 72.
        save_path (str, optional): File path to save the plot image. If None, the plot is not saved. Defaults to None.
    The function filters the response times to those between 0.1 and max_hours, plots a histogram with a KDE curve,
    annotates the median response time, and optionally saves the plot to a file.
    """
    filtered = df[df['response_time_hours'].between(0.1, max_hours)]
    plt.figure(figsize=(10, 6))
    ax = sns.histplot(filtered['response_time_hours'], bins=40, kde=True, color='teal')
    plt.title(f"Host Response Times (Under {max_hours} Hours)")
    plt.xlabel("Response Time (Hours)")
    plt.ylabel("Number of Inquiries")

    # Annotate median
    median = filtered['response_time_hours'].median()
    plt.axvline(median, color='red', linestyle='--', linewidth=2)
    plt.text(median + 1, ax.get_ylim()[1] * 0.8, f'Median: {median:.1f} hrs', color='red')

    if save_path:
        plt.savefig(save_path, bbox_inches='tight')
    plt.show()


def plot_response_time_cdf(df, max_hours=72, save_path=None):
    """
    Plots the cumulative distribution function (CDF) of host response times from a DataFrame.
    Parameters:
        df (pd.DataFrame): DataFrame containing a 'response_time_hours' column with host response times in hours.
        max_hours (float, optional): Maximum response time (in hours) to include in the plot. Defaults to 72.
        save_path (str, optional): File path to save the plot image. If None, the plot is not saved. Defaults to None.
    Displays:
        A matplotlib plot showing the CDF of host response times, with the median response time annotated.
    """
    filtered = df[df['response_time_hours'].between(0.1, max_hours)]
    sorted_vals = filtered['response_time_hours'].sort_values()
    cdf = sorted_vals.rank(method='average', pct=True)

    plt.figure(figsize=(10, 6))
    plt.plot(sorted_vals, cdf, color='purple')
    plt.title("Cumulative Distribution of Host Response Times")
    plt.xlabel("Response Time (Hours)")
    plt.ylabel("Cumulative % of Inquiries")
    plt.grid(True)

    # Median annotation
    median = sorted_vals.median()
    plt.axvline(median, color='red', linestyle='--', linewidth=2)
    plt.text(median + 1, 0.6, f'Median: {median:.1f} hrs', color='red')

    if save_path:
        plt.savefig(save_path, bbox_inches='tight')
    plt.show()
