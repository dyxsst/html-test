<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Agente IA · Auditoría Interna</title>
<link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600&family=DM+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>
  *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

  :root {
    --bg: #F7F8FA;
    --surface: #FFFFFF;
    --border: #E4E7ED;
    --text-primary: #111827;
    --text-secondary: #6B7280;
    --text-muted: #9CA3AF;
    --accent: #1B4FD8;
    --accent-light: #EEF2FF;
    --ext-color: #0891B2;
    --ext-light: #ECFEFF;
    --int-color: #059669;
    --int-light: #ECFDF5;
    --output-color: #7C3AED;
    --output-light: #F5F3FF;
    --shadow-sm: 0 1px 3px rgba(0,0,0,0.06), 0 1px 2px rgba(0,0,0,0.04);
    --shadow-md: 0 4px 12px rgba(0,0,0,0.08), 0 2px 4px rgba(0,0,0,0.04);
    --shadow-lg: 0 8px 30px rgba(0,0,0,0.1);
  }

  body {
    font-family: 'DM Sans', sans-serif;
    background: var(--bg);
    color: var(--text-primary);
    min-height: 100vh;
    padding: 40px 24px 60px;
  }

  /* HEADER */
  .header {
    text-align: center;
    margin-bottom: 52px;
    animation: fadeDown 0.6s ease both;
  }
  .header .eyebrow {
    display: inline-block;
    font-family: 'DM Mono', monospace;
    font-size: 11px;
    font-weight: 500;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: var(--accent);
    background: var(--accent-light);
    padding: 4px 12px;
    border-radius: 100px;
    margin-bottom: 14px;
  }
  .header h1 {
    font-size: clamp(22px, 3vw, 34px);
    font-weight: 600;
    color: var(--text-primary);
    letter-spacing: -0.02em;
    line-height: 1.2;
  }
  .header p {
    margin-top: 10px;
    font-size: 15px;
    color: var(--text-secondary);
    font-weight: 300;
  }

  /* MAIN GRID */
  .diagram {
    max-width: 1100px;
    margin: 0 auto;
    display: grid;
    grid-template-columns: 1fr 80px 1fr 80px 1fr;
    grid-template-rows: auto auto auto;
    gap: 0;
    align-items: center;
  }

  /* COLUMN LABELS */
  .col-label {
    text-align: center;
    font-family: 'DM Mono', monospace;
    font-size: 10px;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    font-weight: 500;
    padding-bottom: 16px;
    border-bottom: 1.5px solid var(--border);
    margin-bottom: 28px;
  }
  .col-label.input { color: var(--accent); }
  .col-label.agent { color: var(--text-secondary); }
  .col-label.sources { color: var(--text-secondary); }
  .col-label.output { color: var(--output-color); }
  .col-label-spacer { padding-bottom: 16px; border-bottom: 1.5px solid var(--border); margin-bottom: 28px; }

  /* CARDS */
  .card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 22px 20px;
    box-shadow: var(--shadow-sm);
    position: relative;
    transition: box-shadow 0.2s, transform 0.2s;
  }
  .card:hover {
    box-shadow: var(--shadow-md);
    transform: translateY(-2px);
  }
  .card-icon {
    width: 36px; height: 36px;
    border-radius: 10px;
    display: flex; align-items: center; justify-content: center;
    font-size: 18px;
    margin-bottom: 12px;
  }
  .card-title {
    font-size: 14px;
    font-weight: 600;
    color: var(--text-primary);
    margin-bottom: 6px;
  }
  .card-desc {
    font-size: 12.5px;
    color: var(--text-secondary);
    line-height: 1.55;
    font-weight: 300;
  }

  /* INPUT CARD */
  .card.input-card { border-color: #BFDBFE; }
  .card.input-card .card-icon { background: var(--accent-light); }
  .chat-mock {
    margin-top: 14px;
    background: var(--bg);
    border-radius: 10px;
    padding: 12px 14px;
    border: 1px solid var(--border);
  }
  .chat-line {
    display: flex;
    align-items: flex-start;
    gap: 8px;
    margin-bottom: 8px;
  }
  .chat-line:last-child { margin-bottom: 0; }
  .chat-avatar {
    width: 20px; height: 20px;
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 10px;
    flex-shrink: 0;
    margin-top: 1px;
  }
  .chat-avatar.user { background: var(--accent); color: white; }
  .chat-avatar.ai { background: #F3F4F6; color: var(--text-secondary); }
  .chat-bubble {
    background: white;
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 6px 10px;
    font-size: 11px;
    color: var(--text-primary);
    line-height: 1.4;
  }
  .chat-bubble.ai-bubble {
    background: var(--accent-light);
    border-color: #BFDBFE;
    color: var(--accent);
  }

  /* AGENT CARD */
  .card.agent-card {
    border-color: #E5E7EB;
    background: var(--text-primary);
    color: white;
    grid-column: 3;
  }
  .card.agent-card .card-title { color: white; }
  .card.agent-card .card-desc { color: #9CA3AF; }
  .agent-steps {
    margin-top: 14px;
    display: flex;
    flex-direction: column;
    gap: 8px;
  }
  .agent-step {
    display: flex;
    align-items: center;
    gap: 10px;
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 8px;
    padding: 8px 12px;
  }
  .step-num {
    font-family: 'DM Mono', monospace;
    font-size: 10px;
    color: var(--accent);
    background: rgba(27,79,216,0.2);
    width: 20px; height: 20px;
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    flex-shrink: 0;
    font-weight: 500;
  }
  .step-text {
    font-size: 11.5px;
    color: #D1D5DB;
    line-height: 1.35;
  }

  /* SOURCES COLUMN */
  .sources-col {
    display: flex;
    flex-direction: column;
    gap: 12px;
  }

  .source-group-label {
    font-family: 'DM Mono', monospace;
    font-size: 10px;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    font-weight: 500;
    margin-bottom: 4px;
  }
  .source-group-label.ext { color: var(--ext-color); }
  .source-group-label.int { color: var(--int-color); }

  .source-tag-group {
    background: var(--surface);
    border-radius: 14px;
    border: 1px solid var(--border);
    padding: 16px 18px;
    box-shadow: var(--shadow-sm);
    transition: box-shadow 0.2s, transform 0.2s;
  }
  .source-tag-group:hover {
    box-shadow: var(--shadow-md);
    transform: translateY(-2px);
  }
  .source-tag-group.ext { border-left: 3px solid var(--ext-color); }
  .source-tag-group.int { border-left: 3px solid var(--int-color); }

  .tag-header {
    display: flex;
    align-items: center;
    gap: 8px;
    margin-bottom: 10px;
  }
  .tag-icon {
    font-size: 16px;
  }
  .tag-title {
    font-size: 12.5px;
    font-weight: 600;
  }
  .tag-title.ext { color: var(--ext-color); }
  .tag-title.int { color: var(--int-color); }

  .tags {
    display: flex;
    flex-wrap: wrap;
    gap: 5px;
  }
  .tag {
    font-size: 11px;
    padding: 3px 10px;
    border-radius: 100px;
    font-weight: 400;
    line-height: 1.5;
  }
  .tag.ext {
    background: var(--ext-light);
    color: var(--ext-color);
    border: 1px solid #A5F3FC;
  }
  .tag.int {
    background: var(--int-light);
    color: var(--int-color);
    border: 1px solid #A7F3D0;
  }

  /* OUTPUT CARD */
  .card.output-card {
    border-color: #DDD6FE;
  }
  .card.output-card .card-icon { background: var(--output-light); }
  .dossier-mock {
    margin-top: 14px;
    border: 1px solid #DDD6FE;
    border-radius: 10px;
    overflow: hidden;
  }
  .dossier-header {
    background: var(--output-color);
    padding: 8px 12px;
    display: flex;
    align-items: center;
    gap: 6px;
  }
  .dossier-header span { font-size: 11px; color: white; font-weight: 500; letter-spacing: 0.02em; }
  .dossier-body {
    background: var(--output-light);
    padding: 10px 12px;
    display: flex;
    flex-direction: column;
    gap: 6px;
  }
  .dossier-row {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 11px;
    color: var(--text-secondary);
  }
  .dossier-row::before {
    content: '';
    width: 6px; height: 6px;
    border-radius: 50%;
    background: var(--output-color);
    flex-shrink: 0;
    opacity: 0.6;
  }

  /* ARROWS */
  .arrow-col {
    display: flex;
    align-items: center;
    justify-content: center;
    flex-direction: column;
    gap: 4px;
    padding: 0 4px;
  }
  .arrow-line {
    display: flex;
    align-items: center;
    gap: 3px;
    color: var(--text-muted);
    font-size: 18px;
  }
  .arrow-label {
    font-family: 'DM Mono', monospace;
    font-size: 9px;
    color: var(--text-muted);
    text-align: center;
    letter-spacing: 0.06em;
  }

  /* BIDIRECTIONAL ARROW between agent and sources */
  .bidir {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 6px;
  }
  .bidir-arrow {
    display: flex;
    align-items: center;
    gap: 2px;
    font-size: 15px;
  }
  .bidir-arrow.ext-a { color: var(--ext-color); }
  .bidir-arrow.int-a { color: var(--int-color); }

  /* FOOTER NOTE */
  .footer-note {
    max-width: 1100px;
    margin: 40px auto 0;
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 12px;
    animation: fadeUp 0.8s ease 0.4s both;
  }
  .note-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 14px 16px;
    display: flex;
    align-items: flex-start;
    gap: 10px;
    box-shadow: var(--shadow-sm);
  }
  .note-icon { font-size: 18px; flex-shrink: 0; }
  .note-text { font-size: 12px; color: var(--text-secondary); line-height: 1.5; }
  .note-text strong { color: var(--text-primary); font-weight: 600; display: block; margin-bottom: 2px; }

  /* GRID LAYOUT ASSIGNMENTS */
  .col1 { grid-column: 1; }
  .col2 { grid-column: 2; }
  .col3 { grid-column: 3; }
  .col4 { grid-column: 4; }
  .col5 { grid-column: 5; }
  .row1 { grid-row: 1; }
  .row2 { grid-row: 2; }

  @keyframes fadeDown {
    from { opacity: 0; transform: translateY(-16px); }
    to { opacity: 1; transform: translateY(0); }
  }
  @keyframes fadeUp {
    from { opacity: 0; transform: translateY(12px); }
    to { opacity: 1; transform: translateY(0); }
  }

  .diagram > * {
    animation: fadeUp 0.5s ease both;
  }
  .diagram > *:nth-child(1) { animation-delay: 0.05s; }
  .diagram > *:nth-child(2) { animation-delay: 0.1s; }
  .diagram > *:nth-child(3) { animation-delay: 0.15s; }
  .diagram > *:nth-child(4) { animation-delay: 0.2s; }
  .diagram > *:nth-child(5) { animation-delay: 0.25s; }
  .diagram > *:nth-child(6) { animation-delay: 0.3s; }
  .diagram > *:nth-child(7) { animation-delay: 0.35s; }
  .diagram > *:nth-child(8) { animation-delay: 0.4s; }
  .diagram > *:nth-child(9) { animation-delay: 0.45s; }
  .diagram > *:nth-child(10) { animation-delay: 0.5s; }

  /* responsive */
  @media (max-width: 820px) {
    .diagram {
      grid-template-columns: 1fr;
      grid-template-rows: none;
    }
    .diagram > * { grid-column: 1 !important; grid-row: auto !important; }
    .arrow-col { transform: rotate(90deg); }
    .bidir { flex-direction: row; }
    .footer-note { grid-template-columns: 1fr; }
  }
</style>
</head>
<body>

<header class="header">
  <div class="eyebrow">Piloto · Copilot AI Agents</div>
  <h1>Agente de IA para Estudio Preliminar de Auditoría</h1>
  <p>Flujo de trabajo y arquitectura de fuentes · Auditoría Interna</p>
</header>

<div class="diagram">

  <!-- Col 1: Input -->
  <div class="col1 row1 col-label input">Entrada del Auditor</div>
  <div class="col2 row1 col-label-spacer"></div>
  <div class="col3 row1 col-label agent">Agente IA Copilot</div>
  <div class="col4 row1 col-label-spacer"></div>
  <div class="col5 row1" style="display:flex; flex-direction:column; gap:0; padding-bottom:16px; border-bottom:1.5px solid var(--border); margin-bottom:28px;">
    <div style="font-family:'DM Mono',monospace;font-size:10px;letter-spacing:0.12em;text-transform:uppercase;font-weight:500;color:var(--ext-color); margin-bottom:2px;">Fuentes externas</div>
    <div style="font-family:'DM Mono',monospace;font-size:10px;letter-spacing:0.12em;text-transform:uppercase;font-weight:500;color:var(--int-color);">/ Fuentes internas</div>
  </div>

  <!-- Row 2: main cards -->
  <div class="card input-card col1 row2">
    <div class="card-icon">💬</div>
    <div class="card-title">Interfaz de Chat</div>
    <div class="card-desc">El auditor describe la auditoría a realizar, temática, alcance y puntos de interés clave.</div>
    <div class="chat-mock">
      <div class="chat-line">
        <div class="chat-avatar user">A</div>
        <div class="chat-bubble">Auditoría a TI: controles de acceso y gestión de vulnerabilidades. Marco COBIT e ISO 27001.</div>
      </div>
      <div class="chat-line">
        <div class="chat-avatar ai">🤖</div>
        <div class="chat-bubble ai-bubble">Analizando regulaciones aplicables y procesos internos relevantes…</div>
      </div>
    </div>
  </div>

  <!-- Arrow 1 -->
  <div class="arrow-col col2 row2">
    <div class="arrow-line">→</div>
    <div class="arrow-label">consulta</div>
  </div>

  <!-- Agent card -->
  <div class="card agent-card col3 row2">
    <div class="card-icon" style="background:rgba(255,255,255,0.08)">⚙️</div>
    <div class="card-title">Agente Orchestrator</div>
    <div class="card-desc">Interpreta el contexto, despacha consultas a fuentes y consolida los hallazgos.</div>
    <div class="agent-steps">
      <div class="agent-step">
        <div class="step-num">1</div>
        <div class="step-text">Extrae entidades: tema, marcos regulatorios, áreas de interés</div>
      </div>
      <div class="agent-step">
        <div class="step-num">2</div>
        <div class="step-text">Consulta fuentes externas → recupera leyes, regulaciones y marcos de referencia</div>
      </div>
      <div class="agent-step">
        <div class="step-num">3</div>
        <div class="step-text">Consulta SharePoint interno → recupera procesos, políticas y responsables</div>
      </div>
      <div class="agent-step">
        <div class="step-num">4</div>
        <div class="step-text">Genera pruebas de auditoría sugeridas alineadas a los puntos de interés</div>
      </div>
      <div class="agent-step">
        <div class="step-num">5</div>
        <div class="step-text">Produce dossier estructurado para el estudio preliminar</div>
      </div>
    </div>
  </div>

  <!-- Arrow 2: bidir -->
  <div class="arrow-col col4 row2">
    <div class="bidir">
      <div class="bidir-arrow ext-a">⇄</div>
    </div>
    <div class="arrow-label" style="color:var(--ext-color); margin-bottom:8px;">externos</div>
    <div class="bidir">
      <div class="bidir-arrow int-a">⇄</div>
    </div>
    <div class="arrow-label" style="color:var(--int-color);">internos</div>
  </div>

  <!-- Sources column -->
  <div class="sources-col col5 row2">

    <!-- External sources -->
    <div class="source-tag-group ext">
      <div class="tag-header">
        <span class="tag-icon">🌐</span>
        <span class="tag-title ext">Fuentes Externas</span>
      </div>
      <div class="card-desc" style="margin-bottom:10px; font-size:11.5px;">Documentos públicos, normas y marcos regulatorios en formato PDF</div>
      <div class="tags">
        <span class="tag ext">SBP · Superint. de Bancos</span>
        <span class="tag ext">SMV · Superint. de Valores</span>
        <span class="tag ext">SSRP · Seguros y Reaseguros</span>
        <span class="tag ext">SUGEF</span>
        <span class="tag ext">CONASSIF</span>
        <span class="tag ext">CIMA</span>
        <span class="tag ext">ISO</span>
        <span class="tag ext">NIST</span>
        <span class="tag ext">COBIT</span>
        <span class="tag ext">IIA</span>
        <span class="tag ext">COSO</span>
      </div>
    </div>

    <!-- Internal sources -->
    <div class="source-tag-group int">
      <div class="tag-header">
        <span class="tag-icon">🏢</span>
        <span class="tag-title int">Fuentes Internas · SharePoint</span>
      </div>
      <div class="card-desc" style="margin-bottom:10px; font-size:11.5px;">Políticas, procedimientos y matrices de responsabilidad por área</div>
      <div class="tags">
        <span class="tag int">TI</span>
        <span class="tag int">Operaciones</span>
        <span class="tag int">Cumplimiento</span>
        <span class="tag int">Subsidiarias</span>
        <span class="tag int">Capital Humano</span>
      </div>
    </div>

  </div>

</div>

<!-- Output section -->
<div style="max-width:1100px; margin: 32px auto 0; animation: fadeUp 0.6s ease 0.55s both;">
  <div style="display:flex; align-items:center; gap:12px; margin-bottom:16px;">
    <div style="flex:1; height:1px; background:var(--border);"></div>
    <span style="font-family:'DM Mono',monospace; font-size:10px; letter-spacing:0.12em; text-transform:uppercase; color:var(--output-color); font-weight:500;">Output · Dossier de Estudio Preliminar</span>
    <div style="flex:1; height:1px; background:var(--border);"></div>
  </div>

  <div style="display:grid; grid-template-columns: repeat(4,1fr); gap:12px;">
    
    <div class="card output-card" style="border-top: 3px solid var(--output-color);">
      <div class="card-icon">📋</div>
      <div class="card-title" style="font-size:13px;">Marco Regulatorio Aplicable</div>
      <div class="card-desc">Leyes, normas y estándares vinculados a la auditoría, con referencias y artículos clave.</div>
    </div>

    <div class="card output-card" style="border-top: 3px solid var(--output-color);">
      <div class="card-icon">🗂️</div>
      <div class="card-title" style="font-size:13px;">Procesos & Procedimientos Relevantes</div>
      <div class="card-desc">Documentación interna recuperada de SharePoint, ordenada por relevancia para el alcance.</div>
    </div>

    <div class="card output-card" style="border-top: 3px solid var(--output-color);">
      <div class="card-icon">👥</div>
      <div class="card-title" style="font-size:13px;">Departamentos & Roles Clave</div>
      <div class="card-desc">Áreas y responsables identificados que deben formar parte del proceso de revisión.</div>
    </div>

    <div class="card output-card" style="border-top: 3px solid var(--output-color);">
      <div class="card-icon">🧪</div>
      <div class="card-title" style="font-size:13px;">Pruebas de Auditoría Sugeridas</div>
      <div class="card-desc">Pruebas recomendadas por el agente, alineadas con los puntos de interés definidos.</div>
    </div>

  </div>
</div>

<!-- Footer notes -->
<div class="footer-note">
  <div class="note-card">
    <div class="note-icon">🔒</div>
    <div class="note-text">
      <strong>Seguridad y Gobernanza</strong>
      El agente opera dentro del ecosistema Microsoft 365 / Copilot, respetando los permisos y controles de acceso existentes en SharePoint.
    </div>
  </div>
  <div class="note-card">
    <div class="note-icon">⚡</div>
    <div class="note-text">
      <strong>Valor Inmediato</strong>
      Reduce significativamente el tiempo del estudio preliminar al automatizar la búsqueda y correlación de fuentes regulatorias e internas.
    </div>
  </div>
  <div class="note-card">
    <div class="note-icon">🔄</div>
    <div class="note-text">
      <strong>Proceso Iterativo</strong>
      El auditor puede refinar el alcance desde la interfaz de chat. El agente actualiza el dossier en ciclos hasta llegar al estudio final.
    </div>
  </div>
</div>

</body>
</html>
