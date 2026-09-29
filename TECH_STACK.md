# KaryaSetu AI — Technology Stack Specification

> **SIH 26154 — Gen AI Platform for Automated Content Transformation**
> *Theme: Blockchain & CyberSecurity* | *Canonical Technology Stack Reference*

This document outlines the concrete, verified technology stack implemented in the KaryaSetu AI repository. Every component and library listed here corresponds directly to pinned dependencies and running code in the application layers.

---

## 1. Frontend

* **Application Framework:** Next.js 14 (App Router) + React 18
* **Programming Language:** TypeScript 5.7
* **Design & Styling:** Tailwind CSS 3.4 with custom design tokens, dark mode, and dynamic CSS animations
* **UI Components & Icons:** Radix UI primitives, Lucide React icons, Class Variance Authority (`cva`), `tailwind-merge`
* **State & Data Fetching:** Custom React hooks (`usePolling`), Server/Client Component boundary, SSE streaming handlers
* **Testing & Quality:** Jest 29, `@testing-library/react`, `@testing-library/jest-dom`, ESLint

---

## 2. Backend

* **API Framework:** FastAPI 0.115 (Asynchronous ASGI application)
* **Application Server:** Uvicorn 0.32 (with standard ASGI worker loop)
* **Programming Language:** Python 3.12
* **Data Validation & Settings:** Pydantic 2.10 and `pydantic-settings` 2.7
* **Structured Observability:** `structlog` 24.4 (JSON-formatted contextual logging)
* **Resilience & Retries:** `tenacity` 9.0 (exponential backoff and retry ceilings)
* **Testing Suite:** `pytest` 8.3, `pytest-asyncio`, `pytest-cov`, `httpx`

---

## 3. Artificial Intelligence & Orchestration

* **Orchestration Engine:** LangGraph 0.2 (`StateGraph` state machines) + `langchain-core` 0.3
* **LLM Provider Abstraction:** Provider-agnostic gateway interface (`LLMProviderInterface`) with dynamic fallback routing:
  * **Cloud Route:** Google Gemini API / OpenAI-compatible endpoint for Public/Internal policy tiers
  * **Private / Air-Gapped Route:** Local LLM adapter targeting on-premises endpoints (Ollama / vLLM hosting Gemma 3 12B) for Restricted/Confidential tiers
  * **Offline Deterministic Route:** `FakeLLMProvider` for isolated unit testing and CI test execution
* **RAG & Evidence Retrieval:** Dense semantic retrieval pipeline over dense vector embeddings, chunk-level citation anchoring, and entailment calculation
* **Structured Generation:** Pydantic output schemas with JSON mode enforcement across all transformation formats
* **Output-Specific Generators:** Modular generation pipeline for all seven governed deliverables

---

## 4. Data & Persistence

* **Relational Database:** PostgreSQL 16 (production) / SQLite (`aiosqlite`) for test runners
* **Vector Indexing:** `pgvector` 0.3 (`VECTOR(1536)` / `VECTOR(768)` HNSW index for sub-second semantic retrieval)
* **ORM & Migrations:** SQLAlchemy 2.0 (asyncio) + Alembic 1.14
* **Asynchronous Queue:** Redis 7 + Python-RQ 2.0 (multi-queue priority routing, job isolation, and lifecycle tracking)
* **Object Storage:** S3-compatible object storage (MinIO for on-premise/local dev, AWS S3 compatible)
* **Provenance Ledger:** Tamper-evident ledger table recording immutable event histories, input hashes, and output signatures

---

## 5. Security & Cyber-Governance

* **Authentication & Access Control:** OAuth2 Bearer tokens, JSON Web Tokens (JWT via `python-jose`), Argon2id password hashing
* **Policy Engine:** Declarative policy gate matching data classification (Public, Internal, Restricted, Confidential) to permissible processing pipelines
* **Malware & File Ingress Defense:** Magic-byte MIME verification, file size clamping, and ClamAV integration hooks
* **PII & Data Hygiene:** Regular expression and token-based PII identification, redaction, and sanitization before LLM ingestion
* **Prompt Injection Defense:** Strict delimiter encapsulation of untrusted user documents and system instruction fencing
* **Cryptographic Integrity:** SHA-256 content digests for all source chunks and deliverables
* **Digital Signatures:** Ed25519 asymmetric cryptographic signing for artifact non-repudiation and verification seals

---

## 6. Output & Artifact Generation

* **Presentation Engine:** `python-pptx` 1.0 (programmatic generation of slide decks from structured layouts)
* **Document Processing:** PyMuPDF (`fitz`) 1.25 (high-speed PDF parsing and rendering), `python-docx` 1.1 (Word processing)
* **Infographic Deliverable:** Structured semantic JSON blueprint paired with SVG / rendered PNG visualization
* **Video Package Deliverable:** Structured production package comprising scene-by-scene storyboard specification (PDF) and synchronized subtitle cues (SRT) — *strictly structured metadata, not MP4 video rendering*
* **Social & Advisory Payloads:** Platform-formatted markdown and clean text payloads (Summary, LinkedIn, Advisory, X)

---

## 7. Infrastructure & Deployment

* **Containerization:** Docker multi-stage builds (`python:3.12-slim`, `node:18-alpine`)
* **Service Orchestration:** Docker Compose (`docker-compose.yml`, `docker-compose.prod.yml`, `docker-compose.minio.yml`)
* **Reverse Proxy & Ingress:** Nginx reverse proxy managing SSL/TLS termination, rate limiting, and defensive security headers
* **Deployment Environments:** Self-hostable on bare-metal Linux servers, air-gapped secure enclaves, or containerized cloud VMs (AWS ECS, GCP Cloud Run, Azure Container Apps)