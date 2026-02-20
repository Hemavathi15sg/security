# Exercise 2: MCP & Dependency Supply Chain Security

**Duration**: 20 minutes  
**Expected Time to Complete**: 20 min

---

## 🎯 Learning Objectives

By the end of this exercise, you will:

✅ Configure and use Model Context Protocol (MCP) for external tool access  
✅ Deploy a custom `dependency-supply-chain-scout` agent using Copilot SDK  
✅ Query GitHub security advisories via MCP  
✅ Generate a Software Bill of Materials (SBOM)  
✅ Create automated remediation PRs for vulnerable dependencies  

---

## 📖 Scenario Context

Executive question: **"Are we using any packages with known security vulnerabilities?"**

Supply chain security is critical. A single vulnerable dependency can compromise the entire application. Your task: Use MCP (Model Context Protocol) and a custom agent to map all dependencies, check for CVEs, and propose updates.

This demonstrates how agents can extend Copilot with access to external tools (GitHub APIs, CVE databases, package registries).

---

## 🔍 Task Overview

In this exercise, you'll:
1. Set up GitHub MCP (Model Context Protocol) server
2. Deploy `dependency-supply-chain-scout` custom agent
3. Query CVE databases via MCP tools
4. Generate SBOM report
5. Create fix PRs automatically

---

## 📋 Step-by-Step Instructions

### Step 1: Configure GitHub MCP Server

**Objective**: Enable MCP so agents can access GitHub APIs.

Create MCP configuration file:

```bash
# Navigate to project root
cd securetrails-vulnerable

# Create MCP config directory
mkdir -p .copilot

# Create MCP configuration
cat > .copilot/mcp-config.json << 'EOF'
{
  "version": "0.1.0",
  "servers": {
    "github": {
      "url": "npx",
      "args": ["@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_TOKEN": "<your-github-token>"
      }
    },
    "git": {
      "url": "npx",
      "args": ["@modelcontextprotocol/server-git"],
      "env": {
        "GIT_REPOSITORY_PATH": "."
      }
    }
  }
}
EOF
```

**Initialize MCP servers:**
```bash
# Install GitHub MCP server
npm install -g @modelcontextprotocol/server-github

# Verify MCP is ready
gh copilot mcp init github
```

**Expected output:**
```
✓ GitHub MCP Server initialized
✓ Available Tools: search_code, search_issues, search_repos, get_issues
✓ Authenticated as: <your-username>
```

---

### Step 2: Query Security Advisories via MCP

**Objective**: Access GitHub's vulnerability database through MPC tools.

Use Copilot to access MCP tools:

```bash
gh copilot suggest "Use GitHub MCP tools to search for security advisories. For each package in requirements.txt (Flask, requests, SQLAlchemy, Werkzeug, Jinja2), find published CVE vulnerabilities, their severity, and fix versions. Format as a structured report with package name, current version, CVE ID, severity, and recommended version."
```

**The agent will use MCP tools like:**
- `search_code`: Find version declarations
- `search_issues`: Find GitHub issues/PRs about vulnerabilities
- Query GitHub Security Advisory database

**Expected findings:**
```
DEPENDENCY VULNERABILITY REPORT
================================

Package: Flask
- Current: 1.1.0
- CVE-2021-21342: Remote Code Execution via Werkzeug (CRITICAL)
- CVE-2021-21409: Development server with reloader can execute arbitrary code (HIGH)
- Recommended: 2.3.2

Package: requests
- Current: 2.24.0
- CVE-2021-33503: Improper input validation in URL parsing (MEDIUM)
- Recommended: 2.28.1

Package: SQLAlchemy
- Current: 1.3.0
- SQL Injection via legacy sqlalchemy.ext.sqlphrase (HIGH)
- Recommended: 2.0.8

... (more packages)
```

---

### Step 3: Initialize & Deploy Custom Agent

**Objective**: Deploy the `dependency-supply-chain-scout` agent.

The agent is a custom Copilot SDK implementation that:
- Parses `requirements.txt` and `package.json`
- Cross-references with CVE databases via MCP
- Generates structured SBOM
- Proposes automated fixes

**Initialize the agent:**

```bash
# Agent is provided in .github/agents directory
ls -la .github/agents/dependency-scout.py

# Register agent with Copilot SDK
gh copilot agent register \
  --agent-path .github/agents/dependency-scout.py \
  --name "dependency-supply-chain-scout" \
  --description "Scans dependencies for known vulnerabilities and generates SBOM"
```

**Verify agent registered:**
```bash
gh copilot agent list
```

**Expected output:**
```
Registered Agents:
- dependency-supply-chain-scout (active)
  Location: .github/agents/dependency-scout.py
  Type: Custom
  Status: Ready
```

---

### Step 4: Run Agent to Generate SBOM

**Objective**: Execute the agent to analyze all dependencies.

Invoke the agent with a specific prompt:

```bash
gh copilot agent run dependency-supply-chain-scout \
  --prompt "Analyze requirements.txt and generate a complete Software Bill of Materials (SBOM). For each dependency: list the package name, version, license, severity of known vulnerabilities (CRITICAL/HIGH/MEDIUM/LOW), CVE IDs, and recommended update version. Output as JSON with structure: {packages: [{name, version, license, vulnerabilities: [{cve_id, severity, description}], recommended_version}]}"
```

**Agent runs these steps internally:**
1. Parse `requirements.txt`
2. Query GitHub Security Advisories via MCP
3. Cross-check with CVE databases
4. Generate structured report
5. Store SBOM in `sbom.json`

**Expected SBOM Output:**
```json
{
  "sbom_version": "1.3",
  "generated_at": "2026-02-20T10:30:00Z",
  "packages": [
    {
      "name": "Flask",
      "version": "1.1.0",
      "license": "BSD",
      "vulnerabilities": [
        {
          "cve_id": "CVE-2021-21342",
          "severity": "CRITICAL",
          "description": "Werkzeug RCE via environment reloader"
        }
      ],
      "recommended_version": "2.3.2"
    },
    {
      "name": "requests",
      "version": "2.24.0",
      "license": "Apache-2.0",
      "vulnerabilities": [
        {
          "cve_id": "CVE-2021-33503",
          "severity": "MEDIUM",
          "description": "Improper URL validation"
        }
      ],
      "recommended_version": "2.28.1"
    }
    // ... more packages
  ],
  "summary": {
    "total_packages": 7,
    "packages_with_vulnerabilities": 5,
    "critical_vulnerabilities": 2,
    "high_vulnerabilities": 3,
    "medium_vulnerabilities": 2
  }
}
```

**Your Task:**
- [ ] Agent successfully generated SBOM
- [ ] Verify `sbom.json` created in project root
- [ ] Review vulnerability summary
- [ ] Note packages requiring urgent updates

---

### Step 5: Invoke Remediation Agent

**Objective**: Automatically propose fixes for vulnerable dependencies.

Chain to the remediation agent:

```bash
gh copilot agent run remediation-proposer \
  --prompt "Based on the SBOM (sbom.json), generate a new requirements.txt with all packages updated to their recommended secure versions. Ensure compatibility by testing import statements. Create a detailed commit message explaining the security fixes. Return the updated requirements.txt content and a summary of changes."
```

**This agent:**
- Reads `sbom.json` findings
- Updates each package to recommended version
- Tests for compatibility
- Generates commit message
- Prepares for PR creation

---

### Step 6: Create Remediation PR

**Objective**: Submit the dependency updates as a PR.

Create a branch and PR:

```bash
# Create feature branch
git checkout -b security/update-dependencies

# Copy updated requirements
# (Agent output provides new requirements.txt)

# Commit changes
git add requirements.txt
git commit -m "security: Update vulnerable dependencies

This commit updates the following packages to address security vulnerabilities:
- Flask 1.1.0 → 2.3.2 (CVE-2021-21342, CVE-2021-21409)
- requests 2.24.0 → 2.28.1 (CVE-2021-33503)
- SQLAlchemy 1.3.0 → 2.0.8 (SQL injection vectors)

Resolves Exercise 2: Supply Chain Security Audit

SBOM Report: sbom.json
Testing Status: ✓ Imports verified
Compatibility: ✓ No breaking changes detected"

# Push and create PR
git push origin security/update-dependencies

gh pr create \
  --title "[SECURITY] Update vulnerable dependencies" \
  --label "security,dependencies" \
  --body "## Supply Chain Security Update

### Vulnerabilities Fixed
✓ Flask CRITICAL RCE  (CVE-2021-21342)
✓ requests MEDIUM URL parsing (CVE-2021-33503)
✓ SQLAlchemy HIGH SQL injection vectors

### Summary
Updated 5 packages to latest secure versions. All imports verified compatible.

### SBOM
See \`sbom.json\` for complete Software Bill of Materials

### Testing
- [x] Import statements verified
- [x] No breaking API changes
- [x] Application startup tested

Generated by Exercise 2: Dependency Supply Chain Scout Agent"
```

**Verify PR created:**
```bash
gh pr list --label security
```

---

### Step 7: Document Findings

**Objective**: Create a comprehensive supply chain audit record.

Create GitHub issue:

```bash
gh issue create \
  --title "[SECURITY AUDIT] Exercise 2: Supply Chain Analysis" \
  --label "security,review-exercise" \
  --body "## Supply Chain Security Audit - Exercise 2

### Scope
SecureTrails requirements.txt analyzed for vulnerable dependencies

### Tool Used
- Agent: \`dependency-supply-chain-scout\`
- Method: MCP GitHub Security Advisories + CVE databases
- SBOM Generated: \`sbom.json\`

### Key Findings

#### Critical Issues: 2
- Flask 1.1.0: Remote Code Execution (CVE-2021-21342)
- Werkzeug incompatibility cascade

#### High Risk Issues: 3
- SQLAlchemy 1.3.0: SQL injection patterns
- Requests encoding issues
- Jinja2 sandbox escape potential

#### Medium Risk Issues: 2
- Various URL parsing issues
- Optional dependency concerns

### Statistics
- Total Dependencies: **7**
- With Known CVEs: **5** (71%)
- Critical Vulnerabilities: **2**
- High Vulnerabilities: **3**
- Medium Vulnerabilities: **2**

### Remediation Status
✓ Remediation PR created: [Link to PR]
✓ All updates maintain compatibility
✓ No breaking changes detected

### Software Bill of Materials (SBOM)
Full SBOM available at: \`sbom.json\`

### Impact Assessment
Current state: **HIGH RISK** ⚠️
After updates: **LOW RISK** ✓

### Next Steps
1. Peer review PR
2. Run security tests
3. Merge when approved
4. Monitor for future vulnerabilities
"
```

---

## ✅ Acceptance Criteria

- [ ] MCP GitHub server configured and initialized
- [ ] Queried security advisories via MCP tools
- [ ] `dependency-supply-chain-scout` agent deployed and registered
- [ ] SBOM generated successfully (`sbom.json` created)
- [ ] Identified ≥5 vulnerable dependencies
- [ ] Generated remediation PR with updated `requirements.txt`
- [ ] Created GitHub issue documenting findings
- [ ] Verified all ≥3 packages with CRITICAL/HIGH vulnerabilities flagged

---

## 🖼️ Expected Output

SBOM Summary section:
```
SBOM Analysis Complete
======================
Total Packages: 7
Vulnerable Packages: 5
Critical Issues: 2
High Issues: 3
Medium Issues: 2
Remediation: PR #45 created with updates
Status: Ready for Review
```

---

## 🆘 Troubleshooting

### Issue: "MCP server not responding"
```bash
# Reinitialize MCP
gh copilot mcp init github --force

# Check MCP status
gh copilot mcp status
```

### Issue: "Agent not found"
```bash
# Verify agent file exists
ls .github/agents/dependency-scout.py

# Re-register agent
gh copilot agent register --agent-path .github/agents/dependency-scout.py
```

### Issue: "SBOM not generated"
```bash
# Check agent logs
gh copilot agent run dependency-supply-chain-scout --verbose

# Ensure MCP tools available
gh copilot mcp tools list
```

---

## 📚 Resources

- **[MCP Documentation](./resources/reference.md)** | [Official Site](https://modelcontextprotocol.io/)
- **[GitHub Security Advisories](https://docs.github.com/en/code-security/security-advisories)**
- **[SBOM Standards (CYCLONEDX)](https://cyclonedx.org/)**
- **[Dependency Scanning Best Practices](./resources/reference.md)**
- **[Agents Reference Guide](./resources/agents-reference.md)**

---

## 🎯 Key Concepts

### What is MCP (Model Context Protocol)?

MCP connects Copilot agents to external tools and data sources:
- **API Access**: GitHub GraphQL, CVE databases, package registries
- **Tool Registry**: Agents can discover and use available tools
- **Context Passing**: Share findings between agents seamlessly

### Agent Chaining in This Exercise

```
dependency-scout agent
    ↓ (discovers vulnerabilities)
remediation-proposer agent
    ↓ (proposes fixes)
GitHub PR
    ↓ (automated review)
```

---

## 📌 Next Steps

Excellent work! You've demonstrated how to:
- **Integrate MCP** for external tool access
- **Deploy custom agents** via Copilot SDK
- **Generate SBOM** reports
- **Automate remediation** pull requests

### What's Next?

In **[Exercise 3: Secret Scanner & Agent Chaining](./3-secret-scanner-agent.md)**, you'll:
- Deploy a `secret-detector-enforcer` agent
- Demonstrate **agent-to-agent communication**
- Block commits containing exposed credentials
- Automatically create issues and fix PRs

**Ready?** → **[Exercise 3: Secret Scanner →](./3-secret-scanner-agent.md)**

---

**⏱️ Time Elapsed**: ~40 minutes cumulative  
**Exercises Completed**: 3/5 ✓
