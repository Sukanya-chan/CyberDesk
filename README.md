# 🛡️ CyberDesk

> Interactive cybersecurity learning and practical platform for students.

CyberDesk combines structured learning, assessments, safe CTF-style challenges, progress tracking, authentication, and an optional AI tutor in one web application.

## 🌐 Live Services

- **Live Demo:** Frontend deployment is being finalized.
- **API:** https://cyberdesk-pldr.onrender.com
- **API Docs:** https://cyberdesk-pldr.onrender.com/docs
- **API Health:** https://cyberdesk-pldr.onrender.com/api/health

## ✨ Features

- 🔐 Clerk authentication and student/admin authorization
- 📚 Categories, courses, modules, and lessons
- 📝 Quizzes, MCQs, attempts, scoring, results, and retry
- 🧩 Safe cybersecurity challenges with hints, flags, solved state, and points
- 📊 Student progress dashboard
- 🤖 Optional Gemini-powered defensive AI Tutor
- 👨‍💻 Protected admin content management
- 🔌 FastAPI REST API
- 🧪 Automated backend and frontend testing
- 🛡️ Defensive security design with no arbitrary code execution or real-target scanning

## 🏗️ Architecture

```text
React + TypeScript Frontend
          │
          │ REST / HTTPS
          ▼
FastAPI Backend
   │       │       │
   ▼       ▼       ▼
SQLite   Clerk   Gemini
Database  Auth   Optional AI
```

## 🧱 Project Structure

```text
CyberDesk/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── core/
│   │   ├── models/
│   │   ├── schemas/
│   │   └── services/
│   └── tests/
├── frontend/
│   └── src/
├── context/
├── specs/
├── .ai/
├── DEPLOYMENT.md
└── PHASE6_8_IMPLEMENTATION.md
```

## 🚀 Development Phases

| Phase | Module | Status |
|---|---|:---:|
| 1 | Foundation | ✅ |
| 2 | Authentication & Authorization | ✅ |
| 3 | Learning Content System | ✅ |
| 4 | Assessment System | ✅ |
| 5 | Cybersecurity Challenges | ✅ |
| 6 | Progress & Student Dashboard | ✅ |
| 7 | AI Tutor | ✅ |
| 8 | Production Readiness | ✅ |

## 🛠️ Technology Stack

**Frontend:** React, TypeScript, Vite, CSS  
**Backend:** Python, FastAPI, SQLAlchemy, SQLite  
**Authentication:** Clerk  
**AI:** Google Gemini API  
**Testing:** pytest, Vitest  
**Version Control:** Git, GitHub  
**Deployment:** Render

## 🧪 Testing

| Area | Result |
|---|---:|
| Backend tests | **31 passed** |
| Frontend tests | **4 passed** |
| Production frontend build | **Successful** |
| Public API health | **Live** |
| FastAPI Swagger | **Live** |

Authentication boundaries were also verified, including unauthenticated 401 responses and unauthorized student access to admin functionality returning 403.

## 🔐 Security

CyberDesk is designed as a controlled educational platform. It deliberately avoids arbitrary code execution, shell execution, real-target network scanning, credential theft workflows, persistence mechanisms, and unrestricted offensive automation.

Challenge flags are validated using hashed values. The AI Tutor is optional and constrained toward defensive cybersecurity education.

## 📊 Progress Dashboard

The dashboard tracks completed lessons, total published lessons, course completion percentage, quiz attempts, best quiz score, solved challenges, challenge points, and recent learning activity.

## 🤖 AI Tutor

The AI Tutor uses a backend-mediated Gemini integration so the Gemini API key remains server-side. The core learning platform does not depend on AI availability.

## 🔌 API

The backend provides routes for learning content, lesson progress, assessments, challenges, dashboard data, administrative operations, health monitoring, and optional AI assistance.

**Interactive documentation:** https://cyberdesk-pldr.onrender.com/docs

## 💻 Local Development

### Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Create local environment files from the `.env.example` templates. Never commit real API keys or secret credentials.

## ☁️ Deployment

CyberDesk uses a separated frontend/backend deployment model:

```text
React + Vite
     │
     ▼
Render Static Site
     │ HTTPS
     ▼
Render FastAPI Web Service
     ├── SQLite
     ├── Clerk
     └── Gemini
```

See [DEPLOYMENT.md](DEPLOYMENT.md) for deployment configuration and production-readiness notes.

> For durable production data, PostgreSQL should replace SQLite. The current deployment is intended primarily for demonstration and academic project use.

## 📖 Documentation

- [Deployment Guide](DEPLOYMENT.md)
- [Phase 6–8 Implementation](PHASE6_8_IMPLEMENTATION.md)
- [API Specification](specs/API.md)
- [Project Context](context/)
- [Technical Specifications](specs/)
- [AI Development Workflow](.ai/)

## 🔭 Future Scope

- PostgreSQL-based persistent deployment
- Expanded cybersecurity courses and CTF challenges
- Advanced learning analytics
- Adaptive learning paths
- Improved search and discovery
- Additional AI-assisted learning tools
- PWA/mobile support

## 👩‍💻 Author

**Sukanya Bhuneshwar Singh Chandra**  
Third Year B.Sc. Computer Science  
GitHub: [@Sukanya-chan](https://github.com/Sukanya-chan)

## 📄 License

This project is currently maintained as an academic/student project.