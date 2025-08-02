
from fastapi import FastAPI, Request
from supabase import create_client
from dotenv import load_dotenv
import os, json
#imports

load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
#getting values from .env

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
#creates connection to supabase db 

app = FastAPI()
#creates an instance of the FastAPI framework

@app.post("/paypal/webhook") #when our server recieves a post request from the argument url the function below is executed
async def paypal_webhook(request: Request):
    payload = await request.json() #payload is equal to the payment request 

    resource = payload.get("resource", {}) #gets the values at the dictionary key resource and sets them equal to a local resource value
    
    transaction_time = resource.get("create_time") #gets time from resource dictionary and sets to transaction_time as a "string"
    amount_str = resource.get("amount", {}).get("value") #gets amount from resource dictionary and sets to amount as a "string"

    try:
        amount = float(amount_str) if amount_str is not None else None
    except (ValueError, TypeError):
        amount = None
    #converts amount from s string to a float and if conversion returns an error the except sets amount to None

    supabase.table("paypal_webhooks").insert({
        "amount": amount,
        "transaction_time": transaction_time,
    }).execute()
    #inserts amount and trans time into my supabase db whenever the webhook is triggered

    return {"status": "received"}


