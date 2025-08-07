# Real Time Fraud Detection Pipeline

## [Project Video](www.linkedin.com/in/andrewowen2027)


This pipeline ingests donations and displays potentially fraudulent transactions on a real-time dashboard.

---

## Why?

I strongly believe in the power of generosity and the importance of enabling people to give back. That’s why it's equally critical to protect against misuse, such as the example below. This project aims to detect and prevent misuse quickly, preserving security in digital donation platforms.

Example misuse:
> https://www.cbsnews.com/sanfrancisco/news/apple-6-former-employees-accused-charity-scam/

---

## How?

**Technologies used:**

- **Frontend:** HTML / CSS / JavaScript
- **Backend:** FastAPI (Python)
- **Dashboard:** Streamlit (Python)
- **Database:** Supabase (PostgreSQL)
- **Analytics:** Pandas / Matplotlib


A user initiates a donation on the frontend via the PayPal SDK.

Upon successful payment to a specific PayPal account, PayPal's servers automatically send a webhook—a POST request containing the donation details—to a public URL managed by ngrok.

Ngrok securely tunnels this request to the FastAPI backend. The application receives the webhook data and immediately inserts it into a Supabase database.

A separate Streamlit application functions as the monitoring dashboard. It continuously polls the Supabase database at frequent intervals. When it detects a new entry, it filters the data to identify suspicous donations and updates the dashboard, creating a near real-time display.

This entire process creates a seamless flow from a one-time user action to a persistent and dynamically updated administrative view.

---

## Contact Me

Created by [Andrew Owen](www.linkedin.com/in/andrewowen2027)  
Email: ao9@iu.edu
LinkedIN: [Connect](www.linkedin.com/in/andrewowen2027)