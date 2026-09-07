/* Shared helpers for the iGOT Karmayogi prototype frontend */
if (typeof document !== "undefined" && !document.querySelector('script[src*="i18n.js"]')) {
  const i18nScript = document.createElement("script");
  i18nScript.src = "i18n.js";
  document.head.appendChild(i18nScript);
}

window.IGOT_API_BASE = window.IGOT_API_BASE ||
  (["localhost", "127.0.0.1"].includes(location.hostname)
    ? "http://127.0.0.1:8001"
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

/** Render a page-level load failure as a proper banner inside <main>, instead
 * of a raw line of red text dumped after the footer. Use as:
 *   load().catch(e => showPageError(e.message));
 * Safe to call more than once — replaces any existing banner rather than stacking. */
function showPageError(message) {
  document.getElementById("pageErrorBanner")?.remove();
  const el = document.createElement("div");
  el.id = "pageErrorBanner";
  el.className = "mx-auto max-w-7xl px-6 mt-4";
  el.innerHTML = `
    <div class="bg-red-50 border border-red-200 text-red-700 rounded-2xl px-5 py-4 flex items-start gap-3 shadow-sm">
      <span class="text-lg leading-none">⚠️</span>
      <div>
        <p class="font-semibold text-sm">Something went wrong loading this page</p>
        <p class="text-sm mt-0.5">${String(message).replace(/</g, "&lt;")}</p>
      </div>
    </div>`;
  const main = document.querySelector("main");
  if (main) main.prepend(el); else document.body.prepend(el);
}

const ADMIN_EMAIL = "admin.nssta@mospi.gov.in";
function isAdminUser() {
  const u = getUser();
  return !!u && u.email === ADMIN_EMAIL;
}
/** Call at the top of any learner-only page (dashboard/studio/learn/etc.) to
 * bounce the admin persona straight to the analytics view. */
function redirectIfAdmin() {
  if (isAdminUser() && !location.pathname.endsWith("admin.html")) {
    location.href = "admin.html";
    return true;
  }
  return false;
}

const NAV_LINKS = [
  { href: "dashboard.html", label: "Dashboard" },
  { href: "studio.html", label: "Trainer Studio" },
  { href: "analytics.html", label: "Analytics" },
  { href: "profile.html", label: "Profile" },
];
const ADMIN_NAV_LINKS = [
  { href: "admin.html", label: "Admin Dashboard" },
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
  const langDropdown = typeof renderLanguageDropdown === "function" ? renderLanguageDropdown() : "";
  const govtStrip = `
  <div class="mx-auto max-w-7xl mb-2 flex items-center justify-between text-[11px] font-medium px-6">
    <span class="text-slate-500">भारत सरकार · Government of India</span>
    <div class="flex items-center gap-4">
      <span class="text-slate-500 hidden sm:inline">Department of Personnel &amp; Training · Mission Karmayogi</span>
      ${langDropdown}
    </div>
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
        ${(isAdminUser() ? ADMIN_NAV_LINKS : NAV_LINKS).map(l => `<li><a href="${l.href}" class="${active === l.href ? 'text-blue-800 font-semibold' : 'text-slate-600 hover:text-blue-700'}">${l.label}</a></li>`).join("")}
      </ul>
      <div class="ml-auto flex items-center gap-3">
        ${isAdminUser() ? '<span class="text-[10px] font-bold tracking-wide uppercase px-2.5 py-1 rounded-full bg-orange-50 text-orange-600 border border-orange-100">Administrator</span>' : ''}
        ${user && user.role === "readonly" ? '<span class="text-[10px] font-bold tracking-wide uppercase px-2.5 py-1 rounded-full bg-slate-100 text-slate-500 border border-slate-200">Read-only</span>' : ''}
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

/* ---- Learner chatbot widget: floating button + panel, shared across every
   learner page. Answers questions and can swap a too-hard roadmap course for
   its foundational alternative via POST /api/chat. Admin persona never sees it. */
function renderChatWidget() {
  if (document.getElementById("chatWidgetRoot")) return;
  if (!getToken() || isAdminUser()) return;

  const root = document.createElement("div");
  root.id = "chatWidgetRoot";
  root.innerHTML = `
    <button id="chatFab" aria-label="Open Sahitya, your learning assistant"
            class="fixed bottom-6 right-6 z-[60] w-14 h-14 rounded-full bg-blue-700 text-white shadow-xl
                   hover:bg-blue-800 flex items-center justify-center text-2xl transition-transform hover:scale-105">💬</button>
    <div id="chatPanel" style="display:none"
         class="fixed bottom-24 right-6 z-[60] w-[340px] max-w-[92vw] h-[480px] max-h-[70vh] bg-white rounded-2xl
                shadow-2xl border border-slate-200 flex-col overflow-hidden">
      <div class="bg-blue-800 text-white px-4 py-3 flex items-center justify-between shrink-0">
        <div>
          <p class="font-semibold text-sm">Sahitya</p>
          <p class="text-[11px] text-blue-200">Your learning assistant — ask about gaps, roadmap, or swap a hard course</p>
        </div>
        <button id="chatCloseBtn" class="text-blue-200 hover:text-white text-lg leading-none">✕</button>
      </div>
      <div id="chatMessages" class="flex-1 overflow-y-auto px-3 py-3 space-y-3 text-sm bg-slate-50"></div>
      <div class="border-t border-slate-100 p-2.5 flex gap-2 shrink-0 bg-white">
        <input id="chatInput" type="text" placeholder="e.g. the GNSS course is too hard"
               class="flex-1 text-sm border border-slate-300 rounded-full px-3.5 py-2 focus:outline-none focus:border-blue-500" />
        <button id="chatSendBtn" class="w-9 h-9 rounded-full bg-orange-400 hover:bg-orange-500 text-white shrink-0 flex items-center justify-center">➤</button>
      </div>
    </div>`;
  document.body.appendChild(root);

  const panel = document.getElementById("chatPanel");
  const fab = document.getElementById("chatFab");
  const msgBox = document.getElementById("chatMessages");
  const input = document.getElementById("chatInput");
  let historyLoaded = false;

  function bubble(role, text, action) {
    const mine = role === "user";
    const el = document.createElement("div");
    el.className = mine ? "flex justify-end" : "flex justify-start";
    el.innerHTML = `
      <div class="max-w-[85%] rounded-2xl px-3.5 py-2 ${mine ? "bg-blue-700 text-white rounded-br-sm" : "bg-white border border-slate-200 text-slate-700 rounded-bl-sm"}">
        <p>${text.replace(/</g, "&lt;")}</p>
        ${action ? `<p class="mt-1.5 text-[11px] font-medium ${mine ? "text-blue-100" : "text-emerald-600"}">✓ Roadmap updated</p>` : ""}
      </div>`;
    msgBox.appendChild(el);
    msgBox.scrollTop = msgBox.scrollHeight;
  }

  async function loadHistory() {
    if (historyLoaded) return;
    historyLoaded = true;
    try {
      const h = await api("/api/chat/history");
      if (!h.messages.length) {
        bubble("assistant", "Namaste! I'm Sahitya. I can explain your skill gaps, recommend what to study next, or switch you to an easier version of a course you're finding too hard. What would you like to do?");
      } else {
        h.messages.forEach(m => bubble(m.role, m.content, m.action));
      }
    } catch (e) {
      bubble("assistant", "Namaste! I'm Sahitya. Ask me about your gaps, roadmap, or say a course is too hard and I'll try to swap it for an easier one.");
    }
  }

  async function send() {
    const text = input.value.trim();
    if (!text) return;
    input.value = "";
    bubble("user", text);
    const typing = document.createElement("div");
    typing.id = "chatTyping";
    typing.className = "flex justify-start";
    typing.innerHTML = `<div class="bg-white border border-slate-200 rounded-2xl rounded-bl-sm px-3.5 py-2 text-slate-400 text-xs">thinking…</div>`;
    msgBox.appendChild(typing);
    msgBox.scrollTop = msgBox.scrollHeight;
    try {
      const res = await api("/api/chat", { method: "POST", body: { message: text } });
      document.getElementById("chatTyping")?.remove();
      bubble("assistant", res.reply, res.action);
      if (res.action && (res.action.type === "swap_course" || res.action.type === "revert_swap")) {
        // roadmap changed server-side — refresh the current page's view right now if it
        // shows roadmap/course data (dashboard.html, course_player.html register this hook),
        // and mark it dirty as a fallback for any page that doesn't.
        if (window.__refreshRoadmapUI) window.__refreshRoadmapUI();
        else sessionStorage.setItem("roadmap_dirty", "1");
      }
    } catch (e) {
      document.getElementById("chatTyping")?.remove();
      bubble("assistant", "Sorry, I couldn't reach Sahitya's service just now. Please try again in a moment.");
    }
  }

  function panelOpen() { return panel.style.display !== "none"; }
  function setPanelOpen(open) {
    panel.style.display = open ? "flex" : "none";
    if (open) { loadHistory(); input.focus(); }
  }
  fab.addEventListener("click", () => setPanelOpen(!panelOpen()));
  document.getElementById("chatCloseBtn").addEventListener("click", () => setPanelOpen(false));
  document.getElementById("chatSendBtn").addEventListener("click", send);
  input.addEventListener("keydown", e => { if (e.key === "Enter") send(); });
}

/* Auto-footer + chat widget: append once DOM is ready on any page using common.js */
if (typeof document !== "undefined") {
  document.addEventListener("DOMContentLoaded", renderFooter);
  document.addEventListener("DOMContentLoaded", renderChatWidget);
}
