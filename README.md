# 🛡️ AI Secure Data Intelligence Platform

A full-stack security scanner that detects secrets, PII, and attack patterns in text, files, SQL, chat, and log data using a four-layer detection pipeline (regex, statistics, ML-style anomaly scoring, and AI).

![Python](https://img.shields.io/badge/Python-3.11-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?logo=fastapi&logoColor=white)
![React](https://img.shields.io/badge/React-18-61DAFB?logo=react&logoColor=black)
![TypeScript](https://img.shields.io/badge/TypeScript-5.5-3178C6?logo=typescript&logoColor=white)
![Vite](https://img.shields.io/badge/Vite-5-646CFF?logo=vite&logoColor=white)

🌐 **[Live Demo](https://sisa-hackathon.vercel.app/)** &nbsp;·&nbsp; 📖 **[API Docs (Swagger)](https://secureai-backend-3yg7.onrender.com/docs)** &nbsp;·&nbsp; ⚡ **[Backend API](https://secureai-backend-3yg7.onrender.com/)** &nbsp;·&nbsp; 💻 **[Source Code](https://github.com/Kondareddy1209/AI_Secure_Data_Intelligence_Platform)**

> ⚠️ The backend is hosted on Render's free tier and may take ~30–50s to spin up after a period of inactivity.

---

## 🎥 Demo

> 🎥 Demo video coming soon.

---

## 🖥️ Screenshots

> The repository does not currently include screenshot assets. Add real screenshots to a `screenshots/` folder and reference them below, for example:
>
> `screenshots/dashboard.png` · `screenshots/analysis.png` · `screenshots/logs.png`

---

## 🎯 Overview

- **What it is** — a FastAPI backend paired with a React/TypeScript dashboard that scans arbitrary content (`text`, `file`, `sql`, `chat`, `log`) for sensitive data exposure and attack indicators, then scores and reports on the risk found.
- **What it solves** — accidental secret leakage (API keys, passwords, tokens, private keys, connection strings), PII exposure (SSNs, credit cards, emails), and attack traffic hiding in application/system logs (brute force, SQL injection, XSS, path traversal, privilege escalation).
- **How it detects** — every request runs through up to four independent layers: a 22-pattern regex engine, a statistics engine (Shannon entropy, z-score anomaly windows), a lightweight Isolation-Forest-inspired ML scorer, and an AI reasoning layer (Gemini, with an Anthropic Claude fallback) that produces plain-English remediation insights.
- **Risk-aware by design** — every finding is weighted and rolled into a single risk score, mapped to a risk level, and paired with a policy decision (`allowed` / `masked` / `blocked`) so the platform can be plugged into a gate, not just a report.
- **Observable** — every backend request and detection event is logged in-memory and streamed live to the frontend over Server-Sent Events, so you can watch the system reason about traffic in real time.

---

## ✨ Key Features

### 🔍 Input Types
- Plain **text**, uploaded **files**, raw **SQL** queries, **chat** transcripts, and **log** files — selectable from the dashboard sidebar.
- Log/SQL file uploads auto-detect their `input_type` from the file extension.

### 🧠 Detection Engines
- **Regex engine** — 22 named patterns covering credentials, PII, and injection payloads (see [Detection Patterns](#-detection-patterns) below).
- **Statistical engine** — Shannon-entropy scoring for high-entropy secrets, z-score credential-density outliers, multi-pattern-per-line correlation, and z-score failure-rate spikes.
- **Log-specific analysis** — brute-force detection (5+ consecutive failed logins), IP classification (loopback / private / reserved / public), and correlation of public IPs with attack or failed-login activity.
- **ML anomaly layer** — a hand-rolled, Isolation-Forest-inspired scorer built on entropy, keyword density, and character-ratio features; flags credential-density anomalies, injection-pattern anomalies, and multi-finding correlation spikes.
- **AI insight layer** — Google Gemini is the default provider (`AI_PROVIDER=gemini`), with automatic fallback to Anthropic Claude (`claude-sonnet-4-6`) if Gemini is unavailable, and a final fallback to rule-based, template-driven insights if neither AI service can be reached.

### 🛡️ Security & Policy
- **Type-aware masking** — emails, passwords, API keys, bearer tokens, and JWTs get pattern-specific redaction; everything else falls back to a generic `[MASKED]` value.
- **Policy engine** — maps risk level + request options to an `allowed` / `masked` / `blocked` action.
- **Optional bearer-token auth** — off by default; enabled via `REQUIRE_API_BEARER_TOKEN=true` and validated against `API_BEARER_TOKEN`.
- **CORS allowlist** — explicit origins plus a regex allowing any `*.vercel.app` preview deployment.

### 📊 Risk Assessment
- Findings are weighted (`critical=4, high=3, medium=2, low=1`), summed, and capped at **15**.
- Score → level thresholds: **critical ≥ 11**, **high ≥ 7**, **medium ≥ 4**, **low < 4**.
- Each response includes a human-readable summary, a detection breakdown by method, and the resulting policy `action`.

### 📡 Real-Time Monitoring
- Every request is timed, logged, and broadcast through an SSE stream (`/api/logs/stream`) with a live in-memory history of the last **100** events (`/api/logs/history`).
- The frontend includes a toggleable live-logs viewer that consumes this stream directly.

### 🤖 AI/ML
- Dual-provider AI gateway (Gemini primary → Claude fallback → rule-based fallback) with structured error handling for timeouts, rate limits, auth failures, and exhausted credits.
- Lightweight, dependency-free anomaly scoring (no external ML library) driven by entropy and keyword-density features.

---

## 🏗️ Architecture
```
┌─────────────────────┐
│   Browser (React)   │
│  (localhost:5173)   │
└──────────┬──────────┘
           │
           │ HTTP/REST
           ▼
┌─────────────────────────────────┐
│  FastAPI Backend (Python)       │
│  (localhost:8000)               │
│  ├─ /api/analyze                │
│  ├─ /api/logs/history           │
│  ├─ /api/logs/stream (SSE)      │
│  └─ /health                     │
└──────────┬──────────────────────┘
           │
           │ SDK
           ▼
┌─────────────────────┐
│  Anthropic Claude   │
│  (claude-sonnet)    │
└─────────────────────┘
```

```mermaid
flowchart TD
    A[React + TypeScript Frontend<br/>Vite, Vercel] -->|REST + SSE| B[FastAPI Backend<br/>Render]
    B --> C1[Regex Engine<br/>22 patterns]
    B --> C2[Statistical Engine<br/>entropy / z-score / IP + brute-force]
    B --> C3[ML Anomaly Scorer<br/>Isolation-Forest-inspired]
    C1 --> D[Risk Engine<br/>weighted score, 4 levels]
    C2 --> D
    C3 --> D
    D --> E{AI Insight Gateway}
    E -->|primary| F1[Gemini]
    E -->|fallback| F2[Claude Sonnet]
    E -->|fallback| F3[Rule-based insights]
    D --> G[Policy Engine<br/>mask / block / allow]
    G --> H[/analyze response/]
    B --> I[Request Logger Middleware]
    I --> J[(In-memory log buffer, 100 entries)]
    J --> K[/api/logs/history]
    J --> L[/api/logs/stream — SSE]
```

---

## 📦 Tech Stack

| Layer | Technology |
|---|---|
| **Frontend** | React 18 + TypeScript + Vite (custom CSS, no UI framework) |
| **Backend** | FastAPI 0.115 on Python 3.11 |
| **AI providers** | Google Gemini (`google-generativeai`, primary) · Anthropic Claude (`anthropic` SDK, fallback) |
| **Validation** | Pydantic v2 / `pydantic-settings` |
| **Realtime transport** | Server-Sent Events (`StreamingResponse`) |
| **Storage** | In-memory only — no database is used |
| **Testing** | pytest |
| **Backend deployment** | Docker (`python:3.11-slim`) → Render (`render.yaml`) |
| **Frontend deployment** | Vercel (`vercel.json`); a Docker/Nginx image is also provided for self-hosting |
| **Local orchestration** | Docker Compose |

---

## 🔌 API Reference

Base URL: `https://secureai-backend-3yg7.onrender.com` (or `http://localhost:8000` locally)

| Method | Path | Description |
|---|---|---|
| `GET` | `/` | Service metadata and a list of available endpoints |
| `POST` | `/analyze` | Main scan endpoint — accepts JSON or `multipart/form-data` file upload |
| `GET` | `/health` | Liveness check (`status`, `version`, `model`, `environment`, `timestamp`) |
| `GET` | `/patterns` | Returns all 22 regex pattern names with their risk level and category |
| `GET` | `/api/logs/history` | Last 100 buffered backend log events |
| `GET` | `/api/logs/stream` | Server-Sent Events stream of live backend log events |
| `GET` | `/docs` | Interactive Swagger UI |

### `POST /analyze`

```bash
curl -X POST https://secureai-backend-3yg7.onrender.com/analyze \
  -H 'Content-Type: application/json' \
  -d '{
    "input_type": "log",
    "content": "[ERROR] Database password=secret123 exposed\n[WARN] Login failed from 203.0.113.10",
    "options": {
      "mask": true,
      "block_high_risk": true,
      "log_analysis": true,
      "use_ai": true
    }
  }'
```

`input_type` must be one of `text | file | sql | chat | log`. Content is capped at **500,000 characters** per request (extra content is truncated, not rejected).

Response shape:

```json
{
  "summary": "Log input contains sensitive credentials",
  "content_type": "log",
  "total_lines_analyzed": 2,
  "findings": [
    {
      "type": "password",
      "risk": "critical",
      "category": "credential",
      "detection_method": "regex",
      "value": "password=[REDACTED]"
    }
  ],
  "risk_score": 4,
  "risk_level": "medium",
  "action": "masked",
  "insights": ["CRITICAL: Password exposed in plain text - change immediately and audit all access logs"],
  "detection_breakdown": { "regex": 1, "statistical": 0, "ml": 0, "ai": 0 },
  "truncated": false,
  "generated_at": "2026-08-31T12:00:00+00:00"
}
```

### Detection Patterns

The regex engine (`/patterns`) currently ships **22** named detectors:

`email` · `password` · `api_key` · `secret` · `hardcoded_secret` · `bearer_token` · `token` · `xss_attempt` · `path_traversal` · `privilege_escalation` · `phone` · `ssn` · `stack_trace` · `sql_injection` · `command_injection` · `ip_address` · `debug_mode` · `jwt_token` · `aws_key` · `credit_card` · `private_key_block` · `connection_string`

Plus statistical/log-specific detectors not tied to a fixed regex: `high_entropy_string`, `credential_density_anomaly`, `multi_pattern_line`, `failure_rate_spike`, `brute_force`, `malicious_ip` / `attacker_ip`.

---

## 🚀 Getting Started

### Prerequisites
- Python 3.11
- Node.js 18+
- Docker & Docker Compose (optional)

### 1. Clone

```bash
git clone https://github.com/Kondareddy1209/AI_Secure_Data_Intelligence_Platform.git
cd AI_Secure_Data_Intelligence_Platform
```

### 2. Backend

```bash
cd backend
cp .env.example .env
# Fill in ANTHROPIC_API_KEY and/or GEMINI_API_KEY (see Environment Variables below)
pip install -r requirements.txt
python -m uvicorn app.main:app --reload --port 8000
```

Backend runs at `http://localhost:8000` · Swagger UI at `http://localhost:8000/docs`.

### 3. Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend runs at `http://localhost:5173` and expects the backend at `VITE_API_URL` (defaults to `http://localhost:8000`).

### 4. Or, with Docker Compose

```bash
docker-compose up --build
```

- Backend → `http://localhost:8000`
- Frontend (built + served via Nginx) → `http://localhost:3000`

---

## 🔐 Environment Variables

| Variable | Used by | Default / Notes |
|---|---|---|
| `ANTHROPIC_API_KEY` | AI gateway (Claude fallback) | none — falls back to rule-based insights if unset |
| `GEMINI_API_KEY` | AI gateway (Gemini, default provider) | none — required for the primary AI path; not present in `.env.example` |
| `AI_PROVIDER` | AI gateway | `gemini` if unset |
| `CLAUDE_MODEL` | Settings only | `claude-sonnet-4-6` (analyze route hardcodes this model regardless) |
| `REQUIRE_API_BEARER_TOKEN` | `/analyze` auth | `false` — auth is **disabled by default** |
| `API_BEARER_TOKEN` | `/analyze` auth | only enforced when the flag above is `true` |
| `FRONTEND_URL` | CORS allowlist | appended to the built-in localhost origins |
| `ENVIRONMENT` | `/health` response | `development` |
| `APP_VERSION` | `/`, `/health` | `1.0.0` |
| `VITE_API_URL` | Frontend | `http://localhost:8000` |

---

## 🧪 Testing

```bash
cd backend
pytest tests/ -v
```

The suite currently covers **7 tests** across 4 files: `test_analyze.py`, `test_log_analyzer.py`, `test_regex_engine.py`, and `test_risk_engine.py`. There is no CI workflow configured in this repository yet — tests are run manually.

---

## 📚 Project Structure

```
AI_Secure_Data_Intelligence_Platform/
├── backend/
│   ├── app/
│   │   ├── main.py                  # FastAPI app entry, CORS, router wiring
│   │   ├── api/routes/
│   │   │   ├── analyze.py           # /analyze, /health, /patterns
│   │   │   └── logs.py              # /api/logs/history, /api/logs/stream (SSE)
│   │   ├── modules/
│   │   │   ├── detection/           # regex, statistical, ML, log analyzer
│   │   │   ├── ai/                  # Gemini + Claude gateways
│   │   │   ├── risk/                # risk scoring
│   │   │   └── policy/              # masking + block/allow decisions
│   │   ├── middleware/              # request logging middleware
│   │   └── utils/                   # structured logger, log buffer, masking helpers
│   ├── tests/                       # pytest suite
│   ├── requirements.txt
│   ├── render.yaml
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── App.tsx                  # main dashboard shell
│   │   ├── components/              # input panels, results panel, log viewer
│   │   ├── hooks/useAnalyze.ts
│   │   ├── services/api.ts          # fetch client + SSE subscriber
│   │   └── types/
│   ├── vercel.json
│   └── Dockerfile
├── docker-compose.yml
└── README.md
```

---

## 👤 What I Built

This is a full-stack, end-to-end project — not a template. It includes:

- A four-layer detection pipeline (regex → statistical → ML-style scoring → AI) designed to degrade gracefully when any single layer (especially the AI layer) is unavailable.
- A dual-provider AI gateway with automatic failover (Gemini → Claude → rule-based) and structured handling for timeouts, rate limits, auth errors, and exhausted API credits.
- A custom weighted risk engine and policy layer that turns raw findings into an `allowed / masked / blocked` decision.
- A real-time observability layer (SSE log streaming + in-memory ring buffer) built without a database or message broker.
- A React/TypeScript dashboard consuming all of the above, including a live log viewer and client-side JSON/CSV export.

*(Personalize this section with your specific role, e.g. "solo-built" vs. "led backend/detection pipeline" if this was a team project.)*

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Commit your changes
4. Open a Pull Request

---

## 📄 License

No license file is currently included in this repository. Add a `LICENSE` file to clarify usage terms if you intend this project to be reused by others.
