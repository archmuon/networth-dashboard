# Requirements — 1099 Tax Parser

This document defines the binding requirements for this project.
Claude Code and Claude.ai must read this before making any changes.
If a proposed change conflicts with any requirement here, stop and
flag the conflict before proceeding.

---

## 1. Privacy & network isolation

### 1.1 Absolute network isolation
This tool must operate with **zero network requests** at runtime — not even
to trusted third parties. This means:

- No CDN-hosted fonts, scripts, stylesheets, or assets of any kind
- No analytics, telemetry, or error reporting
- No external API calls of any kind, even for non-sensitive data
- No web search or data enrichment at runtime

**Compliant:** Loading a file from `localhost` or the local filesystem  
**Non-compliant:** Loading Google Fonts from `fonts.googleapis.com`  
**Non-compliant:** Any `fetch()` or `XMLHttpRequest` to a non-localhost URL  
**Non-compliant:** Any `<link>`, `<script>`, or `<img>` tag pointing to an
external domain

### 1.2 Font and asset policy
All fonts, icons, and static assets must be either:
- System fonts (preferred — zero files, zero requests), or
- Self-hosted in a `static/` folder within the repo and served by the local server

Google Fonts, Adobe Fonts, Cloudflare, jsDelivr, unpkg, and similar CDNs
are not permitted even if the content they serve is benign.

### 1.3 AI/ML models
All AI inference must run locally via Ollama. No calls to OpenAI, Anthropic,
Hugging Face inference endpoints, or any other hosted model API.

### 1.4 Verification checklist
Before any release, confirm:
- [ ] No external URLs in any `<link>`, `<script>`, `<img>`, or `<style>` tag
- [ ] No external URLs in any `fetch()`, `XMLHttpRequest`, or `import()` call
- [ ] No external URLs in any Python `urllib`, `requests`, or `httpx` call
      other than `http://localhost:11434` (Ollama)
- [ ] `grep -r "googleapis\|gstatic\|cdnjs\|jsdelivr\|unpkg\|cloudflare" .`
      returns no results in source files

---

## 2. Security

### 2.1 No innerHTML with unescaped user-derived data
Any value that originates from a parsed document (brokerage name, ticker symbol,
tax year, dollar amounts, etc.) must be HTML-escaped before being injected into
the DOM via `innerHTML`. Use a dedicated `esc()` helper function — never insert
raw strings from external data sources directly into HTML.

```javascript
// Required helper — must be present in index.html
function esc(str) {
  if (str === null || str === undefined) return '';
  return String(str)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
}
```

### 2.2 No execution of dynamic code
- No `eval()`
- No `new Function()`
- No `setTimeout` or `setInterval` with string arguments

### 2.3 No secrets in source
- No API keys, tokens, or credentials in any source file
- No hardcoded file paths that expose the user's home directory structure

---

## 3. Architecture constraints

### 3.1 File structure
The split between `server.py` (backend) and `index.html` (frontend) must be
maintained. Do not merge them back into a single file.

### 3.2 No new runtime dependencies without approval
Do not add new Python packages or JavaScript libraries without explicitly
proposing them to the user first and receiving confirmation. State:
- What the dependency does
- Why it is needed
- Whether a simpler alternative exists
- Whether it makes any network calls

### 3.3 Local-only data storage
No data from parsed documents may be written to disk, logged, or cached
between sessions. Each parse is stateless — results exist only in the
browser's memory until the page is refreshed or closed.

---

## 4. Versioning & git hygiene

### 4.1 Versioning scheme
Semantic versioning: `MAJOR.MINOR.PATCH`  
Update `VERSION` in `server.py`, the badge in `index.html`, and the
Changelog in `README.md` with every release.

### 4.2 Git rules
- Never run `git add .` or `git add -A` — stage files individually by name
- Never commit directly to `main` — always use a feature or fix branch
- Branch naming: `feature/short-description` or `fix/short-description`
- Do not merge branches — leave that for the user to review and approve

---

## 5. Proposals before implementation

Before implementing any change to this project that touches more than one
file, or that changes data flow or architecture, Claude must follow the
proposal process defined in `GLOBAL_PREFERENCES.md` section 5:

- Produce a plain-text block diagram of the proposed change
- Provide a verbal description of the flow
- Wait for explicit confirmation before writing any code

For this project specifically, the diagram must show how the change
affects the pipeline:

```
PDF input → pdfplumber → classifier → [regex or vision] → compute_usgo → JSON response → browser
```

Any proposal that adds a new stage, changes data flow between stages, or
introduces a new file must show where it fits in this pipeline.

---

## 6. Known issues to fix (backlog)

| Issue | Severity | Target version |
|---|---|---|
| Google Fonts CDN loaded in index.html | Medium — leaks IP | v1.0.1 |
| innerHTML used without escaping in renderAccount() | Low — local tool | v1.0.1 |
| Fidelity brokerage adapter incomplete | Medium | v1.2.0 |
| USGO data hardcoded for 2024 only | Medium | v1.1.0 |
