# src/plots.py

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

sns.set(style="whitegrid")

def plot_funnel_stage_distribution(df, save_path=None):
    order = ['no_reply', 'replied', 'accepted', 'booked']
    plt.figure(figsize=(8, 5))
    sns.countplot(data=df, x='funnel_stage', order=order, palette="Blues_d")
    plt.title("Guest Inquiry Funnel Stages")
    plt.xlabel("Funnel Stage")
    plt.ylabel("Number of Inquiries")
    if save_path:
        plt.savefig(save_path, bbox_inches='tight')
    plt.show()


def plot_booking_rate_by_contact_channel(df, save_path=None):
    booking_rates = df.groupby('contact_channel_first')['booking_happened'].mean().sort_values()
    plt.figure(figsize=(8, 5))
    booking_rates.plot(kind='barh', color='skyblue')
    plt.title("Booking Rate by Contact Channel")
    plt.xlabel("Booking Rate")
    plt.ylabel("Contact Method")
    if save_path:
        plt.savefig(save_path, bbox_inches='tight')
    plt.show()


def plot_booking_rate_by_room_type(df_contacts, df_listings, save_path=None):
    merged = df_contacts.merge(df_listings, on='id_listing_anon', how='left')
    rates = merged.groupby('room_type')['booking_happened'].mean().sort_values()
    plt.figure(figsize=(8, 5))
    rates.plot(kind='barh', color='salmon')
    plt.title("Booking Rate by Room Type")
    plt.xlabel("Booking Rate")
    plt.ylabel("Room Type")
    if save_path:
        plt.savefig(save_path, bbox_inches='tight')
    plt.show()


def plot_trimmed_response_time_distribution(df, max_hours=72, save_path=None):
    """
    Trim high outliers and show how fast hosts usually respond.
    """
    filtered = df[df['response_time_hours'].between(0.1, max_hours)]
    plt.figure(figsize=(10, 6))
    sns.histplot(filtered['response_time_hours'], bins=40, kde=True, color='teal')
    plt.title(f"Host Response Times (Under {max_hours} Hours)")
    plt.xlabel("Response Time (Hours)")
    plt.ylabel("Number of Inquiries")
    if save_path:
        plt.savefig(save_path, bbox_inches='tight')
    plt.show()


def plot_response_time_cdf(df, max_hours=72, save_path=None):
    """
    Cumulative distribution plot of host response time.
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
    if save_path:
        plt.savefig(save_path, bbox_inches='tight')
    plt.show()

