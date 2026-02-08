# DIUHub git add README.md

DIUHub is a centralized platform designed for Daffodil International University students and faculty to manage attendance, clubs, events, and registrations efficiently.

## 🚀 Getting Started

### Prerequisites
* Python 3.10+
* Virtual Environment (env)

### Installation & Setup

1. **Clone the repository**
   ```bash
   git clone [https://github.com/simantapundori/DIUHub.git](https://github.com/simantapundori/DIUHub.git)
   cd DIUHub

2. Create virtual environment
    python -m venv venv

    venv\Scripts\activate   (Windows)

3. Install requirements

    pip install -r requirements.txt

4. Database Initialization Note: Ensure you are in the (env) before running these.

    python manage.py makemigrations

    python manage.py migrate

    python manage.py createsuperuser

5. Run the Application

    python manage.py runserver