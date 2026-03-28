# 🎬 BookMySeat — Movie Ticket Booking System

A full-featured movie ticket booking web application built using Django. It allows users to browse movies, select seats, and book tickets online with integrated payment support.

---

## 🚀 Features

- Browse currently running movies  
- Interactive seat selection system  
- Secure user authentication (registration & login)  
- Online payments using Razorpay  
- Booking confirmation system  
- Movie posters and detailed information  
- User profile with booking history  
- Admin dashboard to manage movies, shows, and bookings  

---

## 🛠️ Tech Stack

| Technology        | Purpose                    |
|------------------|--------------------------|
| Python           | Backend programming       |
| Django 5.2       | Web framework             |
| SQLite           | Database (development)    |
| Razorpay         | Payment gateway           |
| HTML/CSS/JS      | Frontend                  |
| Pillow           | Image handling            |
| Gunicorn         | Production server         |
| python-dotenv    | Environment management    |

---

## 📦 Requirements

- Python 3.9 or higher  
- Git  
- Code editor (VS Code recommended)

---

## ⚙️ Local Setup

### 1. Clone the Repository


git clone https://github.com/vaishnabipanthi/bookmyseat-final.git
cd bookmyseat-final

2. Create a Virtual Environment
python -m venv venv
Activate it.
Windows:

venv\Scripts\activate

Mac/Linux:

source venv/bin/activate
3. Install Dependencies
pip install -r requirements.txt
4. Configure Environment Variables

Create a .env file in the root directory:
SECRET_KEY=your-secret-key
DEBUG=True

Generate a secret key:
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

5. Apply Migrations
python manage.py migrate

7. Create Admin User (Optional)
python manage.py createsuperuser

9. Run the Server
python manage.py runserver

Open in browser:
http://127.0.0.1:8000

Admin panel:
http://127.0.0.1:8000/admin

bookmyseat-final/
│
├── bookmyseat/        # Project settings
├── movies/            # Movie management app
├── users/             # Authentication app
├── templates/         # HTML templates
├── media/             # Uploaded images
├── manage.py
├── requirements.txt
└── Procfile

💳 Razorpay Setup
Create an account on Razorpay
Generate API keys from dashboard
Add them to .env:
RAZORPAY_KEY_ID=your_key_id
RAZORPAY_KEY_SECRET=your_key_secret

🌐 Deployment (Railway)
Push code to GitHub
Go to Railway → New Project
Deploy from GitHub repository
Add environment variables:
SECRET_KEY
DEBUG=False
RAZORPAY_KEY_ID
RAZORPAY_KEY_SECRET

Railway will automatically deploy your app.

❗ Common Issues
ModuleNotFoundError
→ Virtual environment not activated
No module named 'django'
→ Run:
pip install -r requirements.txt
Port already in use
→ Run:
python manage.py runserver 8080
Static files not loading
→ Run:
python manage.py collectstatic


👩‍💻 Author
Developed by Vaishnabi Panthi


