# 📡 WinnerRadar — MASTER PLAN v2.0

**Metodología:** HIDATA Method v1.4 — 10 Principios · 13 Secciones · Anexo I · Anexo II
**Última actualización:** 20 jun 2026
**Owners:** CEO (Visión/Negocio) + Staff Engineer 100x (Arquitectura/IA)
**Cliente:** Interno — Winner / HIDATA Consulting
**Repo:** `winner-radar` (VS Code + Qoder CN)
**Estado actual:** Fase 0 — Ingesta & Estandarización del Motor Horizontal
**Stack:** Python 3.11+ · Pandas · Regex · Qoder CN / Qwen (IA) · CSV / GSheets (F0-F3) → Render · Supabase · Vercel · Playwright (F4)

---

## 1. Visión y Posicionamiento

**WinnerRadar** es un **Motor Horizontal de Inteligencia Comercial** para e-commerce, media buyers, agencias y emprendedores en Latam.

> *"Permite ingresar CUALQUIER keyword (producto, servicio, nicho, tendencia), cruzarla con la Meta Ads Library, detectar competidores que están escalando (Ballenas), analizar sus copys, ofertas y embudos con IA, y entregar insights accionables para lanzar campañas rentables en <24h."*

### 🔄 El Pivot Estratégico (Lección #5)

| | Visión Táctica (Descartada) | Visión Horizontal (Actual) |
|:--|:--|:--|
| **Alcance** | Catálogo PDF Winner (120 productos) | Cualquier keyword, cualquier industria |
| **Mercado** | 1 empresa | E-commerce, agencias, media buyers, Latam |
| **Modelo** | Herramienta interna | SaaS de Inteligencia Comercial |
| **Escala** | x1 | x1000 |

El origen de la keyword es irrelevante. El valor está en el **Motor de Búsqueda y Análisis Universal**.

### 💎 Diferenciador HIDATA

No vendemos data cruda. Vendemos **Winner Score + Psicología de Venta validada por el mercado**, con un flujo zero-friction que prioriza Time-to-Market sobre perfección arquitectónica.

### 🎯 Los Dos Movimientos (Dogma de Ejecución — el orden NO se negocia)

**MOVIMIENTO 1 — El Radar (Búsqueda por Keyword)**

- **Entrada:** Cualquier keyword ("Moringa", "Corrector de Postura", "Seguros de Vida")
- **Acción:** Buscar en Meta Ads Library general
- **Filtro Mágico:** Identificar Ballenas por días activo (>15 días), variantes visuales (>2) y nivel de impresiones
- **Salida:** Lista de 3-5 Fanpages ganadoras por keyword

**MOVIMIENTO 2 — La Infiltración (Búsqueda por Fanpage)**

- **Entrada:** Fanpage descubierta en Movimiento 1 (ej: NaturaVida con 4,300 ads)
- **Acción:** Entrar al perfil completo del anunciante
- **Hack:** Descubrir el "Catálogo Oculto" (Front-end vs Back-end)
  - Ej: NaturaVida usa Moringa como gancho, pero factura con Ashwagandha y Colágeno
- **Salida:** Mapeo completo del competidor + oportunidades de Upsell

> ⚠️ **El orden de los factores SÍ altera la rentabilidad.** Siempre: Radar → Filtrar Ballenas → Infiltrar. (DA-003, Lección #4)

---

## 2. Fases del Proyecto (F0 → F4)

| Fase | Nombre | Objetivo Clave | Entregable |
|:-----|:-------|:---------------|:-----------|
| **F0** ← actual | Ingesta & Estandarización | Crear el **Parser Universal** que convierte cualquier TXT de Meta Ads en BD estructurada | `parser_meta_ads_universal.py` + Schema v2.0 validado |
| **F1** | El Radar (Keyword Scan) | Probar el Parser con 3 keywords distintas (1 producto, 1 servicio, 1 tendencia) | BD de Anuncios + Filtro de Ballenas funcionando |
| **F2** | La Infiltración | Entrar a fanpages seleccionadas, mapear catálogo oculto y embudos | Reporte de Competidores Top por Keyword |
| **F3** | Capa IA & Winner Score | Automatizar análisis de copys, ganchos y objeciones con LLM. Puntuar ganadores | Dataset etiquetado + Ranking automático |
| **F4** | Escala & Automatización | Migrar a pipeline cloud 24/7. SaaS interno MVP desplegado | Render + Supabase + Vercel + Playwright stealth |

---

## 3. Estado Actual Detallado — F0: Ingesta & Estandarización

### Arquitectura Objetivo F0

```
[Meta Ads Library UI]
        ↓  (copy-paste manual — TXT crudo)
[data/meta_ads_raw/{keyword}_raw.txt]
        ↓  (parser_meta_ads_universal.py)  ← CORAZÓN DE F0
[output/radar/bd_meta_ads_{keyword}.csv]   ← Schema v2.0
        ↓  (filtro_ballenas.py)
[output/infiltracion/ballenas_{keyword}.csv]  ← Top competidores
        ↓  (ia_analisis_copies.py + winner_score.py)
[output/reportes_ia/ranking_ganadores.csv]    ← Winner Score final
```

### Schema de Datos Universal v2.0

**Tabla 1: `keyword_radar_results` — Movimiento 1 (Radar)**

| Columna | Tipo | Ejemplo Producto | Ejemplo Servicio | Ejemplo Real Estate |
|:--------|:-----|:-----------------|:-----------------|:--------------------|
| `Keyword_Buscada` | String | "Moringa" | "Agencia Marketing" | "Depto Miami" |
| `Fanpage_Name` | String | "NaturaVida" | "DigitalPro" | "InmoGlobal" |
| `Fanpage_ID` | String | "946991..." | "883721..." | "772618..." |
| `Total_Ads_Active` | Int | 4300 | 150 | 85 |
| `Ad_ID_Representativo` | String | "16269..." | "99218..." | "55432..." |
| `Start_Date` | Date | 2026-06-10 | 2026-01-15 | 2025-11-02 |
| `Days_Active` | Int | 10 | 156 | 230 |
| `Creative_Variants` | Int | 2 | 1 | 3 |
| `Impressions_Level` | Enum | Alto/Bajo/Normal | Normal | Alto |
| `Format` | Enum | Video/Imagen | Video | Carrusel |
| `Duration` | String | "1:22" | "0:45" | "N/A" |

**Tabla 2: `ad_creative_analysis` — Movimiento 2 + IA (F3)**

| Columna | Tipo | Descripción |
|:--------|:-----|:------------|
| `Ad_ID` | String | FK a Tabla 1 |
| `Copy_Full` | Text | Texto completo del anuncio |
| `Hook_Extracted` | String | Gancho psicológico (IA) |
| `Pain_Point` | String | Dolor que ataca (IA) |
| `Objection_Killed` | String | Objeción que mata (IA) |
| `Sales_Angle` | String | Ángulo de venta (IA) |
| `Tone` | String | Tono (agresivo, educativo, empático, científico, humorístico) |
| `Offer_Extracted` | String | "2x1 S/99" o "Financiamiento 0%" |
| `Funnel_Type` | Enum | WhatsApp / Landing / Form / DM |
| `Winner_Score` | Float | Puntuación final 0-100 |

### Arquitectura de Carpetas

```
winner-radar/
├── 📄 README.md
├── 📄 MASTER-PLAN.md
├── 📄 .gitignore
├── 📄 requirements.txt
│
├── 📂 data/                            # MATERIA PRIMA (Agnóstica)
│   ├── 📂 keywords/
│   │   ├── keywords_batch_001.csv
│   │   └── evals_parametros.json       # Respuestas Sección 9
│   ├── 📂 meta_ads_raw/                # TXTs crudos del Radar
│   │   ├── moringa_raw.txt
│   │   ├── corrector_postura_raw.txt
│   │   └── seguros_vida_raw.txt
│   └── 📂 infiltracion/                # TXTs de perfiles completos (Ballenas)
│       ├── naturavida_completo.txt
│       └── herbalab_completo.txt
│
├── 📂 output/                          # PRODUCTOS PROCESADOS
│   ├── 📂 radar/
│   │   ├── bd_meta_ads_{keyword}.csv
│   │   └── bd_consolidada.csv
│   ├── 📂 infiltracion/
│   │   └── reporte_{fanpage_name}.csv
│   ├── 📂 reportes_ia/
│   │   ├── analisis_copies_{keyword}.json
│   │   └── ranking_ganadores.csv
│   └── ejecuciones_log.csv             # Heartbeat manual F0-F3
│
├── 📂 scripts/                         # CÓDIGO PYTHON
│   ├── 📂 parsers/
│   │   ├── parser_meta_ads_universal.py   # F0 — CORAZÓN (se congela al terminar F0)
│   │   └── parser_infiltracion.py          # F2
│   ├── 📂 analysis/
│   │   ├── filtro_ballenas.py              # F1
│   │   ├── ia_analisis_copies.py           # F3
│   │   └── winner_score.py                 # F3
│   └── 📂 utils/
│       ├── limpieza_texto.py
│       └── validacion.py
│
├── 📂 prompts/                         # PROMPTS REUTILIZABLES
│   ├── prompt_f0_parser_universal.txt
│   ├── prompt_f1_ballenas.txt
│   ├── prompt_f2_infiltracion.txt
│   └── prompt_f3_analisis.txt
│
├── 📂 notebooks/
│   └── 01_exploracion_radar.ipynb
│
└── 📂 docs/
    ├── arquitectura.md
    ├── schema_datos.md
    └── lecciones_aprendidas.md
```

**Setup inicial:**

```bash
mkdir -p winner-radar/{data/{keywords,meta_ads_raw,infiltracion},output/{radar,infiltracion,reportes_ia},scripts/{parsers,analysis,utils},prompts,notebooks,docs}
cd winner-radar
echo "pandas>=2.0.0
regex>=2023.0.0
openpyxl>=3.1.0
python-dateutil>=2.8.2" > requirements.txt
pip install -r requirements.txt
```

### Plan de Ataque Inmediato (Próximas 4 Horas)

| Minuto | Acción | Responsable | Entregable |
|:-------|:-------|:------------|:-----------|
| 0-30 | Crear estructura de carpetas en VS Code | CEO | Repo inicial |
| 30-60 | Pegar Prompt F0 en Qoder CN → generar `parser_meta_ads_universal.py` | CEO + IA | Parser Universal |
| 60-90 | Probar parser con TXT de NaturaVida (Moringa) | CEO | Validación 1 |
| 90-120 | CEO busca 2 keywords distintas en Meta Ads y copia TXTs | CEO | 2 TXTs nuevos |
| 120-150 | Probar parser con los 2 TXTs nuevos | CEO + IA | Validación 2 y 3 |
| 150-180 | Prompt F1 → Filtro de Ballenas sobre los 3 datasets | CEO + IA | Top ballenas |
| 180-210 | CEO selecciona 3 ballenas y copia TXTs de perfiles completos | CEO | Data Infiltración |
| 210-240 | Prompt F3 → IA analiza copies + Winner Score | IA | Ranking final |

### Flujo de Trabajo CDD (Chat-Driven Development)

```
1. CEO extrae .txt crudo de Meta Ads Library (cualquier keyword)
2. CEO coloca .txt en data/meta_ads_raw/{keyword}_raw.txt
3. CEO ejecuta parser_meta_ads_universal.py
4. CEO valida output en output/radar/bd_meta_ads_{keyword}.csv
5. CEO aplica filtro_ballenas.py → obtiene Top competidores
6. CEO infiltra ballenas seleccionadas → copia TXTs completos
7. CEO ejecuta ia_analisis_copies.py → obtiene insights
8. CEO arma campañas con ángulos validados por el mercado
9. Si DoD se cumple → actualizar Master Plan → siguiente fase
```

> 💡 **Nota CDD:** Al abrir un chat nuevo, pegar siempre el **HIDATA Method v1.4** + el **Prompt de la fase actual** (Sección 6). El asistente retoma el contexto completo sin perder ADN.

---

## 4. Definition of Done por Fase

```yaml
F0_done_when:
  parser_universal_creado: true
  probado_con_naturaVida_txt: true
  probado_con_keyword_servicio: true
  probado_con_keyword_tendencia_o_real_estate: true
  columnas_schema_v2_pobladas: true
  zero_codigo_nuevo_de_parsing: true    # El motor se congela después de F0
  evals_parametros_respondidos: true    # Sección 9 completada por CEO
  trigger_f1: "CEO trae 3 TXTs de keywords distintas"

F1_done_when:
  3_keywords_procesadas: true
  filtro_ballenas_funcional: ">7 días activos AND >2 variantes visuales"
  ballena_score_calculado: true
  output_consolidado: "CSV con todas las keywords unificadas"
  trigger_f2: "CEO selecciona 3-5 ballenas para infiltrar"

F2_done_when:
  mapeo_catalogo_oculto: "lista de productos back-end por ballena"
  embudos_identificados: "% WhatsApp vs Web vs Landing vs Formulario"
  ofertas_cruzadas: "tabla comparativa de precios/promos por ballena"
  trigger_f3: "dataset consolidado validado por CEO, listo para análisis IA"

F3_done_when:
  ia_copies_analizados: "Hook, Dolor, Objeción, Ángulo, Tono poblados"
  winner_score_calculado: "fórmula aplicada y ranking generado"
  top_3_por_keyword: "entregable ejecutivo listo para CEO"
  trigger_f4: "CEO lanzó al menos 1 campaña y tiene resultados preliminares"

F4_done_when:
  pipeline_cloud: "script corriendo en Render/Koyeb con heartbeat automático"
  db_persistente: "Supabase con schema v2.0 migrado"
  dashboard_minimo: "Vercel con filtros por keyword y ballena"
  zero_touch_test: "72h de autonomía continua verificadas (Principio 9)"
  health_endpoint: "/health activo y monitoreado por UptimeRobot"
  documentacion: "MASTER-PLAN.md actualizado + prompts archivados"
```

---

## 5. Triggers de Transición

**F0 → F1** (activa cuando se cumplen TODOS):

- ✅ `parser_meta_ads_universal.py` creado y sin errores
- ✅ Probado con al menos 1 TXT real (NaturaVida / Moringa)
- ✅ Schema v2.0 con todas las columnas pobladas correctamente
- ✅ CEO confirma que el parser es agnóstico (funciona en distintas industrias)
- ✅ Sección 9 (Evals) completada

**Acción CEO F0→F1:** Di **"F0 cumplida, paso a F1"** y trae 3 TXTs de keywords distintas.

---

**F1 → F2** (activa cuando se cumplen TODOS):

- ✅ 3 keywords procesadas sin errores de parsing
- ✅ Filtro de Ballenas aplicado (Days_Active ≥ 7, Creative_Variants ≥ 2)
- ✅ Ballena_Score calculado y Top 10 exportado por keyword
- ✅ CEO selecciona Top 3-5 ballenas para infiltrar

**Acción CEO F1→F2:** Di **"F1 cumplida, ballenas seleccionadas"** + lista de fanpages elegidas.

---

**F2 → F3** (activa cuando se cumplen TODOS):

- ✅ Catálogo oculto mapeado para cada ballena infiltrada
- ✅ Embudos identificados (% por tipo)
- ✅ Tabla comparativa de precios y ofertas cruzadas completada
- ✅ Dataset consolidado validado por CEO

**Acción CEO F2→F3:** Di **"F2 cumplida, dataset listo para IA"**.

---

**F3 → F4** (activa cuando se cumplen TODOS):

- ✅ IA analizó todos los copies del dataset consolidado
- ✅ Winner Score calculado con ranking generado
- ✅ Top 3 por keyword entregados al CEO como reporte ejecutivo
- ✅ CEO lanzó ≥ 1 campaña con ángulos validados y tiene resultados

**Acción CEO F3→F4:** Di **"F3 cumplida, validé en mercado, listo para escalar"**.

---

## 6. Prompts de Arranque Pre-escritos

> 💡 **Instrucción:** En cada nuevo chat, pegar primero el **HIDATA Method v1.4** completo, luego el prompt de la fase correspondiente. El asistente retoma el rol de Staff Engineer 100x con ADN completo.

---

### 🔹 Prompt F0 — Parser Universal de Meta Ads (EL CORAZÓN)

```text
Actúa como Senior Data Engineer experto en scraping de Meta Ads Library.

CONTEXTO:
Tengo un archivo .txt copiado manualmente de la Meta Ads Library. El formato SIEMPRE contiene bloques con esta estructura (puede variar el idioma pero la estructura es la misma):

---
Activo
Identificador de la biblioteca: [NÚMERO]
En circulación desde el [DD MMM AAAA]
Plataformas
[POSIBLEMENTE "Número de impresiones bajo/alto"]
[N] anuncios usan este contenido y texto
[Nombre Fanpage]
[Nombre Fanpage]
Publicidad
[TEXTO DEL COPY COMPLETO]
[POSIBLE DURACIÓN: MM:SS / MM:SS]
---

OBJETIVO:
Genera un script Python (pandas + regex) AGNÓSTICO a la industria.
Debe funcionar para CUALQUIER keyword (producto, servicio, real estate, etc.).

REQUISITOS:
1. Leer el archivo .txt desde "data/meta_ads_raw/{keyword}_raw.txt"
2. Dividir en bloques usando "Identificador de la biblioteca:" como ancla infalible
3. Por cada bloque extraer:
   - Fanpage: última línea válida antes de "Publicidad" (excluir: Plataformas, Activo,
     Identificador, En circulación, Número de impresiones)
   - Ad_ID: número después de "Identificador de la biblioteca:"
   - Start_Date: fecha después de "En circulación desde el"
   - Days_Active: calcular desde hoy (meses en español: ene, feb, mar, abr, may, jun,
     jul, ago, sep, oct, nov, dic)
   - Creative_Variants: número antes de "anuncios usan este contenido" (default 1)
   - Impressions_Level: "Bajo" / "Alto" / "Normal" según texto presente
   - Format: "Video" si hay patrón MM:SS / MM:SS, sino "Imagen"
   - Duration: el segundo tiempo MM:SS si existe
   - Embudo: "WhatsApp" si wa.me/WhatsApp, "Web" si http, "Formulario" si formulario,
     sino "Otro"
   - Oferta: regex para "2x1", "S/\d+", "USD \d+", "% OFF", "Gratis"
   - Copy_Completo: todo el texto entre "Publicidad" y la duración/número de impresiones
4. Guardar en "output/radar/bd_meta_ads_{keyword}.csv" con encoding utf-8-sig
5. Imprimir primeras 5 filas para validar
6. Manejar errores gracefully (try/except por bloque, log de bloques fallidos)
7. Al final: imprimir "Bloques detectados: X | Bloques parseados: Y | Fallos: Z"
8. Código robusto, comentado, listo para producción

NO hardcodees ninguna industria. El parser debe ser UNIVERSAL.
```

---

### 🔹 Prompt F1 — Filtro de Ballenas

```text
Actúa como Data Scientist. Tengo un CSV "bd_meta_ads_{keyword}.csv" con resultados del Radar.

Genera script Python que:
1. Lea el CSV
2. Aplique filtro de Ballenas:
   - Days_Active >= 7 (Scaler confirmado)
   - Creative_Variants >= 2 (creative testing validado)
3. Agrupe por Fanpage_Name y calcule:
   - total_ads_por_fanpage
   - avg_days_active
   - max_creative_variants
4. Cree "Ballena_Score" = (total_ads * 0.4) + (avg_days * 0.3) + (max_variants * 0.3)
5. Ordene descendente y guarde Top 10 en "output/infiltracion/ballenas_{keyword}.csv"
6. Imprima Top 5 con sus métricas
7. Registre timestamp de ejecución en "output/ejecuciones_log.csv" (heartbeat manual)
```

---

### 🔹 Prompt F2 — Parser de Infiltración (Fanpage Completa)

```text
Actúa como Senior Data Engineer. Tengo un TXT completo del perfil de un anunciante
infiltrado en Meta Ads Library (nombre: {fanpage_name}).

OBJETIVO:
Genera script Python que extraiga del TXT completo:
1. Lista de productos/servicios detectados (front-end visibles y back-end inferidos)
2. Tipos de embudo presentes (WhatsApp, Web, Landing, Formulario, DM) con % de cada uno
3. Rangos de precios y patrones de oferta detectados
4. Ángulos de venta dominantes (salud, ahorro, urgencia, autoridad, etc.)
5. CTAs más frecuentes
6. Ads activos vs inactivos: ratio de actividad

Guardar en "output/infiltracion/reporte_{fanpage_name}.csv"
Output: 1 fila por producto/servicio detectado, con columnas para cada punto anterior.
Registrar timestamp en "output/ejecuciones_log.csv".
```

---

### 🔹 Prompt F3 — Análisis IA de Copies + Winner Score (Agnóstico)

```text
Actúa como experto en Marketing Directo y Psicología de Ventas.
Lee el CSV "bd_meta_ads_{keyword}.csv", columna Copy_Completo.

Para CADA copy, devuelve un objeto JSON con:
- Hook_Principal: primeras 1-2 líneas que captan atención
- Pain_Point: problema emocional/físico/financiero que ataca
- Objection_Killed: objeción que mata (precio, confianza, tiempo, resultados)
- Sales_Angle: salud, estética, ahorro, urgencia, autoridad, estatus, miedo
- Tone: agresivo, educativo, empático, científico, humorístico
- Target_Audience: perfil inferido (edad, género, situación)
- CTA_Type: qué acción pide (comprar, agendar, descargar, contactar)
- Winner_Score: puntuación 0-100
  Pesos: Hook 30% · Pain_Point 25% · Objection_Killed 20% · Sales_Angle 15% · CTA 10%

Guardar resultado en "output/reportes_ia/analisis_copies_{keyword}.json"
Devolver SOLO JSON válido. Sin preamble, sin backticks, sin explicaciones.
```

---

## 7. Backlog de Visión (Postergado Conscientemente)

- Integración con TikTok Creative Center
- Scraping automatizado con Playwright stealth + proxies rotativos (F4)
- API REST para consumir desde dashboard externo
- Alertas WhatsApp cuando competidor lanza nuevo anuncio (Evolution API)
- Multi-usuario con billing (SaaS comercial)
- Integración con Google Trends para sugerencia de keywords
- Histórico de anuncios: tracking de cambios de copy over time
- Competitor benchmarking automático (delta semanal)
- Integración con Meta Ads Manager para lanzar campañas directamente
- Módulo de recomendación de ángulo ganador por industria (cross-keyword)

---

## 8. Decisiones Arquitectónicas Archivadas

### DA-001 — Ejecución Local (F0-F3) vs Cloud-Native (Principio 2)

**Decisión:** F0-F3 ejecutan en entorno local (Python + CSV). F4 migra a Render + Supabase.
**Rationale:** Validar el modelo de datos antes de invertir en infraestructura. Zero-friction para MVP. El código local es 100% portable a cloud sin modificaciones de lógica de negocio.
**Consecuencia:** Principio 9 (Zero-Touch 24/7) no aplica hasta F4. El test de autonomía de 72h es obligatorio antes de producción en F4.
**Deuda técnica documentada:** La migración a cloud en F4 requiere añadir `/health`, heartbeat automático en Supabase y UptimeRobot.

---

### DA-002 — Granularidad: 1 fila = 1 Clúster de Copy (Principio 10)

**Decisión:** La BD tiene una fila por grupo de anuncios que comparten el mismo copy, no por anuncio individual.
**Rationale:** Meta agrupa ads por COPY, no por visual. 5 visuales + 1 copy = 5 anuncios en la UI = 1 fila en BD. `Creative_Variants` es la señal de escalamiento horizontal (Lección #6).
**Consecuencia:** `Ad_ID_Representativo` es el ID del primer ad del clúster. `Creative_Variants` es el indicador de presupuesto real. La granularidad impacta directamente la calidad del filtro de Ballenas.

---

### DA-003 — Motor Horizontal vs Herramienta Vertical (Principio 1)

**Decisión:** WinnerRadar es un motor agnóstico de keywords, no una herramienta para el catálogo Winner.
**Rationale:** Mercado direccionable x1000. El parser agnóstico tiene mayor ROI que el parser especializado (Lección #5).
**Consecuencia:** Todo código se testa con ≥ 3 industrias distintas antes de declarar F0 completa. Dogma: Radar → Filtrar → Infiltrar. El orden no se negocia (Lección #4).

---

### DA-004 — TXT Manual vs API Oficial de Meta Ads (Principio 8, Anexo I)

**Decisión:** No usar la API oficial de Meta Ads Library.
**Rationale:** La API oficial solo sirve para anuncios políticos y mercados UE/Brasil. Para Perú/Latam comercial: inútil (Lección #7). Decisión validada con Anexo I (Stack de 4 Capas).
**Alternativa F4:** Reverse engineering de la UI vía Playwright stealth + proxies rotativos.
**Consecuencia:** F0-F2 son procesos manuales. F4 automatiza la ingesta. El parser (congelado en F0) es el puente entre ambas fases.

---

### DA-005 — Qoder CN (Qwen-Coder 32B) como Cerebro IA (Principio 6)

**Decisión:** Qwen-Coder 32B+ vía Alibaba Cloud ($1 USD de retención) en lugar de Gemini 2.5 Flash (default HIDATA).
**Rationale:** Acceso completo a Qoder CN con inversión mínima. Capacidad de reasoning complejo para código robusto (Lección #3). ROI 1000x sobre alternativas inferiores.
**Fallback:** Scripts Python 100% locales no dependen de Qoder CN en runtime. La IA es solo para generación (F0) y análisis (F3). Código generado es independiente de la IA que lo generó.
**Revisión en F4:** Evaluar migración a Gemini 2.5 Flash para análisis cloud (Principio 6: stack gratuito por defecto).

---

### DA-006 — Congelamiento del Parser en F0 (Principio 10 — Design for Change)

**Decisión:** Una vez validado en F0, `parser_meta_ads_universal.py` se congela. Cero código nuevo de parsing después.
**Rationale:** El parser es el componente de más alta rotación potencial. Congelarlo elimina deuda técnica y protege la estabilidad del pipeline completo.
**Consecuencia:** Si Meta cambia el formato del TXT, se crea `parser_meta_ads_v2.py` en paralelo, no se modifica el original. El sistema es inmutable por diseño.

---

## 9. Evals y Datos de Negocio (5 Preguntas CEO)

> ⚠️ **El CEO debe responder estas preguntas antes de ejecutar F1.** Las respuestas se guardan en `data/keywords/evals_parametros.json` y calibran los parámetros del sistema.

**Q1 — Volumen de extracción:**
¿Cuántos bloques de anuncios puedes copiar manualmente de Meta Ads Library en 30 minutos?
*(Calibra el tamaño óptimo del batch por sesión. Determina si necesitamos Playwright antes de F4.)*

**Q2 — Umbral de Ballena (tiempo):**
¿Cuántos días activo necesita un anuncio para que lo consideres "Ballena confirmada" según tu experiencia como media buyer?
*(Valida o ajusta el parámetro `Days_Active >= 7` del Filtro de Ballenas)*

**Q3 — Umbral de Ballena (creative testing):**
¿Cuántas variantes creativas mínimas son señal de que un anunciante está haciendo A/B testing serio en Latam?
*(Valida o ajusta el parámetro `Creative_Variants >= 2` del Filtro de Ballenas)*

**Q4 — Keywords del Batch 001:**
¿Cuáles son las 3 keywords exactas que procesarás en F1?
*(Formato sugerido: 1 producto físico + 1 servicio + 1 tendencia o Real Estate)*

**Q5 — Criterio Winner Score:**
En tu experiencia, ¿qué elemento de un copy es el más predictivo de conversión alta en tus nichos?
*(Calibra los pesos de la fórmula: Hook 30% · Pain 25% · Objection 20% · Angle 15% · CTA 10%)*

---

## 10. Resilient Integration Patterns (Anti-Ban)

*Adaptado del HIDATA Method v1.4, Principio 8. Separado por fase de madurez del sistema.*

### F0-F3 — Fase Manual

| Regla | Implementación | Verificación |
|:------|:---------------|:-------------|
| **Rate Limiting Manual** | Máx. 10 búsquedas/hora en Meta Ads UI | Log manual en `output/ejecuciones_log.csv` |
| **Fingerprint Rotation** | User-Agents distintos por sesión de navegador | Validación visual: distintos perfiles/navegadores |
| **Circuit Breaker Manual** | Si aparece CAPTCHA → pausa mínima 30 min | Alerta directa al CEO. No reintentar antes |
| **Heartbeat de Ejecución** | Log de timestamp + keyword + filas parseadas por script | Columnas: `timestamp, keyword, bloques_total, bloques_ok, fallos` |
| **Fallback a IA** | Si regex falla en un bloque → IA re-procesa el bloque raw | Métrica de fallos < 5%. Bloques fallidos se loguean para revisión |
| **Validación post-parse** | Imprimir: bloques detectados vs parseados vs fallidos | Diferencia > 10% = señal de alerta de cambio de formato |

### F4 — Fase Automatizada (Pendiente)

| Regla | Implementación | Verificación |
|:------|:---------------|:-------------|
| **Exponential Backoff** | Reintentos con espera 2^n seg, máx. 10 intentos, jitter aleatorio | Simular caída de scraper y medir tiempos de recuperación |
| **Respetar Retry-After** | Si el servidor envía `Retry-After`, el bot duerme exactamente ese tiempo | Log del header recibido en cada 429 |
| **Circuit Breaker** | 5 fallos consecutivos → estado "abierto" 5 min → "half-open" | Estado visible en dashboard Vercel |
| **Playwright Stealth** | Headers rotativos, delays aleatorios, fingerprint evasión | Test: el scraper no activa detección de bot en Meta |
| **Alerta Anti-ban** | UptimeRobot monitorea logs; alerta si detecta 429 frecuentes | Notificación WhatsApp vía Evolution API en < 5 min |
| **Heartbeat cada 5 min** | Insert automático en tabla `heartbeats` de Supabase con timestamp | Consulta SQL: `SELECT MAX(ts) FROM heartbeats` |
| **Alerta proactiva de caída** | UptimeRobot monitorea `/health`. Si falla > 10 min → WhatsApp | Alerta recibida en < 5 min. SLA documentado |
| **Dashboard de salud** | Panel Vercel: último heartbeat, uptime, ads/hora procesados, errores | Accesible desde cualquier navegador sin autenticación |

### Checklist de Selección de Plataforma (Principio 9 — Obligatorio en F4)

| Criterio | Estado F0-F3 | Plan F4 | Regla de Decisión |
|:---------|:-------------|:--------|:------------------|
| ¿Garantiza ejecución continua sin dormir? | ❌ Local/Manual | Render (paid) o Koyeb (free) | Leer ToS antes de elegir |
| ¿Supera test de autonomía 72h? | ❌ N/A | Prueba empírica obligatoria | Sin test = no va a producción |
| ¿WebSocket nativo sin proxies? | N/A | N/A (HTTP scraping) | No aplica en WinnerRadar |
| ¿IP estable o rotativa documentada? | ✅ Local estable | Proxies rotativos documentados | Documentar en arquitectura F4 |
| ¿Límites de uso claros y predecibles? | ✅ Sin límites local | Verificar plan Render/Koyeb | Documentar en Mapa de Riesgos F4 |

---

## 11. Mapa de Riesgos Red Team

| Riesgo | Prob | Impacto | Mitigación |
|:-------|:-----|:--------|:-----------|
| Meta bloquea comportamiento bot | Media | Crítico | F0-F2 manual. F4: Playwright stealth + proxies rotativos + rate limiting + Circuit Breaker |
| Parser falla con nuevo formato TXT | Alta | Alto | Regex con fallback a IA. Logging de bloques fallidos. Alerta si fallos > 10% |
| Cambios en UI de Meta Ads Library | Media | Alto | Parser basado en anclas estructurales ("Identificador de la biblioteca:"), no en selectores HTML |
| Time-to-market presiona y se saltan DoD | Alta | Crítico | DoD binario. No avanzar sin todas las métricas cumplidas. CEO firma cada trigger de transición |
| Dependencia Qoder CN / Alibaba Cloud | Baja | Medio | Scripts Python 100% locales en runtime. IA solo para F3. Código generado es independiente |
| Keywords ambiguas o multi-industria | Media | Medio | Contexto manual por keyword en F1. Campo de descripción de nicho en `evals_parametros.json` |
| Dataset F3 con copies en otro idioma | Baja | Medio | Prompt F3 funciona en español e inglés. Añadir campo `idioma` al schema v2.0 si aplica |
| Alta rotación del código del parser | Media | Alto | Principio 10: parser se congela en F0 (DA-006). Cero código nuevo de parsing después de F0 |
| Plataforma 24/7 se duerme en F4 | Alta | Crítico | Principio 9: checklist de selección obligatorio. Heartbeat + UptimeRobot + test de 72h antes de producción |
| Variables de entorno expuestas en F4 | Baja | Crítico | Principio 2: secretos solo en PaaS (Render env vars). Nunca en repo ni en código |

---

## 12. Lecciones Aprendidas (Registro Vivo)

### #1 — 2026-06-20 — PDF con fuentes corruptas

**Problema:** `pdfplumber` extraía `(cid:)` y letras duplicadas en el catálogo Winner.
**Causa raíz:** PDF sin mapa Unicode (PDF de imagen, no nativo).
**Solución:** OCR con Tesseract + limpieza heurística.
**Impacto ADN:** Siempre validar si un PDF es nativo o imagen antes de elegir la librería de extracción. Aplicar Stack de 4 Capas (Anexo I): playground antes de codificar.

---

### #2 — 2026-06-20 — Precios inflados (2200.0 vs 22.00)

**Problema:** PDF omitía el punto decimal en precios del catálogo.
**Causa raíz:** Formateo no estándar del PDF fuente.
**Solución:** Regla de normalización automática: dividir entre 100 valores > 500.
**Impacto ADN:** Toda ingesta de precios requiere validación de rango esperado. Incluir en `utils/validacion.py`.

---

### #3 — 2026-06-20 — Inversión mínima desbloquea herramienta premium

**Problema:** Qoder CN (Qwen-Coder 32B) exigía tarjeta de crédito en Alibaba Cloud.
**Solución:** CEO invirtió $1 USD de retención.
**Impacto ADN:** ROI estimado 1000x (100+ horas de trabajo manual ahorradas). Regla: antes de descartar una herramienta premium por fricción, verificar si hay una inversión mínima que la desbloquea (DA-005).

---

### #4 — 2026-06-20 — El orden de los movimientos altera la rentabilidad

**Problema:** La intuición llevaba a empezar directamente por Infiltración sin filtrar primero.
**Causa raíz:** "Ir al dato rico" sin priorizar es ruido, no señal.
**Solución:** Dogma establecido: Radar → Filtrar Ballenas → Infiltrar. El orden es parte del método.
**Impacto ADN:** Los Dos Movimientos son inmutables. No se negocian (DA-003, Sección 1).

---

### #5 — 2026-06-20 — Pivot a Motor Horizontal

**Problema:** Enfoque inicial en catálogo Winner (120 productos) limitaba el mercado.
**Causa raíz:** Visión táctica, no estratégica. Herramienta vs. plataforma.
**Solución:** CEO identificó que el verdadero valor es el **Motor Universal** de análisis de keywords.
**Impacto ADN:** WinnerRadar pasó de herramienta a SaaS de inteligencia comercial. Mercado direccionable x1000 (DA-003). Refuerza Principio 1 HIDATA: la arquitectura y el negocio son el producto.

---

### #6 — 2026-06-20 — Granularidad: clúster de copy, no anuncio individual

**Problema:** Confusión entre cantidad de anuncios totales vs. copys únicos en Meta Ads Library.
**Causa raíz:** Meta agrupa ads por COPY en su UI. 5 visuales + 1 copy = 5 anuncios = 1 clúster.
**Solución:** 1 fila en BD = 1 Clúster de Copy. `Creative_Variants` captura el escalamiento horizontal real.
**Impacto ADN:** La granularidad de la BD impacta directamente la calidad del Filtro de Ballenas y del Winner Score (DA-002).

---

### #7 — 2026-06-20 — Meta Ads Library API Oficial no sirve para Latam comercial

**Problema:** Se evaluó la API oficial de Meta Ads Library como alternativa al copy-paste manual.
**Hallazgo:** Solo sirve para anuncios políticos o mercados UE/Brasil. Para Perú/Latam comercial: inútil.
**Solución:** Reverse engineering de la UI vía TXT copy-paste (F0-F3) y Playwright stealth (F4).
**Impacto ADN:** No depender de APIs oficiales cerradas. Construir parsers propios. Auditar siempre con Anexo I antes de integrar cualquier API (DA-004).

---

## 13. Anexo II Aplicado — Plataforma de Autoservicio (Estado: Pendiente F4)

*El patrón HIDATA Anexo II se activa cuando WinnerRadar escale a SaaS multi-usuario en F4.*

**Trigger de activación:** CEO valida demanda externa y define precio por keyword scaneada.

**Diseño preliminar de las 6 capas para F4:**

| Capa | Implementación WinnerRadar F4 |
|:-----|:------------------------------|
| **API de Aprovisionamiento** | FastAPI en Render: `POST /api/scan` con `{ keyword, industry_hint }` |
| **Cola Asíncrona** | Supabase Realtime + tabla `jobs` para encolar scraping jobs |
| **Plano de Control** | Worker Python: lee `jobs`, aplica Filtro de Ballenas, dispara análisis IA, escribe resultados |
| **Plano de Datos** | Playwright scraper + `parser_meta_ads_universal.py` (congelado desde F0) |
| **Infraestructura** | Render (worker 24/7) + Supabase (BD) + Vercel (dashboard) |
| **Dashboard de Autoservicio** | Vercel: tabla por keyword, ballenas detectadas, Winner Score, estado del job |

**Principios de diseño a respetar en F4:**
- El parser de F0 es el plano de datos inmutable. No se toca.
- Los jobs se validan en el plano de control antes de ejecutar (cero scrapes sin validación previa).
- Cada job emite heartbeat. Cualquier job sin heartbeat > 10 min genera alerta.
- El dashboard es legible por el CEO sin soporte técnico.

---

## ANEXO I — Stack de 4 Capas: Meta Ads Library como Fuente de Datos

*Aplicación del patrón HIDATA Anexo I al ecosistema de WinnerRadar.*

### Las 4 Capas Aplicadas

| Capa | Herramienta WinnerRadar | Función |
|:-----|:------------------------|:--------|
| **1. API / Fuente de Datos** | Meta Ads Library UI (manual F0-F3) · Playwright stealth (F4) | Autopista de datos. Acceso a anuncios activos de cualquier anunciante en Latam sin las restricciones de la API oficial |
| **2. Playground** | La propia UI de Meta Ads Library + Network Tab del navegador | Validación inmediata. El CEO prueba keywords, filtros y patrones antes de que el parser los formalice. Reduce prototipado de días a minutos |
| **3. Automatización Nativa** | ❌ No disponible para Latam comercial (Lección #7) | Ventaja competitiva: no existe solución "drag & drop" en este mercado. WinnerRadar llena ese vacío |
| **4. AI Hub** | Qoder CN (Qwen-Coder 32B) vía Alibaba Cloud | Acelerador de desarrollo. Genera parser, filtro de Ballenas y análisis de copies. $1 USD → herramienta de nivel unicornio |

### Contingencias (Anti-Frágil)

| Si Meta no tiene… | WinnerRadar usa… |
|:------------------|:-----------------|
| API oficial para Latam | Reverse engineering de UI. TXT copy-paste. Parser propio congelado en F0 |
| Playground técnico documentado | La UI de Meta Ads Library es nuestro playground. Network Tab para inspección profunda |
| Automatización nativa abierta | Playwright stealth + proxies rotativos en F4. Ventaja: somos los primeros en Latam |
| Documentación de estructura TXT | Ingeniería inversa de los patrones del TXT exportado + regex inductivo |

### Ventaja Competitiva

El Stack de 4 Capas aplicado a Meta Ads Library permite a WinnerRadar:
- **Auditar** un nicho completo en < 30 minutos (manual F0-F3) o < 5 minutos (F4 automatizado)
- **Generar** análisis competitivo de IA en segundos sobre cualquier keyword de Latam
- **Diseñar** campañas superiores basadas en lo que el mercado ya validó con presupuesto real

Es la diferencia entre un media buyer que analiza a mano y una consultora que opera con método de inteligencia repetible.

---

> **CEO, este es nuestro contrato de ejecución blindado con el ADN HIDATA completo.**
> 10 Principios · 13 Secciones · Anexo I · Anexo II · RIP Matrix · Red Team · Design for Change.
> Cero distracciones. Cero over-engineering. Solo fases medibles, outputs accionables y velocidad de mercado.

## 🎯 TU PRIMERA ACCIÓN

1. Responde las **5 preguntas de la Sección 9** → guarda en `data/keywords/evals_parametros.json`
2. Crea la estructura de carpetas (Setup Inicial, Sección 3)
3. Abre Qoder CN
4. Pega el **Prompt F0** (Sección 6)
5. Pruébalo con el TXT de NaturaVida
6. Di **"F0 cumplida, paso a F1"**

---

*El radar está encendido. El ADN HIDATA corre en nuestras venas. El imperio espera.* 📡🔥

**Vamos por el número uno de Latinoamérica.**
