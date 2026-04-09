# DSI Sales Dashboard 📊

A full-stack, responsive sales dashboard web application built with **React (Vite)** and **Django**. This project is designed to fetch, visualize, and manage sales data directly using a serverless architecture by leveraging Google Sheets as the database via the **Sheety API**.

## 🚀 Features
- **Interactive Data Visualization:** View KPI summaries including Gross Sales, Net Revenue, Returns, and Local Currency (LC) values.
- **Dynamic Charting:** Features Donut charts and other visual analytics for "Sales by Material Group" and "Top Customers".
- **Google Sheets as DB:** Replaced traditional file-based Excel storage with **Sheety API** to provide full CRUD operations directly on a Google Sheet.
- **Serverless-Ready (Vercel):** The architecture guarantees read-only file system compatibility with platforms like Vercel and AWS Lambda.
- **Responsive Design:** A fully responsive, modern interface styled using **Tailwind CSS**.

## 🛠️ Tech Stack
- **Frontend:** React, Vite, Tailwind CSS, Recharts/Chart.js
- **Backend:** Django Rest Framework (Python)
- **Database / API:** Google Sheets & [Sheety API](https://sheety.co/)
- **Deployment:** Vercel (Ready)

---

## 💻 Running Locally

### 1. Backend (Django API) Setup
1. Open your terminal and navigate to the `backend` folder:
    ```bash
    cd backend
    ```
2. Create and activate a Virtual Environment (Optional but recommended):
    ```bash
    python -m venv venv
    venv\Scripts\activate   # For Windows
    ```
3. Install the required Python dependencies:
    ```bash
    pip install -r requirements.txt
    # Or manually install them: pip install django djangorestframework django-cors-headers pandas numpy requests
    ```
4. Start the Django development server:
    ```bash
    python manage.py runserver
    ```
    *The backend API will run on `http://localhost:8000/`*

### 2. Frontend (React) Setup
1. Open a **new terminal tab** and navigate to the `frontend` folder:
    ```bash
    cd frontend
    ```
2. Install Node.js dependencies:
    ```bash
    npm install
    ```
3. Start the Vite development server:
    ```bash
    npm run dev
    ```
    *The frontend will run on `http://localhost:5173/`*

---

## 🌐 Sheety API Integration (Database)
The Django backend interacts with Google Sheets via Sheety to bypass serverless (read-only) deployment restrictions. 
The integration file can be found at `backend/api/excel_handler.py`. 
* **GET:** Fetches all data on application launch to heavily cache responses for speed.
* **POST/PUT/DELETE:** Any modifications made on the frontend update the Google Sheet live in real-time.

> **Note:** To connect your own data, replace the `SHEETY_URL` inside `excel_handler.py` with your personal Sheety endpoint URL.

---

## 📦 Deployment (Vercel)

This application is customized to be seamlessly deployed onto Vercel. 
Since the backend utilizes Sheety instead of a strict `.xlsx` file, it complies with Vercel's Ephemeral File System guidelines.

**To Deploy:**
1. Connect this repository to your **Vercel** account.
2. In the Root directory, ensure you have an appropriate `vercel.json` configured with `builds` pointing to `@vercel/python` for the backend and `@vercel/vite` for the frontend.
3. Configure your API Rewrites within `vercel.json` to route `/api/*` to your Django WSGI entry point.
4. Deploy! 🎉
