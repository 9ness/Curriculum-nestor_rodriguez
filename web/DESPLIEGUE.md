# Cómo desplegar la web en Vercel

La web es **estática** (un solo `index.html` + `cv.pdf`). Se despliega en 2 minutos y gratis.

## Opción A — Desde la web de Vercel (la más fácil, sin instalar nada)
1. Entra en https://vercel.com y regístrate con tu cuenta de GitHub.
2. **Add New → Project** e importa el repositorio `Curriculum-nestor_rodriguez`.
3. En la configuración del proyecto pon:
   - **Root Directory:** `web`
   - Framework Preset: **Other** (es estático).
4. Deploy. Te dará una URL tipo `https://curriculum-nestor.vercel.app`.

## Opción B — Desde tu terminal (CLI)
```bash
npm i -g vercel
cd web
vercel        # sigue el asistente; para producción: vercel --prod
```

## Antes de dar la URL a empresas — checklist de 3 minutos
- [ ] En `index.html`, sustituye los enlaces de **LinkedIn** y **GitHub** (busca `data-todo`).
- [ ] Pon tu **teléfono** si quieres mostrarlo.
- [ ] Activa el formulario: crea una Access Key gratis en https://web3forms.com con tu email `ness4b@gmail.com` y pégala en el campo `access_key` de `index.html`. *(Sin esto, el formulario abre el email del visitante como alternativa — funciona igual.)*
- [ ] Actualiza `cv.pdf` cada vez que cambies el CV (o usa una versión adaptada como CV por defecto).

## Compartir desde el móvil
Una vez desplegada, comparte la URL por WhatsApp/email. Desde el móvil, cualquier empresa puede **descargar tu CV** y **rellenar el formulario** para contactarte.
