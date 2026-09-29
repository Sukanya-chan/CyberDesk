# CyberDesk Phase 3

Implemented:
- public learning APIs
- admin learning CRUD
- draft/published visibility
- module/lesson ordering
- student catalogue, course detail and lesson reader
- simple admin content management UI
- standalone idempotent learning seed script
- API/progress documentation

Local verification commands:

```bash
PYTHONPATH=backend pytest -v
cd frontend
npm test -- --run
npm run build
```

Do not commit secrets, `.env`, local databases, virtual environments, or `node_modules`.
