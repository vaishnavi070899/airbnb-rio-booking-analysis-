# src/plots.py

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

sns.set(style="whitegrid")

def plot_funnel_stage_distribution(df, save_path=None):
    order = ['no_reply', 'replied', 'accepted', 'booked']
    ax = sns.countplot(data=df, x='funnel_stage', order=order, palette="Blues_d")
    plt.title("Guest Inquiry Funnel Stages")
    plt.xlabel("Funnel Stage")
    plt.ylabel("Number of Inquiries")
    if save_path:
        plt.savefig(save_path, bbox_inches='tight')
    plt.show()


def plot_booking_rate_by_contact_channel(df, save_path=None):
    booking_rates = df.groupby('contact_channel_first')['booking_happened'].mean().sort_values()
    ax = booking_rates.plot(kind='barh', color='skyblue')
    plt.title("Booking Rate by Contact Channel")
    plt.xlabel("Booking Rate")
    plt.ylabel("Contact Method")
    if save_path:
        plt.savefig(save_path, bbox_inches='tight')
    plt.show()


def plot_booking_rate_by_room_type(df_contacts, df_listings, save_path=None):
    merged = df_contacts.merge(df_listings, on='id_listing_anon', how='left')
    rates = merged.groupby('room_type')['booking_happened'].mean().sort_values()
    ax = rates.plot(kind='barh', color='salmon')
    plt.title("Booking Rate by Room Type")
    plt.xlabel("Booking Rate")
    plt.ylabel("Room Type")
    if save_path:
        plt.savefig(save_path, bbox_inches='tight')
    plt.show()


def plot_response_time_distribution(df, save_path=None):
    sns.histplot(df['response_time_hours'].dropna(), bins=30, kde=True, color='teal')
    plt.title("Distribution of Host Response Times")
    plt.xlabel("Response Time (Hours)")
    plt.ylabel("Frequency")
    if save_path:
        plt.savefig(save_path, bbox_inches='tight')
    plt.show()
