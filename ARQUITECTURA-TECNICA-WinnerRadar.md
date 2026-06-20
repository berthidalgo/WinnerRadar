# 📡 WinnerRadar — ARQUITECTURA TÉCNICA COMPLETA v2.0

**Documento complementario al MASTER-PLAN.md**  
**Fecha:** 20 jun 2026  
**Owner:** Staff Engineer 100x  
**Estado:** Fase 0 (blueprint técnico validado, listo para implementación)

---

## Índice

1. [Visión de Arquitectura](#1-visión-de-arquitectura)
2. [Capa 1: Frontend](#2-capa-1-frontend)
3. [Capa 2: Backend API](#3-capa-2-backend-api)
4. [Capa 3: IA / ML Engine](#4-capa-3-ia--ml-engine)
5. [Capa 4: Data & Storage](#5-capa-4-data--storage)
6. [Capa 5: Infraestructura & DevOps](#6-capa-5-infraestructura--devops)
7. [Flujo de Datos End-to-End](#7-flujo-de-datos-end-to-end)
8. [Schema de Base de Datos (DDL)](#8-schema-de-base-de-datos-ddl)
9. [API Endpoints (REST + WebSocket)](#9-api-endpoints-rest--websocket)
10. [Pipeline IA/ML Detallado](#10-pipeline-iaml-detallado)
11. [Decisiones Técnicas Archivadas](#11-decisiones-técnicas-archivadas)
12. [Matriz de Dependencias](#12-matriz-de-dependencias)

---

## 1. Visión de Arquitectura

WinnerRadar opera en **dos modos**:

| Modo | Fase | Infraestructura | Usuario |
|:-----|:-----|:----------------|:--------|
| **Modo Local** | F0-F3 | Python + CSV + SQLite + CLI Rich | CEO (único usuario) |
| **Modo SaaS** | F4 | FastAPI + Supabase + Vercel + Render | Múltiples usuarios (agencias, media buyers) |

**Principio rector:** El código de negocio (parser, filtros, scoring) es **100% portable** entre modos. Solo cambia la capa de presentación y persistencia.

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         USUARIO (CEO / Cliente)                        │
├─────────────────────────────────────────────────────────────────────────┤
│  CAPA 1: FRONTEND                                                      │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌────────────┐  │
│  │ Dashboard    │  │ Panel Admin  │  │ Mobile PWA   │  │ CLI Local  │  │
│  │ (Next.js 14) │  │ (shadcn/ui)  │  │ (Responsive) │  │ (Rich TUI) │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  └────────────┘  │
├─────────────────────────────────────────────────────────────────────────┤
│  CAPA 2: BACKEND API (FastAPI)                                         │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────────┐  │
│  │ Gateway  │ │ Auth     │ │ Jobs     │ │ WebSocket│ │ Health/Metrics│  │
│  │ REST     │ │ JWT/RBAC │ │ Celery   │ │ Real-time│ │ /health      │  │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘ └──────────────┘  │
├─────────────────────────────────────────────────────────────────────────┤
│  CAPA 3: IA / ML ENGINE (Cerebro)                                      │
│  ┌────────────┐ ┌────────────┐ ┌────────────┐ ┌──────────┐ ┌────────┐ │
│  │ NLP        │ │ LLM        │ │ Winner     │ │ Cluster  │ │ Embed  │ │
│  │ Pipeline   │ │ Gateway    │ │ Score      │ │ Analysis │ │ ding   │ │
│  │ (spaCy)    │ │ (Qoder/Gem)│ │ (XGBoost)  │ │ (K-Means)│ │ (BERT) │ │
│  └────────────┘ └────────────┘ └────────────┘ └──────────┘ └────────┘ │
├─────────────────────────────────────────────────────────────────────────┤
│  CAPA 4: DATA & STORAGE                                                │
│  ┌────────────┐ ┌────────────┐ ┌────────────┐ ┌──────────┐ ┌────────┐  │
│  │ Supabase   │ │ Storage    │ │ Cache      │ │ GSheets  │ │ Raw    │  │
│  │ PostgreSQL │ │ (S3 API)   │ │ (Redis)    │ │ (F0-F3)  │ │ TXT    │  │
│  └────────────┘ └────────────┘ └────────────┘ └──────────┘ └────────┘  │
├─────────────────────────────────────────────────────────────────────────┤
│  CAPA 5: INFRA & DEVOPS                                                │
│  ┌────────────┐ ┌────────────┐ ┌────────────┐ ┌─────────────────────┐  │
│  │ GitHub     │ │ Render     │ │ Vercel     │ │ UptimeRobot         │  │
│  │ (CI/CD)    │ │ (Backend)  │ │ (Frontend) │ │ (Monitoreo 24/7)    │  │
│  └────────────┘ └────────────┘ └────────────┘ └─────────────────────┘  │
├─────────────────────────────────────────────────────────────────────────┤
│  FUENTE EXTERNA: Meta Ads Library                                      │
│  ┌────────────────────┐  ┌────────────────────┐                         │
│  │ Manual TXT (F0-F3) │  │ Playwright (F4)    │                         │
│  │ Copy-Paste         │  │ Stealth + Proxies  │                         │
│  └────────────────────┘  └────────────────────┘                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Capa 1: Frontend

### 2.1 Stack Tecnológico

| Componente | Tecnología | Justificación |
|:-----------|:-----------|:--------------|
| Framework | **Next.js 14** (App Router) | SSR/SSG, Edge Runtime, API Routes integrados, SEO nativo |
| Lenguaje | TypeScript 5.3 | Tipado estricto, autocompletado, refactor seguro |
| Estilos | **Tailwind CSS** + **shadcn/ui** | Zero-CSS-in-JS, componentes accesibles, dark mode nativo |
| Estado Global | **Zustand** | Ligero, sin boilerplate, persistencia local opcional |
| Data Fetching | **TanStack Query** (React Query) | Caché inteligente, revalidación, loading states automáticos |
| Charts | **Recharts** + **Tremor** | Dashboards rápidos, responsive, temas consistentes |
| Formularios | **React Hook Form** + **Zod** | Validación declarativa, performance óptima |
| Auth | **Supabase Auth** | OAuth (Google, GitHub), Email/Password, JWT automático |
| Deploy | **Vercel** | Edge Network, deploy automático desde GitHub, preview por PR |

### 2.2 Estructura de Carpetas (Frontend)

```
frontend/
├── app/                          # Next.js 14 App Router
│   ├── (dashboard)/              # Grupo de rutas (layout compartido)
│   │   ├── layout.tsx            # Sidebar + Header + AuthGuard
│   │   ├── page.tsx              # Dashboard principal (Radar)
│   │   ├── radar/
│   │   │   ├── page.tsx          # Búsqueda por keyword
│   │   │   └── [keyword]/
│   │   │       └── page.tsx      # Resultados del radar
│   │   ├── ballenas/
│   │   │   └── page.tsx          # Top competidores filtrados
│   │   ├── infiltracion/
│   │   │   └── [fanpage]/
│   │   │       └── page.tsx      # Perfil completo de ballena
│   │   ├── reportes/
│   │   │   └── page.tsx          # Winner Score + Ranking
│   │   └── settings/
│   │       └── page.tsx          # Configuración usuario
│   ├── api/                      # API Routes (proxy a backend)
│   │   └── scan/
│   │       └── route.ts          # POST /api/scan → FastAPI
│   ├── login/
│   │   └── page.tsx              # Auth page (Supabase)
│   └── layout.tsx                # Root layout (providers)
├── components/
│   ├── ui/                       # shadcn/ui components
│   ├── charts/                   # Recharts wrappers
│   ├── tables/                   # TanStack Table wrappers
│   └── forms/                    # Formularios reutilizables
├── hooks/                        # Custom React hooks
│   ├── useAuth.ts
│   ├── useRadar.ts
│   ├── useBallenas.ts
│   └── useRealtime.ts            # Supabase Realtime
├── lib/
│   ├── supabase.ts               # Cliente Supabase
│   ├── api.ts                    # Cliente HTTP (axios/fetch)
│   └── utils.ts                  # Helpers
├── stores/                       # Zustand stores
│   ├── radarStore.ts
│   └── authStore.ts
├── types/                        # Interfaces TypeScript
│   └── index.ts
└── public/                       # Assets estáticos
```

### 2.3 Pantallas Principales (Wireframes Lógicos)

**Pantalla 1: Radar (Búsqueda)**
```
┌────────────────────────────────────────────────────────────┐
│  WinnerRadar 🎯                              [User] [⚙️]  │
├────────────────────────────────────────────────────────────┤
│                                                            │
│  [ 🔍 Ingresa keyword: _________________ ] [ ESCANEAR ]   │
│                                                            │
│  Keywords recientes: Moringa | Corrector Postura | Seguros │
│                                                            │
│  ┌────────────────────────────────────────────────────┐   │
│  │  Resultados para "Moringa"                          │   │
│  │  ┌────────┬─────────────┬──────────┬────────────┐ │   │
│  │  │ Fanpage│ Ads Activos │ Días Act │ Variantes  │ │   │
│  │  ├────────┼─────────────┼──────────┼────────────┤ │   │
│  │  │Natura..│    4,300    │   156    │     12     │ │   │
│  │  │HerbaLab│    1,200    │    89    │      5     │ │   │
│  │  └────────┴─────────────┴──────────┴────────────┘ │   │
│  └────────────────────────────────────────────────────┘   │
└────────────────────────────────────────────────────────────┘
```

**Pantalla 2: Ballenas (Filtrado)**
```
┌────────────────────────────────────────────────────────────┐
│  Filtros: [Días ≥ 7 ☑] [Variantes ≥ 2 ☑] [Formato ▼]     │
│                                                            │
│  🐋 TOP BALLENAS — Score Calculado                         │
│  ┌────────────────────────────────────────────────────┐   │
│  │ #1 NaturaVida    Score: 94.2  [INFILTRAR →]       │   │
│  │ #2 HerbaLab      Score: 87.5  [INFILTRAR →]       │   │
│  │ #3 VitaPlus     Score: 82.1  [INFILTRAR →]       │   │
│  └────────────────────────────────────────────────────┘   │
└────────────────────────────────────────────────────────────┘
```

**Pantalla 3: Infiltración (Perfil Competidor)**
```
┌────────────────────────────────────────────────────────────┐
│  NaturaVida — Catálogo Oculto                              │
│  ┌─────────────────┐  ┌────────────────────────────────┐  │
│  │  Productos        │  │  Embudos: 70% WhatsApp        │  │
│  │  • Moringa (FE)   │  │         20% Web               │  │
│  │  • Ashwagandha    │  │         10% Form              │  │
│  │  • Colágeno (BE)  │  │  Ofertas: 2x1 S/99, 50% OFF   │  │
│  └─────────────────┘  └────────────────────────────────┘  │
└────────────────────────────────────────────────────────────┘
```

**Pantalla 4: Reporte IA (Winner Score)**
```
┌────────────────────────────────────────────────────────────┐
│  🏆 Ranking de Copies Ganadores                           │
│  ┌────────────────────────────────────────────────────┐   │
│  │ #1 Score: 92/100  Hook: "Dile adiós a la fatiga..." │   │
│  │    Pain: Energía baja | Angle: Salud natural        │   │
│  │ #2 Score: 88/100  Hook: "La moringa que sí funciona"│   │
│  │    Pain: Estafas previas | Angle: Autoridad médica  │   │
│  └────────────────────────────────────────────────────┘   │
└────────────────────────────────────────────────────────────┘
```

### 2.4 CLI Local (F0-F3)

Para las fases iniciales donde no hay frontend cloud, usamos **Rich** para una TUI (Terminal User Interface) sofisticada:

```python
# scripts/cli.py
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress

console = Console()

def show_radar_results(df):
    table = Table(title="🎯 Resultados del Radar", show_header=True)
    table.add_column("Fanpage", style="cyan")
    table.add_column("Ads", justify="right", style="green")
    table.add_column("Días", justify="right", style="yellow")
    table.add_column("Score", justify="right", style="bold red")

    for _, row in df.iterrows():
        table.add_row(row['Fanpage_Name'], str(row['Total_Ads']), 
                      str(row['Days_Active']), f"{row['Ballena_Score']:.1f}")

    console.print(Panel(table, border_style="blue"))
```

---

## 3. Capa 2: Backend API

### 3.1 Stack Tecnológico

| Componente | Tecnología | Justificación |
|:-----------|:-----------|:--------------|
| Framework | **FastAPI** | Async nativo, OpenAPI/Swagger auto, Pydantic v2, performance |
| Server | **Uvicorn** (ASGI) + **Gunicorn** | Workers paralelos, hot reload dev, producción robusta |
| Validación | **Pydantic v2** | Modelos estrictos, serialización automática, docs auto |
| Auth | **Supabase Auth** | JWT validation, RBAC, middleware de protección |
| Jobs | **Celery** + **Redis** / **Supabase Queue** | Procesamiento async, retries, priorización |
| Cache | **Upstash Redis** (edge) / **SQLite** local | Cache distribuida (F4) o local (F0-F3) |
| ORM | **SQLAlchemy 2.0** + **Alembic** | Mapeo ORM, migraciones versionadas, async support |
| Testing | **pytest** + **httpx** | Tests unitarios + integración async |
| Deploy | **Render** (Web Service) / **Koyeb** | Free tier 24/7 (Koyeb), escalable (Render) |

### 3.2 Estructura de Carpetas (Backend)

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                   # Entry point FastAPI
│   ├── config.py                 # Settings (Pydantic-Settings)
│   ├── dependencies.py           # Inyección de dependencias
│   │
│   ├── api/                      # Routers REST
│   │   ├── __init__.py
│   │   ├── v1/
│   │   │   ├── __init__.py
│   │   │   ├── radar.py          # POST /api/v1/radar/scan
│   │   │   ├── ballenas.py       # GET /api/v1/ballenas/{keyword}
│   │   │   ├── infiltracion.py   # GET /api/v1/infiltracion/{fanpage}
│   │   │   ├── reportes.py       # GET /api/v1/reportes/{keyword}
│   │   │   ├── health.py         # GET /health
│   │   │   └── auth.py           # POST /auth/*
│   │   └── deps.py               # Dependencias comunes (DB, Auth)
│   │
│   ├── core/                     # Lógica de negocio
│   │   ├── __init__.py
│   │   ├── parser.py             # Parser Universal (F0 - CONGELADO)
│   │   ├── filtro_ballenas.py    # Filtro + Score Ballena
│   │   ├── infiltracion.py       # Mapeo catálogo oculto
│   │   ├── winner_score.py       # Cálculo Winner Score
│   │   └── scraper.py            # Playwright stealth (F4)
│   │
│   ├── services/                 # Servicios externos
│   │   ├── __init__.py
│   │   ├── supabase.py           # Cliente Supabase
│   │   ├── redis_cache.py        # Cliente Redis/Upstash
│   │   ├── llm_gateway.py        # Qoder CN / Gemini Flash
│   │   └── meta_scraper.py       # Playwright + Anti-ban
│   │
│   ├── models/                   # Pydantic + SQLAlchemy
│   │   ├── __init__.py
│   │   ├── schemas.py            # Pydantic (request/response)
│   │   ├── database.py           # SQLAlchemy models
│   │   └── enums.py              # Enums (Format, Funnel, Tone)
│   │
│   ├── workers/                  # Celery tasks (F4)
│   │   ├── __init__.py
│   │   ├── radar_tasks.py        # Task: scan_keyword
│   │   ├── ia_tasks.py           # Task: analyze_copies
│   │   └── heartbeat.py          # Task: emit_heartbeat
│   │
│   └── utils/
│       ├── __init__.py
│       ├── validators.py           # Validación de rangos, precios
│       ├── text_cleaning.py      # Limpieza de copy
│       └── logger.py             # Structured logging (JSON)
│
├── alembic/                      # Migraciones DB
├── tests/                        # Tests pytest
├── Dockerfile                    # Containerización (F4)
└── requirements.txt
```

### 3.3 Arquitectura de Servicios Internos

```
┌─────────────────────────────────────────────────────────────┐
│                      FastAPI Application                      │
├─────────────────────────────────────────────────────────────┤
│  Middleware Stack (orden de ejecución):                       │
│  1. CORS Middleware                                           │
│  2. TrustedHostMiddleware                                     │
│  3. JWT Auth Middleware (Supabase validation)                │
│  4. RateLimitMiddleware (Redis-backed, 100 req/min)          │
│  5. RequestLoggingMiddleware (structured JSON)               │
├─────────────────────────────────────────────────────────────┤
│  Routers:                                                    │
│  ├── /api/v1/auth     → Auth Service (login, refresh, logout)│
│  ├── /api/v1/radar    → Radar Service (scan, status)       │
│  ├── /api/v1/ballenas → Ballena Service (filter, rank)     │
│  ├── /api/v1/infiltrar → Infiltración Service (profile)    │
│  ├── /api/v1/reportes → Reporte Service (IA analysis)      │
│  ├── /api/v1/jobs     → Job Queue Service (Celery status)  │
│  └── /health          → Health Check (DB + Redis + Disk)   │
├─────────────────────────────────────────────────────────────┤
│  Services (Business Logic):                                │
│  ├── ParserService       → parser_meta_ads_universal.py    │
│  ├── BallenaService      → filtro_ballenas.py              │
│  ├── InfiltracionService → parser_infiltracion.py          │
│  ├── IAService           → ia_analisis_copies.py           │
│  ├── ScoreService        → winner_score.py                 │
│  └── ScraperService      → meta_scraper.py (F4)            │
├─────────────────────────────────────────────────────────────┤
│  External Clients:                                           │
│  ├── SupabaseClient    → PostgreSQL + Auth + Storage       │
│  ├── RedisClient       → Cache + Rate Limit + Pub/Sub      │
│  ├── LLMGateway        → Qoder CN / Gemini Flash           │
│  └── PlaywrightClient  → Meta Ads Stealth (F4)             │
└─────────────────────────────────────────────────────────────┘
```

---

## 4. Capa 3: IA / ML Engine

### 4.1 Stack Tecnológico

| Componente | Tecnología | Justificación |
|:-----------|:-----------|:--------------|
| NLP Local | **spaCy** (es_core_news_lg) | Tokenización, NER, POS tagging en español |
| NLP Cloud | **Transformers** (HuggingFace) | Modelos pre-entrenados para español |
| LLM Local | **Qoder CN 32B** (Alibaba Cloud) | Razonamiento complejo, generación código, $1/mes |
| LLM Cloud | **Gemini 2.5 Flash** | Fallback gratuito, 1M contexto, function calling |
| ML Clásico | **scikit-learn** + **XGBoost** | Winner Score predictivo, clustering, clasificación |
| Embeddings | **sentence-transformers** | Similaridad semántica entre copys |
| Vector DB | **Supabase pgvector** (F4) | Búsqueda por similitud de embeddings |
| Pipeline | **Celery** + **Redis** | Procesamiento async de batches de copys |

### 4.2 Arquitectura del Pipeline IA/ML

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         PIPELINE IA / ML ENGINE                         │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  FASE A: PREPROCESAMIENTO (NLP Local)                                   │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │ Input: Copy crudo (texto plano)                                  │   │
│  │  → spaCy: tokenización, lematización, stopwords removal          │   │
│  │  → Regex: extracción de precios (S/\d+), ofertas (% OFF), URLs   │   │
│  │  → Heurísticas: detección de emoji, mayúsculas, signos !!!!    │   │
│  │ Output: Copy limpio + metadatos estructurados                    │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                              ↓                                          │
│  FASE B: EXTRACCIÓN DE FEATURES (LLM Gateway)                          │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │ Input: Copy limpio + metadatos                                   │   │
│  │  → LLM Prompt estructurado (ver Sección 6 Prompt F3)            │   │
│  │  → Qoder CN: genera JSON con Hook, Pain, Objection, Angle, Tone│   │
│  │  → Fallback: Gemini Flash si Qoder no responde en < 30s          │   │
│  │ Output: Objeto JSON estructurado por copy                        │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                              ↓                                          │
│  FASE C: SCORING (ML Clásico + Heurísticas)                            │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │ Input: Features extraídas (Hook, Pain, Objection, Angle, CTA)    │   │
│  │  → F3 (Heurístico):                                              │   │
│  │      Winner_Score = Hook*0.30 + Pain*0.25 + Objection*0.20      │   │
│  │                     + Angle*0.15 + CTA*0.10                       │   │
│  │  → F4+ (Predictivo): XGBoost entrenado con datos históricos    │   │
│  │      Features: longitud copy, sentiment, keyword density, emoji %  │   │
│  │      Target: conversión estimada (proxy: días activo * variants) │   │
│  │ Output: Score 0-100 + confianza                                  │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                              ↓                                          │
│  FASE D: CLUSTERING Y EMBEDDINGS (Análisis de Patrones)                │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │ Input: Todos los copys de una keyword                            │   │
│  │  → Sentence-BERT: embeddings de cada copy                        │   │
│  │  → K-Means: agrupar copys por similitud semántica                │   │
│  │  → TF-IDF: palabras clave dominantes por cluster                 │   │
│  │ Output: Grupos de copys similares + palabras clave por grupo     │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                              ↓                                          │
│  FASE E: ENRIQUECIMIENTO (Cross-Analysis)                              │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │ Input: Resultados de todas las fases anteriores                  │   │
│  │  → Comparativa: copys ganadores vs perdedores por keyword       │   │
│  │  → Tendencias: ángulos de venta que dominan el nicho             │   │
│  │  → Oportunidades: gaps detectados (keywords no explotadas)      │   │
│  │ Output: Reporte ejecutivo JSON                                   │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### 4.3 Modelo de Datos para ML

```python
# models/ml_models.py
from pydantic import BaseModel, Field
from typing import Literal, Optional
from datetime import datetime

class CopyFeatures(BaseModel):
    """Features extraídas de un copy para ML"""
    ad_id: str
    copy_length: int = Field(..., ge=0, le=5000)
    word_count: int
    sentence_count: int
    avg_word_length: float
    emoji_count: int
    exclamation_count: int
    question_count: int
    uppercase_ratio: float = Field(..., ge=0, le=1)
    price_mentions: int
    urgency_words: int  # "ahora", "último", "corre", "hoy"
    social_proof_words: int  # "miles", "clientes", "testimonios"
    fear_words: int  # "pierde", "olvida", "sufrimiento"
    benefit_words: int  # "gratis", "gana", "mejora", "resultados"

class LLMOutput(BaseModel):
    """Output estructurado del LLM"""
    hook_principal: str = Field(..., max_length=200)
    pain_point: str = Field(..., max_length=200)
    objection_killed: str = Field(..., max_length=200)
    sales_angle: Literal["salud", "estética", "ahorro", "urgencia", 
                          "autoridad", "estatus", "miedo", "comodidad"]
    tone: Literal["agresivo", "educativo", "empático", "científico", 
                  "humorístico", "inspiracional"]
    target_audience: str
    cta_type: Literal["comprar", "agendar", "descargar", "contactar", "registrarse"]

class WinnerScoreInput(BaseModel):
    """Input para el modelo de scoring"""
    features: CopyFeatures
    llm_output: LLMOutput
    days_active: int
    creative_variants: int
    impressions_level: Literal["Bajo", "Normal", "Alto"]

class WinnerScoreOutput(BaseModel):
    """Output del scoring"""
    winner_score: float = Field(..., ge=0, le=100)
    confidence: float = Field(..., ge=0, le=1)
    hook_score: float = Field(..., ge=0, le=100)
    pain_score: float = Field(..., ge=0, le=100)
    objection_score: float = Field(..., ge=0, le=100)
    angle_score: float = Field(..., ge=0, le=100)
    cta_score: float = Field(..., ge=0, le=100)
    cluster_id: Optional[int] = None
    similar_copies: list[str] = []
```

### 4.4 Prompt Engineering (F3)

El prompt para el LLM está versionado en `prompts/prompt_f3_analisis.txt` y se inyecta dinámicamente:

```python
# services/llm_gateway.py
class LLMGateway:
    def __init__(self):
        self.primary = QoderClient(api_key=settings.QODER_API_KEY)
        self.fallback = GeminiClient(api_key=settings.GEMINI_API_KEY)
        self.prompt_template = self._load_prompt("prompts/prompt_f3_analisis.txt")

    async def analyze_copy(self, copy_text: str) -> LLMOutput:
        prompt = self.prompt_template.format(copy=copy_text)

        try:
            # Primary: Qoder CN (timeout 30s)
            response = await self.primary.generate(
                prompt=prompt,
                max_tokens=800,
                temperature=0.3,  # Baja para consistencia
                timeout=30
            )
            return self._parse_json(response)

        except (TimeoutError, JSONDecodeError):
            # Fallback: Gemini Flash
            logger.warning("Qoder timeout, fallback a Gemini")
            response = await self.fallback.generate(
                prompt=prompt,
                max_tokens=800,
                temperature=0.3
            )
            return self._parse_json(response)
```

---

## 5. Capa 4: Data & Storage

### 5.1 Stack Tecnológico

| Componente | Tecnología | Fase | Justificación |
|:-----------|:-----------|:-----|:--------------|
| Base de Datos | **Supabase PostgreSQL** | F4 | PostgreSQL managed, RLS, realtime, backups auto |
| ORM | **SQLAlchemy 2.0** + **Alembic** | F0-F4 | Mapeo ORM, migraciones versionadas, async support |
| Cache | **Upstash Redis** | F4 | Edge cache, rate limiting, pub/sub, serverless |
| Cache Local | **SQLite** | F0-F3 | Zero-config, file-based, suficiente para datasets pequeños |
| Storage | **Supabase Storage** (S3 API) | F4 | Archivos RAW, reportes PDF, imágenes de ads |
| Storage Local | **CSV + TXT** | F0-F3 | Legible por humanos, portable, Git-friendly |
| Sheets | **Google Sheets API** | F0-F3 | DB legible para CEO, sin SQL, edición colaborativa |
| Vector DB | **pgvector** (Supabase) | F4 | Búsqueda por similitud de embeddings |

### 5.2 Schema de Base de Datos (PostgreSQL)

```sql
-- ============================================================
-- WINNERRADAR DATABASE SCHEMA v2.0
-- PostgreSQL + Supabase (RLS enabled)
-- ============================================================

-- Extensión para búsqueda vectorial (F4)
CREATE EXTENSION IF NOT EXISTS vector;

-- Enum types
CREATE TYPE ad_format AS ENUM ('Video', 'Imagen', 'Carrusel', 'Otro');
CREATE TYPE impressions_level AS ENUM ('Bajo', 'Normal', 'Alto');
CREATE TYPE funnel_type AS ENUM ('WhatsApp', 'Web', 'Landing', 'Formulario', 'DM', 'Otro');
CREATE TYPE sales_angle AS ENUM ('salud', 'estética', 'ahorro', 'urgencia', 'autoridad', 'estatus', 'miedo', 'comodidad');
CREATE TYPE tone_type AS ENUM ('agresivo', 'educativo', 'empático', 'científico', 'humorístico', 'inspiracional');
CREATE TYPE cta_type AS ENUM ('comprar', 'agendar', 'descargar', 'contactar', 'registrarse');
CREATE TYPE job_status AS ENUM ('pending', 'processing', 'completed', 'failed', 'cancelled');

-- ============================================================
-- TABLA 1: keyword_radar_results (Movimiento 1 - Radar)
-- ============================================================
CREATE TABLE keyword_radar_results (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now(),

    keyword_buscada TEXT NOT NULL,
    fanpage_name TEXT NOT NULL,
    fanpage_id TEXT,
    total_ads_active INTEGER DEFAULT 0,
    ad_id_representativo TEXT,
    start_date DATE,
    days_active INTEGER DEFAULT 0,
    creative_variants INTEGER DEFAULT 1,
    impressions_level impressions_level DEFAULT 'Normal',
    format ad_format DEFAULT 'Otro',
    duration TEXT,

    funnel_type funnel_type DEFAULT 'Otro',
    offer_extracted TEXT,
    copy_full TEXT,

    user_id UUID REFERENCES auth.users(id),
    batch_id TEXT,

    CONSTRAINT positive_days CHECK (days_active >= 0),
    CONSTRAINT positive_ads CHECK (total_ads_active >= 0)
);

CREATE INDEX idx_keyword ON keyword_radar_results(keyword_buscada);
CREATE INDEX idx_fanpage ON keyword_radar_results(fanpage_name);
CREATE INDEX idx_days_active ON keyword_radar_results(days_active);
CREATE INDEX idx_batch ON keyword_radar_results(batch_id);

-- ============================================================
-- TABLA 2: ad_creative_analysis (Movimiento 2 + IA - F3)
-- ============================================================
CREATE TABLE ad_creative_analysis (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    created_at TIMESTAMPTZ DEFAULT now(),

    radar_id UUID REFERENCES keyword_radar_results(id) ON DELETE CASCADE,
    ad_id TEXT NOT NULL,

    copy_full TEXT,
    copy_cleaned TEXT,

    hook_extracted TEXT,
    hook_score DECIMAL(5,2),
    pain_point TEXT,
    pain_score DECIMAL(5,2),
    objection_killed TEXT,
    objection_score DECIMAL(5,2),
    sales_angle sales_angle,
    angle_score DECIMAL(5,2),
    tone tone_type,
    target_audience TEXT,

    offer_extracted TEXT,
    funnel_type funnel_type,
    cta_type cta_type,
    cta_score DECIMAL(5,2),

    winner_score DECIMAL(5,2) CHECK (winner_score >= 0 AND winner_score <= 100),
    confidence DECIMAL(3,2) CHECK (confidence >= 0 AND confidence <= 1),

    cluster_id INTEGER,
    embedding VECTOR(384),
    similar_copies UUID[],

    llm_model_used TEXT DEFAULT 'qoder-cn-32b',
    processing_time_ms INTEGER,

    CONSTRAINT valid_scores CHECK (
        hook_score IS NULL OR (hook_score >= 0 AND hook_score <= 100)
    )
);

CREATE INDEX idx_radar_id ON ad_creative_analysis(radar_id);
CREATE INDEX idx_winner_score ON ad_creative_analysis(winner_score DESC);
CREATE INDEX idx_cluster ON ad_creative_analysis(cluster_id);

-- ============================================================
-- TABLA 3: ballena_rankings (Resultado del Filtro F1)
-- ============================================================
CREATE TABLE ballena_rankings (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    created_at TIMESTAMPTZ DEFAULT now(),

    keyword_buscada TEXT NOT NULL,
    fanpage_name TEXT NOT NULL,
    fanpage_id TEXT,

    total_ads INTEGER DEFAULT 0,
    avg_days_active DECIMAL(6,1),
    max_creative_variants INTEGER DEFAULT 0,
    ballena_score DECIMAL(6,2),
    ranking_position INTEGER,

    selected_for_infiltration BOOLEAN DEFAULT FALSE,
    infiltration_notes TEXT,

    batch_id TEXT,
    user_id UUID REFERENCES auth.users(id)
);

CREATE INDEX idx_ballena_keyword ON ballena_rankings(keyword_buscada);
CREATE INDEX idx_ballena_score ON ballena_rankings(ballena_score DESC);

-- ============================================================
-- TABLA 4: infiltracion_reports (Movimiento 2 - F2)
-- ============================================================
CREATE TABLE infiltracion_reports (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    created_at TIMESTAMPTZ DEFAULT now(),

    fanpage_name TEXT NOT NULL,
    fanpage_id TEXT,

    products_detected TEXT[],
    frontend_products TEXT[],
    backend_products TEXT[],

    funnel_whatsapp_pct DECIMAL(5,2),
    funnel_web_pct DECIMAL(5,2),
    funnel_landing_pct DECIMAL(5,2),
    funnel_form_pct DECIMAL(5,2),

    price_ranges JSONB,
    offer_patterns TEXT[],

    dominant_angles sales_angle[],
    frequent_ctas TEXT[],

    active_ads_count INTEGER,
    inactive_ads_count INTEGER,
    activity_ratio DECIMAL(5,2),

    user_id UUID REFERENCES auth.users(id)
);

-- ============================================================
-- TABLA 5: jobs (Cola de Trabajo - F4)
-- ============================================================
CREATE TABLE jobs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now(),

    job_type TEXT NOT NULL,
    status job_status DEFAULT 'pending',

    payload JSONB NOT NULL,

    result JSONB,
    error_message TEXT,

    started_at TIMESTAMPTZ,
    completed_at TIMESTAMPTZ,
    processing_time_ms INTEGER,

    retry_count INTEGER DEFAULT 0,
    max_retries INTEGER DEFAULT 3,

    user_id UUID REFERENCES auth.users(id)
);

CREATE INDEX idx_jobs_status ON jobs(status);
CREATE INDEX idx_jobs_user ON jobs(user_id);
CREATE INDEX idx_jobs_type ON jobs(job_type);

-- ============================================================
-- TABLA 6: heartbeats (Monitoreo - Principio 9)
-- ============================================================
CREATE TABLE heartbeats (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    ts TIMESTAMPTZ DEFAULT now(),
    service_name TEXT NOT NULL,
    status TEXT,
    metadata JSONB,

    CONSTRAINT recent_heartbeat CHECK (ts > now() - interval '1 hour')
);

CREATE INDEX idx_heartbeat_service ON heartbeats(service_name, ts DESC);

-- ============================================================
-- TABLA 7: evals_parametros (Sección 9 - Datos de Negocio)
-- ============================================================
CREATE TABLE evals_parametros (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    created_at TIMESTAMPTZ DEFAULT now(),
    user_id UUID REFERENCES auth.users(id),

    q1_volumen_extraccion INTEGER,
    q2_umbral_dias INTEGER,
    q3_umbral_variantes INTEGER,
    q4_keywords TEXT[],
    q5_criterio_winner TEXT,

    parametros_calibrados JSONB
);

-- ============================================================
-- ROW LEVEL SECURITY (RLS) - Supabase
-- ============================================================
ALTER TABLE keyword_radar_results ENABLE ROW LEVEL SECURITY;
ALTER TABLE ad_creative_analysis ENABLE ROW LEVEL SECURITY;
ALTER TABLE ballena_rankings ENABLE ROW LEVEL SECURITY;
ALTER TABLE infiltracion_reports ENABLE ROW LEVEL SECURITY;
ALTER TABLE jobs ENABLE ROW LEVEL SECURITY;
ALTER TABLE evals_parametros ENABLE ROW LEVEL SECURITY;

CREATE POLICY "isolation_user_radar" ON keyword_radar_results
    FOR ALL USING (auth.uid() = user_id);

CREATE POLICY "isolation_user_analysis" ON ad_creative_analysis
    FOR ALL USING (auth.uid() IN (
        SELECT user_id FROM keyword_radar_results WHERE id = radar_id
    ));

CREATE POLICY "isolation_user_ballenas" ON ballena_rankings
    FOR ALL USING (auth.uid() = user_id);

CREATE POLICY "isolation_user_infiltracion" ON infiltracion_reports
    FOR ALL USING (auth.uid() = user_id);

CREATE POLICY "isolation_user_jobs" ON jobs
    FOR ALL USING (auth.uid() = user_id);

CREATE POLICY "isolation_user_evals" ON evals_parametros
    FOR ALL USING (auth.uid() = user_id);
```

### 5.3 Diagrama Entidad-Relación

```
┌─────────────────────────────┐         ┌─────────────────────────────┐
│  keyword_radar_results      │         │  ad_creative_analysis       │
├─────────────────────────────┤         ├─────────────────────────────┤
│  PK: id (UUID)              │◄───────│  PK: id (UUID)              │
│  keyword_buscada            │   1:N   │  FK: radar_id → radar.id    │
│  fanpage_name               │         │  ad_id                      │
│  fanpage_id                 │         │  copy_full                  │
│  total_ads_active           │         │  hook_extracted             │
│  days_active                │         │  pain_point                 │
│  creative_variants          │         │  winner_score               │
│  impressions_level          │         │  embedding (vector)         │
│  copy_full                  │         │  cluster_id                 │
│  user_id (FK auth.users)    │         │  user_id (FK auth.users)    │
└─────────────────────────────┘         └─────────────────────────────┘
           │                                        │
           │ 1:N                                    │ 1:N
           ▼                                        ▼
┌─────────────────────────────┐         ┌─────────────────────────────┐
│  ballena_rankings           │         │  infiltracion_reports       │
├─────────────────────────────┤         ├─────────────────────────────┤
│  PK: id (UUID)              │         │  PK: id (UUID)              │
│  FK: keyword_buscada        │         │  fanpage_name               │
│  fanpage_name               │         │  products_detected[]        │
│  ballena_score              │         │  funnel_whatsapp_pct        │
│  ranking_position           │         │  price_ranges (JSONB)       │
│  selected_for_infiltration  │         │  dominant_angles[]          │
│  user_id (FK auth.users)    │         │  user_id (FK auth.users)    │
└─────────────────────────────┘         └─────────────────────────────┘
           │
           │ N:1
           ▼
┌─────────────────────────────┐
│  jobs                       │
├─────────────────────────────┤
│  PK: id (UUID)              │
│  job_type                   │
│  status                     │
│  payload (JSONB)            │
│  result (JSONB)             │
│  retry_count                │
│  user_id (FK auth.users)    │
└─────────────────────────────┘
```

---

## 6. Capa 5: Infraestructura & DevOps

### 6.1 Stack Tecnológico

| Componente | Tecnología | Propósito |
|:-----------|:-----------|:----------|
| Source Control | **GitHub** | Repo, branches, PRs, code review |
| CI/CD | **GitHub Actions** | Test + Lint + Deploy automático |
| Backend | **Render** (Web Service) | FastAPI 24/7, auto-deploy desde GitHub |
| Worker | **Render** (Background Worker) | Celery workers para jobs async |
| Frontend | **Vercel** | Next.js edge, preview deployments |
| Database | **Supabase** | PostgreSQL managed, auth, storage, realtime |
| Cache | **Upstash Redis** | Edge cache, rate limit, pub/sub |
| Monitoreo | **UptimeRobot** | Ping /health cada 5 min, alerta email/SMS |
| Alertas | **Evolution API** (WhatsApp) | Alertas críticas al CEO |
| Notificaciones | **ntfy** | Push notifications internas |

### 6.2 Pipeline CI/CD (GitHub Actions)

```yaml
# .github/workflows/deploy.yml
name: WinnerRadar CI/CD

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_PASSWORD: postgres
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
    steps:
      - uses: actions/checkout@v4

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          pip install -r backend/requirements.txt
          pip install pytest pytest-asyncio

      - name: Run tests
        run: pytest tests/ -v --cov=app --cov-report=xml
        env:
          DATABASE_URL: postgresql://postgres:postgres@localhost:5432/test

      - name: Lint
        run: |
          pip install ruff
          ruff check .
          ruff format --check .

  deploy-backend:
    needs: test
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Deploy to Render
        run: |
          curl -X POST ${{ secrets.RENDER_DEPLOY_HOOK }}

  deploy-frontend:
    needs: test
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Deploy to Vercel
        uses: vercel/action-deploy@v1
        with:
          vercel-token: ${{ secrets.VERCEL_TOKEN }}
          vercel-org-id: ${{ secrets.VERCEL_ORG_ID }}
          vercel-project-id: ${{ secrets.VERCEL_PROJECT_ID }}
```

### 6.3 Docker (F4)

```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Playwright dependencies (for F4 scraping)
RUN apt-get update && apt-get install -y \
    libglib2.0-0 libnss3 libnspr4 libatk1.0-0 \
    libatk-bridge2.0-0 libcups2 libdrm2 libdbus-1-3 \
    libxkbcommon0 libxcomposite1 libxdamage1 libxfixes3 \
    libxrandr2 libgbm1 libpango-1.0-0 libcairo2 libasound2 \
    && rm -rf /var/lib/apt/lists/*

RUN playwright install chromium

# App
COPY app/ ./app/

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

EXPOSE 8000

CMD ["gunicorn", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "app.main:app", "--bind", "0.0.0.0:8000"]
```

### 6.4 Monitoreo y Alertas

```python
# app/api/v1/health.py
from fastapi import APIRouter, Depends
from sqlalchemy import text
from app.dependencies import get_db, get_redis
import psutil

router = APIRouter()

@router.get("/health")
async def health_check(db=Depends(get_db), redis=Depends(get_redis)):
    checks = {
        "database": False,
        "redis": False,
        "disk": False,
        "status": "down"
    }

    try:
        await db.execute(text("SELECT 1"))
        checks["database"] = True
    except Exception as e:
        logger.error(f"DB health check failed: {e}")

    try:
        await redis.ping()
        checks["redis"] = True
    except Exception as e:
        logger.error(f"Redis health check failed: {e}")

    disk = psutil.disk_usage('/')
    checks["disk"] = disk.percent < 90
    checks["disk_free_gb"] = disk.free / (1024**3)

    if all([checks["database"], checks["redis"], checks["disk"]]):
        checks["status"] = "healthy"
    elif checks["database"] and checks["redis"]:
        checks["status"] = "degraded"

    return checks
```

---

## 7. Flujo de Datos End-to-End

### 7.1 Flujo F0-F3 (Local/Manual)

```
CEO abre Meta Ads Library
        │
        ▼
[1] Copia TXT manual → data/meta_ads_raw/{keyword}_raw.txt
        │
        ▼
[2] Ejecuta: python scripts/parsers/parser_meta_ads_universal.py
        │
        ├── Lee TXT crudo
        ├── Regex divide bloques por "Identificador de la biblioteca:"
        ├── Extrae: Fanpage, Ad_ID, Fecha, Variantes, Copy, etc.
        └── Guarda: output/radar/bd_meta_ads_{keyword}.csv
        │
        ▼
[3] Ejecuta: python scripts/analysis/filtro_ballenas.py
        │
        ├── Lee CSV del radar
        ├── Filtra: Days_Active >= 7 AND Creative_Variants >= 2
        ├── Agrupa por Fanpage, calcula Ballena_Score
        └── Guarda: output/infiltracion/ballenas_{keyword}.csv
        │
        ▼
[4] CEO selecciona Top 3-5 ballenas
        │
        ▼
[5] CEO copia TXTs completos de perfiles → data/infiltracion/{fanpage}_completo.txt
        │
        ▼
[6] Ejecuta: python scripts/parsers/parser_infiltracion.py
        │
        ├── Lee TXT completo del fanpage
        ├── Extrae: productos, embudos, precios, ángulos, CTAs
        └── Guarda: output/infiltracion/reporte_{fanpage}.csv
        │
        ▼
[7] Ejecuta: python scripts/analysis/ia_analisis_copies.py
        │
        ├── Lee copys del CSV del radar
        ├── Llama a LLM (Qoder CN / Gemini) por cada copy
        ├── Extrae: Hook, Pain, Objection, Angle, Tone, CTA
        └── Guarda: output/reportes_ia/analisis_copies_{keyword}.json
        │
        ▼
[8] Ejecuta: python scripts/analysis/winner_score.py
        │
        ├── Lee análisis IA
        ├── Aplica fórmula ponderada (F3) o modelo XGBoost (F4)
        ├── Genera ranking descendente
        └── Guarda: output/reportes_ia/ranking_ganadores.csv
        │
        ▼
[9] CEO arma campaña con ángulos validados 🎯
```

### 7.2 Flujo F4 (Cloud/Automatizado)

```
Usuario ingresa keyword en Dashboard Vercel
        │
        ▼
POST /api/v1/radar/scan → FastAPI (Render)
        │
        ├── Valida keyword (no vacío, no baneada)
        ├── Crea job en tabla `jobs` (status: pending)
        └── Retorna job_id al frontend
        │
        ▼
Celery Worker (Render Background) detecta job
        │
        ├── Actualiza job → status: processing
        ├── Playwright Stealth → Meta Ads Library
        │   ├── Proxy rotativo
        │   ├── Exponential backoff + jitter
        │   └── Extrae ads (simula comportamiento humano)
        ├── Parser Universal (congelado desde F0)
        │   └── Convierte HTML/TXT → estructura CSV
        ├── Guarda en Supabase PostgreSQL
        └── Actualiza job → status: completed
        │
        ▼
Frontend recibe WebSocket: "Scan completado"
        │
        ▼
Usuario presiona "Analizar con IA"
        │
        ▼
POST /api/v1/reportes/analyze → FastAPI
        │
        ├── Lee copys de Supabase
        ├── Encola N tareas Celery (1 por copy)
        ├── LLM Gateway procesa cada copy async
        │   ├── Qoder CN (primary)
        │   └── Gemini Flash (fallback)
        ├── Winner Score calculado
        ├── Embeddings generados (Sentence-BERT)
        ├── Clustering K-Means aplicado
        └── Resultados guardados en Supabase
        │
        ▼
Frontend muestra: Ranking + Insights + Clusters 🏆
        │
        ▼
Heartbeat cada 5 min → tabla `heartbeats`
UptimeRobot monitorea /health
Si falla > 10 min → Alerta WhatsApp (Evolution API) 🚨
```

---

## 8. Schema de Base de Datos (DDL)

*(Ver Sección 5.2 para el DDL completo de PostgreSQL)*

### 8.1 Migraciones (Alembic)

```python
# alembic/versions/001_initial_schema.py
"""Initial schema for WinnerRadar v2.0"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = '001'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    ad_format = postgresql.ENUM('Video', 'Imagen', 'Carrusel', 'Otro', name='ad_format')
    ad_format.create(op.get_bind())

    op.create_table(
        'keyword_radar_results',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.func.now()),
        sa.Column('keyword_buscada', sa.Text(), nullable=False),
        sa.Column('fanpage_name', sa.Text(), nullable=False),
        sa.Column('total_ads_active', sa.Integer(), default=0),
        sa.Column('days_active', sa.Integer(), default=0),
        sa.Column('creative_variants', sa.Integer(), default=1),
        sa.Column('format', ad_format, default='Otro'),
        sa.Column('copy_full', sa.Text()),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('auth.users.id'))
    )

    op.create_index('idx_keyword', 'keyword_radar_results', ['keyword_buscada'])
    op.create_index('idx_fanpage', 'keyword_radar_results', ['fanpage_name'])

    op.execute('ALTER TABLE keyword_radar_results ENABLE ROW LEVEL SECURITY')
    op.execute("""
        CREATE POLICY "isolation_user" ON keyword_radar_results
        FOR ALL USING (auth.uid() = user_id)
    """)

def downgrade():
    op.drop_table('keyword_radar_results')
    ad_format = postgresql.ENUM('Video', 'Imagen', 'Carrusel', 'Otro', name='ad_format')
    ad_format.drop(op.get_bind())
```

---

## 9. API Endpoints (REST + WebSocket)

### 9.1 REST API Specification (OpenAPI 3.0)

```yaml
openapi: 3.0.0
info:
  title: WinnerRadar API
  version: 2.0.0
  description: Motor Horizontal de Inteligencia Comercial

servers:
  - url: https://api.winnerradar.io/api/v1
    description: Production
  - url: http://localhost:8000/api/v1
    description: Local Development

paths:
  /health:
    get:
      summary: Health check completo
      tags: [Monitoreo]
      responses:
        200:
          description: Estado del sistema
          content:
            application/json:
              schema:
                type: object
                properties:
                  status: { type: string, enum: [healthy, degraded, down] }
                  database: { type: boolean }
                  redis: { type: boolean }
                  disk_free_gb: { type: number }

  /auth/login:
    post:
      summary: Login con Supabase Auth
      tags: [Autenticación]
      requestBody:
        content:
          application/json:
            schema:
              type: object
              properties:
                email: { type: string, format: email }
                password: { type: string, minLength: 8 }
      responses:
        200:
          description: JWT token + refresh token
          content:
            application/json:
              schema:
                type: object
                properties:
                  access_token: { type: string }
                  refresh_token: { type: string }
                  expires_in: { type: integer }

  /radar/scan:
    post:
      summary: Iniciar scan de keyword
      tags: [Radar]
      security: [BearerAuth: []]
      requestBody:
        content:
          application/json:
            schema:
              type: object
              properties:
                keyword: { type: string, minLength: 2, maxLength: 100 }
                industry_hint: { type: string, enum: [producto, servicio, tendencia, real_estate] }
                max_results: { type: integer, default: 100, maximum: 500 }
      responses:
        202:
          description: Scan encolado
          content:
            application/json:
              schema:
                type: object
                properties:
                  job_id: { type: string, format: uuid }
                  status: { type: string, enum: [pending, processing] }
                  estimated_seconds: { type: integer }

  /radar/results/{keyword}:
    get:
      summary: Obtener resultados del radar
      tags: [Radar]
      security: [BearerAuth: []]
      parameters:
        - name: keyword
          in: path
          required: true
          schema: { type: string }
        - name: limit
          in: query
          schema: { type: integer, default: 50 }
        - name: offset
          in: query
          schema: { type: integer, default: 0 }
      responses:
        200:
          description: Lista de anuncios detectados
          content:
            application/json:
              schema:
                type: object
                properties:
                  total: { type: integer }
                  results:
                    type: array
                    items:
                      $ref: '#/components/schemas/RadarResult'

  /ballenas/{keyword}:
    get:
      summary: Obtener ballenas filtradas por keyword
      tags: [Ballenas]
      security: [BearerAuth: []]
      parameters:
        - name: keyword
          in: path
          required: true
          schema: { type: string }
        - name: min_days
          in: query
          schema: { type: integer, default: 7 }
        - name: min_variants
          in: query
          schema: { type: integer, default: 2 }
      responses:
        200:
          description: Top ballenas con score
          content:
            application/json:
              schema:
                type: object
                properties:
                  keyword: { type: string }
                  total_ballenas: { type: integer }
                  ballenas:
                    type: array
                    items:
                      $ref: '#/components/schemas/Ballena'

  /infiltracion/{fanpage}:
    get:
      summary: Mapear catálogo oculto de un competidor
      tags: [Infiltración]
      security: [BearerAuth: []]
      parameters:
        - name: fanpage
          in: path
          required: true
          schema: { type: string }
      responses:
        200:
          description: Reporte completo de infiltración
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/InfiltracionReport'

  /reportes/analyze:
    post:
      summary: Analizar copys con IA y generar Winner Score
      tags: [Reportes IA]
      security: [BearerAuth: []]
      requestBody:
        content:
          application/json:
            schema:
              type: object
              properties:
                keyword: { type: string }
                use_cache: { type: boolean, default: true }
      responses:
        202:
          description: Análisis encolado
          content:
            application/json:
              schema:
                type: object
                properties:
                  job_id: { type: string, format: uuid }
                  status: { type: string }

  /reportes/ranking/{keyword}:
    get:
      summary: Obtener ranking de copys ganadores
      tags: [Reportes IA]
      security: [BearerAuth: []]
      parameters:
        - name: keyword
          in: path
          required: true
          schema: { type: string }
        - name: top_n
          in: query
          schema: { type: integer, default: 10 }
      responses:
        200:
          description: Ranking ordenado por Winner Score
          content:
            application/json:
              schema:
                type: object
                properties:
                  keyword: { type: string }
                  ranking:
                    type: array
                    items:
                      $ref: '#/components/schemas/WinnerScoreResult'

  /jobs/{job_id}:
    get:
      summary: Consultar estado de un job
      tags: [Jobs]
      security: [BearerAuth: []]
      parameters:
        - name: job_id
          in: path
          required: true
          schema: { type: string, format: uuid }
      responses:
        200:
          description: Estado del job
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Job'

components:
  securitySchemes:
    BearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT

  schemas:
    RadarResult:
      type: object
      properties:
        id: { type: string, format: uuid }
        fanpage_name: { type: string }
        total_ads_active: { type: integer }
        days_active: { type: integer }
        creative_variants: { type: integer }
        impressions_level: { type: string, enum: [Bajo, Normal, Alto] }
        format: { type: string, enum: [Video, Imagen, Carrusel, Otro] }
        copy_full: { type: string }

    Ballena:
      type: object
      properties:
        fanpage_name: { type: string }
        total_ads: { type: integer }
        avg_days_active: { type: number }
        max_creative_variants: { type: integer }
        ballena_score: { type: number }
        ranking_position: { type: integer }

    InfiltracionReport:
      type: object
      properties:
        fanpage_name: { type: string }
        products_detected: { type: array, items: { type: string } }
        funnel_whatsapp_pct: { type: number }
        funnel_web_pct: { type: number }
        price_ranges: { type: object }
        dominant_angles: { type: array, items: { type: string } }

    WinnerScoreResult:
      type: object
      properties:
        ad_id: { type: string }
        fanpage_name: { type: string }
        winner_score: { type: number, minimum: 0, maximum: 100 }
        hook: { type: string }
        pain_point: { type: string }
        sales_angle: { type: string }
        tone: { type: string }

    Job:
      type: object
      properties:
        id: { type: string, format: uuid }
        job_type: { type: string }
        status: { type: string, enum: [pending, processing, completed, failed, cancelled] }
        payload: { type: object }
        result: { type: object }
        created_at: { type: string, format: date-time }
        completed_at: { type: string, format: date-time }
```

### 9.2 WebSocket Events (Real-time)

```javascript
// Frontend: conexión WebSocket para updates en tiempo real
const ws = new WebSocket('wss://api.winnerradar.io/ws/jobs');

ws.onopen = () => {
  ws.send(JSON.stringify({
    type: 'subscribe',
    job_id: 'uuid-del-job'
  }));
};

ws.onmessage = (event) => {
  const msg = JSON.parse(event.data);

  switch(msg.type) {
    case 'job.progress':
      updateProgressBar(msg.progress);
      break;
    case 'job.completed':
      showResults(msg.result);
      break;
    case 'job.failed':
      showError(msg.error);
      break;
  }
};
```

**Eventos del servidor:**

| Evento | Payload | Descripción |
|:-------|:--------|:------------|
| `job.created` | `{job_id, type, status}` | Job encolado |
| `job.started` | `{job_id, started_at}` | Worker inició procesamiento |
| `job.progress` | `{job_id, progress, message}` | Actualización de progreso (0-100%) |
| `job.completed` | `{job_id, result, completed_at}` | Job finalizado exitosamente |
| `job.failed` | `{job_id, error, retry_count}` | Job falló, puede reintentar |
| `heartbeat` | `{ts, service, status}` | Latido del sistema cada 5 min |

---

## 10. Pipeline IA/ML Detallado

### 10.1 Fase A: Preprocesamiento NLP

```python
# services/nlp_pipeline.py
import spacy
import re
from typing import Dict, List

class NLPPipeline:
    def __init__(self):
        self.nlp = spacy.load("es_core_news_lg")

        self.patterns = {
            'price': re.compile(r'S/\s*\d+(?:\.\d{2})?|USD\s*\d+|\$\d+'),
            'offer': re.compile(r'2x1|50%\s*OFF|GRATIS|DESCUENTO|PROMO'),
            'urgency': re.compile(r'ahora|último|corre|hoy|limitado|quedan\s+\d+'),
            'social_proof': re.compile(r'miles|clientes|testimonios|reseñas|estrellas'),
            'fear': re.compile(r'pierde|olvida|sufrimiento|dolor|crisis|alerta'),
            'benefit': re.compile(r'gratis|gana|mejora|resultados|transforma|logra'),
            'whatsapp': re.compile(r'wa\.me|whatsapp|\.com\/wa'),
            'url': re.compile(r'https?://[^\s]+'),
        }

    def preprocess(self, copy: str) -> Dict:
        doc = self.nlp(copy)
        cleaned = self._clean_text(copy)
        entities = self._extract_entities(doc)
        linguistics = self._analyze_linguistics(doc)
        business = self._extract_business_patterns(copy)
        sentiment = self._calculate_sentiment(doc)

        return {
            'copy_cleaned': cleaned,
            'entities': entities,
            'linguistics': linguistics,
            'business_patterns': business,
            'sentiment': sentiment,
            'word_count': len(doc),
            'sentence_count': len(list(doc.sents)),
        }

    def _clean_text(self, copy: str) -> str:
        text = re.sub(r'https?://\S+', ' URL ', copy)
        text = re.sub(r'\s+', ' ', text).strip()
        return text.lower()

    def _extract_entities(self, doc) -> List[Dict]:
        return [
            {'text': ent.text, 'label': ent.label_}
            for ent in doc.ents
        ]

    def _analyze_linguistics(self, doc) -> Dict:
        pos_counts = {}
        for token in doc:
            pos_counts[token.pos_] = pos_counts.get(token.pos_, 0) + 1

        imperatives = [token.text for token in doc 
                      if token.pos_ == 'VERB' and token.morph.get('Mood') == ['Imp']]

        return {
            'pos_distribution': pos_counts,
            'imperative_verbs': imperatives,
            'avg_word_length': sum(len(token.text) for token in doc) / max(len(doc), 1),
        }

    def _extract_business_patterns(self, copy: str) -> Dict:
        return {
            'prices': self.patterns['price'].findall(copy),
            'offers': self.patterns['offer'].findall(copy),
            'urgency_words': len(self.patterns['urgency'].findall(copy)),
            'social_proof_words': len(self.patterns['social_proof'].findall(copy)),
            'fear_words': len(self.patterns['fear'].findall(copy)),
            'benefit_words': len(self.patterns['benefit'].findall(copy)),
            'has_whatsapp': bool(self.patterns['whatsapp'].search(copy)),
            'has_url': bool(self.patterns['url'].search(copy)),
        }

    def _calculate_sentiment(self, doc) -> Dict:
        positive_words = {'gratis', 'mejor', 'gana', 'resultados', 'feliz', 'éxito', 'amor'}
        negative_words = {'pierde', 'dolor', 'sufrimiento', 'crisis', 'problema', 'miedo'}

        pos_count = sum(1 for token in doc if token.lemma_ in positive_words)
        neg_count = sum(1 for token in doc if token.lemma_ in negative_words)
        total = len(doc)

        return {
            'positive_ratio': pos_count / max(total, 1),
            'negative_ratio': neg_count / max(total, 1),
            'polarity': (pos_count - neg_count) / max(total, 1),
        }
```

### 10.2 Fase B: LLM Gateway

```python
# services/llm_gateway.py
import json
import asyncio
from typing import Optional
from pydantic import BaseModel, ValidationError

class LLMGateway:
    def __init__(self, settings):
        self.primary = QoderClient(api_key=settings.QODER_API_KEY)
        self.fallback = GeminiClient(api_key=settings.GEMINI_API_KEY)
        self.prompt_template = self._load_prompt()

    def _load_prompt(self) -> str:
        with open("prompts/prompt_f3_analisis.txt", "r") as f:
            return f.read()

    async def analyze_copy(self, copy_text: str) -> LLMOutput:
        prompt = self.prompt_template.format(copy=copy_text[:2000])

        try:
            response = await asyncio.wait_for(
                self.primary.generate(prompt, temperature=0.3, max_tokens=800),
                timeout=30
            )
            return self._parse_and_validate(response)

        except (asyncio.TimeoutError, json.JSONDecodeError, ValidationError) as e:
            logger.warning(f"Qoder failed ({type(e).__name__}), falling back to Gemini")

            try:
                response = await asyncio.wait_for(
                    self.fallback.generate(prompt, temperature=0.3, max_tokens=800),
                    timeout=30
                )
                return self._parse_and_validate(response)

            except Exception as e2:
                logger.error(f"Both LLMs failed: {e2}")
                return self._heuristic_fallback(copy_text)

    def _parse_and_validate(self, raw_response: str) -> LLMOutput:
        cleaned = raw_response.strip()
        if cleaned.startswith("```json"):
            cleaned = cleaned[7:]
        if cleaned.endswith("```"):
            cleaned = cleaned[:-3]
        cleaned = cleaned.strip()

        data = json.loads(cleaned)
        return LLMOutput(**data)

    def _heuristic_fallback(self, copy_text: str) -> LLMOutput:
        lines = copy_text.split('\n')
        hook = ' '.join(lines[:2])[:150] if lines else copy_text[:150]

        pain_keywords = ['dolor', 'problema', 'cansado', 'estres', 'ansiedad', 'dinero']
        pain = next((p for p in pain_keywords if p in copy_text.lower()), "general")

        cta_keywords = ['compra', 'ordena', 'llama', 'escribe', 'clica', 'regístrate']
        cta = next((c for c in cta_keywords if c in copy_text.lower()), "contactar")

        return LLMOutput(
            hook_principal=hook,
            pain_point=pain,
            objection_killed="precio",
            sales_angle="salud",
            tone="educativo",
            target_audience="adultos 25-45",
            cta_type=cta
        )
```

### 10.3 Fase C: Winner Score (F3 Heurístico → F4 ML)

```python
# services/winner_score.py
from typing import List, Dict
import numpy as np

class WinnerScoreCalculator:
    def __init__(self, mode: str = "heuristic"):
        self.mode = mode
        if mode == "ml":
            import xgboost as xgb
            self.model = xgb.Booster()
            self.model.load_model("models/winner_score_xgb.json")

    def calculate(self, features: CopyFeatures, llm_output: LLMOutput) -> WinnerScoreOutput:
        if self.mode == "heuristic":
            return self._heuristic_score(features, llm_output)
        else:
            return self._ml_score(features, llm_output)

    def _heuristic_score(self, features: CopyFeatures, llm_output: LLMOutput) -> WinnerScoreOutput:
        hook_score = self._score_hook(llm_output.hook_principal, features)
        pain_score = self._score_pain(llm_output.pain_point, features)
        objection_score = self._score_objection(llm_output.objection_killed, features)
        angle_score = self._score_angle(llm_output.sales_angle, features)
        cta_score = self._score_cta(llm_output.cta_type, features)

        weights = {
            'hook': 0.30,
            'pain': 0.25,
            'objection': 0.20,
            'angle': 0.15,
            'cta': 0.10
        }

        winner_score = (
            hook_score * weights['hook'] +
            pain_score * weights['pain'] +
            objection_score * weights['objection'] +
            angle_score * weights['angle'] +
            cta_score * weights['cta']
        )

        confidence = self._calculate_confidence(llm_output)

        return WinnerScoreOutput(
            winner_score=round(winner_score, 2),
            confidence=round(confidence, 2),
            hook_score=round(hook_score, 2),
            pain_score=round(pain_score, 2),
            objection_score=round(objection_score, 2),
            angle_score=round(angle_score, 2),
            cta_score=round(cta_score, 2)
        )

    def _score_hook(self, hook: str, features: CopyFeatures) -> float:
        score = 50.0
        hook_len = len(hook)
        if 80 <= hook_len <= 150:
            score += 20
        elif 50 <= hook_len <= 200:
            score += 10
        if any(c.isdigit() for c in hook):
            score += 10
        if '!' in hook or '?' in hook:
            score += 10
        if ' tú ' in hook.lower() or ' tu ' in hook.lower():
            score += 10
        return min(score, 100)

    def _score_pain(self, pain: str, features: CopyFeatures) -> float:
        score = 50.0
        generic_pains = {'problema', 'dolor', 'cansancio'}
        if pain.lower() not in generic_pains:
            score += 20
        emotional_words = {'crisis', 'desesperación', 'frustración', 'miedo', 'pánico'}
        if any(w in pain.lower() for w in emotional_words):
            score += 15
        if any(w in pain.lower() for w in {'ahora', 'ya', 'cada día'}):
            score += 15
        return min(score, 100)

    def _score_objection(self, objection: str, features: CopyFeatures) -> float:
        score = 50.0
        common_objections = {'precio', 'dinero', 'costo', 'caro', 'confianza', 
                              'estafa', 'tiempo', 'resultados', 'garantía'}
        if any(w in objection.lower() for w in common_objections):
            score += 25
        if any(w in objection.lower() for w in {'garantía', 'prueba', 'devolución', 'reembolso'}):
            score += 25
        return min(score, 100)

    def _score_angle(self, angle: str, features: CopyFeatures) -> float:
        score = 60.0
        proven_angles = {'salud', 'ahorro', 'urgencia'}
        if angle in proven_angles:
            score += 20
        if angle == 'estética' and any(w in features.copy_cleaned for w in {'belleza', 'piel', 'cuerpo'}):
            score += 20
        return min(score, 100)

    def _score_cta(self, cta: str, features: CopyFeatures) -> float:
        score = 50.0
        low_friction = {'contactar', 'descargar'}
        high_friction = {'comprar', 'registrarse'}
        if cta in low_friction:
            score += 25
        elif cta in high_friction:
            score += 10
        if features.has_whatsapp:
            score += 15
        if cta == 'comprar' and features.urgency_words > 0:
            score += 10
        return min(score, 100)

    def _calculate_confidence(self, llm_output: LLMOutput) -> float:
        confidence = 0.5
        if llm_output.hook_principal and len(llm_output.hook_principal) > 20:
            confidence += 0.1
        if llm_output.pain_point and llm_output.pain_point not in ['general', 'dolor']:
            confidence += 0.1
        if llm_output.target_audience and len(llm_output.target_audience) > 5:
            confidence += 0.1
        if llm_output.sales_angle != 'salud':
            confidence += 0.1
        if llm_output.tone != 'educativo':
            confidence += 0.1
        return min(confidence, 1.0)

    def _ml_score(self, features: CopyFeatures, llm_output: LLMOutput) -> WinnerScoreOutput:
        import xgboost as xgb
        X = np.array([[
            features.copy_length,
            features.word_count,
            features.emoji_count,
            features.exclamation_count,
            features.uppercase_ratio,
            features.price_mentions,
            features.urgency_words,
            features.social_proof_words,
            features.fear_words,
            features.benefit_words,
            len(llm_output.hook_principal),
            hash(llm_output.sales_angle) % 10,
            hash(llm_output.tone) % 10,
        ]])
        dmatrix = xgb.DMatrix(X)
        prediction = self.model.predict(dmatrix)[0]
        winner_score = prediction * 100

        return WinnerScoreOutput(
            winner_score=round(winner_score, 2),
            confidence=round(prediction, 2),
            hook_score=0,
            pain_score=0,
            objection_score=0,
            angle_score=0,
            cta_score=0
        )
```

### 10.4 Fase D: Clustering y Embeddings

```python
# services/clustering.py
from sentence_transformers import SentenceTransformer
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np

class CopyClustering:
    def __init__(self, n_clusters: int = 5):
        self.n_clusters = n_clusters
        self.embedder = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
        self.kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
        self.vectorizer = TfidfVectorizer(max_features=100, stop_words='spanish')

    def fit(self, copies: List[str]) -> Dict:
        embeddings = self.embedder.encode(copies, show_progress_bar=False)
        clusters = self.kmeans.fit_predict(embeddings)

        cluster_keywords = {}
        for cluster_id in range(self.n_clusters):
            cluster_copies = [copies[i] for i, c in enumerate(clusters) if c == cluster_id]
            if cluster_copies:
                tfidf = self.vectorizer.fit_transform(cluster_copies)
                feature_names = self.vectorizer.get_feature_names_out()
                scores = tfidf.sum(axis=0).A1
                top_indices = scores.argsort()[-5:][::-1]
                cluster_keywords[cluster_id] = [feature_names[i] for i in top_indices]

        centroids = []
        for cluster_id in range(self.n_clusters):
            cluster_indices = [i for i, c in enumerate(clusters) if c == cluster_id]
            if cluster_indices:
                cluster_embeddings = embeddings[cluster_indices]
                centroid = cluster_embeddings.mean(axis=0)
                distances = np.linalg.norm(cluster_embeddings - centroid, axis=1)
                closest_idx = cluster_indices[distances.argmin()]
                centroids.append({
                    'cluster_id': cluster_id,
                    'representative_copy': copies[closest_idx][:200],
                    'size': len(cluster_indices),
                    'keywords': cluster_keywords.get(cluster_id, [])
                })

        return {
            'clusters': clusters.tolist(),
            'centroids': centroids,
            'embeddings': embeddings.tolist()
        }
```

---

## 11. Decisiones Técnicas Archivadas

### DT-001 — FastAPI vs Flask vs Django

**Decisión:** FastAPI
**Rationale:** Async nativo, OpenAPI auto-generado, Pydantic v2 integrado, performance superior. Flask es síncrono por defecto. Django es overkill para API-only.
**Consecuencia:** Curva de aprendizaje menor para CDD (Chat-Driven). Documentación API automática acelera frontend.

### DT-002 — Next.js vs React puro vs Vue

**Decisión:** Next.js 14 (App Router)
**Rationale:** SSR para SEO (landing pages), API Routes para proxy, Edge Runtime compatible con Vercel, file-based routing reduce decisiones.
**Consecuencia:** No necesitamos servidor backend separado para funciones simples (API Routes). Menos infraestructura.

### DT-003 — Supabase vs Firebase vs MongoDB Atlas

**Decisión:** Supabase
**Rationale:** PostgreSQL (SQL relacional = mejor para datos estructurados de ads), Auth integrado, Storage S3, Realtime WebSocket, RLS nativo. Firebase es NoSQL (menos estructurado para nuestro schema). MongoDB Atlas tiene costos de escalamiento impredecibles.
**Consecuencia:** Schema relacional con joins eficientes. RLS simplifica multi-tenancy sin código extra.

### DT-004 — Celery vs RQ vs Asyncio puro

**Decisión:** Celery + Redis (F4) / Asyncio (F0-F3)
**Rationale:** Celery tiene retries, priorización, monitoreo, y workers distribuidos. RQ es más simple pero menos features. Asyncio puro es suficiente para F0-F3 (procesamiento secuencial manual).
**Consecuencia:** F0-F3 no necesitan Celery. F4 requiere Celery para procesamiento paralelo de múltiples keywords.

### DT-005 — Sentence-BERT vs OpenAI Embeddings

**Decisión:** Sentence-BERT (paraphrase-multilingual-MiniLM-L12-v2)
**Rationale:** Gratuito, local, multilingüe (español), 384 dimensiones (ligero). OpenAI embeddings requieren API key y tienen costo por token.
**Consecuencia:** Embeddings generados localmente en el worker. Sin dependencia de API externa para clustering.

### DT-006 — XGBoost vs Random Forest vs Neural Networks

**Decisión:** XGBoost (F4+)
**Rationale:** Tabular data (features estructurados), interpretable, rápido de entrenar, buen performance con pocos datos. Neural networks requieren más datos y son caja negra.
**Consecuencia:** Modelo entrenable con ~1000 ejemplos. Feature importance interpretable por el CEO.

---

## 12. Matriz de Dependencias

```
┌────────────────────────────────────────────────────────────────────────────┐
│                    MATRIZ DE DEPENDENCIAS EXTERNAS                         │
├────────────────────────────────────────────────────────────────────────────┤
│                                                                            │
│  Meta Ads Library (Fuente)                                                 │
│  ├── Tipo: Fuente de datos externa                                         │
│  ├── Riesgo: ALTO (puede bloquear scraping)                                │
│  ├── Mitigación: Playwright stealth + proxies + rate limiting + manual F0-F3 │
│  └── Alternativa: Ninguna (monopolio de Meta)                             │
│                                                                            │
│  Qoder CN / Alibaba Cloud (LLM Primary)                                    │
│  ├── Tipo: Servicio IA (generación)                                        │
│  ├── Riesgo: MEDIO (dependencia de $1/mes, puede cambiar pricing)         │
│  ├── Mitigación: Fallback a Gemini Flash. Código generado es independiente │
│  └── Alternativa: Gemini 2.5 Flash, Claude, local LLMs                     │
│                                                                            │
│  Google AI / Gemini (LLM Fallback)                                         │
│  ├── Tipo: Servicio IA (fallback)                                          │
│  ├── Riesgo: BAJO (gratuito, límites generosos)                            │
│  ├── Mitigación: Rate limiting propio, cache de respuestas                 │
│  └── Alternativa: Qoder CN (primary), OpenAI (último recurso)             │
│                                                                            │
│  Supabase (Database + Auth + Storage)                                      │
│  ├── Tipo: Infraestructura crítica                                         │
│  ├── Riesgo: MEDIO (free tier tiene límites, pero escalable)              │
│  ├── Mitigación: Backups automáticos, schema portable a cualquier PG       │
│  └── Alternativa: PostgreSQL en Render, Railway, AWS RDS                  │
│                                                                            │
│  Render (Backend Hosting)                                                  │
│  ├── Tipo: Infraestructura de ejecución                                    │
│  ├── Riesgo: MEDIO (free tier puede dormir, paid es estable)              │
│  ├── Mitigación: Koyeb como alternativa free 24/7. Test 72h obligatorio   │
│  └── Alternativa: Koyeb, Railway, Fly.io, AWS ECS                          │
│                                                                            │
│  Vercel (Frontend Hosting)                                                 │
│  ├── Tipo: Infraestructura de presentación                                 │
│  ├── Riesgo: BAJO (edge network robusto, free tier generoso)               │
│  ├── Mitigación: Cloudflare Pages como alternativa                         │
│  └── Alternativa: Cloudflare Pages, Netlify, AWS S3 + CloudFront          │
│                                                                            │
│  Upstash Redis (Cache)                                                       │
│  ├── Tipo: Infraestructura de cache                                        │
│  ├── Riesgo: BAJO (free tier 10k req/día, suficiente para MVP)            │
│  ├── Mitigación: SQLite local como cache fallback                          │
│  └── Alternativa: Redis en Render, Memcached, local dict                   │
│                                                                            │
│  UptimeRobot (Monitoreo)                                                   │
│  ├── Tipo: Servicio de monitoreo                                           │
│  ├── Riesgo: BAJO (free tier: 50 monitores, 5 min interval)               │
│  ├── Mitigación: Logs propios + alertas manual como backup                  │
│  └── Alternativa: Pingdom, StatusCake, monitoreo propio con cron           │
│                                                                            │
│  GitHub (Source Control + CI/CD)                                           │
│  ├── Tipo: Infraestructura de desarrollo                                   │
│  ├── Riesgo: BAJO (GitLab, Bitbucket como alternativas inmediatas)         │
│  ├── Mitigación: Git es distribuido, migración trivial                     │
│  └── Alternativa: GitLab, Bitbucket, GitBucket (self-hosted)              │
│                                                                            │
└────────────────────────────────────────────────────────────────────────────┘
```

---

## Apéndice: Glosario Técnico

| Término | Definición |
|:--------|:-----------|
| **ASGI** | Asynchronous Server Gateway Interface. Protocolo para servidores Python async (como Uvicorn). |
| **RLS** | Row Level Security. Política de PostgreSQL que filtra filas por usuario autenticado. |
| **Pydantic** | Librería de validación de datos con tipos de Python. Usada en FastAPI para request/response. |
| **Celery** | Sistema de colas de tareas distribuido. Usado para procesamiento async de jobs. |
| **pgvector** | Extensión de PostgreSQL para almacenar y buscar vectores (embeddings). |
| **Sentence-BERT** | Modelo de embeddings semánticos. Convierte texto en vectores numéricos para comparación. |
| **Playwright Stealth** | Técnica para evitar detección de bots en navegación automatizada. |
| **Circuit Breaker** | Patrón que evita reintentos continuos cuando un servicio externo falla. |
| **Exponential Backoff** | Estrategia de reintentos donde el tiempo de espera crece exponencialmente. |
| **Jitter** | Variación aleatoria añadida a los tiempos de espera para evitar thundering herd. |
| **Zero-Touch** | Sistema que opera sin intervención humana durante 72h+ continuas. |
| **Design for Change** | Principio de diseñar componentes para ser modificados fácilmente en el futuro. |

---

> **CEO, este es el blueprint técnico completo.** Cada capa, cada tecnología, cada decisión, cada flujo de datos está documentado. No hay caja negra. No hay magia. Solo arquitectura limpia, medible y ejecutable.
>
> **El parser se congela en F0. El resto escala a F4 sin tocar una línea de lógica de negocio.**
>
> *Staff Engineer 100x — ADN HIDATA Method v1.4*
