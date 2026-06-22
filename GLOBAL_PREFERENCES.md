# Global Developer Preferences

This file defines my personal standards and preferences that apply to
**every project** I work on, regardless of domain or tech stack.

When starting a new project or continuing an existing one, Claude Code
and Claude.ai should read this file and treat it as binding. If a
proposed approach conflicts with anything here, flag it before proceeding.

This file lives at the root of each repo as a reference copy, but the
canonical version is maintained separately and should be propagated to
new projects when they are created.

---

## 1. Privacy — the most important requirement

### 1.1 Definition of "local" or "offline"

When I describe a tool as "local", "offline", or "private", this means:

**Zero network requests at runtime — to anyone, for anything.**

This includes:
- Font CDNs (Google Fonts, Adobe Fonts, Typekit)
- Asset CDNs (Cloudflare, jsDelivr, unpkg, cdnjs)
- Analytics or telemetry services (Google Analytics, Sentry, Mixpanel)
- External APIs of any kind, even for non-sensitive metadata
- Any `<link>`, `<script>`, `<img>`, or `<style>` tag pointing to a
  non-localhost URL
- Any `fetch()`, `XMLHttpRequest`, `requests`, `urllib`, or `httpx` call
  to a non-localhost URL

Do not assume that "local" means only the primary data is local while
supporting resources like fonts or icons can come from the internet.
If I say local, I mean the entire page load is local.

### 1.2 How to satisfy asset needs locally

| Need | Compliant approach |
|---|---|
| Custom fonts | Use system font stacks — no files, no requests |
| Icons | Inline SVG in the HTML file |
| CSS frameworks | Copy only the needed rules into the file |
| JS libraries | Copy into a `static/` folder and serve locally |
| Charting | Use a locally served library or inline SVG/Canvas |

### 1.3 Verification before any release

Before presenting a completed feature, run this check and confirm it passes:

```bash
grep -rn "googleapis\|gstatic\|cdnjs\|jsdelivr\|unpkg\|cloudflare\|fonts\." \
  --include="*.html" --include="*.js" --include="*.css" --include="*.py" .
```

The result must be empty (excluding comments that reference these as
examples of what NOT to use).

---

## 2. Security defaults

### 2.1 No innerHTML with unescaped external data
Any value derived from user input, file parsing, API responses, or AI model
output must be HTML-escaped before DOM injection. Always include and use
an `esc()` helper in frontend JavaScript:

```javascript
function esc(str) {
  if (str === null || str === undefined) return '';
  return String(str)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
}
```

### 2.2 No dynamic code execution
- No `eval()` or `new Function()`
- No `setTimeout`/`setInterval` with string arguments
- No dynamic `import()` from external URLs

### 2.3 No secrets in source files
- No API keys, tokens, passwords, or credentials in any committed file
- Use `.env` files for secrets and ensure `.env` is in `.gitignore`
- No hardcoded absolute file paths that expose home directory structure

### 2.4 Dependency hygiene
Before adding any new library or package:
1. State what it does and why it is needed
2. Confirm it makes no network calls at runtime
3. Check whether a simpler built-in alternative exists
4. Confirm it will be installed locally, not loaded from a CDN

---

## 3. Git discipline

### 3.1 Staging files
- **Never run `git add .` or `git add -A`**
- Always stage files individually: `git add filename1 filename2`
- Before staging, state which files are being added and why

### 3.2 Branching
- Never commit directly to `main`
- Create a `feature/` or `fix/` branch for every change
- Branch naming: `feature/short-description` or `fix/short-description`
- Do not merge branches — leave merges for me to review and approve

### 3.3 Commit messages
- Start with the version number if a version bump is included
- Be specific: describe what changed, not just that something changed
- Good: `v1.0.1 — replace Google Fonts with system font stack, add esc() helper`
- Bad: `update index.html`

### 3.4 After completing work
Always print a summary of:
- Which files were changed
- What git commands were run
- What the current branch is
- What I need to do to test and merge

---

## 4. Code quality

### 4.1 No unnecessary complexity
Prefer the simplest solution that meets the requirements. Do not introduce
a framework, pattern, or abstraction unless the simpler alternative has a
specific, demonstrable limitation.

### 4.2 Separation of concerns
Keep backend logic and frontend code in separate files. Do not embed large
blocks of HTML, CSS, or JavaScript inside Python strings.

### 4.3 Comments
Add comments for non-obvious decisions — especially when a simpler approach
was considered and rejected. Future maintainers (including me) should
understand why, not just what.

### 4.4 No silent failures
Functions that can fail should either raise a clear exception or return a
value that forces the caller to handle the error case. Avoid swallowing
exceptions with bare `except: pass`.

---

## 5. Proposals — architecture first

### 5.1 Required before any implementation

Before writing any code for a new feature, a refactor, or any change that
touches more than one file, Claude must first produce:

1. **A plain-text architecture diagram** showing the high-level structure
   and data flow of the proposed solution
2. **A verbal description** of the same flow in plain English

Implementation must not begin until I have reviewed and confirmed the proposal.
This step is mandatory — do not skip it even for changes that seem small or obvious.

### 5.2 Diagram format

Use plain text with ASCII arrows and boxes. No external tools, no image files,
no Mermaid syntax that requires a renderer. The diagram must be readable
directly in the terminal or in a chat response.

A block diagram style is preferred — boxes representing components or files,
arrows showing data flow and call direction, labels on arrows describing
what is passed. Example of the expected style:

```
[ Browser / index.html ]
        |
        | HTTP POST /parse (PDF bytes + state)
        v
[ FastAPI — server.py ]
        |
        |-- pdfplumber ---------> [ Text extraction ]
        |                                 |
        |                                 v
        |                    [ Page classifier ]
        |                         |         |
        |                    div_detail   usgo_pct
        |                         |         |
        |                    [ Regex extractor ]
        |
        |-- pdf2image + poppler -> [ Page images ]
        |                                 |
        |                                 v
        |                    [ Ollama qwen2.5vl:3b ]
        |                         |
        |                    [ JSON parser ]
        |
        +----> [ compute_usgo() ] <-- [ data/usgo/2024.json ]
        |
        v
[ JSON response ]
        |
        v
[ Browser renders account card ]
```

### 5.3 Verbal description

After the diagram, provide 3–6 sentences in plain English describing:
- What the user does to trigger the flow
- What each major component does
- Where data enters and exits the system
- Any meaningful decision points or branches

Avoid implementation detail (variable names, line numbers) in the verbal
description — keep it at the level a non-programmer could follow.

### 5.4 Wait for confirmation

After presenting the diagram and description, explicitly ask:

> "Does this match your expectation? Shall I proceed with implementation?"

Do not begin writing or editing any files until confirmation is received.

---

## 6. Versioning

All projects use semantic versioning: `MAJOR.MINOR.PATCH`

| Increment | When |
|---|---|
| PATCH (x.x.1) | Bug fix, no new features |
| MINOR (x.1.0) | New feature, backward compatible |
| MAJOR (2.0.0) | Significant rewrite or breaking change |

When bumping a version, always update it consistently everywhere it appears
(Python constants, HTML badges, README changelog, etc.).

---

## 7. Communication preferences

### 6.1 Flag conflicts before acting
If a task as described would violate any requirement in this file or in
the project's `REQUIREMENTS.md`, stop and flag the conflict explicitly
before writing any code. Do not silently work around it.

### 6.2 Propose before adding dependencies
Never add a new package, library, or tool without proposing it first and
receiving explicit confirmation.

### 6.3 Summarise what changed
After completing any task, provide a concise summary of:
- What was changed and why
- Which files were modified
- What the next step is (if applicable)

### 6.4 Prefer reversible changes
When multiple approaches exist, prefer the one that is easiest to undo.
Use feature branches, avoid destructive operations, and keep backups of
files before significant edits.
