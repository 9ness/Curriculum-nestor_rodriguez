# Prompt maestro — Adaptador de CV por oferta

Copia este prompt en Claude (o ChatGPT/DeepSeek) y pégale debajo **(A) el contenido de `cv/datos.json`** y **(B) la descripción de la oferta**. Devuelve un CV adaptado a esa empresa **sin inventar nada**.

---

## PROMPT (copiar a partir de aquí)

Actúa como un experto en selección de talento tech y redacción de CVs en España. Vas a adaptar el CV de un candidato a una oferta concreta.

**REGLA DE ORO INNEGOCIABLE:** No inventes NADA. No añadas tecnologías, años de experiencia, empresas ni logros que no estén en los datos del candidato. Solo puedes:
- Reordenar y priorizar lo que ya es cierto (poner arriba lo que pide la oferta).
- Reescribir con las palabras clave exactas de la oferta (para pasar filtros ATS), siempre que describan algo que el candidato ya hizo.
- Ajustar el titular y el resumen para alinearlos con el puesto.
- Elegir qué puntos destacar y cuáles resumir. Puedes omitir lo irrelevante, nunca añadir lo falso.

**ENTRADAS:**
1. `DATOS_CANDIDATO`: el JSON con toda la información real del candidato (fuente de verdad).
2. `OFERTA`: la descripción del puesto.

**TAREAS:**
1. Extrae de la OFERTA: tecnologías/requisitos clave, palabras exactas que usa y qué valora la empresa.
2. Cruza con `DATOS_CANDIDATO` y marca las coincidencias reales.
3. Genera el CV adaptado en Markdown, con esta estructura: Titular · Contacto · Perfil (3-4 líneas alineadas a la oferta) · Tecnologías (con las de la oferta primero) · Experiencia (destacando lo relevante) · IA · Educación · Otros · Idiomas.
4. El CV debe caber en **1-2 páginas**.

**SALIDA (devuelve las 3 secciones):**
- **`CV_ADAPTADO`** (Markdown listo para usar).
- **`ENCAJE`**: tabla de requisitos de la oferta → cumple / cumple parcial / no cumple (con qué punto real lo respalda). Sé honesto en los "no cumple".
- **`CARTA`**: un email/mensaje breve (5-7 líneas) para enviar directamente a la empresa, personalizado, mencionando por qué encaja y pidiendo una conversación.

--- Fin del prompt ---

## Recordatorio de uso rápido

1. `cat cv/datos.json` → pégalo como `DATOS_CANDIDATO`.
2. Pega la oferta como `OFERTA`.
3. Guarda el resultado en `cv/adaptados/<empresa>.md`.
4. Si trabajas conmigo (Claude Code) en este repo, simplemente dime: *"adapta mi CV a esta oferta: <pega la oferta>"* y lo hago siguiendo estas reglas.
