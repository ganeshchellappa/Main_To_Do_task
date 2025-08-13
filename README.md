# To Do Translation App 📝🌐  
_A multilingual AI-powered task management application._

---

## 🔗 Live Links

- 🚀 **Live App**: [https://main-to-do-task-p83t.vercel.app/](https://main-to-do-task-p83t.vercel.app/)
- 💻 **GitHub Repository**: [https://github.com/ganeshchellappa/Main_To_Do_task](https://github.com/ganeshchellappa/Main_To_Do_task)

---

## 📌 Project Overview

# Task Manager with Translation (LLM-powered)

A simple task management app with:
- PostgreSQL (Neon) for data storage
- Frontend: HTML + JavaScript
- Backend: Python (Flask/FastAPI)
- LLM-powered task translation
- Deployment on Vercel

---

## 🚀 Features
- Add, edit, and delete tasks
- Store tasks in a Neon-hosted PostgreSQL database
- Translate tasks into different languages using an LLM API
- Deployed serverless on Vercel

---

## 🛠 Tech Stack
- **Frontend:** HTML, CSS, JavaScript
- **Backend:** Flask (depending on your version)
- **Database:** PostgreSQL (Neon)
- **LLM API:** OpenRouter
- **Deployment:** Vercel

---


## 📂 Project Structure

```bash

Main_To_Do_task/
├── my-venv/  
│
├── static/
│   ├── css/
│   └── js/
│
├── templates/
│   └── index.html
│
├── .env
├── app.py
├── requirements.txt
└── translate.py

```
---

## 📦 Setup Instructions (Local)

### 1️⃣ Clone the repository
```bash
git clone https://github.com/ganeshchellappa/Main_To_Do_task.git
cd your-repo

### 2. Configure environment variables

Create a `.env` file in the root directory:

```env
NEON_CONN_STRING=Your_Neo_DB_Credentials
API_KEY=Your_Open_Router_API_KEY
```


## 🚀 Deployment

This app is fully compatible with **Vercel**:

```bash
vercel --prod
```

Make sure your environment variables are added under Vercel project settings.

---

## 👤 Author

**Sree Ganesha Chellappa** <br/>
Developed during a technical assessment at **NeoSOFT Technologies**.

---
