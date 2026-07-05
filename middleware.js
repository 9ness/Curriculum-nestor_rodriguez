export const config = {
  matcher: [
    "/panel", "/panel.html",
    "/ofertas", "/ofertas.html",
    "/seguimiento", "/seguimiento.html",
    "/preparacion", "/preparacion.html",
    "/emails-cto", "/emails-cto.html",
  ],
};

async function sha256Hex(text) {
  const data = new TextEncoder().encode(text);
  const digest = await crypto.subtle.digest("SHA-256", data);
  return Array.from(new Uint8Array(digest)).map((b) => b.toString(16).padStart(2, "0")).join("");
}

export default async function middleware(request) {
  const password = process.env.PANEL_PASSWORD;
  // Si aún no se ha configurado la contraseña en Vercel, no bloquear
  // (evita dejarte fuera del panel antes de terminar la configuración).
  if (!password) return;

  const cookieHeader = request.headers.get("cookie") || "";
  const match = cookieHeader.match(/(?:^|;\s*)panel_auth=([^;]+)/);
  const expected = await sha256Hex(password + ":panel-ok");

  if (match && match[1] === expected) {
    return; // cookie válida, deja pasar
  }

  const url = new URL(request.url);
  const loginUrl = new URL("/login", url.origin);
  loginUrl.searchParams.set("next", url.pathname);
  return Response.redirect(loginUrl, 302);
}
