# 🚗 CarHub - Second-Hand Car Marketplace

CarHub is a full-featured web platform built with Django for buying and selling second-hand cars in India. It provides a complete end-to-end user experience, from user registration and listing creation to a secure messaging system and seller reviews. The platform is designed to be intuitive for both buyers and sellers, with a clean, modern, and responsive user interface.
---

## ✨ Key Features

CarHub is packed with features designed to provide a seamless and trustworthy experience for all users.

### For Buyers:
* **Advanced Search & Filtering:** Users can browse all active listings with a powerful search bar and filter results by Brand, City, Year, Price Range, Transmission, and Fuel Type.
* **Detailed Listings:** Each car has a dedicated detail page featuring a photo gallery, key specifications (KMs Driven, Mileage, etc.), and a detailed description.
* **Car Comparison Tool:** Buyers can select up to three cars from the list view and see a side-by-side comparison of their features and price.
* **Wishlist:** Users can save their favorite listings to a personal wishlist for easy access later.
* **Secure Messaging:** Buyers can contact sellers directly through a built-in, secure messaging system to ask questions or negotiate.
* **Seller Profiles & Reviews:** Buyers can view seller profiles, including their average rating and feedback from previous transactions, to build trust.

### For Sellers:
* **Full Listing Management:** Sellers have a dedicated dashboard to view, edit, and delete their listings.
* **Easy Listing Creation:** A user-friendly form allows sellers to post new cars with all necessary details, including a main photo and multiple additional photos.
* **Performance Dashboard:** On their "My Listings" page, sellers can track the performance of each car, including how many users have **viewed** it and how many have added it to their **wishlist**.
* **Mark as Sold:** Sellers can easily mark their car as "SOLD" to finalize the transaction and remove it from the active listings.
* **Image Management:** Sellers can add or delete individual photos from their listings at any time.

### Platform & Administration:
* **Secure User Authentication:** Complete user registration, login, logout, and password management system.
* **Custom Admin Dashboard:** A powerful admin panel with custom analytics, including charts for listings by brand and status, and key metrics like total users and cars sold.
* **Full Moderation:** Administrators can manage all car listings, users, messages, and reviews from the backend.
---

## 🛠️ Tech Stack

* **Backend:** Python, Django
* **Frontend:** HTML, Tailwind CSS, JavaScript
* **Database:** SQLite (for development)
* **Key Django Packages:**
    * `Pillow` for image processing.

---

## 🚀 Getting Started

To get a local copy up and running, follow these simple steps.

### Prerequisites

* Python 3.x
* pip (Python package installer)

### Installation

1.  **Clone the repository:**
    ```sh
    git clone [https://github.com/your-username/your-repo-name.git](https://github.com/your-username/your-repo-name.git)
    cd your-repo-name
    ```

2.  **Create and activate a virtual environment:**
    ```sh
    # For Windows
    python -m venv venv
    .\venv\Scripts\activate

    # For macOS/Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install the required packages:**
    ```sh
    pip install -r requirements.txt
    ```

4.  **Apply database migrations:**
    This will create your local `db.sqlite3` file with all the necessary tables.
    ```sh
    python manage.py makemigrations
    python manage.py migrate
    ```

5.  **Create a superuser:**
    This will create an administrator account so you can access the admin panel.
    ```sh
    python manage.py createsuperuser
    ```
    Follow the prompts to create your username and password.

6.  **Run the development server:**
    ```sh
    python manage.py runserver
    ```
    Your website will be available at `http://127.0.0.1:8000/`. You can access the admin panel at `http://127.0.0.1:8000/admin/`.

---

## 🔮 Future Enhancements

This project has a solid foundation. Future features could include:

* **Saved Searches & Email Alerts:** Allow users to save their filter settings and receive email alerts for new matching listings.
* **Real-Time Chat:** Upgrade the messaging system to a live chat using Django Channels.
* **Featured Listings:** Implement a system for sellers to feature their listings for better visibility.
