# Exercise 2: Dependency Supply Chain Security (20 min)

**Duration**: 20 minutes  
**Level**: ⭐⭐ Intermediate  

---

## 🎯 Learning Objectives

By the end of this exercise, you will:

✅ Understand supply chain vulnerabilities in dependencies  
✅ Run a custom Python agent to scan for CVEs  
✅ Generate a Software Bill of Materials (SBOM)  
✅ Identify outdated packages with security issues  
✅ Get recommendations for vulnerability remediation  

---

## 📖 Scenario

Executive: **"Are we using any packages with known security vulnerabilities?"**

The answer: **Very likely.** The SecureTrails app uses outdated dependencies with known CVEs. Your task:
- ✅ Scan all dependencies
- ✅ Find vulnerable ones
- ✅ Get fix recommendations
- ✅ Understand supply chain risk

---

## 📝 Important Clarification: File Types in This Workshop

**Two Different File Types:**

| What | File Type | Purpose | Example |
|------|-----------|---------|---------|
| **Exercise Instructions** | `.md` (Markdown) | What YOU read to learn | `2-mcp-supply-chain.md` (this file) |
| **Agent Code** | `.py` (Python) | Actual executable code that runs | `.github/agents/dependency-scout.py` |

**Key Point:**
- **This file** (`.md`) = Instructions for you to follow
- **Agent files** (`.py`) = Real Python scripts that detect vulnerabilities
- You RUN the `.py` agents, you READ the `.md` exercises

---

## 🛠️ What You're Running

**Agent File:** [`.github/agents/dependency-scout.py`](../../.github/agents/dependency-scout.py)  
**Type**: Standalone Python script (`*.py` executable)  
**What it does:**
- Parses `requirements.txt`
- Looks up known CVEs for each package
- Generates SBOM (Software Bill of Materials)
- Recommends package updates
- Outputs JSON findings

---

## 🚀 Run The Dependency Scout Agent

### Step 1: Execute the Agent

```bash
# Navigate to the vulnerable app
cd apps/securetrails-vulnerable

# Run the dependency scanning agent
python ../../.github/agents/dependency-scout.py

# Or from project root:
python .github/agents/dependency-scout.py
```

**What happens:**
1. ✅ Agent reads `requirements.txt`
2. ✅ Checks each package version against known CVE database
3. ✅ Identifies vulnerable versions and their CVE IDs
4. ✅ Recommends updated versions
5. ✅ Outputs JSON report with findings

**Expected output:**
```json
{
  "packages_analyzed": 8,
  "vulnerable_packages": [
    {
      "name": "Flask",
      "current_version": "1.1.0",
      "severity_issues": [
        {
          "cve_id": "CVE-2021-21342",
          "severity": "CRITICAL",
          "description": "Remote Code Execution via Werkzeug",
          "affected_versions": "< 2.0.0",
          "fix_available": true,
          "recommended_version": "2.3.2"
        },
        {
          "cve_id": "CVE-2021-21409",
          "severity": "HIGH",
          "description": "Development server reloader can execute code",
          "recommended_version": "2.3.2"
        }
      ]
    },
    {
      "name": "requests",
      "current_version": "2.24.0",
      "severity_issues": [
        {
          "cve_id": "CVE-2021-33503",
          "severity": "MEDIUM",
          "description": "URL parsing vulnerability",
          "recommended_version": "2.28.1"
        }
      ]
    },
    {
      "name": "SQLAlchemy",
      "current_version": "1.3.0",
      "severity_issues": [
        {
          "cve_id": "CVE-2021-XXXXX",
          "severity": "HIGH",
          "description": "SQL injection via legacy sqlphrase",
          "recommended_version": "2.0.8"
        }
      ]
    }
  ],
  "sbom": {
    "format": "SPDX",
    "packages": ["Flask==1.1.0", "requests==2.24.0", "SQLAlchemy==1.3.0", "..."],
    "generated_at": "2026-02-21T..."
  },
  "summary": {
    "total_packages": 8,
    "secure_packages": 1,
    "packages_with_vulnerabilities": 5,
    "critical_issues": 2,
    "high_issues": 2,
    "medium_issues": 1
  }
}
```

---

### Step 2: Understand the Findings

The agent report shows:

**Critical Severity** = Must fix before production  
**High Severity** = Fix soon after launch  
**Medium Severity** = Plan to fix in next release  

For SecureTrails:
```
✗ Flask 1.1.0 has 2 CVEs (CRITICAL + HIGH)
✗ Requests 2.24.0 has 1 CVE (MEDIUM)
✗ SQLAlchemy 1.3.0 has 1 CVE (HIGH)

Assessment: NOT PRODUCTION READY without updates
```

---

### Step 3: What "Supply Chain Security" Means

**Your code might be perfect, but:**

```
If you use vulnerable dependencies...
    ↓
Attackers exploit those vulnerabilities
    ↓
Your security is broken, independent of code quality
    ↓
One vulnerable package = whole system compromised
```

**Real attack example:**
```
1. Attacker finds vulnerability in Flask 1.1.0
2. Searches GitHub for projects using Flask 1.1.0
3. Finds your SecureTrails app
4. Exploits the Flask vulnerability
5. Gets remote code execution on your server
6. Your beautiful security-reviewed code doesn't matter!
```

**Solution:** Keep all dependencies updated!

---

### Step 4: Review the SBOM Output

SBOM = Software Bill of Materials (inventory of all your code components)

The agent provides:
- ✅ List of all packages you use
- ✅ Current versions
- ✅ Which have known vulnerabilities  
- ✅ CVE IDs and descriptions
- ✅ Recommended upgrade versions
- ✅ Risk severity breakdown

**Key Numbers:**
```
Critical: 2       ← Must fix NOW before launch
High: 2          ← Fix ASAP 
Medium: 1        ← Plan to fix in next release
Total: 8 packages
```

---

### Step 5: Create an Issue to Document Findings

Create a GitHub issue with the findings:

```bash
cat > dependency-findings.json << 'EOF'
# Paste the agent output here (the JSON from Step 1)
EOF

# Create issue documenting your findings
gh issue create \
  --title "[SECURITY AUDIT] Exercise 2: Supply Chain Analysis" \
  --label "security,review-exercise" \
  --body "## Supply Chain Security Audit - Exercise 2

Agent scanned SecureTrails dependencies and found **5 packages with vulnerabilities**.

### Critical Issues (Must Fix)
- Flask 1.1.0: CVE-2021-21342 (RCE) + CVE-2021-21409 (RCE)

### High Issues (Fix ASAP)
- SQLAlchemy 1.3.0: CVE-2021-XXXXX (SQL injection)
- Requests 2.24.0: Encoding issues

### Medium Issues
- Various optional dependencies with low-risk CVEs

### Summary
Current Status: **HIGH RISK** ⚠️
- 5 out of 8 packages have known vulnerabilities
- 2 critical remote code execution vulnerabilities
- All CRITICAL/HIGH should be fixed before launch

### Next: Proceed to Exercise 3"
```

---

## 🎯 What This Demonstrates

✅ **Automated vulnerability scanning** - No manual package checking  
✅ **Supply chain risk assessment** - Understanding dependency security  
✅ **SBOM generation** - Complete inventory of components  
✅ **Risk prioritization** - Which vulnerabilities matter most  
✅ **Actionable recommendations** - Specific versions to upgrade to  

---

## ✅ Exercise Complete

**What You Learned:**
- SecureTrails has 5 packages with known vulnerabilities
- Flask is CRITICAL (2 CVEs permitting remote code execution)
- Requests and SQLAlchemy have HIGH severity issues
- SBOM scanning is essential before every deployment
- Supply chain security = as important as code review

**Key Insight:** Perfect code + vulnerable dependencies = pwned application.

---

## 🚀 Next Steps

**In Exercise 3**, you'll:
- Run the **secret-detector** agent (`.py` file)
- See how agents work together
- Document findings in GitHub

**In Exercise 4**, you'll:
- Auto-block PRs with vulnerabilities
- Integrate agents into GitHub Actions
- Enterprise-scale security automation

---

## 📚 Resources

- [GitHub Advisory Database](https://github.com/advisories)
- [OWASP: Use of Untrusted Libraries](https://owasp.org/www-project-top-10-code-analysis-issues/#a1-use-of-untrusted-libraries)
- [SBOM Standard: CYCLONEDX](https://cyclonedx.org/)
- [CVE Database](https://cve.mitre.org/)
- [Agent Reference Guide](./resources/agents-reference.md)

---

**⏱️ Time**: 20 min | **Exercises**: 3/5
