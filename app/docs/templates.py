"""
HTML templates for the API documentation pages.

All CSS/HTML is assembled via string replacement (not f-strings) so that
curly braces in CSS rules and JSON examples work without escaping.
"""

# ---------------------------------------------------------------------------
# Stylesheet
# ---------------------------------------------------------------------------

_CSS = """
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

:root {
    --sidebar-w: 272px;
    --bg-body: #09090b;
    --bg-sidebar: #0c0c0f;
    --bg-card: #141419;
    --bg-card-hover: #1a1a20;
    --bg-code: #0a0a0d;
    --bg-table-header: #111116;
    --text-1: #fafafa;
    --text-2: #a1a1aa;
    --text-3: #52525b;
    --accent: #6366f1;
    --accent-2: #818cf8;
    --accent-glow: rgba(99, 102, 241, 0.08);
    --green: #22c55e;
    --green-bg: rgba(34, 197, 94, 0.1);
    --amber: #f59e0b;
    --amber-bg: rgba(245, 158, 11, 0.1);
    --red: #ef4444;
    --red-bg: rgba(239, 68, 68, 0.1);
    --blue: #3b82f6;
    --blue-bg: rgba(59, 130, 246, 0.1);
    --border: #1e1e24;
    --border-2: #27272a;
    --radius: 12px;
    --radius-sm: 8px;
    --transition: 0.2s ease;
    --font-sans: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    --font-mono: 'JetBrains Mono', 'Fira Code', 'Cascadia Code', monospace;
}

html { scroll-behavior: smooth; }

body {
    font-family: var(--font-sans);
    background: var(--bg-body);
    color: var(--text-2);
    line-height: 1.7;
    -webkit-font-smoothing: antialiased;
}

/* gradient bar */
body::before {
    content: '';
    position: fixed; top: 0; left: 0;
    width: 100%; height: 2px;
    background: linear-gradient(90deg, var(--accent), #a855f7, #ec4899, var(--accent));
    background-size: 200% 100%;
    animation: gradient-bar 4s ease infinite;
    z-index: 1000;
}
@keyframes gradient-bar {
    0%   { background-position: 0% 50%; }
    50%  { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

/* scrollbar */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: var(--border-2); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: var(--text-3); }

/* -------- Sidebar -------- */
.sidebar {
    position: fixed; top: 0; left: 0;
    width: var(--sidebar-w); height: 100vh;
    background: var(--bg-sidebar);
    border-right: 1px solid var(--border);
    display: flex; flex-direction: column;
    z-index: 100; overflow-y: auto;
}
.sidebar-header {
    padding: 28px 24px 20px;
    border-bottom: 1px solid var(--border);
}
.logo {
    font-size: 1.25rem; font-weight: 700;
    color: var(--text-1); letter-spacing: -0.02em;
}
.logo-sub {
    font-size: 0.75rem; color: var(--text-3); margin-top: 4px;
}
.sidebar-nav { padding: 16px 12px; flex: 1; }
.nav-section {
    font-size: 0.6875rem; text-transform: uppercase;
    letter-spacing: 0.08em; color: var(--text-3);
    padding: 16px 12px 8px; font-weight: 600;
}
.nav-link {
    display: flex; align-items: center; gap: 10px;
    padding: 10px 12px; border-radius: var(--radius-sm);
    color: var(--text-2); text-decoration: none;
    font-size: 0.875rem; font-weight: 500;
    transition: all var(--transition);
    position: relative; margin-bottom: 2px;
}
.nav-link:hover { background: var(--accent-glow); color: var(--text-1); }
.nav-link.active { background: var(--accent-glow); color: var(--accent-2); }
.nav-link.active::before {
    content: ''; position: absolute; left: 0; top: 50%;
    transform: translateY(-50%);
    width: 3px; height: 20px;
    background: var(--accent); border-radius: 0 2px 2px 0;
}
.nav-icon { font-size: 1rem; width: 20px; text-align: center; }
.nav-divider { height: 1px; background: var(--border); margin: 12px; }

/* -------- Main -------- */
.main { margin-left: var(--sidebar-w); min-height: 100vh; }
.page-header {
    padding: 48px 48px 32px;
    border-bottom: 1px solid var(--border);
    position: relative; overflow: hidden;
}
.page-header::after {
    content: ''; position: absolute;
    top: 50%; left: 20%; width: 60%; height: 120px;
    background: radial-gradient(ellipse, rgba(99,102,241,0.07), transparent 70%);
    transform: translateY(-50%); pointer-events: none;
}
.page-title {
    font-size: 2.25rem; font-weight: 800;
    background: linear-gradient(135deg, #e0e7ff 0%, #818cf8 50%, #6366f1 100%);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    background-clip: text; letter-spacing: -0.03em; line-height: 1.2;
    background-size: 200% 200%;
    animation: gradient-shift 8s ease infinite;
    position: relative; z-index: 1;
}
@keyframes gradient-shift {
    0%   { background-position: 0% 50%; }
    50%  { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}
.page-subtitle {
    font-size: 1.0625rem; color: var(--text-3);
    margin-top: 8px; max-width: 600px;
    position: relative; z-index: 1;
}
.content {
    padding: 32px 48px 80px; max-width: 920px;
    animation: fade-in 0.4s ease-out;
}
@keyframes fade-in {
    from { opacity: 0; transform: translateY(12px); }
    to   { opacity: 1; transform: translateY(0); }
}

/* -------- Section -------- */
.section { margin-bottom: 40px; }
.section-title {
    font-size: 1.375rem; font-weight: 700;
    color: var(--text-1); margin-bottom: 16px;
    letter-spacing: -0.02em;
}
.section-desc { margin-bottom: 16px; line-height: 1.7; }

/* -------- Card -------- */
.card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    overflow: hidden;
    transition: border-color var(--transition);
}
.card:hover { border-color: var(--border-2); }
.card-body { padding: 20px 24px; }
.card + .card { margin-top: 16px; }

/* -------- Table -------- */
table { width: 100%; border-collapse: collapse; }
thead th {
    background: var(--bg-table-header);
    text-align: left; padding: 12px 16px;
    font-size: 0.75rem; text-transform: uppercase;
    letter-spacing: 0.06em; color: var(--text-3);
    font-weight: 600; border-bottom: 1px solid var(--border);
}
tbody td {
    padding: 12px 16px; border-bottom: 1px solid var(--border);
    font-size: 0.875rem; vertical-align: top;
}
tbody tr:last-child td { border-bottom: none; }
tbody tr:hover { background: var(--accent-glow); }

/* -------- Code -------- */
code {
    font-family: var(--font-mono); font-size: 0.8125rem;
    background: var(--bg-code); padding: 2px 6px;
    border-radius: 4px; color: var(--accent-2);
}
pre {
    background: var(--bg-code);
    border: 1px solid var(--border);
    border-radius: var(--radius-sm);
    padding: 20px 24px; overflow-x: auto;
    margin: 12px 0; position: relative;
}
pre code {
    background: none; padding: 0;
    font-size: 0.8125rem; line-height: 1.8;
    color: var(--text-2);
}
.copy-btn {
    position: absolute; top: 8px; right: 8px;
    padding: 4px 10px; font-size: 0.6875rem;
    background: var(--border-2); color: var(--text-3);
    border: none; border-radius: 4px; cursor: pointer;
    font-family: var(--font-sans);
    transition: all var(--transition);
}
.copy-btn:hover { background: var(--accent); color: white; }
.copy-btn.copied { background: var(--green); color: white; }

/* -------- Badges -------- */
.badge {
    display: inline-flex; align-items: center;
    padding: 2px 8px; border-radius: 4px;
    font-size: 0.6875rem; font-weight: 600;
    letter-spacing: 0.04em; text-transform: uppercase;
}
.badge-post { background: var(--green-bg); color: var(--green); }
.badge-get  { background: var(--blue-bg);  color: var(--blue); }
.badge-required { background: var(--amber-bg); color: var(--amber); font-size: 0.625rem; }
.badge-optional { background: rgba(161,161,170,0.08); color: var(--text-3); font-size: 0.625rem; }

/* -------- Endpoint -------- */
.endpoint {
    display: flex; align-items: center; gap: 12px;
    padding: 16px 20px; background: var(--bg-code);
    border: 1px solid var(--border);
    border-radius: var(--radius-sm); margin: 12px 0;
}
.endpoint-path {
    font-family: var(--font-mono); font-size: 0.9375rem;
    color: var(--text-1); font-weight: 500;
}

/* -------- Model card row -------- */
.model-card {
    display: flex; justify-content: space-between; align-items: center;
    padding: 14px 20px; border-bottom: 1px solid var(--border);
}
.model-card:last-child { border-bottom: none; }
.model-name {
    font-family: var(--font-mono); font-weight: 600;
    color: var(--accent-2); font-size: 0.875rem;
}
.model-desc { color: var(--text-3); font-size: 0.8125rem; margin-top: 2px; }

/* -------- Callout -------- */
.callout {
    padding: 16px 20px; border-radius: var(--radius-sm);
    border-left: 3px solid; margin: 16px 0; font-size: 0.875rem;
}
.callout a { color: inherit; text-decoration: underline; }
.callout-info    { background: var(--blue-bg);  border-color: var(--blue); }
.callout-warning { background: var(--amber-bg); border-color: var(--amber); }
.callout-tip     { background: var(--green-bg); border-color: var(--green); }

/* -------- Content typography -------- */
.content h3 {
    font-size: 1rem; font-weight: 600;
    color: var(--text-1); margin: 28px 0 12px;
}
.content ul {
    padding-left: 24px; margin: 8px 0;
}
.content ul li {
    padding: 4px 0; color: var(--text-2);
}
.content ul li::marker { color: var(--accent); }
.content a { color: var(--accent-2); text-decoration: none; }
.content a:hover { text-decoration: underline; }

/* -------- Provider link card -------- */
.provider-link {
    display: flex; justify-content: space-between; align-items: center;
    padding: 18px 20px; border-bottom: 1px solid var(--border);
    text-decoration: none; transition: background var(--transition);
}
.provider-link:last-child { border-bottom: none; }
.provider-link:hover { background: var(--accent-glow); }
.provider-link-arrow {
    color: var(--accent-2); font-size: 0.875rem;
    transition: transform var(--transition);
}
.provider-link:hover .provider-link-arrow { transform: translateX(4px); }

/* -------- Responsive -------- */
@media (max-width: 768px) {
    .sidebar {
        position: relative; width: 100%; height: auto;
        border-right: none; border-bottom: 1px solid var(--border);
    }
    .sidebar-nav {
        display: flex; gap: 4px; padding: 8px 12px; overflow-x: auto;
    }
    .nav-section, .nav-divider { display: none; }
    .nav-link { white-space: nowrap; padding: 8px 12px; }
    .nav-link.active::before { display: none; }
    .main { margin-left: 0; }
    .page-header { padding: 32px 24px 24px; }
    .page-title { font-size: 1.75rem; }
    .content { padding: 24px 24px 60px; }
}
"""

# ---------------------------------------------------------------------------
# JavaScript — copy button on code blocks
# ---------------------------------------------------------------------------

_JS = """
document.querySelectorAll('pre').forEach(function(pre) {
    var btn = document.createElement('button');
    btn.className = 'copy-btn';
    btn.textContent = 'Copy';
    btn.addEventListener('click', function() {
        var code = pre.querySelector('code');
        var text = code ? code.textContent : pre.textContent;
        navigator.clipboard.writeText(text).then(function() {
            btn.textContent = 'Copied!';
            btn.classList.add('copied');
            setTimeout(function() {
                btn.textContent = 'Copy';
                btn.classList.remove('copied');
            }, 2000);
        });
    });
    pre.appendChild(btn);
});
"""

# ---------------------------------------------------------------------------
# Navigation items:  (key, icon, label, href)
# ---------------------------------------------------------------------------

_NAV_ITEMS = [
    ("overview", "📖", "Overview", "/docs"),
    ("groq",     "⚡", "Groq",     "/docs/groq"),
    ("sarvam",   "🌏", "Sarvam",   "/docs/sarvam"),
]

# ---------------------------------------------------------------------------
# Base HTML shell  —  placeholders use $NAME$ syntax
# ---------------------------------------------------------------------------

_BASE_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>$TITLE$ — VTS Docs</title>
    <meta name="description" content="Documentation for the Voice Transcription Service API">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
    <style>$CSS$</style>
</head>
<body>
    <aside class="sidebar">
        <div class="sidebar-header">
            <div class="logo">🎙️ VTS Docs</div>
            <div class="logo-sub">Voice Transcription Service</div>
        </div>
        <nav class="sidebar-nav">
            <div class="nav-section">Documentation</div>
            $NAV$
            <div class="nav-divider"></div>
            <div class="nav-section">Tools</div>
            <a href="/swagger" class="nav-link" target="_blank">
                <span class="nav-icon">🔧</span> Swagger UI ↗
            </a>
        </nav>
    </aside>
    <main class="main">
        <div class="page-header">
            <h1 class="page-title">$PAGE_TITLE$</h1>
            <p class="page-subtitle">$PAGE_SUBTITLE$</p>
        </div>
        <div class="content">
            $CONTENT$
        </div>
    </main>
    <script>$JS$</script>
</body>
</html>"""


def _render(
    title: str,
    page_title: str,
    page_subtitle: str,
    content: str,
    active: str,
) -> str:
    """Assemble a complete HTML page."""
    nav_html = ""
    for key, icon, label, href in _NAV_ITEMS:
        cls = "nav-link active" if key == active else "nav-link"
        nav_html += (
            f'<a href="{href}" class="{cls}">'
            f'<span class="nav-icon">{icon}</span> {label}</a>\n'
        )

    return (
        _BASE_HTML
        .replace("$TITLE$", title)
        .replace("$PAGE_TITLE$", page_title)
        .replace("$PAGE_SUBTITLE$", page_subtitle)
        .replace("$NAV$", nav_html)
        .replace("$CONTENT$", content)
        .replace("$CSS$", _CSS)
        .replace("$JS$", _JS)
    )


# ===================================================================
# Page: Overview
# ===================================================================

def overview() -> str:
    content = """
<section class="section">
    <h2 class="section-title">Introduction</h2>
    <p class="section-desc">
        The Voice Transcription Service (VTS) provides a <strong style="color:var(--text-1)">unified API</strong>
        for converting audio to text using multiple transcription providers.
        Send an audio file or a public URL, choose your provider and model, and VTS
        handles routing, normalisation, and error mapping — returning a clean, consistent result.
    </p>
</section>

<section class="section">
    <h2 class="section-title">Quick Start</h2>
    <p class="section-desc">Transcribe a local file with one <code>curl</code> command:</p>
    <pre><code>curl -X POST http://localhost:8000/v1/transcribe \\
  -F "provider=groq" \\
  -F "model=whisper-large-v3-turbo" \\
  -F "api_key=YOUR_API_KEY" \\
  -F 'options={}' \\
  -F "file=@recording.mp3"</code></pre>
</section>

<section class="section">
    <h2 class="section-title">Transcribe Endpoint</h2>
    <div class="endpoint">
        <span class="badge badge-post">POST</span>
        <span class="endpoint-path">/v1/transcribe</span>
    </div>
    <p class="section-desc">
        Transcribes audio from an uploaded file or a publicly accessible URL.
        The request body must be <code>multipart/form-data</code>.
    </p>

    <h3>Request Parameters</h3>
    <div class="card">
        <table>
            <thead>
                <tr><th>Parameter</th><th>Type</th><th>Required</th><th>Description</th></tr>
            </thead>
            <tbody>
                <tr>
                    <td><code>provider</code></td>
                    <td><code>string</code></td>
                    <td><span class="badge badge-required">Required</span></td>
                    <td>Transcription provider — <code>groq</code> or <code>sarvam</code></td>
                </tr>
                <tr>
                    <td><code>model</code></td>
                    <td><code>string</code></td>
                    <td><span class="badge badge-required">Required</span></td>
                    <td>Model identifier valid for the chosen provider</td>
                </tr>
                <tr>
                    <td><code>api_key</code></td>
                    <td><code>string</code></td>
                    <td><span class="badge badge-required">Required</span></td>
                    <td>Your API key for the chosen provider</td>
                </tr>
                <tr>
                    <td><code>options</code></td>
                    <td><code>string</code></td>
                    <td><span class="badge badge-optional">Optional</span></td>
                    <td>JSON string of provider-specific options. Defaults to <code>{}</code></td>
                </tr>
                <tr>
                    <td><code>file</code></td>
                    <td><code>file</code></td>
                    <td><span class="badge badge-optional">One of *</span></td>
                    <td>Audio file upload (max 25 MB)</td>
                </tr>
                <tr>
                    <td><code>audio_url</code></td>
                    <td><code>string</code></td>
                    <td><span class="badge badge-optional">One of *</span></td>
                    <td>Public URL pointing to an audio file (max 25 MB)</td>
                </tr>
            </tbody>
        </table>
    </div>
    <div class="callout callout-info">
        <strong>Audio source:</strong> Provide exactly one of <code>file</code> or
        <code>audio_url</code>. Sending both or neither returns a <code>400</code> error.
    </div>
    <div class="callout callout-warning">
        <strong>Note:</strong> The <code>options</code> field is a <em>JSON-encoded string</em>, not
        a JSON object. Wrap it in single quotes in curl:
        <code>-F 'options={"language_code":"en"}'</code>
    </div>
</section>

<section class="section">
    <h2 class="section-title">Response Format</h2>
    <pre><code>{
    "transcript": "The transcribed text content...",
    "language_code": "en",
    "raw_provider_response": { ... }
}</code></pre>
    <div class="card">
        <table>
            <thead>
                <tr><th>Field</th><th>Type</th><th>Description</th></tr>
            </thead>
            <tbody>
                <tr>
                    <td><code>transcript</code></td>
                    <td><code>string</code></td>
                    <td>The transcribed text</td>
                </tr>
                <tr>
                    <td><code>language_code</code></td>
                    <td><code>string | null</code></td>
                    <td>Detected or specified language code (provider-dependent)</td>
                </tr>
                <tr>
                    <td><code>raw_provider_response</code></td>
                    <td><code>object | null</code></td>
                    <td>Complete unmodified response from the provider SDK</td>
                </tr>
            </tbody>
        </table>
    </div>
</section>

<section class="section">
    <h2 class="section-title">Error Handling</h2>
    <div class="card">
        <table>
            <thead>
                <tr><th>Status</th><th>Condition</th></tr>
            </thead>
            <tbody>
                <tr><td><code>400</code></td><td>Invalid request — bad provider, model, options, or audio source conflict</td></tr>
                <tr><td><code>422</code></td><td>Audio fetch error — URL unreachable, wrong content-type, or empty payload</td></tr>
                <tr><td><code>502</code></td><td>Provider error — upstream transcription provider returned an error</td></tr>
            </tbody>
        </table>
    </div>
    <p class="section-desc" style="margin-top:12px">Provider errors return a structured body:</p>
    <pre><code>{
    "provider": "groq",
    "code": "transcription_failed",
    "message": "Detailed error message from the provider"
}</code></pre>
</section>

<section class="section">
    <h2 class="section-title">Supported Providers</h2>
    <div class="card">
        <a href="/docs/groq" class="provider-link">
            <div>
                <div class="model-name">⚡ Groq</div>
                <div class="model-desc">Lightning-fast inference with OpenAI Whisper models on Groq LPU hardware</div>
            </div>
            <span class="provider-link-arrow">View docs →</span>
        </a>
        <a href="/docs/sarvam" class="provider-link">
            <div>
                <div class="model-name">🌏 Sarvam</div>
                <div class="model-desc">Indian language specialisation with Saarika and Saaras model families</div>
            </div>
            <span class="provider-link-arrow">View docs →</span>
        </a>
    </div>
</section>

<section class="section">
    <h2 class="section-title">Health Check</h2>
    <div class="endpoint">
        <span class="badge badge-get">GET</span>
        <span class="endpoint-path">/health</span>
    </div>
    <pre><code>{ "status": "ok" }</code></pre>
</section>
"""
    return _render(
        title="API Documentation",
        page_title="API Documentation",
        page_subtitle="Everything you need to integrate with the Voice Transcription Service.",
        content=content,
        active="overview",
    )


# ===================================================================
# Page: Groq
# ===================================================================

def groq() -> str:
    content = """
<section class="section">
    <h2 class="section-title">Overview</h2>
    <p class="section-desc">
        Groq provides ultra-fast audio transcription powered by OpenAI's Whisper models
        running on Groq's <strong style="color:var(--text-1)">LPU (Language Processing Unit)</strong> hardware.
        Ideal for low-latency transcription where speed is critical.
    </p>
    <div class="callout callout-tip">
        <strong>Get an API key:</strong> Sign up at
        <a href="https://console.groq.com" target="_blank">console.groq.com</a>
        to obtain your Groq API key.
    </div>
</section>

<section class="section">
    <h2 class="section-title">Supported Models</h2>
    <div class="card">
        <div class="model-card">
            <div>
                <div class="model-name">whisper-large-v3</div>
                <div class="model-desc">Highest accuracy — best for complex audio, accents, and noisy environments</div>
            </div>
        </div>
        <div class="model-card">
            <div>
                <div class="model-name">whisper-large-v3-turbo</div>
                <div class="model-desc">Optimised for speed with near-equivalent accuracy</div>
            </div>
            <span class="badge" style="background:var(--green-bg);color:var(--green);font-size:0.625rem">RECOMMENDED</span>
        </div>
    </div>
</section>

<section class="section">
    <h2 class="section-title">Provider Options</h2>
    <p class="section-desc">
        Pass these inside the <code>options</code> JSON string.
    </p>
    <div class="card">
        <table>
            <thead>
                <tr><th>Option</th><th>Type</th><th>Description</th></tr>
            </thead>
            <tbody>
                <tr>
                    <td><code>language_code</code></td>
                    <td><code>string</code></td>
                    <td>ISO 639-1 code (e.g. <code>en</code>, <code>es</code>, <code>hi</code>).
                        Improves accuracy when the language is known. Omit for auto-detection.</td>
                </tr>
                <tr>
                    <td><code>prompt</code></td>
                    <td><code>string</code></td>
                    <td>Optional context or vocabulary to guide the model.
                        Useful for domain-specific terminology, proper nouns, or acronyms.</td>
                </tr>
            </tbody>
        </table>
    </div>
</section>

<section class="section">
    <h2 class="section-title">Examples</h2>

    <h3>File Upload</h3>
    <pre><code>curl -X POST http://localhost:8000/v1/transcribe \\
  -F "provider=groq" \\
  -F "model=whisper-large-v3-turbo" \\
  -F "api_key=YOUR_GROQ_API_KEY" \\
  -F 'options={"language_code": "en"}' \\
  -F "file=@meeting_recording.mp3"</code></pre>

    <h3>URL Fetch</h3>
    <pre><code>curl -X POST http://localhost:8000/v1/transcribe \\
  -F "provider=groq" \\
  -F "model=whisper-large-v3" \\
  -F "api_key=YOUR_GROQ_API_KEY" \\
  -F 'options={"prompt": "Discussion about Kubernetes, Docker, and CI/CD pipelines"}' \\
  -F "audio_url=https://example.com/podcast.mp3"</code></pre>

    <h3>Sample Response</h3>
    <pre><code>{
    "transcript": "Hello, welcome to the meeting. Today we will discuss...",
    "language_code": "en",
    "raw_provider_response": {
        "text": "Hello, welcome to the meeting. Today we will discuss...",
        "language": "en",
        "duration": 42.5,
        "segments": [ ... ]
    }
}</code></pre>
</section>

<section class="section">
    <h2 class="section-title">Response Details</h2>
    <p class="section-desc">
        Groq returns responses in <code>verbose_json</code> format, which includes:
    </p>
    <div class="card">
        <div class="card-body">
            <ul>
                <li><strong style="color:var(--text-1)">Language detection</strong> — automatically identifies the spoken language</li>
                <li><strong style="color:var(--text-1)">Segment timestamps</strong> — per-segment start/end times in <code>raw_provider_response.segments</code></li>
                <li><strong style="color:var(--text-1)">Duration</strong> — total audio duration in seconds</li>
            </ul>
        </div>
    </div>
</section>
"""
    return _render(
        title="Groq Provider",
        page_title="Groq Provider",
        page_subtitle="Ultra-fast Whisper transcription on Groq LPU hardware.",
        content=content,
        active="groq",
    )


# ===================================================================
# Page: Sarvam
# ===================================================================

def sarvam() -> str:
    content = """
<section class="section">
    <h2 class="section-title">Overview</h2>
    <p class="section-desc">
        Sarvam AI specialises in <strong style="color:var(--text-1)">Indian language speech recognition</strong>
        with state-of-the-art models designed for the linguistic diversity of the Indian subcontinent.
        Two model families cover different use-cases: <em>Saarika</em> for general-purpose STT and
        <em>Saaras</em> for advanced multilingual workloads.
    </p>
    <div class="callout callout-tip">
        <strong>Get an API key:</strong> Sign up at
        <a href="https://www.sarvam.ai" target="_blank">sarvam.ai</a>
        to obtain your API subscription key.
    </div>
</section>

<section class="section">
    <h2 class="section-title">Saarika — General Purpose</h2>
    <div class="card">
        <div class="model-card">
            <div>
                <div class="model-name">saarika:v1</div>
                <div class="model-desc">First-generation model</div>
            </div>
        </div>
        <div class="model-card">
            <div>
                <div class="model-name">saarika:v2</div>
                <div class="model-desc">Improved accuracy and language coverage</div>
            </div>
        </div>
        <div class="model-card">
            <div>
                <div class="model-name">saarika:v2.5</div>
                <div class="model-desc">Enhanced noise handling and robustness</div>
            </div>
        </div>
        <div class="model-card">
            <div>
                <div class="model-name">saarika:flash</div>
                <div class="model-desc">Optimised for speed with reduced latency</div>
            </div>
        </div>
    </div>
</section>

<section class="section">
    <h2 class="section-title">Saaras — Advanced Multilingual</h2>
    <div class="card">
        <div class="model-card">
            <div>
                <div class="model-name">saaras:v3</div>
                <div class="model-desc">Advanced multilingual model with mode support</div>
            </div>
        </div>
        <div class="model-card">
            <div>
                <div class="model-name">saaras:v3-realtime</div>
                <div class="model-desc">Real-time optimised variant of v3</div>
            </div>
        </div>
        <div class="model-card">
            <div>
                <div class="model-name">saaras:v4</div>
                <div class="model-desc">Latest generation — highest accuracy across Indian languages</div>
            </div>
            <span class="badge" style="background:var(--green-bg);color:var(--green);font-size:0.625rem">RECOMMENDED</span>
        </div>
        <div class="model-card">
            <div>
                <div class="model-name">saaras:v4-multispk</div>
                <div class="model-desc">Multi-speaker diarisation support</div>
            </div>
        </div>
    </div>
</section>

<section class="section">
    <h2 class="section-title">Provider Options</h2>
    <p class="section-desc">
        Pass these inside the <code>options</code> JSON string.
    </p>
    <div class="card">
        <table>
            <thead>
                <tr><th>Option</th><th>Type</th><th>Applies to</th><th>Description</th></tr>
            </thead>
            <tbody>
                <tr>
                    <td><code>language_code</code></td>
                    <td><code>string</code></td>
                    <td>All models</td>
                    <td>BCP-47 language tag (e.g. <code>hi-IN</code>, <code>ta-IN</code>, <code>en-IN</code>)</td>
                </tr>
                <tr>
                    <td><code>with_timestamps</code></td>
                    <td><code>boolean</code></td>
                    <td>All models</td>
                    <td>When <code>true</code>, include word-level timestamps in the response</td>
                </tr>
                <tr>
                    <td><code>mode</code></td>
                    <td><code>string</code></td>
                    <td><code>saaras:*</code> only</td>
                    <td>Transcription mode — <code>transcribe</code>, <code>translate</code>, or <code>verbatim</code></td>
                </tr>
            </tbody>
        </table>
    </div>
    <div class="callout callout-info">
        <strong>Note:</strong> The <code>mode</code> parameter is <em>only</em> accepted by
        Saaras-family models (<code>saaras:v3</code>, <code>saaras:v3-realtime</code>,
        <code>saaras:v4</code>, <code>saaras:v4-multispk</code>). It is silently ignored
        for Saarika models.
    </div>
</section>

<section class="section">
    <h2 class="section-title">Examples</h2>

    <h3>File Upload — Hindi</h3>
    <pre><code>curl -X POST http://localhost:8000/v1/transcribe \\
  -F "provider=sarvam" \\
  -F "model=saaras:v4" \\
  -F "api_key=YOUR_SARVAM_API_KEY" \\
  -F 'options={"language_code": "hi-IN"}' \\
  -F "file=@interview.wav"</code></pre>

    <h3>URL Fetch — Tamil with Timestamps</h3>
    <pre><code>curl -X POST http://localhost:8000/v1/transcribe \\
  -F "provider=sarvam" \\
  -F "model=saarika:v2.5" \\
  -F "api_key=YOUR_SARVAM_API_KEY" \\
  -F 'options={"language_code": "ta-IN", "with_timestamps": true}' \\
  -F "audio_url=https://example.com/speech.wav"</code></pre>

    <h3>Saaras with Mode</h3>
    <pre><code>curl -X POST http://localhost:8000/v1/transcribe \\
  -F "provider=sarvam" \\
  -F "model=saaras:v4" \\
  -F "api_key=YOUR_SARVAM_API_KEY" \\
  -F 'options={"language_code": "hi-IN", "mode": "translate"}' \\
  -F "file=@lecture.mp3"</code></pre>

    <h3>Sample Response</h3>
    <pre><code>{
    "transcript": "नमस्ते, आज हम चर्चा करेंगे...",
    "language_code": "hi-IN",
    "raw_provider_response": {
        "transcript": "नमस्ते, आज हम चर्चा करेंगे...",
        "language_code": "hi-IN"
    }
}</code></pre>
</section>

<section class="section">
    <h2 class="section-title">SDK Note</h2>
    <div class="card">
        <div class="card-body">
            <p class="section-desc" style="margin-bottom:0">
                The Sarvam SDK is <strong style="color:var(--text-1)">synchronous</strong>.
                VTS automatically offloads each call to a background thread via
                <code>asyncio.to_thread()</code>, so the async event loop is never blocked.
                No action is needed on your part — this is handled transparently.
            </p>
        </div>
    </div>
</section>
"""
    return _render(
        title="Sarvam Provider",
        page_title="Sarvam Provider",
        page_subtitle="Indian language speech recognition with Saarika and Saaras models.",
        content=content,
        active="sarvam",
    )
