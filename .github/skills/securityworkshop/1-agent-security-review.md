# Exercise 1: GitHub Agent Security Review

**Duration**: 20 minutes  
**Expected Time to Complete**: 20 min

---

## 🎯 Learning Objectives

By the end of this exercise, you will:

✅ Use Copilot CLI (`gh copilot explain` and `gh copilot suggest`) for vulnerability discovery  
✅ Identify OWASP Top 10 vulnerabilities in real code  
✅ Understand how AI agents analyze code for security issues  
✅ Document findings in GitHub issues  

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

### Step 1: Analyze Flask Backend for Vulnerabilities

**Objective**: Scan the main Flask application for security flaws.

Navigate to the SecureTrails repository:
```bash
cd securetrails-vulnerable
```

Use Copilot to analyze the Flask backend:
```bash
gh copilot explain app.py
```

**When prompted for how Copilot can help, provide this specific prompt:**

```
Analyze this Flask application for security vulnerabilities. Identify:
1. SQL injection risks in database queries
2. Authentication and authorization flaws
3. Hardcoded credentials or secrets
4. Session management issues
5. CORS and security header misconfigurations
Provide specific line numbers and remediation advice.
```

**Expected Analysis Output:**
The agent should identify:
- Line ~47: SQL query with unsanitized user input (SQL Injection)
- Line ~12: Hardcoded JWT secret
- Line ~156: Weak session handling
- Line ~200: MD5 password hashing (insecure)
- Line ~5: CORS `*` allowing all origins

**Your Task:**
- [ ] Read the Copilot analysis carefully
- [ ] Note the file paths and line numbers
- [ ] Understand the security risk for each finding

---

### Step 2: Review HTML Templates for XSS Vulnerabilities

**Objective**: Identify Cross-Site Scripting (XSS) entry points in templates.

Use Copilot to suggest security improvements:
```bash
gh copilot suggest "Analyze templates/trails.html and templates/login.html for XSS vulnerabilities. Check if user input is properly escaped in HTML rendering and in JavaScript context. List specific lines where HTML is rendered without escaping."
```

**When Copilot responds, review its findings for:**
- HTML injection points (lines where templates render user data)
- DOM manipulation without sanitization
- Event handler injection possibilities

**Expected Findings:**
- Line ~89 (trails.html): Trail comments rendered without escaping
- Line ~124 (trails.html): Direct innerHTML usage
- Line ~45 (login.html): Username field not validated on client

**Your Task:**
- [ ] Identify ≥2 XSS vulnerabilities
- [ ] Note the specific vulnerability type (stored vs. reflected)
- [ ] Understand the attack vector

---

### Step 3: Check for Hardcoded Secrets & Credentials

**Objective**: Detect exposed sensitive information.

Examine the .env.example and app.py files:
```bash
gh copilot explain .env.example
```

**Prompt for Copilot:**
```
This file contains environment variable examples for SecureTrails. Identify any hardcoded secrets, API keys, credentials, or sensitive information that should NEVER be in version control. Check for: database passwords, API keys, JWT secrets, encryption keys, OAuth tokens. Explain the security risk of each exposure.
```

Also check app.py for secrets:
```bash
gh copilot suggest "Search app.py for hardcoded API keys, database passwords, encryption keys, JWT secrets, or any sensitive strings that should be environment variables instead of code. List line numbers and severity."
```

**Expected Findings:**
- `.env.example` line ~3: Database password example
- `.env.example` line ~8: AWS API key format exposed
- `app.py` line ~12: JWT_SECRET hardcoded
- `app.py` line ~18: Database connection string with credentials

**Your Task:**
- [ ] Identify ≥3 exposed credentials
- [ ] Understand the risk of each exposure
- [ ] Note which should be moved to `.env`

---

### Step 4: Analyze JavaScript for Client-Side Vulnerabilities

**Objective**: Check frontend code for injection and unsafe operations.

Analyze client-side code:
```bash
gh copilot explain static/js/app.js
```

**Prompt:**
```
Review this JavaScript code for security vulnerabilities including:
1. DOM-based XSS (innerHTML, eval, unsafe DOM methods)
2. SQL injection in API calls
3. Lack of input validation
4. Insecure API endpoints
5. Missing HTTPS enforcement
Identify specific lines and suggest fixes.
```

**Expected Findings:**
- Line ~42: `innerHTML` usage without sanitization
- Line ~67: `eval()` used on user data
- Line ~89: Direct API call without CSRF token
- Line ~105: Sensitive data in browser console (debug logs)

**Your Task:**
- [ ] Identify ≥2 DOM-based vulnerabilities
- [ ] Note the specific JavaScript methods creating risk
- [ ] Document attack scenarios

---

### Step 5: Check Dependencies for Known Vulnerabilities

**Objective**: Identify outdated packages with security issues.

Analyze requirements file:
```bash
gh copilot suggest "I have a Python requirements.txt file. Analyze each package version and check if any have known security vulnerabilities (CVEs). Flag packages that are outdated or have critical security issues. Recommend updated versions."
```

Then show Copilot the file:
```bash
gh copilot explain requirements.txt
```

**Expected Findings:**
- Flask 1.1.0 — Multiple CVEs (upgrade to 2.3+)
- requests 2.24.0 — HTTP request smuggling (upgrade to 2.28+)
- SQLAlchemy 1.3.0 — SQL injection vectors (upgrade to 2.0+)

**Your Task:**
- [ ] Note all dependencies with vulnerabilities
- [ ] Record severity levels
- [ ] List recommended upgrade versions

---

### Step 6: Document Findings in GitHub Issue

**Objective**: Create a comprehensive audit report.

Create a GitHub issue to document all findings:

```bash
gh issue create --title "[SECURITY AUDIT] Exercise 1: Agent Security Review Findings" \
  --label "security,review-exercise" \
  --body "## SecureTrails Security Audit - Exercise 1

## Vulnerabilities Found

### Critical Issues (MUST FIX)

#### 1. SQL Injection in Login Form
- **File**: app.py:47
- **Severity**: CRITICAL
- **Description**: User input directly interpolated into SQL query
- **Code**: \`query = f\"SELECT * FROM users WHERE username = '{username}'\"\`
- **Impact**: Complete database compromise
- **Fix**: Use parameterized queries

#### 2. Hardcoded JWT Secret
- **File**: app.py:12
- **Severity**: CRITICAL
- **Description**: JWT secret hardcoded in source
- **Evidence**: \`JWT_SECRET = 'super-secret-key-12345'\`
- **Impact**: Token forgery, account takeover
- **Fix**: Move to .env variable

#### 3. XSS in Trail Comments
- **File**: templates/trails.html:89
- **Severity**: HIGH
- **Description**: User comments rendered without escaping
- **Code**: \`{{ trail.comment }}\` without filter
- **Impact**: Cookie theft, session hijacking
- **Fix**: Apply Jinja2 auto-escape or manual escape

### High-Risk Issues

#### 4. Weak Password Hashing
- **File**: app.py:200
- **Severity**: HIGH
- **Description**: MD5 used for password hashing (broken hash)
- **Impact**: Rainbow table attacks
- **Fix**: Use bcrypt or argon2

#### 5. CORS Misconfiguration
- **File**: app.py:5
- **Severity**: HIGH
- **Description**: CORS allows all origins (\`*\`)
- **Impact**: Cross-origin attacks
- **Fix**: Restrict to known domains

#### 6. Exposed Credentials in .env.example
- **File**: .env.example
- **Severity**: HIGH
- **Description**: Database and API credentials in example
- **Impact**: If committed, credentials exposed
- **Fix**: Keep example values generic

#### 7. Insecure Dependencies
- **File**: requirements.txt
- **Severity**: MEDIUM
- **Description**: Outdated packages with known CVEs
  - Flask 1.1.0 (multiple CVEs)
  - requests 2.24.0 (CVE-2021-XXXXX)
  - SQLAlchemy 1.3.0 (injection vectors)
- **Impact**: Exploitation via dependencies
- **Fix**: Update all packages

## Summary

- Total Vulnerabilities Found: **7**
- Critical: **2**
- High: **4**
- Medium: **1**
- Status: **NOT READY FOR LAUNCH** ⚠️

## Next Steps

1. Proceed to Exercise 2 for supply chain analysis
2. Generate fixes using Copilot agent
3. Create PRs to remediate each issue

---
Generated by Exercise 1: GitHub Agent Security Review
"
```

**Verify issue created:**
```bash
gh issue list --label security
```

---

## ✅ Acceptance Criteria

- [ ] Ran `gh copilot explain app.py` and reviewed analysis
- [ ] Ran `gh copilot suggest` for templates and JavaScript
- [ ] Identified ≥5 security vulnerabilities
- [ ] Found ≥3 exposed credentials
- [ ] Noted ≥3 vulnerable dependencies
- [ ] Created GitHub issue with comprehensive findings
- [ ] Documented each vulnerability with:
  - [ ] File and line number
  - [ ] Severity level
  - [ ] Description and impact
  - [ ] Recommended fix

---

## 🖼️ Expected Output

Copilot analysis output should look similar to:

```
Flask Application Security Analysis
====================================

CRITICAL FINDINGS (2):
1. SQL Injection (app.py:47) - User input in SQL query
2. Hardcoded JWT Secret (app.py:12) - Credential exposure

HIGH FINDINGS (4):
3. XSS in Templates (templates/trails.html:89)
4. Weak Password Hashing (app.py:200)
5. CORS Misconfiguration (app.py:5)
6. Exposed .env Example (credentials listed)

MEDIUM FINDINGS (1):
7. Vulnerable Dependencies (multiple packages outdated)

REMEDIATION OVERVIEW:
- Use parameterized queries for SQL
- Move secrets to environment variables
- Apply output escaping in templates
- Use bcrypt for passwords
- Restrict CORS to specific origins
- Update all packages to latest versions
```

---

## 🆘 Troubleshooting

### Issue: "Copilot CLI not responding"
```bash
# Restart authentication
gh copilot auth
```

### Issue: "File not found" in copilot explain
```bash
# Make sure you're in the correct directory
pwd
ls -la app.py

# Use full paths if needed
gh copilot explain ./securetrails-vulnerable/app.py
```

### Issue: "No output from copilot suggest"
```bash
# Try with simpler prompt first
gh copilot suggest "Find SQL injection in Flask"
```

---

## 📚 Resources

- [OWASP Top 10 2023](https://owasp.org/Top10/)
- [OWASP SQL Injection](https://owasp.org/www-community/attacks/SQL_Injection)
- [OWASP XSS Prevention](https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html)
- [GitHub Copilot CLI Docs](https://docs.github.com/en/copilot/github-copilot-cli/using-github-copilot-cli)
- [Reference Materials](./resources/reference.md)
- [Copilot Cheatsheet](./resources/copilot-cheatsheet.md)

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
