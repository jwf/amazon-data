# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Amazon Purchase Analytics — a full-stack web app for visualizing Amazon order history data. Python/Flask backend with SQLite, React/TypeScript frontend with Recharts.

## Development Commands

### Backend
```bash
python backend/app.py              # Start Flask server on port 5001 (debug mode)
python backend/import_data.py      # Import CSV data from data/ into amazon_data.db
```

### Frontend
```bash
cd frontend
npm start                          # Dev server on port 3000 with hot reload
npm run build                      # Production build to frontend/build/
npm test                           # Run tests via react-scripts
```

Both servers needed during development: backend on 5001, frontend on 3000.

## Architecture

**Backend** (`backend/`):
- `app.py` — Flask entry point, also serves the React production build
- `api/routes.py` — All API endpoints under `/api/` (Flask Blueprint)
- `data_processor.py` — Core query/analytics logic against SQLite (largest file)
- `database.py` — Schema definitions and DB initialization
- `import_data.py` — CSV-to-SQLite import pipeline

**Frontend** (`frontend/src/`):
- `App.tsx` — Main component, orchestrates all dashboard views
- `api.ts` — Axios client + TypeScript interfaces for all API responses
- `components/` — Chart and card components (Recharts-based): `SpendingOverTimeChart`, `DigitalVsRetailChart`, `RetailBreakdown`, `DigitalBreakdown`, `ReturnStatsCard`, `SummaryCard`, `CategoryOrderTable`, `DigitalOrderTable`

**Data flow**: CSV files → `import_data.py` → SQLite (`amazon_data.db`) → Flask API → React frontend

**Database tables**: `retail_orders`, `digital_items`, `returns`, `cart_items`

## Key Tech Choices

- Create React App (react-scripts 5) with TypeScript
- Tailwind CSS for styling
- Recharts for all chart visualizations
- Flask with flask-cors for cross-origin dev setup
- Raw SQLite queries (no ORM)
