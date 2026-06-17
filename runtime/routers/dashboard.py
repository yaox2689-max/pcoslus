"""PCOS Dashboard

Simple web UI to visualize the decision process.
"""

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from typing import Dict, Any

router = APIRouter(tags=["dashboard"])


@router.get("/dashboard", response_class=HTMLResponse)
async def dashboard():
    """PCOS Dashboard - Visualize decision process."""
    return """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PCOS Dashboard</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body { font-family: 'Segoe UI', system-ui, sans-serif; background: #0f172a; color: #e2e8f0; }
        .container { max-width: 1200px; margin: 0 auto; padding: 20px; }
        h1 { color: #60a5fa; margin-bottom: 20px; }

        .grid { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }
        .card { background: #1e293b; border-radius: 12px; padding: 20px; border: 1px solid #334155; }
        .card h2 { color: #94a3b8; font-size: 14px; text-transform: uppercase; margin-bottom: 15px; }

        .input-group { margin-bottom: 15px; }
        .input-group label { display: block; color: #94a3b8; margin-bottom: 5px; font-size: 13px; }
        textarea, input, select { width: 100%; padding: 10px; background: #0f172a; border: 1px solid #334155; border-radius: 8px; color: #e2e8f0; font-size: 14px; }
        textarea { height: 80px; resize: vertical; }

        button { background: #3b82f6; color: white; border: none; padding: 12px 24px; border-radius: 8px; cursor: pointer; font-size: 14px; font-weight: 500; }
        button:hover { background: #2563eb; }
        button:disabled { background: #475569; cursor: not-allowed; }

        .status { padding: 10px; border-radius: 8px; margin-bottom: 15px; font-size: 13px; }
        .status.loading { background: #1e3a5f; color: #60a5fa; }
        .status.success { background: #14532d; color: #4ade80; }
        .status.error { background: #7f1d1d; color: #f87171; }

        .result { display: none; }
        .result.active { display: block; }

        .metric { display: inline-block; background: #0f172a; padding: 8px 12px; border-radius: 6px; margin: 4px; }
        .metric .label { font-size: 11px; color: #64748b; }
        .metric .value { font-size: 18px; font-weight: bold; color: #60a5fa; }

        .badge { display: inline-block; padding: 4px 8px; border-radius: 4px; font-size: 12px; font-weight: 500; }
        .badge.fast { background: #166534; color: #4ade80; }
        .badge.slow { background: #713f12; color: #fbbf24; }

        .list { list-style: none; }
        .list li { padding: 8px 0; border-bottom: 1px solid #1e293b; font-size: 13px; }
        .list li:last-child { border-bottom: none; }

        .bar { height: 8px; background: #334155; border-radius: 4px; overflow: hidden; margin-top: 4px; }
        .bar-fill { height: 100%; border-radius: 4px; transition: width 0.3s; }

        .option-card { background: #0f172a; padding: 15px; border-radius: 8px; margin-bottom: 10px; }
        .option-card .name { font-weight: 500; margin-bottom: 8px; }
        .option-card .scores { display: grid; grid-template-columns: repeat(5, 1fr); gap: 8px; }
        .option-card .score { text-align: center; }
        .option-card .score .label { font-size: 10px; color: #64748b; }
        .option-card .score .value { font-size: 16px; font-weight: bold; }

        #timeline { position: relative; padding-left: 30px; }
        #timeline::before { content: ''; position: absolute; left: 10px; top: 0; bottom: 0; width: 2px; background: #334155; }
        .timeline-item { position: relative; margin-bottom: 20px; }
        .timeline-item::before { content: ''; position: absolute; left: -24px; top: 4px; width: 12px; height: 12px; border-radius: 50%; background: #3b82f6; border: 2px solid #0f172a; }
        .timeline-item .time { font-size: 11px; color: #64748b; }
        .timeline-item .content { font-size: 13px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🧠 PCOS Decision Dashboard</h1>

        <div class="grid">
            <!-- Input Panel -->
            <div class="card">
                <h2>📝 Decision Input</h2>
                <div class="input-group">
                    <label>Question</label>
                    <textarea id="question" placeholder="What decision are you facing?"></textarea>
                </div>
                <div class="input-group">
                    <label>Context (optional)</label>
                    <textarea id="context" placeholder="Background information, constraints, etc." style="height: 60px;"></textarea>
                </div>
                <div class="input-group">
                    <label>Category</label>
                    <select id="category">
                        <option value="">Auto-detect</option>
                        <option value="startup">Startup</option>
                        <option value="product">Product</option>
                        <option value="tech">Technology</option>
                        <option value="business">Business</option>
                        <option value="hiring">Hiring</option>
                        <option value="career">Career</option>
                    </select>
                </div>
                <button id="submit" onclick="askPCOS()">Ask PCOS</button>
                <div id="status" class="status" style="display: none;"></div>
            </div>

            <!-- Process Panel -->
            <div class="card">
                <h2>⚙️ Decision Process</h2>
                <div id="timeline">
                    <div class="timeline-item">
                        <div class="time">Step 1</div>
                        <div class="content">Waiting for input...</div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Results -->
        <div id="results" class="result" style="margin-top: 20px;">
            <div class="grid">
                <!-- Decision Panel -->
                <div class="card">
                    <h2>💡 Decision</h2>
                    <div style="margin-bottom: 15px;">
                        <span id="thinking-mode" class="badge"></span>
                        <span id="confidence" class="metric" style="float: right;">
                            <span class="label">Confidence</span>
                            <span class="value">-</span>
                        </span>
                    </div>
                    <div id="recommendation" style="font-size: 16px; line-height: 1.6; margin-bottom: 15px;"></div>
                    <div>
                        <h3 style="font-size: 13px; color: #94a3b8; margin-bottom: 10px;">Reasoning Chain</h3>
                        <ul id="reasoning" class="list"></ul>
                    </div>
                </div>

                <!-- Context Panel -->
                <div class="card">
                    <h2>🎯 Context Used</h2>
                    <div style="margin-bottom: 15px;">
                        <h3 style="font-size: 13px; color: #94a3b8; margin-bottom: 10px;">Values Aligned</h3>
                        <div id="values"></div>
                    </div>
                    <div style="margin-bottom: 15px;">
                        <h3 style="font-size: 13px; color: #94a3b8; margin-bottom: 10px;">Beliefs Used</h3>
                        <ul id="beliefs" class="list"></ul>
                    </div>
                    <div>
                        <h3 style="font-size: 13px; color: #94a3b8; margin-bottom: 10px;">Key Risks</h3>
                        <ul id="risks" class="list"></ul>
                    </div>
                </div>
            </div>

            <!-- Options Evaluation -->
            <div class="card" style="margin-top: 20px;">
                <h2>📊 Options Evaluation</h2>
                <div id="options"></div>
            </div>
        </div>

        <!-- Journal -->
        <div class="card" style="margin-top: 20px;">
            <h2>📜 Recent Decisions</h2>
            <button onclick="loadJournal()" style="margin-bottom: 15px; background: #475569;">Refresh</button>
            <div id="journal"></div>
        </div>
    </div>

    <script>
        const API = 'http://localhost:8001';

        function showStatus(msg, type = 'loading') {
            const el = document.getElementById('status');
            el.style.display = 'block';
            el.className = `status ${type}`;
            el.textContent = msg;
        }

        function updateTimeline(steps) {
            const el = document.getElementById('timeline');
            el.innerHTML = steps.map((s, i) => `
                <div class="timeline-item">
                    <div class="time">Step ${i + 1}</div>
                    <div class="content">${s}</div>
                </div>
            `).join('');
        }

        async function askPCOS() {
            const question = document.getElementById('question').value.trim();
            if (!question) { showStatus('Please enter a question', 'error'); return; }

            const context = document.getElementById('context').value.trim();
            const category = document.getElementById('category').value;

            document.getElementById('submit').disabled = true;
            showStatus('Analyzing decision...', 'loading');
            updateTimeline(['Parsing input...', 'Loading context...', 'Building prompt...']);

            try {
                const res = await fetch(`${API}/decide/`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ question, context, category })
                });

                if (!res.ok) throw new Error(`HTTP ${res.status}`);
                const data = await res.json();

                showStatus('Decision complete!', 'success');
                updateTimeline([
                    'Input parsed ✓',
                    `Topics detected: ${data.beliefs_used?.length || 0} beliefs loaded ✓`,
                    `Thinking mode: ${data.thinking_mode} ✓`,
                    `Options evaluated: ${data.options_evaluated?.length || 0} ✓`,
                    'Decision made ✓'
                ]);

                renderResult(data);
                loadJournal();
            } catch (e) {
                showStatus(`Error: ${e.message}`, 'error');
            } finally {
                document.getElementById('submit').disabled = false;
            }
        }

        function renderResult(data) {
            document.getElementById('results').className = 'result active';

            // Thinking mode
            const modeEl = document.getElementById('thinking-mode');
            modeEl.textContent = data.thinking_mode.toUpperCase();
            modeEl.className = `badge ${data.thinking_mode}`;

            // Confidence
            document.querySelector('#confidence .value').textContent =
                `${(data.confidence * 100).toFixed(0)}%`;

            // Recommendation
            document.getElementById('recommendation').textContent = data.recommendation;

            // Reasoning
            document.getElementById('reasoning').innerHTML =
                (data.reasoning_chain || []).map(r => `<li>${r}</li>`).join('');

            // Values
            document.getElementById('values').innerHTML =
                (data.values_alignment || []).map(v => `<span class="badge" style="background: #1e3a5f; margin: 2px;">${v.split(':')[0]}</span>`).join('');

            // Beliefs
            document.getElementById('beliefs').innerHTML =
                (data.beliefs_used || []).map(b => `<li>${b}</li>`).join('');

            // Risks
            document.getElementById('risks').innerHTML =
                (data.key_risks || []).map(r => `<li style="color: #f87171;">⚠️ ${r}</li>`).join('');

            // Options
            document.getElementById('options').innerHTML =
                (data.options_evaluated || []).map(opt => `
                    <div class="option-card">
                        <div class="name">${opt.option}</div>
                        <div class="scores">
                            ${renderScore('Values', opt.score.value_alignment)}
                            ${renderScore('Beliefs', opt.score.belief_support)}
                            ${renderScore('Resources', opt.score.resource_feasibility)}
                            ${renderScore('Risk', opt.score.risk_acceptability)}
                            ${renderScore('Learning', opt.score.learning_potential)}
                        </div>
                        <div style="text-align: right; margin-top: 8px;">
                            <span class="metric">
                                <span class="label">Total</span>
                                <span class="value">${(opt.score.weighted_total * 100).toFixed(0)}%</span>
                            </span>
                        </div>
                    </div>
                `).join('');
        }

        function renderScore(label, value) {
            const pct = (value * 100).toFixed(0);
            const color = value > 0.7 ? '#4ade80' : value > 0.4 ? '#fbbf24' : '#f87171';
            return `
                <div class="score">
                    <div class="label">${label}</div>
                    <div class="value" style="color: ${color}">${pct}%</div>
                    <div class="bar"><div class="bar-fill" style="width: ${pct}%; background: ${color};"></div></div>
                </div>
            `;
        }

        async function loadJournal() {
            try {
                const res = await fetch(`${API}/decide/journal?limit=5`);
                const data = await res.json();
                document.getElementById('journal').innerHTML = data.length ?
                    data.map(d => `
                        <div style="padding: 10px; background: #0f172a; border-radius: 8px; margin-bottom: 8px;">
                            <div style="font-size: 13px;">${d.question}</div>
                            <div style="font-size: 12px; color: #64748b; margin-top: 4px;">
                                <span class="badge ${d.thinking_mode}" style="font-size: 10px;">${d.thinking_mode}</span>
                                Confidence: ${(d.confidence * 100).toFixed(0)}%
                                • ${new Date(d.timestamp).toLocaleString()}
                            </div>
                        </div>
                    `).join('') :
                    '<div style="color: #64748b;">No decisions yet</div>';
            } catch (e) {
                document.getElementById('journal').innerHTML = `<div style="color: #f87171;">Error loading journal</div>`;
            }
        }

        // Load journal on start
        loadJournal();
    </script>
</body>
</html>
"""
