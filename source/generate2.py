import sqlite3
import random
from datetime import datetime, timedelta

# Your custom data generation logic, no direct Faker used except for date if you want (you can add if needed)

# Configuration
NUM_ROWS = 3850
CURRENCY = "USD"
STATUS = "S"
SUBJECTS = {
    "Consulting Services": (500, 150),
    "Software License": (1200, 300),
    "Product Sale": (80, 20),
    "Subscription Fee": (40, 10),
    "Training Program": (300, 100),
    "Hardware Purchase": (900, 250)
}
NUM_FRAUDS = random.randint(3, 7)

# Date range: June 1, 2025 to now
start_date = datetime(2025, 6, 1)
end_date = datetime.now()

def random_date(start, end):
    delta = end - start
    random_seconds = random.randint(0, int(delta.total_seconds()))
    return (start + timedelta(seconds=random_seconds)).isoformat()

def generate_transaction_id():
    return ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=17))

# Connect to SQLite DB (or create it)
conn = sqlite3.connect('../data/transactions.db')
cursor = conn.cursor()

# Create table with matching columns
cursor.execute('''
CREATE TABLE IF NOT EXISTS transactions (
    transaction_id TEXT PRIMARY KEY,
    date TEXT,
    amount REAL,
    currency TEXT,
    status TEXT,
    subject TEXT
)
''')

# Insert fraud transactions first
for _ in range(NUM_FRAUDS):
    txn_id = generate_transaction_id()
    date = random_date(start_date, end_date)
    amount = round(random.uniform(10000, 50000), 2)  # high outlier
    subject = random.choice(list(SUBJECTS.keys()))
    cursor.execute('''
        INSERT INTO transactions (transaction_id, date, amount, currency, status, subject)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (txn_id, date, amount, CURRENCY, STATUS, subject))

# Insert normal transactions
for _ in range(NUM_ROWS - NUM_FRAUDS):
    txn_id = generate_transaction_id()
    date = random_date(start_date, end_date)
    subject = random.choice(list(SUBJECTS.keys()))
    mean, std_dev = SUBJECTS[subject]
    amount = round(random.gauss(mean, std_dev), 2)
    amount = max(amount, 1.00)  # Prevent negative/zero
    cursor.execute('''
        INSERT INTO transactions (transaction_id, date, amount, currency, status, subject)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (txn_id, date, amount, CURRENCY, STATUS, subject))

conn.commit()
conn.close()

print(f"✅ Inserted {NUM_ROWS} transactions into the database, including {NUM_FRAUDS} frauds.")
