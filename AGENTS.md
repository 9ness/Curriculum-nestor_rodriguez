# AGENTS.md — Curriculum-nestor_rodriguez

> Manual de trabajo para agentes de IA (Claude Code / OpenCode) en este repo.
> Idioma de comunicación con el usuario: **ESPAÑOL**.

---

## Selección de modelo (auto-routing — hazlo ANTES de empezar la tarea)
Este proyecto trabaja con dos PERFILES, no con nombres fijos:
- Perfil PESADO (rol tipo "Opus": el potente) — mejor en ficheros enormes y tareas largas/multi-fichero.
- Perfil DIARIO (rol tipo "Sonnet": rápido y barato) — el de por defecto para tareas normales.

| Perfil | Modelo |
|---|---|
| PESADO | el modelo potente del usuario (él sabe cuál cargar) |
| DIARIO | el modelo rápido/barato del usuario (él sabe cuál cargar) |

Al recibir una tarea, clasifícala y avisa en UNA línea. Es PESADA si cumple CUALQUIERA:
- Localizar/modificar detalles en un fichero muy grande (> ~2000 líneas) o varios grandes.
- El cambio toca MÁS de ~3-4 ficheros o muchos call-sites.
- Tarea multi-paso larga (migración, barrido) de muchos turnos.
- Perder el hilo entre pasos tendría coste alto.
Si no, es LIGERA. Si es PESADA: di "Esta tarea es PESADA (motivo: …), usa el perfil PESADO
(ver tabla); si no lo tienes cargado, cámbialo antes de seguir." Si es LIGERA: procede sin avisar.
En ficheros de miles de líneas, si concluyes que algo "no existe", haz grep del nombre exacto antes de afirmarlo.

**Ficheros que casi siempre disparan PESADO aquí:** ninguno por tamaño — el fichero
más grande es `index.html` (~325 líneas). Aquí PESADO se dispara casi siempre por
*amplitud*: un cambio de estilo o de menú que toca a la vez `index.html`, `panel.html`,
`ofertas.html`, `seguimiento.html`, `preparacion.html` y `emails-cto.html` (cada página
lleva su CSS inline duplicado — ver Gotcha 4).

---

## 1. Resumen del proyecto

Sistema personal de búsqueda de empleo de Néstor Rodríguez Tubío (Backend Senior
Java + IA generativa). No es una app: es una **web estática desplegada en Vercel**
servida desde la raíz del repo, más un pequeño toolkit. La parte pública
(`index.html`) es el portafolio con descarga de CV y formulario de contacto; la
parte privada (`panel.html` y sus subpáginas) está protegida por contraseña con
un `middleware.js` de Vercel + dos funciones serverless en `api/`, y contiene el
seguimiento de candidaturas, ofertas con CV adaptado por empresa, guía de
preparación y emails a CTOs. La fuente de verdad de los datos del CV es
`cv/datos.json`: un script Python (`tools/generar_pdf.py`) lo renderiza a
`cv.pdf` + `cv-preview.png` con ReportLab, y puede generar variantes adaptadas a
una oferta concreta a partir de un `*.adapt.json`. `adaptador-cv/PROMPT.md` es el
prompt maestro que produce esas adaptaciones **sin inventar datos**.

**Stack:** HTML/CSS/JS estático (sin framework, sin bundler, sin `package.json`) ·
Vercel (Edge Middleware + Serverless Functions Node, formato `module.exports`) ·
Python 3 + ReportLab + PyMuPDF para el PDF · Web3Forms para el formulario de
contacto · GitHub (`master`) como disparador de despliegue.

---

## 2. Comandos reales

No hay build, ni tests, ni linter en este repo. Los únicos comandos reales son:

### Generar el CV en PDF (desde la raíz del repo)
```bash
pip install -r tools/requirements.txt      # reportlab>=4.0, pymupdf>=1.24

# CV base -> cv.pdf + cv-preview.png + cv/CV-Nestor-Rodriguez-Tubio.pdf
python tools/generar_pdf.py

# CV adaptado a una oferta -> cv/adaptados/<empresa>.pdf + .png
python tools/generar_pdf.py --adapt cv/adaptados/cas-training.adapt.json
```

### Ver la web en local (desde la raíz del repo)
```bash
python -m http.server 8000    # http://localhost:8000
```
Ojo: así **no** se ejecutan `middleware.js` ni `api/*.js` (son de Vercel), así que
el panel privado no pedirá contraseña y el login no funcionará en local.
PENDIENTE: confirmar si se quiere usar `vercel dev` (requiere Vercel CLI, no
instalada ni versionada en el repo).

### Desplegar
Push a `master` → Vercel redespliega solo. Detalle y checklist en
[`DESPLIEGUE.md`](DESPLIEGUE.md).

### Tests / lint
No existen. PENDIENTE: confirmar si se quieren añadir (hoy no hay `package.json`,
ni `.github/workflows/`, ni configuración de formateo Python o JS).

---

## 3. Arquitectura y directorios clave

```
(raíz)                     # la web se sirve DESDE AQUÍ (Vercel sin "Root Directory")
  index.html               # web pública: portafolio + descarga CV + formulario Web3Forms
  login.html               # formulario de contraseña -> POST /api/login
  panel.html               # panel privado: hub de enlaces + "Mis proyectos"
  ofertas.html             # ofertas + CV adaptado por empresa + enlace para aplicar
  seguimiento.html         # seguimiento de candidaturas
  preparacion.html         # guía de preparación de entrevistas
  emails-cto.html          # emails de contacto directo a CTOs
  middleware.js            # Edge Middleware Vercel: protege las páginas del panel
  vercel.json              # cleanUrls + Content-Disposition del cv.pdf
  cv.pdf, cv-preview.png   # GENERADOS por tools/generar_pdf.py — no editar a mano
api/
  login.js                 # POST: valida PANEL_PASSWORD y setea cookie panel_auth
  logout.js                # borra la cookie
cv/
  datos.json               # FUENTE DE VERDAD de todos los datos del CV
  cv-maestro.md            # CV maestro en Markdown
  cv.html                  # CV imprimible (abrir en navegador -> Guardar como PDF)
  CV-Nestor-Rodriguez-Tubio.pdf   # GENERADO
  adaptados/               # por empresa: <slug>.adapt.json (entrada) + .pdf/.png (generados) + .md
adaptador-cv/PROMPT.md     # prompt maestro para adaptar el CV a una oferta sin inventar
tools/
  generar_pdf.py           # ReportLab: datos.json -> PDF; --adapt para variantes
  requirements.txt
research/                  # empresas-y-ofertas.md, startups-ia-espana.md
freelance/perfil-freelancer.md
web/                       # VACÍO (restos de cuando la web no se servía desde la raíz)
```

**Flujo de datos del CV:** `cv/datos.json` (+ opcional `cv/adaptados/<slug>.adapt.json`)
→ `tools/generar_pdf.py` → PDF/PNG. Todo lo demás (HTML de las páginas) es contenido
escrito a mano.

**Contrato de `<slug>.adapt.json`** (lo consume `generar_pdf.py:build`):
`empresa`, `puesto`, `titular`, `perfil`, `cards`, `skills_order`, `checks[{req, estado}]`
con `estado ∈ {cumple, parcial, no}`. `skills_order` referencia claves de
`datos.json:skills` y sus etiquetas están mapeadas en el propio script.

---

## 4. Convenciones

- **Commits:** frase en **español, imperativo, sin prefijo tipo/scope** (NO se usa
  Conventional Commits). Ej.: `Añadir sección "Mis proyectos" al panel privado`,
  `Corregir dominio de Bet AI Master a masterpicksai.com`,
  `Actualizar URLs de proyectos en el panel con datos confirmados`.
- **Rama por defecto: `master`** (no `main`). Remote: `origin` →
  `github.com/9ness/Curriculum-nestor_rodriguez`. **Push a `master` despliega a
  producción en Vercel** — piénsalo antes.
- **Código:** HTML/CSS/JS vanilla, todo inline en cada página. Sin frameworks, sin
  build, sin dependencias npm. Las funciones de `api/` usan CommonJS
  (`module.exports`); `middleware.js` usa ESM (`export default`) porque corre en el
  Edge Runtime — no unifiques ese estilo.
- **Idioma:** contenido, textos y comentarios en español. Identificadores en código
  sin acentos.
- **Frontend mobile-first:** el usuario consulta el panel desde el móvil. Toda UI
  nueva o modificada debe validarse a ancho de móvil, no solo en desktop.
- **Slugs de empresa:** minúsculas con guiones (`cas-training`, `grupo-digital`,
  `agile-monkeys`). El mismo slug se reutiliza en `.adapt.json`, `.pdf` y `.png`.
- **Regla de oro del contenido del CV: NO inventar nada.** Ver `adaptador-cv/PROMPT.md`.
  Solo se puede reordenar, priorizar y reescribir con las palabras de la oferta algo
  que ya sea cierto en `cv/datos.json`.

---

## 5. Gotchas / cosas no obvias

1. **`cv.pdf`, `cv-preview.png`, `cv/CV-Nestor-Rodriguez-Tubio.pdf` y los `.pdf`/`.png`
   de `cv/adaptados/` son GENERADOS.** No los edites a mano: edita `cv/datos.json`
   (o el `.adapt.json`) y regenera con `python tools/generar_pdf.py`. Si cambias el
   CV y no regeneras, la web sirve un PDF desactualizado.
2. **El "encaje/checks" NO se imprime en el CV que se envía a la empresa** — es
   información interna del panel (quedaría presuntuoso). Está documentado como
   decisión deliberada en un comentario de `tools/generar_pdf.py:build`, y hay un
   commit dedicado a ello (`CV enviado limpio (sin recuadro de checks)`). Aunque el
   `.adapt.json` traiga `checks` y `cards`, `build()` **ignora** esos campos y pinta
   tarjetas fijas; la adaptación real se hace vía `titular`, `perfil` y `skills_order`.
   No lo "arregles" sin preguntar.
3. **`middleware.js` no bloquea si falta `PANEL_PASSWORD`**: es intencional (evita
   dejar al usuario fuera del panel antes de configurar la env var en Vercel). Si el
   panel se ve sin pedir contraseña en producción, el diagnóstico es "falta la env
   var en Vercel", no un bug del middleware. Cuando toques el `matcher`, recuerda
   listar **ambas** formas de cada ruta (`/panel` y `/panel.html`) porque
   `vercel.json` tiene `cleanUrls: true`.
4. **Cada página HTML lleva su propio CSS inline duplicado.** No hay hoja de estilos
   compartida. Un cambio de tema/menú hay que replicarlo en las 6 páginas
   (`index`, `panel`, `ofertas`, `seguimiento`, `preparacion`, `emails-cto`).
   Ya hubo un bug real de esto: `Arreglar solapamiento del menú superior en móvil`.
5. **El formulario de contacto está sin activar:** `index.html` tiene
   `access_key="PON_AQUI_TU_ACCESS_KEY_DE_WEB3FORMS"`. Hay un fallback en JS que abre
   el cliente de correo si la key no está puesta, así que "funciona" igualmente. Es
   una tarea pendiente del usuario, no un error a reportar cada vez.
6. **`web/` está vacía** — resto de cuando la web no se servía desde la raíz
   (commit `Servir la web desde la raíz del repo`). No metas nada ahí.
   PENDIENTE: confirmar si se puede borrar.
7. **La raíz tiene material heredado:** `Curriculum - Néstor Rodríguez Tubío.docx.pdf`
   es el CV antiguo subido a mano, no lo generado por el pipeline. No lo uses como
   fuente de verdad — la fuente es `cv/datos.json`.
8. **`.claude/` está en `.gitignore`** (config local). No la comitees ni la muevas.
9. **`vercel.json` fuerza la descarga del `cv.pdf`** con `Content-Disposition:
   attachment` y nombre `CV-Nestor-Rodriguez-Tubio.pdf`. Si alguna vez se quiere
   previsualizar el PDF en el navegador en vez de descargarlo, el culpable es esta
   cabecera.
10. **Datos personales reales en el repo** (email, teléfono, LinkedIn, ubicación) en
    `cv/datos.json` y los PDF/PNG generados. El repo es público en GitHub — es una
    decisión asumida del usuario (es un CV), pero no amplíes la superficie ni añadas
    datos sensibles nuevos sin preguntar.
11. **La cookie `panel_auth` es un SHA-256 sin sal ni caducidad de sesión** (90 días,
    `password + ":panel-ok"`). Es "suficiente" para un panel personal, no seguridad
    seria. No lo presentes como robusto ni construyas nada sensible encima.
12. **Ninguna automatización:** no hay `.github/workflows/`, ni CI, ni tests. Lo único
    que ocurre solo es el redespliegue de Vercel al hacer push a `master`.

---

## 6. Reglas de trabajo

- **Git:** el agente NO commitea ni pushea salvo petición explícita del usuario.
  Cuando se autorice: `git add <fichero concreto>`, nunca `git add .` (la raíz mezcla
  fuentes y artefactos generados). Prohibido: force-push, reescribir historial,
  crear/borrar ramas o tags. Recuerda: la rama es `master` y **push = deploy**.
- **NO tocar sin permiso:** `cv/datos.json` (fuente de verdad de datos reales —
  nunca inventes, añadas ni "mejores" datos del candidato), `middleware.js` +
  `api/*.js` (rompen el acceso al panel), `vercel.json`, y los PDF/PNG generados
  (regénéralos, no los edites).
- **Secretos:** la única env var real es `PANEL_PASSWORD`, definida en el panel de
  Vercel. Nunca la imprimas, la comitees ni la hardcodees en el repo. La Access Key
  de Web3Forms va en `index.html` y es pública por diseño (es una key de front) —
  aun así, no inventes una: la crea el usuario.
- **Antes de una escritura crítica**, párate y razona: *"¿esto rompe la web pública,
  el acceso al panel o el CV que ya se está enviando a empresas?"*.
- **Al adaptar un CV**, sigue `adaptador-cv/PROMPT.md` al pie de la letra: cero
  invención, honestidad en los "no cumple", salida a `cv/adaptados/<slug>.adapt.json`
  y regeneración con `--adapt`.
- **Ante cualquier duda, pregunta.** No inventes rutas, comandos ni datos del CV.
- **Mantén un LEARNINGS.md con 1 línea por bug/aprendizaje resuelto.**
