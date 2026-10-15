# Prompt para sacar la ficha de un proyecto de trabajo

Cuando Néstor pida «instrucciones para la info de un proyecto de Ayesa» (o de otra
empresa), dale ESTE bloque tal cual para que lo pegue en el chat de Claude del PC de
empresa que tiene el contexto del proyecto:

````text
Necesito una ficha de este proyecto para mi currículum. Usa lo que sepas del código, del
repo y de nuestras conversaciones. Reglas: nada confidencial (sin nombres internos de
sistemas, clientes, personas, URLs, IPs ni datos); describe el negocio de forma genérica
(«plataforma de facturación electrónica para administración pública», no el nombre del
cliente). Si no sabes un dato, pon null; no inventes ni redondees al alza.

Devuélvelo como UN bloque de código JSON con este formato exacto:
{
  "empresa": "Ayesa",
  "proyecto": "nombre genérico y corto",
  "sector": "p. ej. administración pública, banca, utilities",
  "desde": "AAAA-MM",
  "hasta": "AAAA-MM o null si sigue",
  "rol": "mi rol real (p. ej. desarrollador backend sénior)",
  "equipo": "tamaño aproximado y metodología, o null",
  "de_que_trata": "2-3 frases para un recruiter, sin jerga interna",
  "tecnologias": ["Java 17", "Spring Boot", "…"],
  "lo_que_hice": ["acciones concretas con verbo en pasado y resultado, con cifras si las hay"],
  "logros_medibles": ["p. ej. reduje el tiempo de X de 10 a 2 min", "…"],
  "habilidades": ["técnicas y blandas que he desarrollado aquí"],
  "palabras_clave_ats": ["términos que un filtro de ofertas buscaría"]
}
````

Cuando Néstor traiga la respuesta (JSON o .md) al VPS:
1. Guárdala en `~/proyectos/consultas-nestor/trabajo/<empresa>-<proyecto>.json`
   (privado, NO en este repo, que es público). Si ya existe, fusiona y conserva `desde`.
2. Añade una línea a `~/proyectos/consultas-nestor/habilidades.md` (sección «Trabajo por
   cuenta ajena») apuntando al fichero.
3. Repasa que no se haya colado nada confidencial; si dudas, pregúntale.
4. No toques el CV todavía: entra en la próxima actualización (AGENTS.md §7).
