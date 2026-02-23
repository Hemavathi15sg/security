# Exercise 1: GitHub Agent Security Review

**Duration**: 20 minutes  
**Expected Time to Complete**: 20 min

---

## 🎯 Learning Objectives

By the end of this exercise, you will:

✅ Launch Copilot CLI interactive agent for code analysis  
✅ Use conversational prompts to discover OWASP Top 10 vulnerabilities  
✅ Identify SQL injection, XSS, hardcoded secrets, and weak dependencies  
✅ Understand how AI agents reason about security issues  
✅ Document findings and generate GitHub issues from agent output  

---

## 📖 Scenario Context

You're the lead security analyst. Executive team is asking: **"Is SecureTrails ready for launch?"**

Your task: Use Copilot Agent to review the application code and identify security vulnerabilities. The agent will help you spot issues that might be missed in manual review. You need to find and document at least 5 security issues.

---

## 🔍 Task Overview

You'll analyze the SecureTrails application using Copilot CLI to discover:
- SQL Injection vulnerabilities
- Cross-Site Scripting (XSS) issues
- Hardcoded secrets/credentials
- Broken authentication
- Insecure dependencies
- Weak cryptography

---

## 📋 Step-by-Step Instructions

### Step 1: Launch Copilot CLI & Analyze Flask Backend

**Objective**: Use the interactive Copilot CLI to scan the Flask application for security vulnerabilities.

Navigate to the SecureTrails repository:
```bash
cd securetrails-vulnerable
```

Launch the Copilot CLI interactive session:
```bash
copilot
```

This opens an **interactive agent session** where you can have a conversation with Copilot. You'll see:
```
Welcome to GitHub Copilot CLI
Type your prompt and press Enter to start. Type /help for commands.
```

#### Slash Commands Available:
- `/login` - Authenticate with GitHub
- `/model` - Select Claude Sonnet 4.5, Claude Sonnet 4, or GPT-5 (currently Sonnet 4.5)
- `/autopilot` or `Shift+Tab` - Toggle Autopilot mode (agent completes tasks autonomously)
- `/experimental` - Enable experimental features
- `/help` - Show all commands
- `/exit` - Exit the session

#### Analyze Flask Backend:

In the Copilot CLI prompt, paste this security analysis request:

```
Analyze the SecureTrails Flask application for OWASP Top 10 vulnerabilities.
Review app.py and identify:
1. SQL injection in database queries (line numbers where user input touches DB)
2. Hardcoded secrets/credentials (API keys, JWT secrets, passwords)
3. Weak authentication (session handling, password hashing)
4. CORS misconfigurations allowing inappropriate origins
5. XSS entry points (unescaped template rendering)
Provide file paths, exact line numbers, severity level, and remediation for each.
```

**Copilot's Response:**
The interactive agent will analyze the code and provide findings like:
```
FLASK APPLICATION SECURITY ANALYSIS
====================================

CRITICAL FINDINGS:
1. SQL Injection (app.py:47)
   - Line: database.execute(f"SELECT * FROM trails WHERE id={request.args.get('id')}")
   - Issue: User input directly interpolated into SQL query
   - Fix: Use parameterized queries

2. Hardcoded JWT Secret (app.py:12)
   - Line: JWT_SECRET = "super-secret-key-12345"
   - Issue: Secret exposed in source code
   - Fix: Move to environment variable

[... more findings ...]
```

**Your Task:**
- [ ] Type your security analysis prompt in Copilot CLI
- [ ] Review the agent's findings carefully
- [ ] Note file paths and line numbers
- [ ] Document the severity of each issue

---

### Step 2: Continue Analysis - XSS Vulnerabilities in Templates

**Objective**: Use Copilot CLI to identify Cross-Site Scripting (XSS) vulnerabilities in templates.

In the **same Copilot CLI session**, continue the conversation:

```
Now analyze templates/trails.html and templates/login.html for XSS vulnerabilities.
Check for:
1. HTML rendered without escaping (unsafe Jinja2 usage)
2. Direct innerHTML manipulation in JavaScript
3. Event handler injection points (onclick, onerror attributes)
4. DOM-based XSS from user-controlled data
List specific lines where templates render user input unsafely.
```

**What to Look For:**
- `{{ user_input }}` without `| escape` filter
- `{% autoescape false %}` disabling escaping
- Direct string concatenation in template loops

**Copilot's Response Example:**
```
XSS VULNERABILITIES IN TEMPLATES
==================================

HIGH SEVERITY:
1. Unescaped Comment Rendering (templates/trails.html:89)
   - Line: <p>{{ trail.comments }}</p>
   - Issue: User comments rendered without HTML escaping
   - Attack: <img src=x onerror="alert('XSS')">
   - Fix: Use {{ trail.comments | escape }} or default autoescape

2. Direct innerHTML Usage (static/js/app.js:42)
   - document.getElementById('comments').innerHTML = userInput;
   - Issue: Directly assigns user data to DOM
   
[... more findings ...]
```

**Your Task:**
- [ ] Review Copilot's XSS findings
- [ ] Identify ≥2 XSS attack vectors
- [ ] Note which are stored vs. reflected XSS

---

### Step 3: Identify Hardcoded Secrets & Credentials

**Objective**: Detect exposed sensitive information in the codebase.

Continuing in your Copilot CLI session, ask the agent:

```
Search the SecureTrails codebase for hardcoded secrets, API keys, and credentials.
Check app.py, .env.example, and configuration files for:
1. Database passwords or connection strings with credentials
2. JWT signs or API keys not parameterized
3. AWS credentials, OAuth tokens, or encryption keys
4. Any sensitive strings that should be environment variables instead
List file paths, line numbers, and the exposed secret type.
```

**Copilot's Response Example:**
```
HARDCODED SECRETS FOUND
=======================

CRITICAL:
1. JWT Secret in app.py (line 12)
   Secret: "super-secret-key-12345"
   Risk: Exposes session signing key

2. Database Password in .env.example (line 3)
   DB_PASSWORD = "password123"
   Risk: Credentials leaked to anyone with repo access

3. AWS API Key in app.py (line 18)
   REGIONS = "us-east-1" 
   AWS_KEY_ID = "AKIA..."
   
MEDIUM:
4. Debug mode credentials in config.py

[... more secrets ...]
```

**Your Task:**
- [ ] Identify ≥3 exposed credentials
- [ ] Understand the risk of each exposure
- [ ] Document which should move to environment variables
- [ ] Note the scope of exposure (local dev only? production?)

---

### Step 4: Analyze JavaScript for Client-Side Vulnerabilities

**Objective**: Check frontend code for DOM-based attacks and unsafe operations.

Continue in Copilot CLI:

```
Review static/js/app.js for JavaScript security vulnerabilities including:
1. DOM-based XSS (innerHTML, eval, unsafe DOM manipulation)
2. Missing input validation before API calls
3. CSRF token not included in state-changing requests
4. Sensitive data exposed in browser console
5. Unsafe eval() or Function() constructors
6. Direct URL construction without validation
Provide line numbers and the specific vulnerability.
```

**Copilot's Response Example:**
```
JAVASCRIPT VULNERABILITIES
===========================

HIGH:
1. Unsafe innerHTML Assignment (app.js:42)
   document.getElementById('comments').innerHTML = userComments;
   Issue: Directly assigns user data, XSS opportunity
   Fix: Use .textContent or sanitize with DOMPurify

2. eval() on User Data (app.js:67)
   eval(userCode);
   Issue: Allows arbitrary code execution
   Fix: Never use eval()

3. Missing CSRF Token (app.js:89)
   fetch('/api/update-trail', {...})
   Issue: No anti-CSRF token in POST request
   Fix: Include CSRF token from DOM

MEDIUM:
4. Debug Data in Console (app.js:105)
   console.log('User token:', authToken);
   Issue: Sensitive data logged to browser console
   
[... more findings ...]
```

**Your Task:**
- [ ] Identify ≥2 DOM-based vulnerabilities
- [ ] Note the specific JavaScript methods creating risk
- [ ] Document realistic attack scenarios

---

### Step 5: Check Dependencies for Known Vulnerabilities

**Objective**: Identify outdated packages with known CVEs.

In Copilot CLI, ask the agent to analyze dependencies:

```
I have a Python requirements.txt file with package dependencies.
Analyze each package version and identify:
1. Any known security vulnerabilities (CVEs)
2. Packages that are significantly outdated
3. Packages with critical/high severity security issues
4. Recommended safe upgrade versions for each vulnerable package
Provide the package name, current version, CVE details, and suggested upgrade.
```

Show Copilot the requirements.txt content, or ask it to analyze:
```
requirements.txt contains:
Flask==1.1.0
requests==2.24.0
SQLAlchemy==1.3.0
Jinja2==2.11.0
Werkzeug==0.16.0

For each, report known vulnerabilities.
```

**Copilot's Response Example:**
```
DEPENDENCY VULNERABILITY ANALYSIS
===================================

CRITICAL:
1. Flask 1.1.0 → Multiple CVEs (upgrade to 2.3+)
   - CVE-2021-29453: Bypass of gettext lookups
   - CVE-2021-21330: SSRF vulnerability
   Action: Upgrade to Flask==2.3.0 or later

2. Werkzeug 0.16.0 → Path traversal (upgrade to 2.3+)
   - CVE-2021-29454: Path traversal in safe_join()

HIGH:
3. requests 2.24.0 → HTTP smuggling (upgrade to 2.28+)
   - CVE-2021-33503: Incorrect handling of newlines
   Action: Upgrade to requests==2.28.0 or later

4. SQLAlchemy 1.3.0 → SQL injection vectors
   Action: Upgrade to SQLAlchemy==2.0.0

5. Jinja2 2.11.0 → Template injection risks
   Action: Upgrade to Jinja2==3.1.0

[... more packages ...]
```

**Your Task:**
- [ ] Note all dependencies with vulnerabilities
- [ ] Record the severity level (CRITICAL/HIGH/MEDIUM)
- [ ] List the recommended upgrade versions
- [ ] Understand the security implication of each CVE

---

### Step 6: Create GitHub Issue with Comprehensive Findings

**Objective**: Consolidate all findings into a GitHub issue.

You now have comprehensive security analysis from Copilot CLI. **Still in the Copilot CLI session**, ask the agent to help generate the issue:

```
Based on all the vulnerabilities we just identified (SQL injection, XSS, hardcoded secrets, weak dependencies), 
generate the exact GitHub CLI command I should run to create an issue titled "[SECURITY] Exercise 1: SecureTrails Audit" 
with labels "security,exercise".

The issue body should include:
1. CRITICAL findings (SQL injection, hardcoded secrets)
2. HIGH findings (XSS, weak auth, vulnerable dependencies)
3. MEDIUM findings (debug logs, etc.)
4. For each finding: file path, line numbers, severity, description, and recommended fix
5. A summary assessment: 'Ready for production?' (Yes/No/Needs Review)
6. Next steps for remediation

Output the complete gh issue create command with the full body text that I can copy and run.
```

**Copilot CLI Will Output:**
```
gh issue create \
  --title "[SECURITY] Exercise 1: SecureTrails Audit" \
  --label "security,exercise" \
  --body "## Security Audit Results

### CRITICAL (2 issues)
- SQL Injection in app.py:47
  File: app.py, Line: 47
  Description: Unsanitized user input in SQL query
  Fix: Use parameterized queries with SQLAlchemy ORM

- Hardcoded JWT Secret in app.py:12
  File: app.py, Line: 12
  Description: JWT signing key exposed in source code
  Fix: Move to environment variable

### HIGH (3 issues)
- XSS in templates/trails.html:89
[... etc ...]"
```

**Your Task:**
1. [ ] Copy the generated command from Copilot CLI
2. [ ] Exit Copilot CLI (`/exit` or Ctrl+C)
3. [ ] Run the copied issue creation command:
   ```bash
   gh issue create --title "[SECURITY]..." [rest of command]
   ```
4. [ ] Verify the issue was created in your GitHub repository

**Alternative: If Copilot Needs Formatting Direction**

If the output is too long or needs reformatting, you can ask within Copilot CLI:
```
Format that as a markdown table instead of a list for the CRITICAL findings section.
```

Or ask for a more concise version:
```
Create a shorter version suitable for an executive summary - just the count of issues by severity and top 3 actionable fixes.
```

---

## ✅ Acceptance Criteria

- [ ] Launched `copilot` interactive CLI successfully
- [ ] Analyzed Flask app (app.py) for SQL injection, hardcoded secrets, weak auth
- [ ] Identified XSS vulnerabilities in templates (escaping issues)
- [ ] Found ≥3 exposed credentials in code/config
- [ ] Analyzed JavaScript for DOM-based vulnerabilities
- [ ] Checked dependencies (requirements.txt) against known CVEs
- [ ] Asked Copilot to generate GitHub issue creation command
- [ ] Created GitHub issue with findings grouped by severity
- [ ] Issue includes file paths, line numbers, severity, and fixes
- [ ] Assessment documented: "Ready for production?" (Yes/No/Needs Review)

---

## 🖼️ Expected Output

### Copilot CLI Interactive Session

When you launch `copilot`, the analysis conversation looks like:

```
$ copilot
Welcome to GitHub Copilot CLI
Type your prompt and press Enter to start. Type /help for commands.

> Analyze the SecureTrails Flask application for OWASP Top 10 vulnerabilities...
[Copilot thinking...]

Flask Application Security Analysis  
====================================

CRITICAL FINDINGS (2):
1. SQL Injection (app.py:47)
   - database.execute(f"SELECT * FROM trails WHERE id={request.args.get('id')}")
   - User input directly interpolated into SQL query
   - Fix: Use parameterized queries (SQLAlchemy ORM, prepared statements)

2. Hardcoded JWT Secret (app.py:12)
   - JWT_SECRET = "super-secret-key-12345"
   - Signing key exposed in source code
   - Fix: Move to environment variable, rotate key

HIGH FINDINGS (4):
3. XSS in Templates (templates/trails.html:89)
   - {{ trail.comments }} rendered without escaping
   - Fix: Use {{ trail.comments | escape }} or default autoescape

4. Weak Password Hashing (app.py:200)
   - Using MD5 instead of bcrypt
   - Fix: Import bcrypt, use bcrypt.hashpw()

5. CORS Misconfiguration (app.py:5)
   - @cross_origin() with default '*' origin
   - Fix: Specify specific allowed origins

6. Exposed .env Example (credentials listed)
   - File: .env.example contains real looking credentials
   - Fix: Use placeholder values only

MEDIUM FINDINGS (1):
7. Vulnerable Dependencies (multiple packages outdated)

> Now generate a GitHub issue command...
[Copilot generates gh issue create command]
```

### What You'll See in Copilot CLI

✅ Real-time analysis as Copilot reviews your code  
✅ Line-by-line vulnerability details  
✅ Severity ratings and remediation guidance  
✅ Ability to ask follow-up questions  
✅ Generated commands ready to copy-paste  

### Modes Available While in Copilot CLI

- **Normal Mode** (default): Copilot responds to your prompts
- **Autopilot Mode** (`Shift+Tab` or `/autopilot`): Agent completes tasks autonomously without asking
- **Model Selection** (`/model`): Choose Claude Sonnet 4.5, Sonnet 4, or GPT-5

---

## 🆘 Troubleshooting

### Issue: "copilot: command not found"
```bash
# Install Copilot CLI if not already installed
# macOS/Linux with Homebrew:
brew install copilot-cli

# Windows with WinGet:
winget install GitHub.Copilot

# Or with npm (all platforms):
npm install -g @github/copilot
```

### Issue: "Not authenticated" or login prompt appears
```bash
# In Copilot CLI, run login command
/login

# Or exit and use PAT authentication
# Set GH_TOKEN or GITHUB_TOKEN environment variable
export GH_TOKEN="your_fine_grained_pat_with_copilot_scope"
copilot
```

### Issue: "No response from agent"
```bash
# Try simpler prompt first
> Analyze app.py for SQL injection

# If still stuck, try changing mode
# Press Shift+Tab to cycle through modes
# Or type: /model (to select a different AI model)
```

### Issue: "Output is too verbose or truncated"
```bash
# Ask in Copilot CLI for format adjustment
> Can you provide that in a shorter format?
> Show just the CRITICAL findings first
> Make it a markdown table instead of a list
```

### Issue: "Generated command is incomplete or malformed"
```bash
# Ask Copilot to regenerate with different format request
> That command got cut off. Can you regenerate it? 
> Make sure to include the full --body text.

# Or request it in a file instead
> Write the full gh issue create command to a file called issue-command.sh
```

---

## 📚 Agent Deep Dive: Understanding baseline-checker.py

This exercise uses a **custom Python security agent**. Let's examine how it works:

### Agent Structure

```bash
# View the agent source code
cat .github/agents/baseline-checker.py
```

**Key Components:**
1. **SecurityPattern class** - Defines detection regex patterns
2. **BaselineChecker class** - Scans files and reports violations
3. **Regex patterns** - Real security vulnerability signatures
4. **JSON output** - Machine-readable findings

### Detection Patterns (How It Works)

```python
PATTERNS = {
    'SQL_INJECTION': [
        r'f["\']SELECT.*WHERE.*{',      # F-string SQL injection
        r'query.*format\(',               # Format-based SQL (app.py:47)
        r'\.execute\(.*\+.*\)',          # String concatenation (vulnerable)
    ],
    'XSS_VULNERABLE': [
        r'innerHTML\s*=',                 # Unsafe DOM manipulation
        r'\.html\(',                      # Jinja2 without escape filter
        r'eval\(',                        # Code evaluation (dangerous)
    ],
    'HARDCODED_SECRETS': [
        r'(API_KEY|PASSWORD|TOKEN|SECRET)\s*=\s*["\']',
        r'(JWT_SECRET|PRIVATE_KEY)\s*=',  # Found in app.py:12
    ],
}
```

**How it detects vulnerabilities:** Uses regex patterns to find suspicious code patterns that indicate security issues.

---

## 🛠️ Hands-On: Modify Detection Patterns

### Step 1: Enhance the Agent

Edit the agent to add a new detection pattern:

```bash
# Open agent in your editor
code .github/agents/baseline-checker.py

# Or view what we're modifying
head -40 .github/agents/baseline-checker.py
```

### Step 2: Add Weak Password Hashing Detection

Find the `PATTERNS` dict and add MD5 detection:

```python
'WEAK_CRYPTO': [
    r'md5\(',              # ← Already here
    r'sha1\(',             # ← Already here  
    r'def.*hash.*md5',     # ← NEW: Add this pattern
    r'password.*sha1',     # ← NEW: Add this pattern
],
```

**Why:** These patterns catch common weak hashing mistakes.

### Step 3: Test Your Modified Agent

```bash
# Run the modified agent
python .github/agents/baseline-checker.py

# Verify it detects the added patterns
python .github/agents/baseline-checker.py | grep WEAK_CRYPTO
```

**Result:** Agent now catches more weak cryptography patterns!

---

### Step 4: Copy Agent Output for Issue Creation

The agent outputs JSON that you'll use in Step 6:

```bash
# Capture agent findings
python .github/agents/baseline-checker.py > findings.json

# Use findings in Copilot to generate issue
copilot << EOF
Create a GitHub issue from these findings:
$(cat findings.json)
EOF
```

---

## 🎯 Next Steps

Congratulations! You've completed Exercise 1. You've demonstrated how Copilot agents can quickly identify major security vulnerabilities.

### What's Next?

In **[Exercise 2: MCP & Supply Chain Security](./2-mcp-supply-chain.md)**, you'll:
- Integrate Model Context Protocol (MCP) to query CVE databases
- Deploy the `dependency-supply-chain-scout` agent
- Generate a Software Bill of Materials (SBOM)
- Create remediation pull requests

**Ready?** → **[Exercise 2: MCP & Supply Chain →](./2-mcp-supply-chain.md)**

---

**⏱️ Time Elapsed**: ~20 minutes (cumulative: 30 min)  
**Exercises Completed**: 2/5 ✓
