# 🏎️ Formula D Store - Consumables Tracking System

An internal tool designed for the **Formula D Workshop** to track consumables (Oil, Coolant, Sprays), manage stock levels, and gamify staff performance.

## 🌟 Key Features

### 📦 Consumables Tracking
-   **Real-time Stock Levels:** Visual indicators for stock status:
    -   🟢 **Green:** Healthy (>50%)
    -   🟡 **Yellow:** Low (25-50%)
    -   🔴 **Red:** Critical (<25%)
-   **One-Click "Take":** Simple workflow for staff to log usage.
-   **Restock Mode:** Admin interface to quickly update inventory.

### 🏆 Gamification & Leaderboard
-   **Lifetime Leaderboard:** Tracks total credits earned by staff over time.
-   **🏎️ Weekly Race:**
    -   **Mon-Thu:** "Mystery Box" hides the current leader to keep suspense.
    -   **Friday:** Winner is revealed with a celebration animation!
    -   **Prize:** Visual 3D "Apple Fizz" floating prize for the weekly MVP.

### 📱 "Skinny Mode" (Mobile First)
-   Fully optimized for mobile devices.
-   Compact UI to minimize scrolling and maximize data visibility.
-   Dark/Light mode support (defaulting to a premium Dark theme).

## 🛠️ Tech Stack
-   **Backend:** Django (Python)
-   **Database:** SQLite3 (Portable & Robust)
-   **Frontend:** HTML5, CSS3 (Vanilla, Custom Design System)

## 🚀 Quick Start (Local)

1.  **Clone the Repository**
    ```bash
    git clone https://github.com/Irshaduu/formula-stock.git
    cd formula-stock
    ```

2.  **Set up Virtual Environment**
    ```bash
    python -m venv venv
    venv\Scripts\activate
    ```

3.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the Server**
    ```bash
    python manage.py runserver
    ```

5.  **Access the App**
    -   Open `http://127.0.0.1:8000` in your browser.

## ☁️ Deployment (PythonAnywhere)

1.  **Pull Code:** Clone this repo into your PythonAnywhere console.
2.  **Database:** The `db.sqlite3` is included in the repo, so your users, stock, and history will be live immediately.
3.  **Static Files:** Run `python manage.py collectstatic` to serve CSS/Images.
4.  **Web App:** Configure the WSGI file to point to your project.
