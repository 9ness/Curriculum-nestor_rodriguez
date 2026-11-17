# Néstor Rodríguez Tubío
### Desarrollador Backend Senior · Java, Seguridad & IA Generativa / Agentes

📍 Padrón (A Coruña), Galicia · Remoto · ✉️ ness4b@gmail.com · 📱 638 412 999 · 💼 [LinkedIn](https://www.linkedin.com/in/néstor-rodríguez-tubío-6914a7171) · 🐙 [github.com/9ness](https://github.com/9ness) · 🌐 [curriculum-nestor-rodriguez.vercel.app](https://curriculum-nestor-rodriguez.vercel.app)

---

## Perfil

Desarrollador backend senior con **más de 6 años de experiencia** en **Java (Spring Boot, Java EE)** sobre microservicios y monolitos en **WebLogic y Oracle**, en banca, administración pública, ámbito judicial, automoción y sanidad. Trabajo la **seguridad de aplicaciones** (remediación de vulnerabilidades de **SonarQube**: inyección SQL, SSL/TLS, XXE) y la **firma electrónica**. Desde 2024 llevo **IA generativa a producción**: **dos SaaS propios en uso real** con LLM de varios proveedores (Claude, OpenAI, Gemini, DeepSeek), **servidores MCP** para que **agentes de IA** operen esos productos, **elección de modelos por pruebas A/B** con coste medido por llamada, y una **flota de agentes** (Claude Code, Codex) que gestiono en mi propio servidor con Docker, CI/CD y observabilidad.

---

## Tecnologías

**Backend:** Java · Spring Boot · Spring Cloud · Spring Security · JPA / Hibernate · JSF / PrimeFaces · EJB · Servicios SOAP · API REST · Python (FastAPI)
**Arquitectura:** Microservicios · Eureka · Ribbon · RabbitMQ · Docker · Weblogic · Wildfly
**IA / Agentes:** Integración de LLM en producción (Claude, OpenAI, Gemini, DeepSeek) · Agentes de IA y servidores MCP · Orquestación multiagente (Claude Code, Codex) · Evaluación A/B de modelos y control de coste · Salidas estructuradas (JSON Schema), validadores y caché de prompt · IA multimodal (visión, Whisper) · Ingeniería de prompts
**Bases de datos:** Oracle · SQL Server · MySQL · MongoDB · SAP HANA
**Seguridad:** SonarQube · OWASP · SSL/TLS · Inyección SQL · XXE · Firma electrónica
**Cloud & DevOps:** Docker / Compose · CI/CD (GitHub Actions, webhooks) · Linux / VPS propio (systemd, Caddy) · Redis · Vercel · AWS · Git · Maven · Gradle · Jira · SAP BTP
**Testing:** JUnit · Mockito · pytest · Vitest · Playwright · SOAPUI · TestLink
**Frontend:** Next.js · React / Redux · TypeScript · JavaScript · JSP/XHTML · HTML/CSS

**Años por tecnología (a noviembre 2026):** Java (6a 1m) · Microservicios (4a 6m) · Spring Boot (3a 8m) · IA aplicada (2a 10m) · Integración de APIs de IA (2a 8m)

---

## Experiencia profesional

### Desarrollador Backend — Ayesa · Sevilla (en remoto)
**Ene 2023 – Actualidad**

**Plataforma de facturación electrónica para una entidad bancaria** · Sep 2026 – Actualidad
- Remedié vulnerabilidades detectadas por **SonarQube** en una plataforma con más de 100 repositorios Java (WebLogic, Oracle): **inyección SQL** en JDBC, validación de certificados **SSL/TLS**, **XXE** y otras.
- Analicé y justifiqué ante el cliente los falsos positivos, con documentación técnica de cada caso.
- Inventarié las integraciones con terceros que no validaban certificados (incluidas varias que el análisis automático no detectaba) y definí el patrón común de corrección (TLS 1.2 con el truststore de la JVM).
- Estimé y planifiqué las correcciones críticas y coordiné con sistemas el despliegue sin cortar conexiones en producción.
- *Stack:* Java · JDBC · SonarQube · SSL/TLS · WebLogic · Oracle · Maven · Git

**Portal de empleo público · Junta de Andalucía** · Abr 2025 – Actualidad
- Desarrollé de principio a fin la solicitud y adjudicación de plazas (acceso libre y bolsa): formulario reutilizable, PDF, **firma electrónica**, registro telemático e integración con el sistema de RR. HH.
- Rediseñé la custodia documental multi-entorno del microservicio de gestión documental: una sola columna en lugar de cambios en 19 tablas, y cerré un riesgo de borrado cruzado entre preproducción y producción.
- Migré la configuración por entorno de Maven a base de datos para generar un único WAR para los 4 entornos.
- Resolví la mezcla de logs entre dos aplicaciones en el mismo WebLogic y recuperé las trazas que se perdían en 732 puntos del código.
- Unifiqué los filtros de 66 pantallas con herramientas propias en Python que validan cada cambio.
- *Unos 285 commits en 5 repositorios y más de 50 tareas.* *Stack:* Java 8 · JSF/PrimeFaces · EJB · JPA · REST (Jersey) · Spring Boot 3 · Oracle PL/SQL · iText 7 · WebLogic 12.2 · Podman

**Proyectos Java/SAP · Junta de Andalucía** · Ene 2023 – Mar 2025
- Microservicios Java con **Spring Boot** integrando el ecosistema **SAP** (BTP Cockpit, SAP HANA Cloud, SAP Logon).
- Lectura, validación y procesamiento de archivos CSV con persistencia en base de datos.
- Desarrollo full-stack (XHTML/JSP + JavaScript) sobre **WebLogic**, **Oracle** y **MongoDB**.
- *Stack:* Java · Spring Boot · Microservicios · SAP HANA · MongoDB · Oracle · Docker · AWS · JUnit · Mockito

### Desarrollador Backend — Indra (vía Soltel) · Sevilla
**Nov 2021 – Dic 2022**
- Backend en **microservicios Java** para el ámbito judicial: gestión de juicios y reservas de salas.
- Desarrollo de **servicios SOAP con Spring Boot** para el intercambio seguro de datos entre sistemas.
- Manejo de contratos WSDL y pruebas con SOAPUI.
- *Stack:* Java · Spring Boot · Microservicios · SOAP · WSDL · Oracle · Docker · Bitbucket

### Desarrollador Backend — Coremain · Santiago de Compostela
**Feb 2021 – Ago 2021**
- Nuevo proyecto Java para **Ford** basado en microservicios con Spring Boot (equipo de 5-6 personas).
- Arquitectura de microservicios con **Spring Cloud, Eureka, Ribbon** y mensajería con **RabbitMQ**.
- *Stack:* Java · Spring Boot · Spring Cloud · Hibernate · Eureka · Ribbon · RabbitMQ · Wildfly · SQL Server · Maven/Gradle · AWS

### Desarrollador de aplicaciones — Plexus Tech · Santiago de Compostela
**Oct 2019 – Jul 2020**
- Proyecto **SCCOM** para hospitales de toda España: desarrollo full-stack (Java backend + JavaScript/HTML/CSS/AJAX).
- Tres meses para el **Servicio Gallego de Salud (SERGAS)** desarrollando en **.NET/C#** en solitario; algunos proyectos siguen en producción.
- *Stack:* Java · Spring MVC/JPA · Hibernate · MySQL · .NET · C# · ASP.NET MVC · JavaScript

---

## Proyectos propios con IA (en producción)

**TikTok Factory · SaaS de automatización de vídeo con IA** · Dic 2025 – Actualidad
- SaaS multiusuario en solitario (**FastAPI** con ~140.000 líneas de Python + **Next.js**) que crea y publica vídeos cortos: guion con LLM, voz, subtítulos y montaje, con cola de trabajos propia por WebSocket.
- Orquesta **Claude, Gemini, OpenAI** y modelos de vídeo y voz con respaldo automático; coste de cada llamada por usuario y producto.
- Servidor **MCP** con 60 herramientas para que agentes hagan el trabajo de producción de punta a punta.
- Reduje los despliegues de 30 minutos de caída a segundos (Docker Compose, Caddy, CI/CD por webhook).
- *Stack:* Python · FastAPI · Next.js · Redis · Docker · Claude API · Gemini · MCP · FFmpeg · Whisper

**MasterPicks · SaaS de pronósticos deportivos con IA** · Dic 2025 – Actualidad
- Web y app Android con suscripciones de pago y agente conversacional de soporte; 339 usuarios registrados (sep 2026).
- Pipeline de predicción con la **API de Claude**: el modelo principal publica y otros corren en sombra con el mismo validador; caché de prompt y coste real por modelo en el panel.
- 28 flujos automatizados en GitHub Actions y almacén analítico con DuckDB.
- *Stack:* Next.js · TypeScript · Python · Anthropic SDK · Redis · GitHub Actions · Capacitor

**Plataforma de asistentes y agentes de IA** · Oct 2026 – Actualidad
- Asistentes de IA para varias personas (web, app Android y Telegram) sobre Claude Code, Codex y OpenCode, con **pasarela MCP multiusuario** que deniega por defecto y fija la identidad de cada usuario.
- Integraciones OAuth (Google Calendar) verificadas antes de confirmar cada acción y skill de Alexa con Claude Haiku.
- *Stack:* Python · asyncio · MCP · Claude API · OAuth 2.0 · Android

Otros: Rumbo (planificador de viajes con lectura de tickets por IA, servidor MCP remoto y 289 tests), Fit9ness (app Android + web con plugin nativo Kotlin), Forja (SaaS multi-gimnasio con PostgreSQL y Row Level Security).

---

## IA generativa y agentes en producción (desde 2024)

- Diseñé **servidores MCP** (hasta 60 herramientas, acceso por token firmado con HMAC) para que agentes de IA (Claude Code, Codex) operen productos reales con los mismos permisos que la web.
- **Elijo modelos con datos:** pruebas A/B «en la sombra» con casos reales y coste medido por llamada; p. ej., guiones pasados de Sonnet a Haiku con 5-10 veces menos coste y 8 de 8 guiones válidos en las pruebas.
- Integro varios proveedores (Claude, OpenAI, Gemini, DeepSeek) con **respaldo automático**, salida JSON con esquema, validadores con reintento y caché de prompt.
- Gestiono una **flota de agentes de IA** en servidor propio: reparto de tareas programadas, cambio de proveedor al agotarse la cuota, memoria persistente y panel de observabilidad de uso y coste.
- Llevé el **desarrollo asistido por agentes** a todos mis repositorios y evalué 3 modelos como agentes de programación sobre un proyecto en producción.

---

## Educación

**Ciclo Formativo de Grado Superior en Desarrollo de Aplicaciones Multiplataforma (DAM)** — 2017–2019
Bases de datos, desarrollo de interfaces, Java, JavaScript, HTML/CSS/XML y desarrollo Android.

---

## Otros datos relevantes

- 🚀 **Creador de filtros de realidad aumentada (Spark AR) para Instagram con +5.700 millones de visualizaciones acumuladas**, incluyendo scripts propios para funcionalidades personalizadas. *(Producto a escala masiva y autonomía técnica de principio a fin.)*
- Certificado validado de **React / Redux** (financiado por empresa).
- Diseño gráfico y motion (Photoshop, Cinema 4D) y edición de vídeo (Premiere, Sony Vegas, CapCut).
- Futbolista amateur — persona sociable y orientada al trabajo en equipo.

---

## Idiomas

**Español** (nativo) · **Gallego** (nativo) · **Portugués** (buena comprensión) · **Inglés** (intermedio)
