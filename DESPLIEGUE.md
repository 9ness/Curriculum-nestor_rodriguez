# Cómo desplegar la web en Vercel

La web es **estática** (`index.html` + `cv.pdf`, ambos en la raíz del repo). Como están en la raíz, Vercel **no necesita ninguna configuración especial de "Root Directory"**.

## Ya está conectada a GitHub
Cada vez que se suba un cambio a `master`, Vercel **redespliega solo**. Si acabas de mover los archivos a la raíz, espera ~30 s y recarga la URL.

## Si necesitas importarla de nuevo
1. https://vercel.com → *Continue with GitHub* (cuenta 9ness).
2. *Add New → Project* → importa `Curriculum-nestor_rodriguez`.
3. **Deja Root Directory en la raíz** (por defecto). Framework Preset: **Other**.
4. Deploy.

## Forzar un nuevo despliegue (si no se actualiza)
En el panel de Vercel: pestaña **Deployments** → botón **⋯** del último → **Redeploy**.

## Checklist antes de compartir la URL con empresas
- [ ] Formulario: crea una Access Key gratis en https://web3forms.com con tu email `ness4b@gmail.com` y pégala en el campo `access_key` de `index.html`. *(Sin esto, el formulario abre el correo del visitante — funciona igual.)*
- [ ] El `cv.pdf` se regenera con `python tools/generar_pdf.py` cada vez que cambies el CV.

## Compartir desde el móvil
Comparte la URL por WhatsApp/email. Cualquier empresa podrá **descargar tu CV** y **rellenar el formulario** para contactarte.
