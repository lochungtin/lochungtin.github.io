/* ══════════════════════════════════════════════════════════════════════
   theme.js — Three-way theme toggle (light / dark / auto)
   Shared by portfolio.html and all project.html pages.

   Modes stored in localStorage key "theme-mode":
     "light"  → always light
     "dark"   → always dark
     "auto"   → 06:00–18:00 = light, 18:00–06:00 = dark  (DEFAULT)
   ══════════════════════════════════════════════════════════════════════ */

(function () {

  // ── Resolve which visual theme to apply ──────────────────────────────
  function resolveTheme(mode) {
    if (mode === 'light') return 'light';
    if (mode === 'dark')  return 'dark';
    // auto: time-based
    const h = new Date().getHours();
    return (h >= 6 && h < 18) ? 'light' : 'dark';
  }

  // ── Apply theme to <html> ─────────────────────────────────────────────
  function applyTheme(mode) {
    const theme = resolveTheme(mode);
    document.documentElement.setAttribute('data-theme', theme);
    document.documentElement.setAttribute('data-mode', mode);
  }

  // ── Read persisted mode, defaulting to 'auto' ────────────────────────
  function getSavedMode() {
    return localStorage.getItem('theme-mode') || 'auto';
  }

  // ── Save and apply a new mode ─────────────────────────────────────────
  function setMode(mode) {
    localStorage.setItem('theme-mode', mode);
    applyTheme(mode);
    updateToggleUI(mode);
  }

  // ── Update the three-button toggle to reflect current mode ───────────
  function updateToggleUI(mode) {
    document.querySelectorAll('.theme-btn').forEach(btn => {
      btn.classList.toggle('active', btn.dataset.mode === mode);
    });
  }

  // ── Wire up toggle buttons once DOM is ready ─────────────────────────
  function initToggle() {
    document.querySelectorAll('.theme-btn').forEach(btn => {
      btn.addEventListener('click', () => setMode(btn.dataset.mode));
    });
    updateToggleUI(getSavedMode());
  }

  // ── Apply theme immediately (before paint) to prevent flash ──────────
  applyTheme(getSavedMode());

  // ── Init toggle after DOM ─────────────────────────────────────────────
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initToggle);
  } else {
    initToggle();
  }

  // ── Re-evaluate auto mode every minute (handles the 6am/6pm boundary) ─
  setInterval(() => {
    if (getSavedMode() === 'auto') applyTheme('auto');
  }, 60 * 1000);

})();
