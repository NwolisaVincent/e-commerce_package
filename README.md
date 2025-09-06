# 🛒 E-Commerce Backend (Python)

This is a backend system for an **E-commerce platform**.  
It is built with **Python** and designed to handle **user accounts, product management, shopping cart, orders, and payments**.  
The project follows a modular structure so that it can be extended to production-ready systems.

---

## 🚀 Features

### 👤 User Authentication
- Register (create account)
- Login / Logout
- JWT-based authentication
- Profile management

### 📦 Product Management
- Add, edit, delete products (Admin only)
- View all products
- Product categories & filtering
- Product details (price, description, stock, image, etc.)

### 🛒 Cart & Orders
- Add items to cart
- Remove items from cart
- Checkout process
- Create and track orders
- Order status updates (Pending, Processing, Delivered)

### 💳 Payments
- Supports **USD ($)** transactions
- Integration with **Stripe** or **PayPal**
- Secure payment processing

### 🔑 Admin Features
- Manage product inventory
- Manage orders (view, update status, cancel)
- Manage users

---

## 🏗️ Tech Stack

- **Python** (Django REST Framework)
- **db.sqlite3** (Database)
- **Django ORM** (ORM)
- **JWT** (Authentication)
- **Stripe / PayPal API** (Payments)
- **Docker** (optional, for containerization)

---

## 📂 Project Structure

ecommerce-backend/
│── app/
│ ├── models/ # Database models
│ ├── routes/ # API routes (auth, products, orders, etc.)
│ ├── services/ # Business logic
│ ├── utils/ # Helper functions
│ ├── init.py
│── tests/ # Unit tests
│── requirements.txt # Dependencies
│── config.py # Environment configs
│── README.md # Documentation
│── main.py # Application entry point
