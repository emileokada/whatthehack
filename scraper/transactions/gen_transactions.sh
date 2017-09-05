#!/usr/bin/env bash

python generate_transactions.py
python format_transaction_data.py
python rev_and_pop.py
