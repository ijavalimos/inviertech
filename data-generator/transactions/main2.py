from faker import Faker
import pandas as pd
import datetime
import random

fake = Faker()

categories = [
    {'name': 'Expenses/Food', 'min_amount': 100/30, 'max_amount': 300/30},
    {'name': 'Expenses/Transportation', 'min_amount': 100/30, 'max_amount': 1000/30},
    {'name': 'Expenses/Health', 'min_amount': 100/30, 'max_amount': 1_000/30},
    {'name': 'Expenses/Education', 'min_amount': 100/30, 'max_amount': 1_000/30},
    {'name': 'Expenses/Housing', 'min_amount': 15_000/30, 'max_amount': 30_000/30},
    {'name': 'Expenses/Entertainment', 'min_amount': 100/30, 'max_amount': 1_000/30},
    {'name': 'Expenses/Others'},
    {'name': 'Income/Salary', 'min_amount': 8_000/30, 'max_amount': 30_000/30},
]

all_transactions = pd.DataFrame()

"""# Generate random number of periodic income transactions
for i in range(fake.random_int(min=1, max=10, step=1)):
    initial_date = fake.date_between(start_date='-3y', end_date='now').isoformat()
    periodicity = fake.random_element(elements=['daily', 'weekly', 'monthly'])
    periods = fake.random_int(min=1, max=10, step=1)
    # Get date range from initial_date to initial_date + periods
    if periodicity == 'daily':
        dates = pd.date_range(initial_date, periods=periods, freq='D')
    elif periodicity == 'weekly':
        dates = pd.date_range(initial_date, periods=periods, freq='W')
    elif periodicity == 'monthly':
        dates = pd.date_range(initial_date, periods=periods, freq='M')
    for date in dates:
        transaction = {
            'id': fake.uuid4(),
            'date': date.isoformat(),
            'category': 'Income/Salary',
            'amount': random.uniform(categories[-1]['min_amount'], categories[-1]['max_amount']),
            'periodicity': periodicity
        }
        all_transactions = pd.concat([all_transactions, pd.DataFrame([transaction])])"""

savings = 0

# Get date range from 3 years ago to now
dates = pd.date_range(datetime.datetime.now() - datetime.timedelta(days=5*365), periods=365*5, freq='D')
for date in dates:
    # Generate random number of non-periodic incomes
    num_of_incomes = random.choices([0, 1, 2, 3], [0.8, 0.1, 0.05, 0.05])[0]
    for i in range(num_of_incomes):
        transaction = {
            'id': fake.uuid4(),
            'date': date.isoformat(),
            'category': 'Income/Salary',
            'amount': random.uniform(categories[-1]['min_amount'], categories[-1]['max_amount']),
            'periodicity': 'none'
        }
        savings += transaction['amount']
        all_transactions = pd.concat([all_transactions, pd.DataFrame([transaction])])
    # Get all income transactions for this date
    # income_transactions = all_transactions[(all_transactions['date'] == date.isoformat()) & (all_transactions['category'] == 'Income/Salary')]
    # savings += income_transactions['amount'].sum()
    # Generate random number of non-periodic expenses
    for i in range(fake.random_int(min=0, max=15, step=1)):
        transaction = {
            'id': fake.uuid4(),
            'date': date.isoformat(),
            'category': fake.random_element(elements=categories)['name'],
            'amount': random.uniform(
                min(categories[-1]['min_amount'], savings), 
                min(categories[-1]['max_amount'], savings)),
            'periodicity': 'none'
        }
        all_transactions = pd.concat([all_transactions, pd.DataFrame([transaction])])

# Modify file
all_transactions.sort_values('date')
# Get rows of expenses
expenses = all_transactions[all_transactions['category'].str.startswith('Expenses')]
# Get rows of income
income = all_transactions[all_transactions['category'].str.startswith('Income')]

# To csv
expenses.to_csv('transactions/expenses.csv', index=False)
income.to_csv('transactions/income.csv', index=False)
