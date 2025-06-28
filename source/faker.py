import os
import random
from datetime import datetime, timedelta
from dotenv import load_dotenv
from supabase import create_client, Client

# --- Configuration ---
# Make sure you have a .env file in the same directory with these variables:
# SUPABASE_URL="your_supabase_url"
# SUPABASE_KEY="your_supabase_service_role_key"

load_dotenv()

# --- Initialize Supabase Client ---
# Fetches the Supabase URL and Key from your environment variables.
# It's crucial to use the service role key for admin-level access to bypass RLS.
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError(
        "Supabase URL and Key must be set in your .env file."
    )

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
TABLE_NAME = "paypal_webhooks" # The table to insert data into

def generate_mock_transactions():
    """
    Generates a list of mock PayPal transactions with a downward trend,
    a target average, and statistical outliers.
    """
    print("Starting transaction generation...")

    # --- Date Range Setup ---
    # Transactions will be generated from June 6th of the current year until today.
    today = datetime.now()
    start_date = datetime(today.year, 6, 6)
    if start_date > today:
        print(f"Start date {start_date.date()} is in the future. No transactions will be generated.")
        return []
    
    total_days = (today - start_date).days + 1
    print(f"Generating data for {total_days} days (from {start_date.date()} to {today.date()}).")

    # --- Outlier Setup ---
    # Randomly select 4 unique days within the date range to place our outliers.
    outlier_days = random.sample(range(total_days), 4)
    print(f"Outliers will be placed on days: {sorted([d + 1 for d in outlier_days])}")

    all_transactions = []
    total_amount = 0

    # --- Main Generation Loop ---
    # Iterate through each day in the specified range.
    for day_index in range(total_days):
        current_date = start_date + timedelta(days=day_index)

        # --- Downward Trend Logic ---
        # The base amount for transactions starts higher and decreases each day.
        # We start at an initial amount and reduce it based on how far we are through the period.
        initial_base_amount = 68.00 # Starting average amount
        final_base_amount = 38.00   # Ending average amount
        progress = day_index / (total_days - 1) if total_days > 1 else 1
        daily_base_amount = initial_base_amount - (initial_base_amount - final_base_amount) * progress

        # --- Daily Transaction Volume ---
        # Create a random number of transactions for the current day.
        # This range has been increased to ensure the total number of transactions exceeds 4500.
        num_transactions_today = random.randint(190, 210)

        for _ in range(num_transactions_today):
            # --- Transaction Amount Generation ---
            # Use a normal distribution to create some variance around the daily base amount.
            # This makes the data look more natural.
            amount = round(random.normalvariate(daily_base_amount, 8.5), 2)
            
            # Ensure the amount is not negative.
            if amount < 1.00:
                amount = round(random.uniform(1.00, 5.00), 2)

            # --- Outlier Injection ---
            # If today is one of our designated outlier days, make the next transaction a big one.
            if day_index in outlier_days:
                amount = round(random.uniform(250.00, 500.00), 2)
                outlier_days.remove(day_index) # Remove the day to ensure exactly 4 outliers

            # --- Timestamp Generation ---
            # Create a random, precise timestamp for sometime within the current day.
            random_seconds = random.randint(0, 86399)
            transaction_time = current_date + timedelta(seconds=random_seconds)
            
            # Format the timestamp into an ISO 8601 string, which is standard for APIs.
            iso_transaction_time = transaction_time.isoformat()

            # --- Assemble Transaction Record ---
            all_transactions.append({
                "amount": amount,
                "transaction_time": iso_transaction_time,
                # The original script did not include currency, but it's good practice.
                # "currency": "USD" 
            })
            total_amount += amount

    # --- Final Calculations & Output ---
    if all_transactions:
        average_amount = total_amount / len(all_transactions)
        print(f"\nGenerated a total of {len(all_transactions)} transactions.")
        print(f"Target average was ~53.00. Actual average: ${average_amount:.2f}")
    else:
        print("No transactions were generated.")

    return all_transactions

def upload_to_supabase(transactions: list):
    """
    Uploads a list of transaction records to the Supabase table in chunks
    to avoid payload size limits and timeouts.
    """
    if not transactions:
        print("No transactions to upload.")
        return

    chunk_size = 500  # Number of records to upload per API call
    total_records = len(transactions)
    print(f"\nPreparing to upload {total_records} records to '{TABLE_NAME}' table in chunks of {chunk_size}...")

    # Loop through the master list in chunk-sized steps
    for i in range(0, total_records, chunk_size):
        chunk = transactions[i:i + chunk_size]
        chunk_number = (i // chunk_size) + 1
        total_chunks = (total_records + chunk_size - 1) // chunk_size
        
        print(f"Uploading chunk {chunk_number}/{total_chunks} (records {i+1}-{min(i+chunk_size, total_records)})...")
        
        try:
            # Execute the insert for the current chunk
            data, error = supabase.table(TABLE_NAME).insert(chunk).execute()
            
            # The execute() method returns a tuple (APIResponse, error)
            if error:
                print(f"An error occurred during upload of chunk {chunk_number}:")
                print(error)
                # We stop the process on the first error to avoid partial data uploads
                print("Upload process stopped due to an error.")
                return 
        
        except Exception as e:
            print(f"An unexpected error occurred with chunk {chunk_number}: {e}")
            print("Upload process stopped due to an unexpected error.")
            return

    print(f"\n✅ Success! All {total_chunks} chunks have been uploaded to Supabase.")


if __name__ == "__main__":
    mock_data = generate_mock_transactions()
    
    # Optional: Confirmation before uploading
    if mock_data:
        # The 'y' is pre-filled, so you can just press Enter to confirm.
        proceed = input(f"Do you want to upload these {len(mock_data)} records? (Y/n): ").lower().strip()
        if proceed == '' or proceed == 'y':
            upload_to_supabase(mock_data)
        else:
            print("Upload cancelled by user.")
