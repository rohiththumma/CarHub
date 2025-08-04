# 🚗 CarHub - A Full-Featured Car Marketplace

CarHub is a complete web application built with Django that allows users to buy and sell second-hand cars. It features a clean, modern interface and a robust set of features designed to create a trustworthy and user-friendly online marketplace.

## ✨ Key Features

* **User Authentication:** Secure user registration, login, profile editing, and password management.
* **Comprehensive Listings:** Users can post detailed car listings with multiple images, key specifications (make, model, year, kms driven), and descriptions.
* **Advanced Search & Filtering:** A powerful search and filter system allows buyers to find cars by brand, city, price range, fuel type, and more.
* **Interactive Car Comparison:** Users can select up to three cars to compare their specifications side-by-side in a detailed table view.
* **Real-time Messaging:** A private, chat-style messaging system for direct communication between buyers and sellers. Includes unread message notifications.
* **Wishlist & Reviews:** Buyers can add cars to their wishlist and leave reviews with ratings for sellers after a purchase.
* **Seller Engagement:** Sellers can publicly respond to reviews left on their profile, building trust and community.
* **Custom Admin Dashboard:** A rich, interactive dashboard for site administrators with analytics on user growth, listing statuses, and a live "Recent Activity" feed.

## 🛠️ Tech Stack

* **Backend:** Python, Django
* **Frontend:** HTML, CSS, JavaScript
* **Styling:** Tailwind CSS
* **Database:** SQLite (for development)
* **Key Libraries:** Pillow (for image handling), Chart.js (for admin dashboard visualizations)

## 🚀 Setup and Installation

To run this project locally, follow these steps:

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/your-username/CarHub.git](https://github.com/your-username/CarHub.git)
    cd CarHub
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    # For Windows
    python -m venv venv
    venv\Scripts\activate

    # For macOS/Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Apply database migrations:**
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

5.  **Create a superuser to access the admin panel:**
    ```bash
    python manage.py createsuperuser
    ```

6.  **Run the development server:**
    ```bash
    python manage.py runserver
    ```
    The application will be available at `http://127.0.0.1/`.

## 🤖 AI-Assisted Development

This project was developed by a single developer. To enhance productivity and explore modern development workflows, AI assistance (powered by Google Gemini) was used for tasks such as code analysis, feature brainstorming, debugging, and generating boilerplate content. All core logic and final implementation were directed and written by the developer.

## 📸 Screenshots

*(You should add screenshots of your application here to showcase the different pages like the landing page, car detail page, and the admin dashboard.)*
