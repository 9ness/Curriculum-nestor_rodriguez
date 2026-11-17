# Logros y proyectos para el CV

> Destilado de `~/proyectos/consultas-nestor/habilidades.md` y de los repos. Lo mantiene
> el agente del CV (ver AGENTS.md §7). Una entrada por proyecto: qué es, qué demuestra
> para una empresa, tecnologías, fechas, ¿está ya en el CV?

## Proyectos

- **TikTok Factory (TikTok_Automation_Python)** · dic 2025 → hoy · en solitario. SaaS multiusuario
  FastAPI (~140.000 líneas Python, 35 routers) + Next.js; cola de trabajos propia; orquesta Claude,
  Gemini, OpenAI, voz y vídeo con respaldo; servidor MCP de 60 herramientas; coste por llamada;
  despliegues de 30 min a segundos; migración de Drive en producción (150 GB, 6.700 rutas Redis).
  Demuestra: backend asíncrono, IA en producción, agentes, DevOps. **En el CV:** sí (Proyectos propios).
- **MasterPicks (bet-ai-master)** · dic 2025 → hoy. SaaS con suscripciones (web + Play Billing),
  pipeline de Claude con modelos en sombra y validador, caché de prompt, 28 workflows en GitHub
  Actions, almacén DuckDB, SEO i18n; 339 registrados (sep 2026). Demuestra: LLM en producción,
  evaluación A/B, pagos. **En el CV:** sí.
- **Plataforma de asistentes y agentes (Mi Dot, asistentes-telegram, panel-agentes, alexa-claude)** ·
  oct 2026 → hoy. Pasarela MCP multiusuario denegar-por-defecto, cadena Codex→OpenCode→Claude por
  cuota, memoria persistente en ficheros, OAuth Calendar, skill Alexa, observabilidad de agentes.
  Demuestra: arquitectura de agentes multi-tenant y seguridad de herramientas. **En el CV:** sí.
- **Rumbo (planificador-viajes)** · jun 2026 → hoy. PWA + APK, tickets con IA (Gemini Vision,
  Claude Haiku), MCP remoto, 289 tests + e2e que destaparon 3 fallos de seguridad. **En el CV:** mención.
- **Fit9ness (fitness-life)** · jun 2026 → hoy. Android + web, plugin Kotlin Health Connect,
  migración Gemini→Claude por evaluación. **En el CV:** mención.
- **Forja (app de gimnasios)** · nov 2026. Postgres con Row Level Security multi-gimnasio, triggers
  concurrentes, 165 tests + mutación, RGPD. **En el CV:** mención.
- **Editor Auto / Nebulabs Media** · jun 2026 → hoy. SaaS de edición de vídeo con IA, créditos,
  JWT entre Vercel y servidor, banco de evaluación de 20 métodos de limpieza de voz.
  **En el CV:** no (de reserva para ofertas de vídeo/IA multimodal).
- **Escáner IA de pisada (Shopify)** · may-ago 2025. OpenAI Vision en tienda real. **En el CV:** no.

## Para entrevista (no caben en el CV)
- A/B Sonnet→Haiku en guiones: 5-10x menos coste, 8/8 dentro del tope, ~55 % del gasto mensual de API.
- Despliegues: uvicorn esperando WebSockets + pool de hilos saturado por E/S de Drive → segundos.
- MCP: enlaces de descarga firmados con HMAC 24 h; test de deriva entre herramientas y documentación.
- Flota de agentes: relevo automático de chats por contexto, freno por cuota, rutinas por cron.

Última revisión: 2026-11
