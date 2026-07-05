const crypto = require("crypto");

function hash(text) {
  return crypto.createHash("sha256").update(text, "utf8").digest("hex");
}

module.exports = async (req, res) => {
  if (req.method !== "POST") {
    res.status(405).json({ error: "Método no permitido" });
    return;
  }

  let body = req.body;
  if (typeof body === "string") {
    try { body = JSON.parse(body); } catch { body = {}; }
  }
  const { password, next } = body || {};
  const expectedPassword = process.env.PANEL_PASSWORD;

  if (!expectedPassword) {
    res.status(500).json({ error: "El panel aún no tiene contraseña configurada en Vercel (PANEL_PASSWORD)." });
    return;
  }

  if (password !== expectedPassword) {
    res.status(401).json({ error: "Contraseña incorrecta" });
    return;
  }

  const cookieVal = hash(expectedPassword + ":panel-ok");
  const maxAge = 60 * 60 * 24 * 90; // 90 días
  res.setHeader(
    "Set-Cookie",
    `panel_auth=${cookieVal}; Path=/; Max-Age=${maxAge}; HttpOnly; Secure; SameSite=Lax`
  );
  res.status(200).json({ ok: true, next: next || "/panel" });
};
