# 🏦 Credit System API

A backend system for managing customers and their loans, including credit eligibility checks, loan creation, and admin-level reporting — all fully Dockerized.

---

## 🚀 Features

- Register new customers
- Check loan eligibility based on income or credit history
- Create loans and calculate EMI
- View individual customer loans
- Admin view to list all loans
- Fully Dockerized with PostgreSQL
- Data load from CSV/Excel

---

## 🛠️ Tech Stack

- Python 3.11
- Django 5.x
- PostgreSQL (via Docker)
- Docker & Docker Compose

---

## 🛆 Installation (Local without Docker)

1. Clone the repo:

```bash
git clone https://github.com/your-username/credit_system.git
cd credit_system
```

2. Create a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Set up database:

```bash
python manage.py migrate
python manage.py load_initial_data  # optional: loads sample customers & loans
```

5. Run the server:

```bash
python manage.py runserver
```

---

## 🐳 Running with Docker

Ensure Docker and Docker Compose are installed and Docker Desktop engine is running.

1. Build & run the app:

```bash
docker-compose up --build
```

2. Visit: http://localhost:8000/

---

## 🔑 API Endpoints

All endpoints use application/json.

| Method | Endpoint                      | Description                             |
|--------|-------------------------------|-----------------------------------------|
| POST   | /register                     | Register a new customer                 |
| POST   | /check-eligibility            | Check loan eligibility                  |
| POST   | /create-loan                  | Create a loan if eligible               |
| GET    | /view-loans/<customer_id>     | View customer loans                     |
| GET    | /view-all-loans               | Admin: View all loans                   |

Example: Register a customer

POST /register

```json
{
  "first_name": "John",
  "last_name": "Doe",
  "age": 30,
  "monthly_salary": 50000,
  "phone_number": "1234567890"
}
```

---

## 📁 Project Structure

```
credit_system/
├── backend/
│   ├── core/
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── serializers.py
│   │   ├── management/
│   │   │   └── commands/load_initial_data.py
│   ├── settings.py
│   ├── urls.py
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── README.md
```

---

## 🥪 Testing

To run tests:

```bash
python manage.py test
```

---

## ✍️ Author

- Your Name — [@yourhandle](https://github.com/yourhandle)

---

## 📄 License

This project is licensed under the MIT License.
