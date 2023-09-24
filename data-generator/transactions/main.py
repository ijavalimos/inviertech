from faker import Faker
import pandas as pd
import datetime
fake = Faker()

categories = [
    {'name': 'Expenses/Food', 'min_amount': 100, 'max_amount': 300},
    {'name': 'Expenses/Transportation', 'min_amount': 100, 'max_amount': 1000},
    {'name': 'Expenses/Health', 'min_amount': 100, 'max_amount': 1000},
    {'name': 'Expenses/Education', 'min_amount': 100, 'max_amount': 1000},
    {'name': 'Expenses/Housing', 'min_amount': 15_000, 'max_amount': 30_000},
    {'name': 'Expenses/Entertainment', 'min_amount': 100, 'max_amount': 1000},
    {'name': 'Expenses/Others'},
    {'name': 'Income/Salary', 'min_amount': 80_000, 'max_amount': 90_000},
]

def generate_transaction(date):
    # Generate random date from 3 years ago to now
    # date = fake.date_between(start_date='-3y', end_date='now').isoformat()
    category = fake.random_element(elements=categories)
    if category['name'] == 'Expenses/Others':
        amount = fake.random_int(min=1, max=10_000, step=1)
    else:
        amount = fake.random_int(min=category['min_amount'], max=category['max_amount'], step=1)
    return {
        'id': fake.uuid4(),
        'date': date,
        'category': category['name'],
        'amount': amount,
        'periodicity': 'none'
    }

def generate_periodic_transactions(periodicity, periods, initial_date):
    dates = None
    if periodicity == 'daily':
        dates = pd.date_range(initial_date, periods=periods, freq='D')
    elif periodicity == 'weekly':
        dates = pd.date_range(initial_date, periods=periods, freq='W')
    elif periodicity == 'monthly':
        dates = pd.date_range(initial_date, periods=periods, freq='M')
    transaction = generate_transaction()
    # For each date, generate a duplicate transaction with updated date
    transactions = []
    for date in dates:
        transactions.append({
            'id': fake.uuid4(),
            'date': date.isoformat(),
            'category': transaction['category'],
            'amount': transaction['amount'],
            'periodicity': periodicity
        })
    return transactions

user_transactions = []

# Get date range from 3 years ago to now

dates = pd.date_range(datetime.datetime.now() - datetime.timedelta(days=3*365), periods=365*3, freq='D')
for date in dates:
    # Generate random number of non-periodic transactions
    for i in range(fake.random_int(min=0, max=10, step=1)):
        user_transactions.append(generate_transaction(date=date))

# Generate csv file
df = pd.DataFrame(user_transactions)
df.sort_values('date')

# Get rows of expenses
expenses = df[df['category'].str.startswith('Expenses')]

# Get rows of income
income = df[df['category'].str.startswith('Income')]

# Get daily expesnes from 2 days ago to now
daily_expenses = expenses[expenses['periodicity'] == 'daily']
daily_expenses = daily_expenses[daily_expenses['date'] >= (pd.Timestamp.now() - pd.Timedelta(days=2)).isoformat()]

expenses.to_csv('transactions/expenses.csv', index=False)
income.to_csv('transactions/income.csv', index=False)