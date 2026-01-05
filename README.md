# StockFlow Backend Case Study

## Overview
This is a minimal backend implementation for StockFlow, a B2B inventory management platform. 
It allows adding products, tracking inventory, and retrieving low-stock alerts.

## Features
- Add a new product with initial inventory
- Track inventory per warehouse
- Retrieve low-stock alerts with supplier information

## Technology
- Python 3
- Flask
- SQLAlchemy (SQLite database for simplicity)

## Assumptions
- Low-stock threshold is defined per product
- Each product has at least one supplier
- Recent sales tracking is not implemented in this minimal version
- Simplified relationships to focus on clarity and correctness

## How to Run
1. Clone the repository
2. Install dependencies:
   `pip install -r requirements.txt`
3. Run the app:
   `python app.py`
4. Use Postman or curl to test endpoints

## Future Improvements
- Add authentication and authorization
- Track sales and recent sales activity
- Support bundle products
- Move from SQLite to PostgreSQL or MySQL for production
