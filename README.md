# 📡 WinnerRadar — Motor Horizontal de Inteligencia Comercial

**Metodología:** HIDATA Method v1.4 — 10 Principios · 13 Secciones · Anexo I · Anexo II
**Última actualización:** 20 jun 2026
**Owners:** CEO (Visión/Negocio) + Staff Engineer 100x (Arquitectura/IA)
**Cliente:** Interno — Winner / HIDATA Consulting
**Repo:** `winner-radar` (VS Code + Qoder CN)
**Estado actual:** Fase 0 — Ingesta & Estandarización del Motor Horizontal
**Stack:** Python 3.11+ · Pandas · Regex · Qoder CN / Qwen (IA) · CSV / GSheets (F0-F3) → Render · Supabase · Vercel · Playwright (F4)

---

## Visión y Posicionamiento

**WinnerRadar** es un **Motor Horizontal de Inteligencia Comercial** para e-commerce, media buyers, agencias y emprendedores en Latam.

> *"Permite ingresar CUALQUIER keyword (producto, servicio, nicho, tendencia), cruzarla con la Meta Ads Library, detectar competidores que están escalando (Ballenas), analizar sus copys, ofertas y embudos con IA, y entregar insights accionables para lanzar campañas rentables en <24h."*

## Las Dos Fases Principales

### MOVIMIENTO 1 — El Radar (Búsqueda por Keyword)

- **Entrada:** Cualquier keyword ("Moringa", "Corrector de Postura", "Seguros de Vida")
- **Acción:** Buscar en Meta Ads Library general
- **Filtro Mágico:** Identificar Ballenas por días activo (>15 días), variantes visuales (>2) y nivel de impresiones
- **Salida:** Lista de 3-5 Fanpages ganadoras por keyword

### MOVIMIENTO 2 — La Infiltración (Búsqueda por Fanpage)

- **Entrada:** Fanpage descubierta en Movimiento 1 (ej: NaturaVida con 4,300 ads)
- **Acción:** Entrar al perfil completo del anunciante
- **Hack:** Descubrir el "Catálogo Oculto" (Front-end vs Back-end)
  - Ej: NaturaVida usa Moringa como gancho, pero factura con Ashwagandha y Colágeno
- **Salida:** Mapeo completo del competidor + oportunidades de Upsell

## Fases del Proyecto (F0 → F4)

| Fase | Nombre | Objetivo Clave | Entregable |
|:-----|:-------|:---------------|:-----------|
| **F0** ← actual | Ingesta & Estandarización | Crear el **Parser Universal** que convierte cualquier TXT de Meta Ads en BD estructurada | `parser_meta_ads_universal.py` + Schema v2.0 validado |
| **F1** | El Radar (Keyword Scan) | Probar el Parser con 3 keywords distintas (1 producto, 1 servicio, 1 tendencia) | BD de Anuncios + Filtro de Ballenas funcionando |
| **F2** | La Infiltración | Entrar a fanpages seleccionadas, mapear catálogo oculto y embudos | Reporte de Competidores Top por Keyword |
| **F3** | Capa IA & Winner Score | Automatizar análisis de copys, ganchos y objeciones con LLM. Puntuar ganadores | Dataset etiquetado + Ranking automático |
| **F4** | Escala & Automatización | Migrar a pipeline cloud 24/7. SaaS interno MVP desplegado | Render + Supabase + Vercel + Playwright stealth |

## Estructura de Carpetas

```
winner-radar/
├── README.md
├── MASTER-PLAN.md
├── .gitignore
├── requirements.txt
│
├── data/                            # MATERIA PRIMA (Agnóstica)
│   ├── keywords/
│   ├── meta_ads_raw/                # TXTs crudos del Radar
│   └── infiltracion/                # TXTs de perfiles completos (Ballenas)
│
├── output/                          # PRODUCTOS PROCESADOS
│   ├── radar/
│   ├── infiltracion/
│   └── reportes_ia/
│
├── scripts/                         # CÓDIGO PYTHON
│   ├── parsers/
│   ├── analysis/
│   └── utils/
│
├── prompts/                         # PROMPTS REUTILIZABLES
│
├── notebooks/
│
└── docs/
```

## Contribuidores

- [berthidalgo](https://github.com/berthidalgo) - Desarrollador Principal

## Comenzar a trabajar

1. Instalar dependencias:
   ```
   pip install -r requirements.txt
   ```

2. Para comenzar con la Fase 0, responder las 5 preguntas de la Sección 9 del MASTER PLAN
3. Crear el archivo `data/keywords/evals_parametros.json` con las respuestas
4. Implementar el `parser_meta_ads_universal.py` siguiendo el Prompt F0