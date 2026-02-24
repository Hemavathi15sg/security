# Exercise 1: GitHub NATIVE Security (GHAS)
## What GitHub Provides Out-of-the-Box

**Duration**: 20 minutes  
**Type**: ⭐⭐ Understanding GitHub's native capabilities  
**Focus**: GitHub Advanced Security - Built-in scanning without custom tools

---

## 🎯 Learning Objectives

✅ Understand what GitHub GHAS provides   
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

GHAS includes THREE built-in security **SERVICES**:

| Feature | What It Does | Type | Where It Runs |
|---------|--------------|------|----------------|
| **CodeQL** | Finds code vulnerabilities (SQL injection, XSS, etc.) | GitHub Native Service | GitHub servers |
| **Secret Scanning** | Detects hardcoded API keys, passwords, tokens | GitHub Native Service | GitHub servers |
| **Dependabot** | Identifies vulnerable packages | GitHub Native Service | GitHub servers |


---

## ⚙️ Step 1: Navigate to Security Settings

### Step 1.1: Go to Repository Settings

In your GitHub repository, navigate to **Settings** tab:

![Settings Tab Navigation](./images/1.png)

**You'll see:**
- Repository name and basic info
- Settings sidebar on the left

---

### Step 1.2: Enable Security Features

Scroll left sidebar to **Security and analysis** section:

![Security Settings Location](./images/2.png)

**Click**: "Security and analysis" → You'll see available security features

---

### Step 1.3: Enable GHAS Features

Toggle ON all these features:

![Enable Security Features](./images/3.png)

**Features to enable:**
- ☑ Dependabot alerts
- ☑ Dependabot security updates  
- ☑ Code scanning with CodeQL
- ☑ Secret scanning
- ☑ Push protection (blocks secrets in commits)

Once enabled, GitHub starts scanning automatically.

---

## 🔍 Step 2: Navigate to Security Tab

### Step 2.1: Open Security Dashboard

Click the **Security** tab in your repository header:

![Security Tab](./images/4.png)

**You'll see:**
- Security alerts overview
- Links to Code scanning, Dependabot, Secret scanning

---

### Step 2.2: View Code Scanning Results

Click **Code scanning** in the left menu:

![Code Scanning Results](./images/5.png)

**You'll see:**
- List of vulnerabilities found by CodeQL
- Severity levels (CRITICAL, HIGH, MEDIUM, LOW)
- File locations and line numbers
- Recommendations for each finding

---

## 📊 Step 3: Review CodeQL Vulnerabilities

### Real Findings in SecureTrails

CodeQL has found vulnerabilities in the app:

![CodeQL Findings List](./images/6.png)

**Examples you'll see:**

```
🔴 SQL Injection (CRITICAL)
Location: app.py:47
Issue: Unsanitized user input concatenated into SQL query
Code: database.execute(f"SELECT * WHERE id={user_input}")
Fix: Use parameterized queries

🟠 XSS in Templates (HIGH)  
Location: templates/trails.html:89
Issue: User comment rendered without escaping
Code: <p>{{ trail.comments }}</p>
Fix: {{ trail.comments | escape }}

🟡 Weak Cryptography (MEDIUM)
Location: app.py:200
Issue: MD5 used for password hashing
Code: hashlib.md5(password.encode())
Fix: Use bcrypt instead
```

**Your task:** Click each finding to understand:
- Why it's a vulnerability
- Where exactly it occurs
- What the recommended fix is

---

## 🔑 Step 4: Check Secret Scanning

### Real Secrets Found

GitHub's Secret Scanning automatically detects hardcoded credentials:

![Secret Scanning Alerts](./images/7.png)

**Types of secrets found:**

```
🔴 GitHub Personal Access Token (CRITICAL)
Location: .env.example:3
Issue: PAT exposed in repository
Risk: Anyone can use this token to access your GitHub account
Action: Revoke immediately

🔴 AWS Access Key (CRITICAL)
Location: config.py:18
Issue: AWS credentials hardcoded  
Risk: Attacker can access your AWS resources
Action: Deactivate key and create new one

🔴 Database Password (CRITICAL)
Location: .env.example:5
Issue: DB connection string with password
Risk: Database can be accessed by unauthorized users
Action: Rotate password and regenerate connection string
```

**Your task:** Review each secret:
- Is this a real credential or test value?
- Has this ever been used?
- Is the corresponding service still accessible?

---

## 📦 Step 5: Review Dependabot Alerts

Navigate to **Dependabot** tab to see vulnerable packages:

**You'll see dependencies with known CVEs:**

```
🔴 Flask 1.1.0 (CRITICAL)
CVE: CVE-2021-21342  
Issue: Remote Code Execution possible
Current: 1.1.0 → Available: 2.3.2
Action: Update Flask to 2.3.2

🟠 requests 2.24.0 (MEDIUM)
CVE: CVE-2021-33503
Issue: URL parsing vulnerability
Current: 2.24.0 → Available: 2.28.1
Action: Update requests to 2.28.1

🟠 SQLAlchemy 1.3.0 (HIGH)
CVE: CVE-2021-XXXXX  
Issue: SQL injection in legacy code patterns
Current: 1.3.0 → Available: 2.0.8
Action: Update SQLAlchemy to 2.0.8
```

**Your task:** Review the vulnerable packages and understand:
- What version are you currently using?
- What's the security issue?
- What version fixes it?

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

- [ ] **Step 1.1**: Located Settings tab in repository
- [ ] **Step 1.2**: Found "Security and analysis" in settings sidebar
- [ ] **Step 1.3**: Enabled all security features (Dependabot, CodeQL, Secret scanning)
- [ ] **Step 2**: Navigated to Security tab and viewed dashboard
- [ ] **Step 3**: Reviewed CodeQL findings - found ≥3 code vulnerabilities
- [ ] **Step 4**: Reviewed Secret Scanning - found ≥3 hardcoded secrets
- [ ] **Step 5**: Reviewed Dependabot alerts - found ≥3 vulnerable packages
- [ ] **Step 6**: Created GitHub issue documenting all findings
- [ ] **Understanding**: Can explain what each GHAS service does (CodeQL, Secret Scanning, Dependabot)

---

## 🎯 Key Learning

**What GitHub GHAS Found in SecureTrails:**

✅ **9+ Security Issues** without writing ANY custom code:
- 3 code vulnerabilities (SQL injection, XSS, weak crypto)
- 3 hardcoded secrets (GitHub PAT, AWS keys, DB password)
- 3+ vulnerable packages (Flask, requests, SQLAlchemy)

**GitHub provides this FOR FREE** on enterprise/org repos or DEFAULT on public repos.

This is why starting here matters - **understand native capabilities before building custom**.

---

## 🚀 Exercise 1 Complete!

You now understand:
- ✅ What GitHub GHAS provides natively
- ✅ How to enable and view security findings
- ✅ The difference between code vulns, secrets, and dependency issues
- ✅ That SecureTrails has real security problems to fix

**Next: Exercise 2** - Use Copilot CLI for interactive analysis and fixing

---

## 📚 Resources

- [GitHub Advanced Security Docs](https://docs.github.com/en/enterprise-cloud@latest/code-security)
- [CodeQL Documentation](https://codeql.github.com/)
- [Dependabot Alerts](https://docs.github.com/en/code-security/dependabot)
- [Secret Scanning](https://docs.github.com/en/code-security/secret-scanning)

---

**⏱️ Time**: 20 min | **Exercises**: 1/5 ✓
