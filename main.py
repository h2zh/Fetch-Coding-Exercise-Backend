"""
This program aims to get payers' balance after a series of transactions

Author: Howard Zhong
"""
import json
import sys
import pandas as pd
import os.path
import requests

"""
args
"""
url = 'https://fetch-hiring.s3.amazonaws.com/transactions.csv'

"""
A hash table to store Payer and Transaction
key: name; value: balance
"""
payer = {} 

def init_data(fname: str):
    """
    Fetch data from current directory or AWS S3 and sort by time
    Summary payer data in a hash table 

    Return the transactions dataframe
    """
    # Check if the file exists. If not, fetch it from AWS.
    if not os.path.isfile(fname):
        res = requests.get(url, allow_redirects=True)
        open(fname, 'wb').write(res.content)
        
    # Store transactions in a dataframe
    df = pd.read_csv(fname)

    # Sort transactions in chronological order
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df = df.sort_values('timestamp')

    # Iterate rows to get the balance of each payer and store in payer
    for idx, row in df.iterrows():
        current_payer = row["payer"]
        if current_payer not in payer:
            payer[current_payer] = row["points"]
        else:
            payer[current_payer] += row["points"]

    return df

def spend(amount: int, df):
    """
    amount: the total amount of points to spend
    df: the transaction dataframe in chronological order

    Return the transaction dataframe when running out of points
    """
    # Iterate rows to adjust each payer's balance
    for idx, row in df.iterrows():
        current_payer = row["payer"]
        curr_Tx_points = row["points"]

        # Different situation according to the difference between 
        # remaining total amount to spend and current Tx points
        if amount >= curr_Tx_points:
            # Prevent payer's points to go negative.
            if not payer[current_payer] - curr_Tx_points < 0:
                payer[current_payer] -= curr_Tx_points
                amount -= curr_Tx_points
        else:
            payer[current_payer] -= amount
            amount = 0

        # End the spending process when points to spend run out
        if amount == 0:
            break
    return df

def to_json():
    """
    Return a json object containing payer data
    """
    return json.dumps(payer, indent=4)

def main():
    """ 
    Run all subordinate functions 
    """
    # Get args from command line
    amount = int(sys.argv[1])
    fname = str(sys.argv[2])

    # Create payer/balance hash table and organize transactions
    init_df = init_data(fname)

    # Process the spendings to alter data in payer hash table
    final_df = spend(amount, init_df)

    # Export the payer hash table in json format
    print(to_json())

main()