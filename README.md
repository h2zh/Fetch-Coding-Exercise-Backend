# Fetch-Coding-Exercise-Backend
This program aims to get payers' balance after a series of transactions

## Requirements

External libraries: Pandas, Requests


## Guide
Sample code to run this program on system command-line:

    python3 main.py 5000 transactions.csv

First arg is the amount of points to spend, second arg is the name of CSV file
Expected output:

    {
        "DANNON": 1000,
        "UNILEVER": 0,
        "MILLER COORS": 5300
    }

## Note
You don't have to locally possess the CSV file in this directory, this program can fetch it from a AWS S3
