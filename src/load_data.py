# src/load_data.py

import pandas as pd

def load_contacts(path='data/contacts.csv'):
    """
    Load contacts.csv with datetime parsing.
    """
    date_columns = [
        'ts_interaction_first', 'ts_reply_at_first',
        'ts_accepted_at_first', 'ts_booking_at',
        'ds_checkin_first', 'ds_checkout_first'
    ]
    contacts = pd.read_csv(path, parse_dates=date_columns)
    return contacts

def load_listings(path='data/listings.csv'):
    """
    Load listings.csv.
    """
    listings = pd.read_csv(path)
    return listings

def load_users(path='data/users.csv'):
    """
    Load users.csv.
    """
    users = pd.read_csv(path)
    return users

def load_all_data(contacts_path='data/contacts.csv',
                  listings_path='data/listings.csv',
                  users_path='data/users.csv'):
    """
    Load all three datasets at once.
    """
    contacts = load_contacts(contacts_path)
    listings = load_listings(listings_path)
    users = load_users(users_path)
    return contacts, listings, users
