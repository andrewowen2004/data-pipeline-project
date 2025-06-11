import csv
import random
from faker import Faker
from datetime import datetime, timedelta

fake = Faker()

def generate_transaction_id():
    return ''.join(random.choices("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", k=17))

def generate_random_time():
    # Generate random datetime on June 9–11, 2025
    day = random.randint(9, 11)
    hour = random.randint(0, 23)
    minute = random.randint(0, 59)
    second = random.randint(0, 59)
    dt = datetime(2025, 6, day, hour, minute, second)

    # Random UTC offset in format ±hhmm
    offset_hour = random.choice(range(-12, 15))  # UTC-12 to UTC+14
    offset_sign = '+' if offset_hour >= 0 else '-'
    offset_formatted = f"{offset_sign}{abs(offset_hour):02}00"

    iso_dt = dt.strftime('%Y-%m-%dT%H:%M:%S') + offset_formatted
    return iso_dt

def generate_status():
    return random.choice(['S', 'P', 'F'])

def generate_subject():
    return random.choice([
        "Initial balance", "Client payment", "Refund issued", "Online order",
        "Service fee", "Freelance payout", "Subscription", "Transfer received", ""
    ])

with open('transactions.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Transaction ID', 'Date', 'Amount', 'Currency', 'Status', 'Subject'])

    for _ in range(5000):
        writer.writerow([
            generate_transaction_id(),
            generate_random_time(),
            round(random.uniform(-500, 5000), 2),
            'USD',
            generate_status(),
            generate_subject()
        ])
