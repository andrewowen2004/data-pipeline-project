import csv
import random
from datetime import datetime, timedelta
from faker import Faker

fake = Faker()

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

# Date range: June 1 to now
start_date = datetime(2025, 6, 1)
end_date = datetime.now()

def random_date(start, end):
    delta = end - start
    random_seconds = random.randint(0, int(delta.total_seconds()))
    return (start + timedelta(seconds=random_seconds)).isoformat()

def generate_transaction_id():
    return ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=17))

# Generate transactions
rows = []

# Add frauds first
for _ in range(NUM_FRAUDS):
    txn_id = generate_transaction_id()
    date = random_date(start_date, end_date)
    amount = round(random.uniform(10000, 50000), 2)  # high outlier
    subject = random.choice(list(SUBJECTS.keys()))
    rows.append([txn_id, date, amount, CURRENCY, STATUS, subject])

# Add normal transactions
for _ in range(NUM_ROWS - NUM_FRAUDS):
    txn_id = generate_transaction_id()
    date = random_date(start_date, end_date)
    subject = random.choice(list(SUBJECTS.keys()))
    mean, std_dev = SUBJECTS[subject]
    amount = round(random.gauss(mean, std_dev), 2)
    amount = max(amount, 1.00)  # Prevent negative/zero
    rows.append([txn_id, date, amount, CURRENCY, STATUS, subject])

# Shuffle transactions
random.shuffle(rows)

# Write to CSV
with open("transactions.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Transaction ID", "Date", "Amount", "Currency", "Status", "Subject"])
    writer.writerows(rows)

print(f"✅ Generated 'transactions.csv' with {NUM_ROWS} rows and {NUM_FRAUDS} fraudulent transactions.")
