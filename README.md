WealthFy: AI-Powered Personal Finance Dashboard

WealthFy is a modern, responsive web application designed to help users track their income and expenses, visualize their financial health, and gain intelligent insights through a conversational AI assistant.

This project was built as a full-stack application with a React frontend, a Python FastAPI backend, and deployed on AWS.

Features

Secure Authentication: User registration and login system with JWT-based authentication.

Interactive Dashboard: At-a-glance view of total net balance, monthly income vs. expense charts, and an expense breakdown pie chart.

Transaction Management: A comprehensive list of all transactions with the ability to add new income or expenses.

AI Financial Advisor: A conversational chatbot powered by Google's Gemini API that answers user questions based on their personal financial data.

Financial Calculators: Built-in tools for calculating SIP (Systematic Investment Plan) and EMI (Equated Monthly Instalment).

Fully Responsive: A mobile-first design that works seamlessly on desktops, tablets, and mobile devices.

Tech Stack

Frontend

Framework: React.js

Routing: React Router

API Communication: Axios

Styling: CSS3 with a mobile-first, responsive approach

Charting: Recharts

Backend

Framework: FastAPI (Python)

Database: PostgreSQL with SQLModel for ORM

Authentication: JWT (JSON Web Tokens) with password hashing (bcrypt)

AI Integration: Google Gemini API

Deployment

Frontend: AWS Amplify

Backend: AWS App Runner (via Docker)

Database: AWS RDS for PostgreSQL

Getting Started

To get a local copy up and running, follow these simple steps.

Prerequisites

Python 3.9+

Node.js and npm

A running PostgreSQL database instance

A Google Gemini API Key

Backend Setup

Clone the repository:

git clone [https://github.com/your-username/Personal-Finance-AI.git](https://github.com/your-username/Personal-Finance-AI.git)
cd Personal-Finance-AI/backend


Create and activate a virtual environment:

# For Windows
python -m venv myenv
myenv\Scripts\activate

# For macOS/Linux
python3 -m venv myenv
source myenv/bin/activate


Install Python dependencies:

pip install -r requirements.txt


Set up environment variables:

Create a file named .env in the backend directory.

Add the following variables, replacing the placeholder values:

DATABASE_URL="postgresql://YOUR_DB_USER:YOUR_DB_PASSWORD@localhost/YOUR_DB_NAME"
SECRET_KEY="your_super_long_and_random_secret_key"
GEMINI_API_KEY="your_google_gemini_api_key"
FRONTEND_URL="http://localhost:3000"


Run the backend server:

uvicorn app.main:app --reload


The server will be running at http://127.0.0.1:8000.

Frontend Setup

Navigate to the frontend directory:

cd ../frontend


Install Node.js dependencies:

npm install


Set up environment variables:

Create a file named .env.local in the frontend directory.

Add the following variable to point to your local backend:

REACT_APP_API_BASE_URL="[http://127.0.0.1:8000](http://127.0.0.1:8000)"


Run the frontend development server:

npm start


The application will open in your browser at http://localhost:3000.


