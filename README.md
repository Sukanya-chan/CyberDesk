# 🛡️ CyberDesk

CyberDesk is an interactive cybersecurity learning and practical platform designed for students to learn security concepts, test their knowledge, solve safe cybersecurity challenges, and track their learning progress in one place.

The project combines structured cybersecurity education with assessments, controlled CTF-style challenges, authentication, progress analytics, and an optional AI-powered defensive cybersecurity tutor.

## 🌐 Live

- **Website:** `YOUR_FRONTEND_RENDER_URL`
- **API:** https://cyberdesk-pldr.onrender.com
- **API Docs:** https://cyberdesk-pldr.onrender.com/docs
- **API Health:** https://cyberdesk-pldr.onrender.com/api/health

> The FastAPI backend is currently live on Render. The frontend URL will be added after the frontend deployment is completed.

---

## ⚙️ Current v1.0 Features

- React + TypeScript cybersecurity learning interface
- Clerk authentication and role-based authorization
- Cybersecurity course → module → lesson hierarchy
- Published/draft learning content
- Interactive cybersecurity assessments
- MCQ questions and automatic scoring
- Quiz attempts and result history
- Safe CTF-style cybersecurity challenges
- Challenge hints and flag validation
- Challenge points and solved-state tracking
- Student progress dashboard
- Course completion tracking
- Quiz statistics
- Challenge statistics
- Protected admin content management
- Optional Gemini-powered AI Tutor
- REST API through FastAPI
- Automated backend and frontend testing
- Production-ready deployment configuration

---

## 🧠 Core Modules

### 📚 Learning System

CyberDesk organizes learning content as:

```text
Category
   └── Course
        └── Module
             └── Lesson
