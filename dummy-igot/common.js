/* Shared helpers for the iGOT Karmayogi prototype frontend */
window.IGOT_API_BASE = window.IGOT_API_BASE ||
  (["localhost", "127.0.0.1"].includes(location.hostname)
    ? "http://localhost:8001"
    : "https://igot-karmayogi-zs8h.onrender.com");
const API = window.IGOT_API_BASE;

function getToken() { return localStorage.getItem("igot_token"); }
function getUser() { return JSON.parse(localStorage.getItem("igot_user") || "null"); }
function requireAuth() {
  if (!getToken()) { location.href = "register.html"; return false; }
  return true;
}
function logout() {
  // invalidate the session server-side (best-effort), then wipe everything local
  const token = localStorage.getItem("igot_token");
  if (token) {
    fetch(API + "/api/auth/logout", {
      method: "POST",
      headers: { "Authorization": "Bearer " + token },
    }).catch(() => {});
  }
  localStorage.removeItem("igot_token");
  localStorage.removeItem("igot_user");
  Object.keys(localStorage)
    .filter(k => k.startsWith("lesson_done_"))
    .forEach(k => localStorage.removeItem(k));
  sessionStorage.clear();
  location.href = "index.html";
}

async function api(path, opts = {}) {
  const headers = { ...(opts.headers || {}) };
  if (getToken()) headers["Authorization"] = "Bearer " + getToken();
  if (opts.body && !(opts.body instanceof FormData)) {
    headers["Content-Type"] = "application/json";
    opts = { ...opts, body: JSON.stringify(opts.body) };
  }
  const res = await fetch(API + path, { ...opts, headers });
  if (res.status === 401) { logout(); throw new Error("Session expired"); }
  const data = await res.json().catch(() => ({}));
  if (!res.ok) throw new Error(data.detail || `Request failed (${res.status})`);
  return data;
}

const NAV_LINKS = [
  { href: "dashboard.html", label: "Dashboard" },
  { href: "studio.html", label: "Trainer Studio" },
  { href: "admin.html", label: "Analytics" },
];

function renderFooter() {
  if (document.getElementById("igotFooter") || document.querySelector("footer")) return;
  const el = document.createElement("footer");
  el.id = "igotFooter";
  el.innerHTML = `
  <div class="h-1 bg-gradient-to-r from-orange-400 via-white to-green-600"></div>
  <div class="bg-[#0f2a5c] text-blue-100">
    <div class="mx-auto max-w-7xl px-6 py-10 grid md:grid-cols-3 gap-8 text-sm">
      <div>
        <div class="flex items-center gap-2 mb-3"><img src="assets/logo.svg" alt="iGOT Karmayogi logo" class="h-11 w-11 shrink-0" /><span class="font-bold text-white text-lg">कर्मण्योगी भारत</span></div>
        <p>An initiative of Mission Karmayogi — NPCSCB, Government of India. Competency-driven capacity building of civil services, 'rule-based' to 'role-based'.</p>
      </div>
      <div>
        <p class="text-white font-semibold mb-2">Quick Links</p>
        <ul class="space-y-1">
          <li><a href="dashboard.html" class="hover:text-white">My Dashboard</a></li>
          <li><a href="studio.html" class="hover:text-white">Trainer Studio</a></li>
          <li><a href="admin.html" class="hover:text-white">Organization Analytics</a></li>
          <li><a href="index.html" class="hover:text-white">Home</a></li>
        </ul>
      </div>
      <div>
        <p class="text-white font-semibold mb-2">Contact</p>
        <p>Support: helpdesk@igotkarmayogi.gov.in</p>
        <p class="mt-4 text-blue-200 text-xs">© 2026 iGOT Karmayogi. Demo/prototype replica built for Smart India Hackathon 2026 — not the official platform.</p>
      </div>
    </div>
  </div>`;
  document.body.appendChild(el);
}

function renderHeader(active) {
  const user = getUser();
  const govtStrip = `
  <div class="mx-auto max-w-7xl mb-2 flex items-center justify-between text-[11px] font-medium px-6">
    <span class="text-slate-500">भारत सरकार · Government of India</span>
    <span class="text-slate-500">Department of Personnel &amp; Training · Mission Karmayogi</span>
  </div>`;
  return `${govtStrip}
  <header class="sticky top-3 z-50 px-4">
    <nav class="mx-auto max-w-7xl bg-white rounded-full shadow-lg border border-slate-100 px-6 py-2.5 flex items-center gap-6">
      <a href="index.html" class="flex items-center gap-2 shrink-0">
        <img src="assets/logo.svg" alt="iGOT Karmayogi logo" class="h-11 w-11 shrink-0" />
        <span class="leading-tight">
          <span class="block font-bold text-xl text-blue-800">कर्मण्योगी भारत</span>
          <span class="block text-[10px] tracking-wide text-slate-500 border-t border-slate-300 mt-0.5">लोकलहित में कार्यतात्</span>
        </span>
      </a>
      <ul class="hidden lg:flex items-center gap-5 text-[15px] font-medium ml-2">
        ${NAV_LINKS.map(l => `<li><a href="${l.href}" class="${active === l.href ? 'text-blue-800 font-semibold' : 'text-slate-600 hover:text-blue-700'}">${l.label}</a></li>`).join("")}
      </ul>
      <div class="ml-auto flex items-center gap-3">
        <span class="text-sm text-slate-600 hidden md:block">Namaste, <span class="font-semibold text-blue-800">${user ? user.name.split(" ")[0] : ""}</span></span>
        <button onclick="logout()" class="px-5 py-2 rounded-full bg-orange-400 text-white font-semibold hover:bg-orange-500 text-sm">Log out</button>
      </div>
    </nav>
  </header>`;
}

function scoreColor(pct) {
  return pct >= 70 ? "bg-emerald-500" : pct >= 40 ? "bg-amber-500" : "bg-red-500";
}
function fmtMins(m) { return m >= 60 ? `${Math.floor(m / 60)}h ${m % 60}m` : `${m}m`; }

/* Auto-footer: append the official footer once DOM is ready on any page using common.js */
if (typeof document !== "undefined") {
  document.addEventListener("DOMContentLoaded", renderFooter);
}
