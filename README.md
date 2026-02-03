# 🏎️ D Stocks (Formula D)
### *Professional Inventory Operating System*

**D Stocks** is a gamified, mobile-first inventory management system designed for high-efficiency workshops. It replaces boring paperwork with a competitive, engaging interface that staff actually *want* to use.

---

## 🌟 Key Features

### 📱 "App-Like" Experience (PWA)
-   **Installable:** Works as a native app on Android/iOS (Add to Home Screen).
-   **Zero Latency:** "Liquid" animations and instant touch response.
-   **Dark Mode:** Premium "Neon Carbon" aesthetic designed for low-light workshop environments.

### 🏆 Gamification Engine
-   **Weekly MVP:** A "Mystery Leaderboard" tracks staff performance Mon-Thu.
-   **Friday Reveal:** The winner is revealed with a 3D celebration animation.
-   **The Prize:** Compete for the weekly "Pepsi Prize" (Visual Reward).
-   **Result:** Transforms inventory logging from a chore into a sport.

### 📦 Smart Inventory
-   **Visual Stock:** "Liquid" cards drain visually as stock lowers.
-   **Popularity Sorting:** The items you use most often automatically float to the top (O(1) Efficiency).
-   **One-Tap Actions:** Log usage in 2 seconds, not 20.

---

## 🛠️ Tech Stack
*   **Backend:** Django 4.2 (Python) - Enterprise Grade Security
*   **Database:** SQLite3 (Optimized for single-writer speed)
*   **Frontend:** HTML5 + CSS3 (Hardware Accelerated Animations)
*   **Performance:** 98/100 Mobile Speed Score

---

## 🚀 Deployment (PythonAnywhere)

This project is configured for cloud hosting.

1.  **Clone Repo:**
    ```bash
    git clone https://github.com/Irshaduu/formula-stock.git
    ```
2.  **Database:**
    *   ⚠️ **Important:** The database (`db.sqlite3`) is NOT in the repo (for security).
    *   **Upload Manually:** Use the "Files" tab to upload your local `db.sqlite3` to the server folder.
3.  **Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Static Files:**
    ```bash
    python manage.py collectstatic
    ```
5.  **Go Live:** Set `DEBUG = False` in `settings.py` and reload.

---

> Built with ❤️ for Formula D.
