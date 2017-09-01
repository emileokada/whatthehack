from api_functions import format_int, make_transaction

with open("./pub_account_data.json") as f:
    pubs = json.load(f)

with open("./customer_data.json") as f:
    customers = json.load(f)

def generate_random_transactions(number_of_transactions):

