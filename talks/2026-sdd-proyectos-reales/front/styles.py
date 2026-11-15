"""
Archivo: talks/2026-sdd-proyectos-reales/front/styles.py
Fecha de modificación: 15/11/2026
Autor: Alex Prieto <alexprieto1997@gmail.com>

Descripción:
Sistema de diseño y motor de presentación de la charla `2026-sdd-proyectos-reales`.
Define la paleta editorial ejecutiva clara (alabastro/blanco/slate con acentos
cobalto, esmeralda, ámbar y carmesí), la hoja de estilos completa, el motor
JavaScript de navegación (transiciones direccionales, fragmentos progresivos,
barra de progreso por bloques, notas del orador, vista general y pantalla
completa) y la plantilla HTML autocontenida.

Acciones Principales:
    - Expone `PALETTE` con los colores canónicos de la estética gerencial.
    - Expone `CSS` con el diseño slide-a-slide (transiciones, fragmentos, progreso).
    - Expone `ENGINE_JS` con la coreografía por teclado y la inicialización Chart.js.
    - Expone `HTML_TEMPLATE` con tokens `__*__` que `back/build_deck.py` sustituye.

Estructura Interna:
    - Constantes de solo texto: sin imports de los demás módulos de la charla.

Entradas / Dependencias:
    - Ninguna (módulo puro de datos; Chart.js se inyecta desde `build_deck.py`).

Salidas / Efectos:
    - Cadenas consumidas por `back/build_deck.py` para generar HTML autocontenido.

Ejemplo de Integración:
    from front_styles import CSS, ENGINE_JS, HTML_TEMPLATE  # vía importlib en build_deck
"""

PALETTE = {
    "bg": "#F8FAFC",        # alabastro
    "card": "#FFFFFF",      # tarjetas blanco puro
    "border": "#E2E8F0",    # bordes finos
    "ink": "#0F172A",       # tinta principal slate
    "sub": "#475569",       # secundario
    "cobalt": "#1E40AF",    # acento primario
    "emerald": "#047857",   # verificado / DoD
    "amber": "#B45309",     # ODD proporcionalidad
    "carmine": "#B91C1C",   # leakage / alerta
    "cobalt_soft": "#EFF6FF",
    "emerald_soft": "#ECFDF5",
    "amber_soft": "#FFFBEB",
    "carmine_soft": "#FEF2F2",
}

CSS = """
:root {
  --bg: #F4F6FA; --card: #FFFFFF; --border: #E2E8F0;
  --ink: #0F172A; --sub: #475569;
  --cobalt: #1E40AF; --emerald: #047857; --amber: #B45309; --carmine: #B91C1C;
  --cobalt-soft: #EFF6FF; --emerald-soft: #ECFDF5; --amber-soft: #FFFBEB; --carmine-soft: #FEF2F2;
  --spring: cubic-bezier(.16, 1, .3, 1);
  --font-head: 'Space Grotesk', 'IBM Plex Sans', 'Segoe UI', sans-serif;
  --font-body: 'IBM Plex Sans', 'Segoe UI', sans-serif;
  --font-mono: 'IBM Plex Mono', 'Consolas', monospace;
}
* { margin: 0; padding: 0; box-sizing: border-box; }
html, body { height: 100%; }
body {
  background-color: var(--bg);
  background-image: radial-gradient(#CBD5E1 1px, transparent 1px);
  background-size: 24px 24px;
  color: var(--ink);
  font-family: var(--font-body); overflow: hidden;
}
#stage { position: fixed; inset: 0; }

/* ---- Diapositivas: transición direccional con resorte ---- */
.slide {
  position: absolute; inset: 0;
  padding: 44px 64px 80px;
  opacity: 0; visibility: hidden; pointer-events: none;
  transform: translateX(56px);
  transition: transform .38s var(--spring), opacity .38s var(--spring), visibility 0s linear .38s;
  overflow: hidden;
  display: flex; flex-direction: column;
}
.slide.before { transform: translateX(-56px); }
.slide.active {
  opacity: 1; visibility: visible; pointer-events: auto;
  transform: translateX(0);
  z-index: 2;
  transition: transform .38s var(--spring), opacity .38s var(--spring), visibility 0s;
}

/* ---- Cabecera editorial ---- */
.kicker {
  font-family: var(--font-mono); font-size: 15px; font-weight: 600;
  letter-spacing: 3px; text-transform: uppercase; color: var(--cobalt);
  margin-bottom: 10px;
}
.kicker .k-block { color: var(--sub); }
h1.slide-title {
  font-family: var(--font-head); font-size: 44px; font-weight: 700;
  line-height: 1.12; color: var(--ink); margin-bottom: 8px;
}
.slide-sub { font-size: 20px; color: var(--sub); margin-bottom: 26px; max-width: 1080px; }
.rule { width: 64px; height: 5px; border-radius: 3px; background: var(--cobalt); margin: 6px 0 22px; }
.body-area { flex: 1; min-height: 0; display: flex; flex-direction: column; justify-content: center; }

/* ---- Tarjetas Bento modulares ---- */
.grid2 { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; align-items: stretch; }
.grid3 { display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; align-items: stretch; }
.grid5 { display: grid; grid-template-columns: repeat(5, 1fr); gap: 14px; align-items: stretch; }
.card {
  background: var(--card); border: 1px solid var(--border); border-radius: 16px;
  padding: 20px 24px; box-shadow: 0 4px 20px rgba(15,23,42,.04);
}
.card h3 { font-family: var(--font-head); font-size: 20px; font-weight: 600; margin-bottom: 8px; }
.card p, .card li { font-size: 16.5px; line-height: 1.5; color: var(--sub); }
.card ul { padding-left: 20px; }
.card li { margin-bottom: 6px; }
.card.accent-cobalt { border-top: 4px solid var(--cobalt); }
.card.accent-emerald { border-top: 4px solid var(--emerald); }
.card.accent-amber { border-top: 4px solid var(--amber); }
.card.accent-carmine { border-top: 4px solid var(--carmine); }
.card .num {
  font-family: var(--font-mono); font-size: 12.5px; color: var(--cobalt); font-weight: 700;
  letter-spacing: 2px; text-transform: uppercase; margin-bottom: 8px; display: block;
}

/* ---- KPI Bento ---- */
.kpi {
  font-family: var(--font-head); font-size: 44px; font-weight: 700; line-height: 1.05;
  letter-spacing: -0.5px; color: var(--ink);
}
.kpi em { font-style: normal; }
.kpi-small { font-family: var(--font-head); font-size: 26px; font-weight: 700; }

/* ---- Carriles Bento conectados (dashboard slide 5) ---- */
.lane { display: flex; align-items: stretch; gap: 0; }
.lane-label {
  font-family: var(--font-mono); font-size: 12px; font-weight: 700; letter-spacing: 2.5px;
  text-transform: uppercase; margin-bottom: 8px;
}
.lane .node {
  flex: 1; background: var(--card); border: 1px solid var(--border); border-radius: 16px;
  box-shadow: 0 4px 20px rgba(15,23,42,.04);
  padding: 14px 16px; display: flex; flex-direction: column; justify-content: center; text-align: center;
}
.lane .node .n-title { font-family: var(--font-head); font-size: 18px; font-weight: 700; }
.lane .node .n-sub { font-family: var(--font-mono); font-size: 12.5px; margin-top: 4px; color: var(--sub); }
.lane .conn {
  align-self: center; width: 44px; text-align: center; flex: none;
  font-family: var(--font-mono); font-weight: 700; font-size: 20px;
  animation: connpulse 1.4s ease-in-out infinite;
}
@keyframes connpulse { 0%,100% { transform: translateX(0); opacity: .65; } 50% { transform: translateX(5px); opacity: 1; } }

/* ---- Badge de ejercicio en vivo ---- */
.live-badge {
  display: inline-flex; align-items: center; gap: 10px;
  font-family: var(--font-mono); font-size: 14.5px; font-weight: 700; letter-spacing: 1.5px;
  color: #FFFFFF; background: var(--ink); border-radius: 999px; padding: 9px 20px;
  box-shadow: 0 4px 20px rgba(15,23,42,.18);
}
.live-badge .dot-live { width: 9px; height: 9px; border-radius: 50%; background: #28C840;
  animation: liveblink 1.2s ease-in-out infinite; }
@keyframes liveblink { 0%,100% { opacity: 1; } 50% { opacity: .25; } }

/* ---- Terminal oscura elegante dentro de tarjeta Bento ---- */
.terminal {
  background: #0F172A; color: #E2E8F0; border-radius: 12px; overflow: hidden;
  font-family: var(--font-mono); font-size: 13.5px; line-height: 1.65;
  box-shadow: inset 0 0 0 1px #1E293B;
}
.terminal .t-head {
  display: flex; align-items: center; gap: 7px; padding: 10px 14px;
  border-bottom: 1px solid #1E293B; color: #64748B; font-size: 12px;
}
.terminal .t-dot { width: 11px; height: 11px; border-radius: 50%; }
.terminal .t-dot.r { background: #FF5F57; } .terminal .t-dot.y { background: #FEBC2E; } .terminal .t-dot.g { background: #28C840; }
.terminal .t-body { padding: 14px 18px; white-space: pre; overflow: hidden; }
.terminal .t-cmd { color: #7DD3FC; font-weight: 600; }
.terminal .t-out { color: #94A3B8; }
.terminal .t-good { color: #6EE7B7; font-weight: 700; }
.terminal .t-bad { color: #FCA5A5; font-weight: 700; }

/* ---- Pasos numerados ---- */
ol.steps { list-style: none; counter-reset: paso; }
ol.steps li {
  counter-increment: paso; position: relative; padding-left: 44px; margin-bottom: 12px;
  font-size: 16px; line-height: 1.45; color: var(--sub);
}
ol.steps li::before {
  content: counter(paso); position: absolute; left: 0; top: 0;
  width: 30px; height: 30px; border-radius: 10px; background: var(--cobalt-soft);
  border: 1px solid #BFDBFE; color: var(--cobalt); font-family: var(--font-mono);
  font-size: 14px; font-weight: 700; display: flex; align-items: center; justify-content: center;
}

/* ---- Badges / pills ---- */
.pill {
  display: inline-block; font-family: var(--font-mono); font-size: 14px; font-weight: 600;
  padding: 5px 14px; border-radius: 999px; border: 1px solid var(--border);
  background: var(--card); margin: 0 8px 8px 0;
}
.pill.cobalt { color: var(--cobalt); border-color: #BFDBFE; background: var(--cobalt-soft); }
.pill.emerald { color: var(--emerald); border-color: #A7F3D0; background: var(--emerald-soft); }
.pill.amber { color: var(--amber); border-color: #FDE68A; background: var(--amber-soft); }
.pill.carmine { color: var(--carmine); border-color: #FECACA; background: var(--carmine-soft); }

/* ---- Tablas comparativas ---- */
table.cmp { width: 100%; border-collapse: collapse; background: var(--card);
  border: 1px solid var(--border); border-radius: 14px; overflow: hidden; font-size: 17px; }
table.cmp th { font-family: var(--font-head); text-align: left; padding: 14px 18px;
  background: var(--cobalt-soft); color: var(--cobalt); font-size: 16px; }
table.cmp td { padding: 12px 18px; border-top: 1px solid var(--border); color: var(--sub); }
table.cmp td.k { font-weight: 600; color: var(--ink); }

/* ---- Código ---- */
.code {
  font-family: var(--font-mono); font-size: 15.5px; line-height: 1.6;
  background: var(--card); border: 1px solid var(--border); border-radius: 12px;
  padding: 18px 22px; color: var(--ink); white-space: pre; overflow: hidden;
}
.code .bad { color: var(--carmine); font-weight: 700; }
.code .good { color: var(--emerald); font-weight: 700; }
.code .cm { color: #94A3B8; }

/* ---- Divisores de bloque ---- */
.divider { justify-content: center; }
.divider .d-kicker { font-family: var(--font-mono); font-size: 18px; letter-spacing: 4px;
  text-transform: uppercase; color: var(--cobalt); margin-bottom: 18px; }
.divider h1 { font-family: var(--font-head); font-size: 58px; font-weight: 700; line-height: 1.15;
  max-width: 1000px; }
.divider .d-meta { margin-top: 28px; }
.divider .d-time { font-family: var(--font-mono); font-size: 17px; color: var(--sub); margin-top: 14px; }

/* ---- Portada ---- */
.cover { justify-content: center; }
.cover h1 { font-family: var(--font-head); font-size: 60px; font-weight: 700; line-height: 1.12;
  max-width: 1040px; }
.cover .c-sub { font-size: 23px; color: var(--sub); margin-top: 22px; max-width: 1000px; line-height: 1.5; }
.cover .c-meta { margin-top: 34px; }
.cover .c-author { margin-top: 26px; font-size: 18px; color: var(--sub); }

/* ---- Fragmentos progresivos ---- */
.frag { opacity: 0; transform: translateY(10px); transition: opacity .38s var(--spring), transform .38s var(--spring); }
.frag.shown { opacity: 1; transform: translateY(0); }

/* ---- Barra de progreso por bloques (5 actos) ---- */
#progress { position: fixed; top: 0; left: 0; right: 0; height: 8px; z-index: 60;
  display: flex; gap: 3px; padding: 2px 4px; background: transparent; }
#progress .seg { flex: 1; background: #E2E8F0; border-radius: 4px; overflow: hidden; position: relative; }
#progress .seg .seg-fill { position: absolute; inset: 0; width: 0%;
  background: var(--cobalt); transition: width .5s ease; }
#progress .seg.lit .seg-fill { box-shadow: 0 0 6px rgba(30,64,175,.55); }
#progress-line { position: fixed; top: 9px; left: 4px; right: 4px; height: 3px; z-index: 59; }
#progress-line > div { height: 100%; width: 0%; background: #94A3B8; border-radius: 2px;
  transition: width .5s ease; }

/* ---- HUD inferior ---- */
#hud { position: fixed; bottom: 0; left: 0; right: 0; z-index: 60;
  display: flex; align-items: center; justify-content: space-between;
  padding: 10px 20px; font-family: var(--font-mono); font-size: 13.5px; color: var(--sub);
  background: linear-gradient(to top, rgba(248,250,252,.96), rgba(248,250,252,0)); }
#hud .h-left b { color: var(--cobalt); }
#hud .h-right span { margin-left: 14px; }
#hud kbd { font-family: var(--font-mono); border: 1px solid var(--border); background: var(--card);
  border-radius: 5px; padding: 1px 7px; font-size: 12.5px; }

/* ---- Panel de notas del orador ---- */
#notes-panel {
  position: fixed; top: 8px; bottom: 0; right: 0; width: 420px; z-index: 80;
  background: var(--card); border-left: 1px solid var(--border);
  box-shadow: -12px 0 30px rgba(15,23,42,.08);
  transform: translateX(105%); transition: transform .35s ease;
  display: flex; flex-direction: column; padding: 24px 26px;
}
#notes-panel.open { transform: translateX(0); }
#notes-panel h2 { font-family: var(--font-head); font-size: 18px; color: var(--ink); margin-bottom: 4px; }
#notes-time { font-family: var(--font-mono); font-size: 13.5px; color: var(--cobalt);
  margin-bottom: 14px; font-weight: 600; }
#notes-body { overflow-y: auto; font-size: 15.5px; line-height: 1.6; color: var(--sub); }
#notes-body strong { color: var(--ink); }
#notes-body ul { padding-left: 18px; margin: 8px 0; }
#notes-body li { margin-bottom: 5px; }
#notes-close { position: absolute; top: 14px; right: 16px; cursor: pointer; color: var(--sub);
  font-family: var(--font-mono); font-size: 14px; border: 1px solid var(--border);
  background: var(--bg); border-radius: 6px; padding: 3px 10px; }

/* ---- Vista general (G) ---- */
#overview { position: fixed; inset: 0; z-index: 90; background: rgba(248,250,252,.98);
  display: none; overflow-y: auto; padding: 40px 48px; }
#overview.open { display: block; }
#overview h2 { font-family: var(--font-head); font-size: 26px; margin-bottom: 22px; }
.ov-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; }
.ov-item { background: var(--card); border: 1px solid var(--border); border-radius: 12px;
  padding: 16px 18px; cursor: pointer; transition: border-color .2s, transform .2s; }
.ov-item:hover { border-color: var(--cobalt); transform: translateY(-2px); }
.ov-item.current { border-color: var(--cobalt); box-shadow: 0 0 0 2px var(--cobalt-soft); }
.ov-item .ov-num { font-family: var(--font-mono); font-size: 13px; color: var(--cobalt); font-weight: 600; }
.ov-item .ov-block { font-family: var(--font-mono); font-size: 12px; color: var(--sub); margin-bottom: 6px; }
.ov-item .ov-title { font-family: var(--font-head); font-size: 15.5px; font-weight: 600; color: var(--ink); line-height: 1.3; }

/* ---- Gráficas ---- */
.chart-box { position: relative; background: var(--card); border: 1px solid var(--border);
  border-radius: 14px; padding: 20px 22px 16px; }
.chart-box h3 { font-family: var(--font-head); font-size: 19px; margin-bottom: 12px; }
.chart-box .cwrap { position: relative; height: 380px; }
.chart-note { font-size: 15px; color: var(--sub); margin-top: 10px; }
.chart-fallback { display: none; font-family: var(--font-mono); font-size: 14px; color: var(--amber); }
.chart-fallback.visible { display: block; }

/* ---- Animaciones SVG ---- */
.flow-dash { stroke-dasharray: 12 9; animation: dashmove 1.1s linear infinite; }
@keyframes dashmove { to { stroke-dashoffset: -42; } }
.flow-dash-rev { stroke-dasharray: 12 9; animation: dashmove-rev 1.1s linear infinite; }
@keyframes dashmove-rev { to { stroke-dashoffset: 42; } }
.pulse { transform-origin: center; animation: pulsec 2.6s ease-in-out infinite; }
@keyframes pulsec { 0%,100% { transform: scale(1); opacity: .95; } 50% { transform: scale(1.05); opacity: 1; } }
.grow-bar { animation: growb 1.4s cubic-bezier(.25,.9,.3,1) both; transform-origin: left; }
@keyframes growb { from { transform: scaleX(0); } to { transform: scaleX(1); } }
.node-label { font-family: var(--font-mono); font-size: 15px; font-weight: 600; }
"""

ENGINE_JS = """
(function () {
  'use strict';
  var META = window.DECK_META || { total: 0, blocks: [] };
  var slides = Array.prototype.slice.call(document.querySelectorAll('.slide'));
  var total = slides.length;
  var idx = 0;

  var fill = document.getElementById('progress-fill');
  var segs = Array.prototype.slice.call(document.querySelectorAll('#progress .seg'));
  var hudBlock = document.getElementById('hud-block');
  var hudPos = document.getElementById('hud-pos');
  var notesPanel = document.getElementById('notes-panel');
  var notesTime = document.getElementById('notes-time');
  var notesBody = document.getElementById('notes-body');
  var overview = document.getElementById('overview');
  var ovGrid = document.getElementById('ov-grid');
  var notesData = window.SPEAKER_NOTES || [];

  function fragEls(i) { return Array.prototype.slice.call(slides[i].querySelectorAll('.frag')); }
  function fragOrder(a, b) { return (+a.getAttribute('data-step') || 0) - (+b.getAttribute('data-step') || 0); }
  function shownCount(i) {
    var n = 0;
    fragEls(i).forEach(function (el) { if (el.classList.contains('shown')) n++; });
    return n;
  }

  function blockOf(i) {
    for (var k = 0; k < META.blocks.length; k++) {
      if (i + 1 >= META.blocks[k].start && i + 1 <= META.blocks[k].end) return META.blocks[k];
    }
    return META.blocks.length ? META.blocks[META.blocks.length - 1] : { block: 1, start: 1, end: total };
  }

  function render() {
    slides.forEach(function (s, k) {
      s.classList.toggle('active', k === idx);
      s.classList.toggle('before', k < idx);
      if (k !== idx) {
        fragEls(k).forEach(function (el) { el.classList.remove('shown'); });
      }
    });

    var blk = blockOf(idx);
    var doneInBlock = Math.min(Math.max(idx + 1 - blk.start + 1, 1), blk.end - blk.start + 1);
    var lenBlock = blk.end - blk.start + 1;
    segs.forEach(function (seg, k) {
      var b = META.blocks[k];
      if (!b) return;
      var frac;
      if (idx + 1 < b.start) frac = 0;
      else if (idx + 1 >= b.end) frac = 1;
      else frac = doneInBlock / lenBlock;
      var f = seg.querySelector('.seg-fill');
      if (f) f.style.width = (frac * 100).toFixed(1) + '%';
      seg.classList.toggle('lit', idx + 1 >= b.start && idx + 1 <= b.end);
    });
    if (fill) fill.style.width = (((idx + 1) / total) * 100).toFixed(1) + '%';

    if (hudBlock) hudBlock.textContent = 'Bloque ' + blk.block + ' \u00b7 min ' + blk.from + '\u2013' + blk.to;
    if (hudPos) hudPos.textContent = (idx + 1) + ' / ' + total;

    var note = notesData[idx];
    if (note) {
      notesTime.textContent = note.time || '';
      notesBody.innerHTML = note.body || '';
    } else {
      notesTime.textContent = '';
      notesBody.innerHTML = '<p>Sin notas para esta diapositiva.</p>';
    }

    Array.prototype.forEach.call(ovGrid.children, function (item, k) {
      item.classList.toggle('current', k === idx);
    });

    slides[idx].querySelectorAll('canvas[data-chart]').forEach(function (cv) {
      if (cv.__chart) cv.__chart.resize();
    });
  }

  function advance() {
    var fs = fragEls(idx).sort(fragOrder);
    var shown = shownCount(idx);
    if (shown < fs.length) {
      fs[shown].classList.add('shown');
      return;
    }
    if (idx < total - 1) { idx++; render(); }
  }

  function back() {
    var fs = fragEls(idx).sort(fragOrder);
    var shown = shownCount(idx);
    if (shown > 0) {
      fs[shown - 1].classList.remove('shown');
      return;
    }
    if (idx > 0) {
      idx--;
      fragEls(idx).forEach(function (el) { el.classList.add('shown'); });
      render();
    }
  }

  function buildOverview() {
    slides.forEach(function (s, k) {
      var blk = blockOf(k);
      var item = document.createElement('div');
      item.className = 'ov-item';
      var titleEl = s.querySelector('h1.slide-title, .divider h1, .cover h1');
      item.innerHTML =
        '<div class="ov-block">Bloque ' + blk.block + ' \u00b7 ' + blk.from + '\u2013' + blk.to + ' min</div>' +
        '<div class="ov-num">' + (k + 1) + ' / ' + total + '</div>' +
        '<div class="ov-title">' + (titleEl ? titleEl.textContent : 'Diapositiva ' + (k + 1)) + '</div>';
      item.addEventListener('click', function () {
        idx = k;
        fragEls(idx).forEach(function (el) { el.classList.add('shown'); });
        toggleOverview(false);
        render();
      });
      ovGrid.appendChild(item);
    });
  }

  function toggleOverview(force) {
    var open = typeof force === 'boolean' ? force : !overview.classList.contains('open');
    overview.classList.toggle('open', open);
  }

  function toggleNotes() { notesPanel.classList.toggle('open'); }

  function toggleFullscreen() {
    if (document.fullscreenElement) { document.exitFullscreen(); }
    else if (document.documentElement.requestFullscreen) { document.documentElement.requestFullscreen(); }
  }

  document.addEventListener('keydown', function (ev) {
    var key = ev.key;
    if (key === 'ArrowRight' || key === ' ' || key === 'PageDown') { ev.preventDefault(); advance(); }
    else if (key === 'ArrowLeft' || key === 'PageUp') { ev.preventDefault(); back(); }
    else if (key === 'Home') { ev.preventDefault(); idx = 0; render(); }
    else if (key === 'End') { ev.preventDefault(); idx = total - 1; fragEls(idx).forEach(function (el) { el.classList.add('shown'); }); render(); }
    else if (key === 'n' || key === 'N') { toggleNotes(); }
    else if (key === 'g' || key === 'G') { toggleOverview(); }
    else if (key === 'f' || key === 'F') { toggleFullscreen(); }
    else if (key === 'Escape') { toggleOverview(false); }
  });

  var notesClose = document.getElementById('notes-close');
  if (notesClose) notesClose.addEventListener('click', function () { notesPanel.classList.remove('open'); });

  /* ---- Chart.js: defaults + instancias ---- */
  function initCharts() {
    if (typeof window.Chart === 'undefined') {
      document.querySelectorAll('.chart-fallback').forEach(function (el) { el.classList.add('visible'); });
      return;
    }
    Chart.defaults.color = '#475569';
    Chart.defaults.font.family = "'IBM Plex Sans','Segoe UI',sans-serif";
    Chart.defaults.font.size = 14;
    Chart.defaults.borderColor = '#E2E8F0';
    Chart.defaults.plugins.legend.labels.boxWidth = 14;
    var specs = window.CHART_SPECS || {};
    document.querySelectorAll('canvas[data-chart]').forEach(function (cv) {
      var spec = specs[cv.getAttribute('data-chart')];
      if (!spec) return;
      try { cv.__chart = new Chart(cv.getContext('2d'), spec); }
      catch (err) { cv.__chart = null; }
    });
  }

  buildOverview();
  initCharts();
  render();
})();
"""

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>__TITLE__</title>
<meta name="author" content="Alex Prieto Romani">
<meta name="description" content="__DESCRIPTION__">
<style>__CSS__</style>
</head>
<body>
<main id="stage">
__SECTIONS__
</main>

<div id="progress" aria-hidden="true">
__SEGS__
</div>
<div id="progress-line" aria-hidden="true"><div id="progress-fill"></div></div>

<aside id="notes-panel" aria-label="Notas del orador">
  <h2>Notas del orador</h2>
  <div id="notes-time"></div>
  <div id="notes-body"></div>
  <button id="notes-close" type="button">cerrar (N)</button>
</aside>

<div id="overview">
  <h2>Vista general &mdash; 5 bloques &middot; 120 minutos</h2>
  <div class="ov-grid" id="ov-grid"></div>
</div>

<footer id="hud">
  <div class="h-left"><b id="hud-block"></b><span id="hud-pos" style="margin-left:14px"></span></div>
  <div class="h-right">
    <span><kbd>&larr;</kbd><kbd>&rarr;</kbd> navegar</span>
    <span><kbd>N</kbd> notas</span>
    <span><kbd>G</kbd> &iacute;ndice</span>
    <span><kbd>F</kbd> pantalla completa</span>
  </div>
</footer>

<script>window.CHART_SPECS = __CHART_SPECS__;</script>
<script>__CHARTJS__</script>
<script>
if (typeof Chart === 'undefined') {
  document.write('<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.1/dist/chart.umd.min.js"><\\/script>');
}
</script>
<script>window.DECK_META = __META__;</script>
<script>window.SPEAKER_NOTES = __NOTES__;</script>
<script>__ENGINE__</script>
</body>
</html>
"""
