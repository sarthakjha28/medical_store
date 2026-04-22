# Medical E-Commerce Platform with Chatbot

## Overview
Medical E-Commerce Platform with Chatbot is a full-stack pharmacy web application that allows users to register, log in, browse medicines, add products to a cart, update quantities, and complete a simple checkout flow. The project also includes a rule-based chatbot that provides basic medical guidance for common symptoms.

## Features
- User Registration and Login
- Medicines Listing with Images
- Add to Cart Functionality
- Cart Quantity Increase and Decrease
- Remove Item from Cart
- Total Price Calculation
- Payment Page
- Address Page
- Rule-Based Chatbot for Basic Medical Guidance

## Technologies Used
- **Frontend:** HTML, CSS, JavaScript
- **Backend:** FastAPI
- **Database:** MySQL

## Project Structure
```bash
medical_store/
│
├── backend/
│   ├── medical_store.py
│   └── db.py
│
├── frontend/
│   ├── medical_store_index.html
│   ├── medical_store_login.html
│   ├── medical_store_register.html
│   ├── medical_store_medicines.html
│   ├── medicine_store_cart.html
│   ├── payment.html
│   ├── medical_store_address.html
│   └── images/
