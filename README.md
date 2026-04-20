# 🎓 DIUHub - A Centralized QR-Enabled Platform for University Clubs and Events

DIUHub is a **full-stack web application** designed for Daffodil International University to digitally manage **clubs, events, and attendance** using QR technology.

It replaces manual processes with a **secure, role-based, and automated system**.

---

## 🎯 Project Overview

* **Goal:** Automate attendance and event management using QR codes
* **Approach:** Django-based system with role-based access and real-time QR validation
* **Use Case:** University clubs, student organizations, and academic events

---

## ✨ Core Features

### 👤 User Management

* Secure login & registration
* Role-based system (Student / Admin / Superadmin)
* Editable student profile

---

### 🏫 Club System

* View all clubs
* Join request system
* Approval-based membership

---

### 📅 Event System

* Club-specific events
* Restricted registration (only approved members)
* Real-time registration tracking

---

### 📱 QR Code System

* Unique QR for each event registration
* Student “My QR” dashboard
* Secure QR validation

---

### 📷 Attendance System

* QR-based attendance scanning (webcam)
* Duplicate scan prevention
* Timestamp recording
* Attendance status tracking (Present / Absent)

---

### 🔐 Role-Based Access Control

| Role       | Permissions                    |
| ---------- | ------------------------------ |
| Student    | View clubs, events, My QR      |
| Admin      | Scan attendance, manage events |
| Superadmin | Full system access             |

---

## 📁 Project Structure

```bash
DIUHub/
├── users/             # Authentication & profile system
├── clubs/             # Club management
├── events/            # Event + QR generation
├── registrations/     # Event registrations
├── attendance/        # QR attendance system
├── templates/         # HTML templates
├── static/            # CSS, JS, assets
├── media/             # QR images
├── manage.py
└── requirements.txt
```

---

## ⚙️ Installation & Setup

### 1️⃣ Clone Repository

```bash
git clone https://github.com/simantapundori/DIUHub.git
cd DIUHub
```

---

### 2️⃣ Create Virtual Environment

```bash
python -m venv venv
```

Activate:

```bash
venv\Scripts\activate   # Windows
```

---

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 4️⃣ Database Setup

```bash
python manage.py makemigrations
python manage.py migrate
```

---

### 5️⃣ Create Superuser

```bash
python manage.py createsuperuser
```

---

### 6️⃣ Run Server

```bash
python manage.py runserver
```

Visit:

```
http://127.0.0.1:8000/
```

---

## 🔄 System Workflow

1. User registers and logs in
2. Student joins a club → approval required
3. Registers for an event
4. QR code is generated
5. Admin scans QR via webcam
6. Attendance is marked instantly

---

## 🛠️ Technologies Used

* **Backend:** Django (Python)
* **Frontend:** HTML, CSS, JavaScript
* **Database:** SQLite
* **QR System:** qrcode, html5-qrcode
* **Authentication:** Django Auth

---

## 📊 Key Functional Highlights

* ✔ Secure QR-based attendance
* ✔ Role-based system control
* ✔ Real-time validation
* ✔ Clean UI with dark mode
* ✔ Toast notification system

---

## 🧩 Future Enhancements

* 📄 Certificate generation system
* 📊 Admin analytics dashboard
* 📥 Export attendance to Excel
* 📱 Mobile camera optimization
* 🔔 Notification system
* 📥 Feedback
---

## 👨‍💻 Author

**Simanta Kumer Pundori** 
,Software Engineering Student
,Daffodil International University

---

## ⭐ Final Note

This project demonstrates:

* Full-stack web development
* Real-world system design
* Role-based architecture
* QR-based automation

👉 Built as a **capstone-level university project with real deployment potential**
