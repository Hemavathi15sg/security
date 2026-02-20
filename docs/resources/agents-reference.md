# Agents Reference Guide

Comprehensive reference for all custom security agents used in the SecureTrails Security Workshop.

---

## 📌 Agent Overview

| Agent Name | Purpose | Exercise | Type | Status |
|-----------|---------|----------|------|--------|
| `baseline-checker` | SAST + pattern detection | 1, 4 | Analysis | Active |
| `dependency-supply-chain-scout` | Vulnerable dependency detection | 2 | Analysis | Active |
| `issue-reporter` | Auto-create GitHub issues | 3 | Helper | Active |
| `secret-detector-enforcer` | Credential leak prevention | 3 | Enforcement | Active |
| `remediation-proposer` | Auto-generate fixes | 3, 4 | Remediation | Active |
| `compliance-enforcer` | Policy validation | 4 | Enforcement | Active |

---

## 🔍 Agent 1: Baseline Security Checker

**Purpose**: Static Application Security Testing (SAST) via pattern matching

**Deployed in**: Exercise 1 (basic usage), Exercise 4 (orchestration)

**Capabilities**:
- Scans code for OWASP Top 10 patterns
- Identifies SQL injection entry points
- Detects XSS vectors in HTML/JS
- Finds hardcoded secrets
- Detects weak cryptography
- Validates user input handling

**Usage**:

```bash
# Basic usage (Exercise 1)
gh copilot explain app.py
# Then provide prompt about security issues

# Agent execution (Exercise 4)
gh copilot agent run baseline-checker \
  --prompt "Analyze all modified files in PR for security violations per .github/policies/security-policy.yaml"
```

**Configuration**:
```yaml
agent_name: baseline-checker
type: analysis
timeout: 60
file_patterns:
  include: ["*.py", "*.js", "*.html", "*.sql"]
  exclude: ["tests/**", "node_modules/**"]
  
policies:
  - SQL_INJECTION: "F-string SQL queries, format-based"
  - XSS_VULNERABLE: "innerHTML, unsafe DOM methods"
  - HARDCODED_SECRETS: "API_KEY, PASSWORD, TOKEN values"
  - WEAK_CRYPTO: "MD5, SHA-1 usage"
  - UNVALIDATED_INPUT: "Direct request access without validation"
```

**Output Format**:
```json
{
  "violations": [
    {
      "file": "app.py",
      "line": 47,
      "severity": "CRITICAL",
      "type": "SQL_INJECTION",
      "description": "User input in SQL query",
      "code_snippet": "query = f\"SELECT * FROM users WHERE username = '{username}'\"",
      "remediation": "Use parameterized queries or ORM"
    }
  ],
  "summary": {
    "total_violations": 7,
    "critical": 2,
    "high": 3,
    "medium": 2
  }
}
```

**Chaining**: Output passed to `compliance-enforcer` for policy validation

---

## 📦 Agent 2: Dependency Supply Chain Scout

**Purpose**: Identify and analyze vulnerable dependencies

**Deployed in**: Exercise 2

**Capabilities**:
- Parses `requirements.txt` and `package.json`
- Queries GitHub Security Advisories via MCP
- Cross-references CVE databases
- Generates Software Bill of Materials (SBOM)
- Recommends package updates
- Assesses upgrade compatibility

**Usage**:

```bash
# Agent execution
gh copilot agent run dependency-supply-chain-scout \
  --prompt "Analyze requirements.txt and generate detailed SBOM. For each dependency: list version, CVE IDs, severity, recommended version"
```

**Configuration**:
```yaml
agent_name: dependency-supply-chain-scout
type: analysis
mode: supply_chain
timeout: 90
targets:
  - requirements.txt
  - package.json
  - Gemfile
  
output_format: sbom_v1.3
```

**Output Format (SBOM)**:
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
          "description": "Werkzeug RCE via environment reloader",
          "published": "2021-03-30",
          "advisory_url": "https://github.com/advisories/..."
        }
      ],
      "recommended_version": "2.3.2"
    }
  ],
  "summary": {
    "total_packages": 7,
    "with_vulnerabilities": 5,
    "critical": 2,
    "high": 3,
    "medium": 2
  }
}
```

**Triggers**: Exercise 2, Exercise 4 (part of orchestration)

**Chaining**: Chains to `remediation-proposer` for automated updates

---

## ⚠️ Agent 3: Secret Detector Enforcer

**Purpose**: Prevent credential leaks before commit

**Deployed in**: Exercise 3

**Capabilities**:
- Regex pattern matching for common secrets
- Entropy analysis for random strings
- Scans file extensions (.env, .pem, .key)
- Blocks commits with exposed credentials
- Integrates with pre-commit hooks
- Provides detailed violation reports

**Usage**:

```bash
# Register agent
gh copilot agent register \
  --agent-path .github/agents/secret-detector.py \
  --name "secret-detector-enforcer" \
  --triggers "pre-commit,pre-push" \
  --chaining-enabled true

# Manual invocation
gh copilot agent run secret-detector-enforcer \
  --prompt "Scan repository for exposed credentials"
```

**Configuration**:
```yaml
agent_name: secret-detector-enforcer
type: enforcement
triggers:
  - pre-commit
  - pre-push
  
detection_patterns:
  api_keys:
    - pattern: "API_KEY['\"]?\\s*[:=]\\s*['\"][^'\"]+['\"]"
    - pattern: "sk_live_[0-9a-zA-Z]{20,}"  # Stripe
  
  aws_keys:
    - pattern: "AKIA[0-9A-Z]{16}"
  
  tokens:
    - pattern: "ghp_[0-9a-zA-Z]{36}"  # GitHub token
    - pattern: "ghu_[0-9a-zA-Z]{36}"  # GitHub user token
  
  passwords:
    - pattern: "PASSWORD['\"]?\\s*[:=]\\s*['\"][^'\"]+['\"]"
    - pattern: "DATABASE_URL.*:[^@]+@"  # DB password
  
  encryption_keys:
    - pattern: "-----BEGIN (RSA|OPENSSH|ENCRYPTED) PRIVATE KEY-----"

entropy_threshold: 0.7  # Shannon entropy for random strings
```

**Triggers**: Git pre-commit hook, manual execution

**Chains To**: 
1. `issue-reporter` (creates GitHub issue)
2. `remediation-proposer` (generates fix PR)

**Example Flow**:
```
Developer: git commit
  ↓
secret-detector-enforcer detects hardcoded API key
  ↓
Commit BLOCKED ✗
  ↓
Calls issue-reporter → Issue #47 created
  ↓
Calls remediation-proposer → PR #48 created
  ↓
Output: "Use PR #48 for remediation"
```

---

## 📝 Agent 4: Issue Reporter

**Purpose**: Auto-create GitHub issues with findings

**Deployed in**: Exercise 3 (chained from secret-detector)

**Capabilities**:
- Creates GitHub issues from agent findings
- Auto-formats violation details
- Adds appropriate labels
- Assigns to security team
- Provides context and remediation steps

**Usage**:

```bash
# Automatically invoked by secret-detector agent
gh copilot agent run issue-reporter \
  --input-file findings.json \
  --prompt "Create GitHub issue with security findings"
```

**Configuration**:
```yaml
agent_name: issue-reporter
type: helper
parent_agent: secret-detector-enforcer

issue_template: |
  🚨 {{SEVERITY}} Security Issue Detected
  
  ## Findings
  {{FORMATTED_VIOLATIONS}}
  
  ## Remediation
  {{SUGGESTED_FIXES}}
  
  Generated by: {{AGENT_NAME}}

labeling:
  - security
  - autogenerated
  - "severity-{{SEVERITY}}"

assignment:
  teams:
    - "@security-team"

comment_on_pr: true
```

**Input Format** (from parent agent):
```json
{
  "violations": [...],
  "severity": "CRITICAL",
  "agent_chain": "secret-detector → issue-reporter"
}
```

**Chained After**: `secret-detector-enforcer`

---

## 🔧 Agent 5: Remediation Proposer

**Purpose**: Auto-generate fixes for security violations

**Deployed in**: Exercise 3, Exercise 4

**Capabilities**:
- Analyzes violations and generates fixes
- Creates pull requests with suggested changes
- Maintains code compatibility
- Provides detailed commit messages
- Tests fixes locally
- Auto-merges low-risk fixes (optional)

**Usage**:

```bash
# Chained from secret-detector or baseline-checker
gh copilot agent run remediation-proposer \
  --input-file violations.json \
  --prompt "Generate PR with security fixes"

# With auto-PR creation
gh copilot agent run remediation-proposer \
  --input-file violations.json \
  --auto-pr true \
  --pr-config ".github/agent-orchestration.yaml"
```

**Configuration**:
```yaml
agent_name: remediation-proposer
type: remediation
auto_fix:
  enabled: true
  create_pr: true
  
fix_strategies:
  SQL_INJECTION: "parameterized_query"
  XSS_VULNERABLE: "jinja2_escape"
  HARDCODED_SECRETS: "move_to_env"
  WEAK_CRYPTO: "upgrade_algorithm"

pr_configuration:
  title_template: "[SECURITY] Fix {{violation_count}} violations"
  branch_prefix: "security/fix-"
  labels:
    - "security"
    - "autoremediation"
  
  commit_message_template: |
    security: Address {{violation_type}} vulnerabilities
    
    Fixes:
    {{FIXED_VIOLATIONS}}
    
    Resolves Exercise {{EXERCISE_NUMBER}}
```

**Example Outputs**:

**For SQL Injection**:
```python
# Before
query = f"SELECT * FROM users WHERE username = '{username}'"
results = db.execute(query)

# After (generated fix)
query = "SELECT * FROM users WHERE username = ?"
results = db.execute(query, (username,))
```

**For XSS in Templates**:
```html
<!-- Before -->
<div>{{ user_comment }}</div>

<!-- After (generated fix) -->
<div>{{ user_comment | escape }}</div>
```

**For Hardcoded Secrets**:
```python
# Before
JWT_SECRET = 'super-secret-key-12345'

# After (generated fix)
import os
JWT_SECRET = os.getenv('JWT_SECRET')
```

**Chained After**: Any detection agent

---

## 🚨 Agent 6: Compliance Enforcer

**Purpose**: Enforce organization security policies

**Deployed in**: Exercise 4 (multi-agent orchestration)

**Capabilities**:
- Validates violations against policies
- Determines merge approval/blocking
- Checks required approvals
- Enforces deployment gates
- Escalates high-severity issues
- Generates compliance reports

**Usage**:

```bash
# In multi-agent orchestration
gh copilot agent run compliance-enforcer \
  --input-file baseline-violations.json \
  --context-file ".github/policies/security-policy.yaml" \
  --prompt "Review violations against compliance policy"
```

**Configuration**:
```yaml
agent_name: compliance-enforcer
type: enforcement
policy_source: ".github/policies/security-policy.yaml"

decision_logic:
  severity_CRITICAL:
    action: block_merge
    require_security_approval: 1
    escalate: create_incident
  
  severity_HIGH:
    action: require_approval
    minimum_approvals: 1
    auto_comment: true
  
  severity_MEDIUM:
    action: flag_review
    notify_team: "@security-team"
  
  severity_LOW:
    action: auto_approve
    comment: "Low severity, auto-approved"
```

**Output Format**:
```json
{
  "merge_allowed": false,
  "blocking_violations": ["SQL_INJECTION", "CRITICAL"],
  "required_approvals": 1,
  "recommended_actions": [
    "Fix SQL injection in app.py:47",
    "Request security review",
    "Review auto-fix PR #XX"
  ],
  "policy_version": "1.0",
  "enforcement_timestamp": "2026-02-20T10:45:00Z"
}
```

**Chained After**: `baseline-checker`

---

## 🔗 Agent Chaining Patterns

### Pattern 1: Security Analysis Chain (Exercise 1)
```
User Analysis
    ↓
baseline-checker (SAST)
    ↓
Issue Documentation
```

### Pattern 2: Supply Chain Chain (Exercise 2)
```
dependency-scout (find vulns)
    ↓
remediation-proposer (create fixes)
    ↓
GitHub PR Created
```

### Pattern 3: Secret Detection Chain (Exercise 3)
```
secret-detector (finds credentials)
    ↓
issue-reporter (creates issue)
    ↓
remediation-proposer (generates fix)
    ↓
Complete Remediation
```

### Pattern 4: SDLC Orchestration Chain (Exercise 4)
```
baseline-checker (SAST)
    ↓
compliance-enforcer (policy check)
    ↓
remediation-proposer (generate fixes)
    ↓
Merge Gate Enforcement
```

---

## 🛠️ Agent Configuration Format

### Template
```yaml
agent_configuration:
  name: "agent-name"
  version: "1.0"
  type: "analysis|enforcement|remediation|helper"
  
  metadata:
    description: "What the agent does"
    author: "@security-team"
    maintained: true
  
  capabilities:
    - "capability 1"
    - "capability 2"
  
  configuration:
    timeout: 60
    retries: 2
    parallel: false
  
  triggers:
    event: "pull_request"
    paths:
      include: ["*.py", "*.js"]
      exclude: ["tests/**"]
  
  inputs:
    - name: "violations"
      type: "json"
      required: true
    - name: "policy"
      type: "yaml"
      required: false
  
  outputs:
    - name: "findings"
      type: "json"
      schema: "findings_schema_v1"
  
  chaining:
    can_call: ["issue-reporter", "remediation-proposer"]
    receives_from: ["baseline-checker"]
  
  error_handling:
    on_failure: "continue|block|notify"
    retry_policy: "exponential_backoff"
```

---

## 📊 Agent Execution Flow

```
┌─────────────────────────────────────────────┐
│ Trigger Event (PR, commit, manual)          │
└────────────┬────────────────────────────────┘
             ↓
┌─────────────────────────────────────────────┐
│ Agent 1: Detection/Analysis                 │
│ - baseline-checker (SAST)                   │
│ - dependency-scout (supply chain)           │
│ - secret-detector (credentials)             │
└────────────┬────────────────────────────────┘
             ↓
     ┌──────────────────┐
     │ Violations?      │
     └───┬──────────┬───┘
     YES │          │ NO
        ↓          └──→ PASS ✓
┌─────────────────────────────────────────────┐
│ Agent 2: Policy/Validation                  │
│ - compliance-enforcer (policy check)        │
│ - issue-reporter (track findings)           │
└────────────┬────────────────────────────────┘
             ↓
     ┌──────────────────┐
     │ Fix?             │
     └───┬──────────┬───┘
     YES │          │ NO
        ↓          └──→ BLOCKED ✗
┌─────────────────────────────────────────────┐
│ Agent 3: Remediation                        │
│ - remediation-proposer (auto-fix)           │
│ - Creates PR with suggested fixes           │
└────────────┬────────────────────────────────┘
             ↓
┌─────────────────────────────────────────────┐
│ Output: Complete Remediation Package        │
│ - Issue with findings                       │
│ - PR with fixes                             │
│ - Audit trail                               │
└─────────────────────────────────────────────┘
```

---

## 🧪 Testing Agents

### Test Pattern
```bash
# 1. Manual invocation
gh copilot agent run <agent-name> \
  --prompt "<test-prompt>" \
  --verbose \
  --log-level debug

# 2. Check output
cat /tmp/agent-output.json | jq

# 3. Verify schema
# Compare against expected output format

# 4. Chain test
gh copilot agent run agent1 --output /tmp/out1.json
gh copilot agent run agent2 --input-file /tmp/out1.json
```

---

## 🐛 Debugging Failed Agents

### Common Issues

**Issue**: Agent timeout
```bash
# Increase timeout in agent config
timeout: 120  # from 60

# Or reduce dataset
# Test on smaller scope first
```

**Issue**: Missing dependencies
```bash
# Check agent logs
gh copilot agent logs <agent-name>

# Install missing libraries
pip install -r .github/agents/requirements.txt
```

**Issue**: Policy file not found
```bash
# Verify file paths
ls -la .github/policies/
ls -la .github/agent-orchestration.yaml

# Use absolute paths in config
policy_source: "/home/user/repo/.github/policies/security-policy.yaml"
```

---

## 📚 Resources

- **Agent SDK**: [Copilot SDK Documentation](https://docs.github.com/en/copilot/building-copilot-extensions)
- **Orchestration**: [Agent Choreography Patterns](https://docs.github.com/en/copilot)
- **Security Policies**: [OWASP Top 10](https://owasp.org/Top10/)

---

## 🎓 Learning Path

1. **Exercise 1**: Understand `baseline-checker` capabilities
2. **Exercise 2**: Learn `dependency-scout` + MCP integration
3. **Exercise 3**: Implement agent chaining with `secret-detector`
4. **Exercise 4**: Master multi-agent orchestration with all agents

---

*Last Updated: February 2026*  
*Agents Version: 1.0*  
*Workshop Edition*
