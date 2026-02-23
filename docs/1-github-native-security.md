# Exercise 1: GitHub NATIVE Security (GHAS)
## What GitHub Provides Out-of-the-Box

**Duration**: 20 minutes  
**Type**: ⭐⭐ Understanding GitHub's native capabilities  
**Focus**: GitHub Advanced Security - Built-in scanning without custom tools

---

## 🎯 Learning Objectives

✅ Understand what GitHub GHAS provides (no custom code needed)  
✅ Enable CodeQL for static analysis  
✅ Review Secret Scanning results  
✅ Understand Dependabot vulnerability alerts  
✅ See real vulnerabilities BEFORE you write custom tools  

---

## 📖 Scenario

**Question**: "Is SecureTrails ready for launch?"

**Without writing ANY custom code**, GitHub can already tell us about:
- Code vulnerabilities (SQL injection, XSS) via CodeQL
- Hardcoded secrets via Secret Scanning  
- Vulnerable dependencies via Dependabot
- Security misconfigurations

This exercise shows what GitHub **NATIVELY** provides.

---

## 🏛️ What is GitHub Advanced Security (GHAS)?

GHAS includes THREE built-in security **SERVICES** (NOT .py files):

| Feature | What It Does | Type | Where It Runs |
|---------|--------------|------|----------------|
| **CodeQL** | Finds code vulnerabilities (SQL injection, XSS, etc.) | GitHub Native Service | GitHub servers |
| **Secret Scanning** | Detects hardcoded API keys, passwords, tokens | GitHub Native Service | GitHub servers |
| **Dependabot** | Identifies vulnerable packages | GitHub Native Service | GitHub servers |

**CRITICAL**: These are **BUILT INTO GitHub**. They are NOT .py files in your repository. GitHub does the heavy lifting on their servers.

**In TIER 3** (Exercise 3), you will write CUSTOM .py files to extend these services. Those are different.

---

## ⚠️ Don't Confuse These:

| What | Type | Files? | Location |
|------|------|--------|----------|
| GitHub GHAS (CodeQL, Secrets, Dependabot) | ✅ Built-in GitHub service | ❌ None - it's a service | GitHub servers |
| Custom Detection Tools (Exercise 3) | ❌ Code YOU write | ✅ .py files | `.github/agents/` in your repo |

---

## ⚙️ Step 1: Enable GitHub Advanced Security

### For Enterprise or Organization Repos

Go to repository **Settings → Security → Security features**:

```
☑ Dependabot alerts
☑ Dependabot security updates
☑ Code scanning with CodeQL
☑ Secret scanning
☑ Push protection
```

Enable all of these.

### For Public Repos

CodeQL and Secret Scanning are **already enabled** by default on public repos.

Check the **Security** tab in your repository:

```
Security
├── Security alerts
├── Dependabot
├── Code scanning
└── Secret scanning
```

---

## 🔍 Step 2: Run CodeQL Analysis

CodeQL analyzes your code for vulnerabilities. It happens automatically when you:
- Push to main branch
- Open a pull request

**Manual trigger** (for existing code):

Go to: **Actions → Run CodeQL Analysis**

Or via CLI:
```bash
# CodeQL CLI (already installed in this workshop)
codeql database create securetrails-db \
  --language python \
  --source-root apps/securetrails-vulnerable

codeql database analyze securetrails-db \
  javascript-code-scanning.qls \
  --format sarif-latest \
  --output results.sarif
```

**What CodeQL finds**:
- SQL Injection patterns
- Cross-Site Scripting (XSS)
- Weak cryptography
- Insecure authentication
- Path traversal
- Command injection

---

## 📊 Step 3: Review CodeQL Results

Navigate to: **Security → Code scanning**

You'll see findings like:

```
🔴 SQL Injection
Location: app.py:47
Severity: CRITICAL
Message: Unsanitized user input in SQL query
  Line 47: database.execute(f"SELECT * WHERE id={user_input}")
Recommendation: Use parameterized queries

🟠 Cross-Site Scripting (XSS)
Location: templates/trails.html:89
Severity: HIGH
Message: User data rendered without escaping
  Line 89: <p>{{ trail.comments }}</p>
Recommendation: Use escape filter: {{ trail.comments | escape }}

🟡 Weak Cryptography
Location: app.py:200
Severity: MEDIUM
Message: MD5 used for password hashing
  Line 200: hash_obj = hashlib.md5(password.encode())
Recommendation: Use bcrypt instead
```

**Your Task**: Review each finding in the Security tab.

---

## 🔑 Step 4: Review Secret Scanning Results

Secret Scanning automatically detects hardcoded credentials.

Navigate to: **Security → Secret scanning**

You'll see alerts like:

```
🔴 GitHub Personal Access Token
Type: github_pat
Location: .env.example:3
Status: Token not revoked (⚠️ at risk if real)
Recommendation: Rotate immediately if real token

🔴 AWS Access Key
Type: aws_access_key_id
Location: app.py:18
Value: AKIA[redacted]
Status: Check AWS console for activity
Recommendation: Deactivate and create new key pair

🔴 Database Password
Type: db_connection_string
Location: .env.example:5
Value: postgres://user:password123@localhost
Recommendation: Use .env file, never commit credentials
```

**Your Task**: Review each secret found. Understand the risk.

---

## 📦 Step 5: Review Dependabot Alerts

Dependabot scans your `requirements.txt` and `package.json` for known vulnerabilities.

Navigate to: **Security → Dependabot**

You'll see packages with issues:

```
🔴 Flask 1.1.0
CVE: CVE-2021-21342
Severity: CRITICAL
Issue: Remote Code Execution via Werkzeug
Fixed in: Flask 2.3.2
Recommendation: Update to Flask 2.3.2 or later

🟠 requests 2.24.0
CVE: CVE-2021-33503
Severity: MEDIUM
Issue: URL parsing vulnerability  
Fixed in: requests 2.28.1
Recommendation: Update to requests 2.28.1 or later

🟠 SQLAlchemy 1.3.0
CVE: CVE-2021-XXXXX
Severity: HIGH
Issue: SQL injection in legacy code
Fixed in: SQLAlchemy 2.0.8
Recommendation: Update to 2.0.8 or later
```

**Your Task**: Review the vulnerable packages.

---

## 📋 Step 6: Create Issues from Findings

GitHub can auto-create issues for each finding. Or manually:

```bash
# Create an issue documenting all GHAS findings
gh issue create \
  --title "[SECURITY] GitHub GHAS findings - SecureTrails" \
  --label "security,review" \
  --body "## Security Analysis Results (GitHub Native)

### CodeQL Findings
- SQL Injection (app.py:47) - CRITICAL
- XSS in templates (templates/trails.html:89) - HIGH  
- Weak password hashing (app.py:200) - MEDIUM

### Secret Scanning
- GitHub PAT in .env.example - CRITICAL
- AWS credentials in app.py - CRITICAL
- DB password exposed - CRITICAL

### Dependabot Alerts
- Flask 1.1.0: 2 CVEs (CRITICAL)
- requests 2.24.0: 1 CVE (MEDIUM)
- SQLAlchemy 1.3.0: 1 CVE (HIGH)

**Assessment**: NOT PRODUCTION READY
- 3 critical code vulnerabilities
- 3 hardcoded secrets  
- 3 vulnerable packages

**Next Steps**:
1. Fix code vulnerabilities (CodeQL findings)
2. Remove hardcoded secrets and use .env
3. Update vulnerable packages to secure versions
4. Proceed to Exercise 2 for interactive analysis"
```

---

## ✅ Acceptance Criteria

- [ ] Enabled GitHub Advanced Security (if applicable)
- [ ] Ran CodeQL analysis (automatic or manual trigger)
- [ ] Found ≥3 code vulnerabilities
- [ ] Found ≥3 hardcoded secrets  
- [ ] Found ≥3 vulnerable packages in Dependabot
- [ ] Reviewed all findings in Security tab
- [ ] Created GitHub issue documenting findings

---

## 🎯 Key Learning

**This is what GitHub provides FOR FREE (enterprise/org repos) or DEFAULT (public repos):**

- ✅ Automated code analysis (CodeQL)
- ✅ Secret detection
- ✅ Dependency scanning

**You don't need to write custom tools for these basic cases.** 

GitHub handles it. This is why starting here matters - understand native capabilities before building custom.

---

## 🚀 Next Steps

**In Exercise 2**, you'll use:
- **Copilot CLI** for interactive, real-time analysis
- Conversational prompts to dig deeper
- AI reasoning about vulnerabilities

**In Exercise 3**, you'll build:
- Custom detection tools (when GitHub GHAS isn't enough)

But first, understand what GitHub NATIVELY provides here in Exercise 1.

---

## 📚 Resources

- [GitHub Advanced Security Docs](https://docs.github.com/en/enterprise-cloud@latest/code-security)
- [CodeQL Documentation](https://codeql.github.com/)
- [Dependabot Alerts](https://docs.github.com/en/code-security/dependabot)
- [Secret Scanning](https://docs.github.com/en/code-security/secret-scanning)

---

**⏱️ Time**: 20 min | **Exercises**: 1/5 ✓
