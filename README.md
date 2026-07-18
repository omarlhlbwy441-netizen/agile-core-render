# AGILE Core System

## Features
- Project Management with Sprints
- Kanban Board (Backlog, Todo, In Progress, Review, Done)
- Task Management with Story Points
- Real-time WebSocket Updates
- Analytics & Velocity Tracking
- Role-based Access Control

## Tech Stack
- FastAPI
- SQLAlchemy + PostgreSQL
- Redis
- WebSocket
- JWT Authentication

## API Endpoints
- `POST /api/v1/auth/register` - Register
- `POST /api/v1/auth/login` - Login
- `GET /api/v1/projects/` - List projects
- `POST /api/v1/projects/` - Create project
- `GET /api/v1/tasks/kanban/{project_id}` - Kanban board
- `GET /api/v1/analytics/project/{project_id}/overview` - Project analytics
- `WS /ws/realtime` - Real-time updates

## Deployment
```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```
