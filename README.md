# Búsqueda de empleo de Néstor Rodríguez Tubío 🎯

Backend Senior **Java + IA generativa** buscando salto de **27 k → 35-45 k** en empresa española (sin inglés obligatorio), remoto o Andalucía.

Este repositorio ya no es "solo un PDF": es un **sistema completo de búsqueda de empleo**.

## 📁 Estructura

```
cv/
├── datos.json          → Fuente de verdad con TODOS tus datos (nunca inventar, solo aquí se edita)
├── cv-maestro.md       → CV maestro actualizado (posicionado como Senior Java + IA)
├── cv.html             → CV imprimible → abre en navegador → "Guardar como PDF" (limpio, 1-2 pág.)
└── adaptados/          → Aquí se guardan los CV adaptados a cada empresa

adaptador-cv/
└── PROMPT.md           → Motor que adapta tu CV a una oferta concreta SIN inventar nada

(raíz)  → la web se sirve desde aquí (Vercel no necesita "Root Directory")
├── index.html          → Web/portafolio (móvil-first): descarga CV + formulario de contacto
├── cv.pdf              → CV que se descarga desde la web
├── vercel.json         → Config de despliegue
└── DESPLIEGUE.md       → Cómo publicarla/redesplegarla en Vercel

tools/
└── generar_pdf.py      → Genera cv.pdf a partir de cv/datos.json (python tools/generar_pdf.py)

research/
└── empresas-y-ofertas.md → Portales, empresas españolas concretas, sueldos reales y estrategia de contacto directo
```

## ✅ Qué ya está hecho
- CV **reescrito y reposicionado** como *Backend Senior · Java & IA*, con datos de contacto y logros (incluido el diferenciador de **+5.700 M de visualizaciones**).
- **Web desplegable en Vercel** con descarga de CV y formulario de entrevista (funciona desde el móvil).
- **Sistema de adaptación de CV** por oferta.
- **Investigación de mercado**: dónde buscar, en qué empresas, cuánto pedir y cómo contactar directo.

## 🔜 Tus 3 tareas rápidas (5 min)
1. Desplegar/redesplegar la web en Vercel (ver `DESPLIEGUE.md`) — se sirve desde la raíz.
2. Crear la Access Key gratis del formulario en web3forms.com y pegarla en `index.html`.
3. Elegir empresas de `research/empresas-y-ofertas.md` y decirme *"adapta mi CV a esta oferta: …"*.

## 💡 Conclusión clave del análisis
Tu perfil **vale más de lo que cobras**. La banda de mercado para tu perfil empieza en ~41 k (Manfred 2026). Tu mayor palanca de subida: **venderte como AI/Backend Engineer** y **saltar de consultora a producto/startup de IA** (banda 51-70 k).
