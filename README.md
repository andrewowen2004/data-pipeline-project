# Real Time Fraud Detection Pipeline

> This pipeline ingests donations and flags potentially fraudulent transactions in real time on a monitoring dashboard.

---

## Table of Contents

- [About](#about)
- [Features](#features)
- [Tech Stack](#tech-stack)

---

## What?

Explain what the project is, the problem it solves, and who it's for. Include a short paragraph that would make a stranger understand the *what* and *why* of this project.

Example:
> This project forecasts trail development in parks using machine learning. It helps park managers allocate maintenance resources by predicting where and how long new trails will be built over the next 10 years.

---

## Why?

I strongly believe in the power of generosity and the importance of enabling people to give back. That’s why it's equally critical to protect against misuse—such as the example below. This project aims to detect and prevent misuse in quickly, preserving trust in donation programs.

https://www.cbsnews.com/sanfrancisco/news/apple-6-former-employees-accused-charity-scam/
---

## How?

**Technologies used:**

- **Frontend:** Streamlit (Python-based UI)
- **Backend:** FastAPI (for webhook handling and API integration)
- **Database:** Supabase (PostgreSQL-based real-time database)
- **ML/Analytics:** Python / Pandas / Matplotlib
- **Hosting:** Streamlit Cloud / Supabase Hosting

---

Incoming donation data is captured in real-time using a **FastAPI webhook**. When a transaction is made, the webhook receives the payload and stores it in a **Supabase database**, enabling low-latency ingestion.

Our **Streamlit dashboard** continuously polls the Supabase database at short intervals, retrieving the latest donations. The dashboard then processes the data using **Pandas**, flags potentially fraudulent donations, and computes summary statistics like the **mean donation amount**. These insights are visualized using **Matplotlib** and displayed on a live monitoring interface built entirely with **Streamlit**.

This system enables near real-time fraud detection and donation analysis with minimal latency between ingestion and visualization.


## 📬 Contact

Created by [Your Name](https://github.com/yourusername)  
Reach me via: your.email@example.com  
LinkedIn: [your-link](https://linkedin.com/in/yourprofile)