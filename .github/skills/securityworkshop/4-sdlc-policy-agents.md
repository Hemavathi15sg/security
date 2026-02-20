# Exercise 4: SDLC Security Policy Agents (Advanced)

**Duration**: 25 minutes  
**Expected Time to Complete**: 25 min

---

## 🎯 Learning Objectives

By the end of this exercise, you will:

✅ Design organization-level security policies  
✅ Orchestrate multiple agents in a complex workflow  
✅ Integrate agents with GitHub Actions  
✅ Implement automated policy enforcement across SDLC  
✅ Understand production-ready security automation  

---

## 📖 Scenario Context

Executive asks: **"How do we ensure EVERY pull request meets our security standards before merge?"**

You need enterprise-level automation. Your solution: Build a **multi-agent orchestration system** that:
- Runs baseline security checks on every PR
- Enforces organization policies
- Blocks violations automatically
- Proposes fixes automatically
- Provides audit trail

This is Exercise 4 — bringing security throughout the entire Software Development Lifecycle (SDLC).

---

## 🔍 Task Overview

You'll:
1. Define security policies in YAML
2. Configure multi-agent orchestration
3. Set up GitHub Actions workflow
4. Test with policy violations
5. Watch automated review + blocking + remediation

---

## 📋 Step-by-Step Instructions

### Step 1: Define Security Policies

**Objective**: Codify your organization's security requirements.

Create organization security policy file:

```bash
cd securetrails-vulnerable

# Create policy file
mkdir -p .github/policies

cat > .github/policies/security-policy.yaml << 'EOF'
##############################################################################
# SecureTrails Security Policy
# Enforced via multi-agent orchestration on every PR
# Scope: Code review, deployment, compliance
##############################################################################

version: "1.0"
policy_name: "SecureTrails SDLC Security"
enforcer_team: "@security-team"

##############################################################################
# SECTION 1: CODE REVIEW POLICIES
##############################################################################

code_review_policies:
  
  baseline_security:
    enabled: true
    agent: "baseline-checker"
    description: "Static security analysis on code"
    rules:
      
      - rule_id: "SQL_INJECTION"
        description: "Detect SQL injection vulnerabilities"
        severity: "CRITICAL"
        check_patterns:
          - pattern: '(f"|f\').*WHERE.*{.*}'
            description: "F-string SQL queries with interpolation"
          - pattern: 'query = .*format\('
            description: "Format-based SQL with user input"
        files: ["*.py"]
        remediation: "Use parameterized queries or ORM"
        
      - rule_id: "XSS_VULNERABLE"
        description: "Cross-Site Scripting vulnerabilities"
        severity: "HIGH"
        check_patterns:
          - pattern: 'innerHTML\s*=\s*(?!.*escape)'
            description: "innerHTML without escaping"
          - pattern: '{{.*}}(?!.*autoescape)'
            description: "Template rendering without auto-escape"
        files: ["*.html", "*.js"]
        remediation: "Use template escaping or sanitization"
        
      - rule_id: "HARDCODED_SECRETS"
        description: "Hardcoded credentials in source"
        severity: "CRITICAL"
        check_patterns:
          - pattern: '(API_KEY|PASSWORD|TOKEN|SECRET)\s*=\s*["\'](?!.*example)'
            description: "Hardcoded secret values"
        files: ["*.py", "*.js", "*.java", "*.go"]
        remediation: "Move to environment variables or secrets manager"
        
      - rule_id: "WEAK_CRYPTO"
        description: "Insecure cryptographic functions"
        severity: "HIGH"
        check_patterns:
          - pattern: 'md5\('
            description: "MD5 hash (broken)"
          - pattern: 'sha1\('
            description: "SHA-1 hash (deprecated)"
          - pattern: 'hashlib\.md5'
            description: "Python MD5 usage"
        files: ["*.py", "*.js"]
        remediation: "Use bcrypt, argon2, or SHA-256+"
        
      - rule_id: "UNVALIDATED_INPUT"
        description: "User input used without validation"
        severity: "MEDIUM"
        check_patterns:
          - pattern: 'request\.(args|form|get)\[.*\]'
            description: "Direct request parameter access"
        files: ["*.py"]
        remediation: "Validate and sanitize all user input"

  compliance_policy:
    enabled: true
    agent: "compliance-enforcer"
    description: "Organization compliance requirements"
    rules:
      
      - rule_id: "CODE_REVIEW_APPROVAL"
        description: "Require security review approval"
        severity: "HIGH"
        requirement: "minimum_security_approvals"
        minimum_approvals: 1
        required_reviewers: ["@security-team", "@architecture-team"]
        
      - rule_id: "TEST_COVERAGE"
        description: "Security tests required"
        severity: "MEDIUM"
        requirement: "security_test_exists"
        message: "Must include test cases for security changes"
        
      - rule_id: "CHANGELOG_ENTRY"
        description: "Document security changes"
        severity: "LOW"
        requirement: "changelog_updated"
        file: "CHANGELOG.md"
        message: "Security changes must be documented"
        
      - rule_id: "NO_DEBUG_IN_PRODUCTION"
        description: "Prevent debug mode in production code"
        severity: "HIGH"
        check_patterns:
          - pattern: 'DEBUG\s*=\s*True'
            description: "Debug mode enabled"
          - pattern: 'console\.log\(.*\)'
            description: "Debug logs in production code"
        remediation: "Remove debug code or wrap in environment checks"

  remediation_policy:
    enabled: true
    agent: "remediation-proposer"
    description: "Automatic fix generation"
    auto_fix: true
    rules:
      - severity_threshold: "MEDIUM"
        auto_create_pr: true
        branch_prefix: "security/fix-"
      - severity_threshold: "HIGH"
        auto_create_branch: true
        require_approval_before_merge: true
      - severity_threshold: "CRITICAL"
        block_merge: true
        notify_security_team: true
        escalation: "create_incident"

##############################################################################
# SECTION 2: DEPLOYMENT POLICIES  
##############################################################################

deployment_policies:
  
  gate_checks:
    enabled: true
    agent: "compliance-enforcer"
    gates:
      
      - gate_id: "SECURITY_SCAN_PASS"
        description: "All security scans must pass"
        blocking: true
        check_type: "status_check"
        required_checks:
          - "baseline-security-check"
          - "dependency-scan"
          - "secret-detection"
        
      - gate_id: "SBOM_GENERATED"
        description: "Software Bill of Materials required"
        blocking: true
        file_required: "sbom.json"
        
      - gate_id: "SECURITY_APPROVAL"
        description: "Security team sign-off required"
        blocking: true
        required_approvals: 1
        teams: ["@security-team"]

##############################################################################
# SECTION 3: AGENT ORCHESTRATION RULES
##############################################################################

agent_orchestration:
  
  trigger_event: "pull_request"
  parallel_execution: false
  
  agents:
    
    - id: 1
      name: "baseline-checker"
      description: "Runs SAST + pattern matching"
      timeout: 60
      on_failure: "continue"
      output: "/tmp/baseline-violations.json"
      
    - id: 2
      name: "compliance-enforcer"
      description: "Checks org policies"
      timeout: 45
      depends_on: [1]
      input_source: "/tmp/baseline-violations.json"
      on_failure: "block_merge"
      output: "/tmp/compliance-decision.json"
      
    - id: 3
      name: "remediation-proposer"
      description: "Suggests + auto-creates fixes"
      timeout: 120
      depends_on: [2]
      input_source: "/tmp/compliance-decision.json"
      auto_fix: true
      on_failure: "notify_only"

##############################################################################
# SECTION 4: POLICY ACTIONS
##############################################################################

policy_actions:
  violation_found:
    - create_comment: true
      comment_tag: "@security-bot"
    - create_issue: true
      label: "security"
    - block_merge: true
    - notify_team: "@security-team"
  
  auto_fix_created:
    - create_pull_request: true
      title_prefix: "[SECURITY]"
    - assign_reviewers: ["@security-team"]
    - add_labels: ["security", "autoremediation", "needs-review"]
  
  policy_passed:
    - add_comment: "✓ Security policy checks passed"
    - allow_merge: true

##############################################################################
# SECTION 5: AUDIT & REPORTING
##############################################################################

audit:
  enabled: true
  log_all_checks: true
  retention_days: 90
  reports:
    daily: true
    weekly: true
    monthly: true

EOF

cat .github/policies/security-policy.yaml
```

---

### Step 2: Configure Multi-Agent Orchestration

**Objective**: Define how agents work together.

Create orchestration configuration:

```bash
cat > .github/agent-orchestration.yaml << 'EOF'
##############################################################################
# Multi-Agent Orchestration Configuration
# Defines agent sequence, dependencies, data flow
##############################################################################

orchestration_version: "1.0"
description: "SecureTrails Security Policy Orchestration"

trigger_configuration:
  events:
    - pull_request
    - pull_request_review
  conditions:
    - base_branch: "main"
    - exclude_paths:
        - "docs/**"
        - "*.md"

agent_pipeline:
  
  # STAGE 1: BASELINE SECURITY CHECK
  # ================================
  
  - stage_id: 1
    agent_name: "baseline-checker"
    description: "Static Application Security Testing (SAST)"
    
    configuration:
      mode: "analysis"
      timeout_seconds: 60
      
      scan_types:
        - "code_patterns"
        - "dependency_check"
        - "secret_scan"
        - "crypto_weak"
      
      file_patterns:
        include:
          - "*.py"
          - "*.js"
          - "*.html"
          - "*.sql"
        exclude:
          - "tests/**"
          - "node_modules/**"
          - "venv/**"
      
      policies: ".github/policies/security-policy.yaml"
    
    outputs:
      - type: "violations"
        file: "/tmp/baseline-violations.json"
        schema: "violations_schema_v1"
      
      - type: "metrics"
        file: "/tmp/baseline-metrics.json"
    
    on_completion:
      - store_artifacts: true
      - pass_to_next: true
      - notify_status: false  # Silent unless violations
  
  # STAGE 2: COMPLIANCE & POLICY ENFORCEMENT
  # ========================================
  
  - stage_id: 2
    agent_name: "compliance-enforcer"
    description: "Organizational Policy Validation"
    
    depends_on:
      - stage_id: 1
        input_mapping:
          violations: "/tmp/baseline-violations.json"
    
    configuration:
      mode: "enforcement"
      timeout_seconds: 45
      
      policy_file: ".github/policies/security-policy.yaml"
      
      decision_rules:
        - violation_severity: "CRITICAL"
          action: "block_merge"
          notify: true
        
        - violation_severity: "HIGH"
          action: "require_approval"
          minimum_approvals: 1
        
        - violation_severity: "MEDIUM"
          action: "flag_review"
          notify_team: "@security-team"
    
    outputs:
      - type: "compliance_decision"
        file: "/tmp/compliance-decision.json"
        structure:
          merge_allowed: boolean
          blocking_violations: array
          required_approvals: integer
          recommended_actions: array
    
    on_completion:
      - if_violations: "continue_to_remediation"
      - if_approved: "allow_merge"
      - pr_comment: true
  
  # STAGE 3: REMEDIATION & AUTO-FIX
  # ==============================
  
  - stage_id: 3
    agent_name: "remediation-proposer"
    description: "Automatic Remediation Proposals"
    
    depends_on:
      - stage_id: 2
        input_mapping:
          compliance_decision: "/tmp/compliance-decision.json"
      - stage_id: 1
        input_mapping:
          violations: "/tmp/baseline-violations.json"
    
    configuration:
      mode: "remediation"
      timeout_seconds: 120
      
      auto_fix:
        enabled: true
        create_pr: true
        branch_pattern: "security/fix-{issue_id}"
        
      fix_types:
        - "sql_injection_remediation"
        - "xss_fix"
        - "weak_crypto_upgrade"
        - "secret_removal"
      
      pr_configuration:
        title_template: "[SECURITY] Auto-fix: {violation_type}"
        description_template: |
          Auto-generated security fix
          Violations: {violation_count}
          Severity: {max_severity}
          
          This PR addresses security findings from automated analysis.
          Review carefully and merge if appropriate.
        
        labels:
          - "security"
          - "autoremediation"
          - "needs-review"
        
        assignees:
          - "@security-team"
        
        request_reviews:
          teams:
            - "@security-team"
            - "@backend-team"
    
    outputs:
      - type: "fix_created"
        file: "/tmp/remediation-result.json"
    
    on_completion:
      - create_pr_if_violations: true
      - notify_team: true
      - pr_comment: true

# MONITORING & LOGGING
monitoring:
  enabled: true
  log_level: "INFO"
  metrics_enabled: true
  
  dashboards:
    - "security_policies_coverage"
    - "agent_execution_performance"
    - "violation_trends"

# ERROR HANDLING
error_handling:
  agent_timeout:
    action: "skip_agent"
    notify: true
  
  agent_failure:
    action: "block_merge"
    notify: "@security-team"
  
  data_inconsistency:
    action: "retry_stage"
    max_retries: 2

EOF

cat .github/agent-orchestration.yaml
```

---

### Step 3: Create GitHub Actions Workflow

**Objective**: Trigger agent orchestration on every PR.

Create the main security workflow:

```bash
cat > .github/workflows/security-policy-check.yml << 'EOF'
name: "Security Policy Check & Enforcement"

on:
  pull_request:
    branches:
      - main
      - develop
      - staging
    paths-ignore:
      - "*.md"
      - "docs/**"

jobs:
  
  security-orchestration:
    name: "Multi-Agent Security Orchestration"
    runs-on: ubuntu-latest
    permissions:
      contents: read
      pull-requests: write
      issues: write
      checks: write
    
    steps:
      
      - name: "Checkout code"
        uses: actions/checkout@v3
        with:
          fetch-depth: 0  # Full history for scanning
      
      - name: "Set up Copilot CLI"
        run: |
          gh extension install github/gh-copilot || gh extension upgrade github/gh-copilot
          gh copilot auth
      
      - name: "Load Orchestration Config"
        run: |
          echo "✓ Loading orchestration configuration..."
          cat .github/agent-orchestration.yaml
      
      # STAGE 1: BASELINE SECURITY CHECK
      - name: "Stage 1: Baseline Security Analysis"
        id: baseline
        run: |
          echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
          echo "STAGE 1: Baseline Security Checker Agent"
          echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
          
          gh copilot agent run "baseline-checker" \
            --prompt "Analyze all modified files in PR #${{ github.event.pull_request.number }} for security violations per .github/policies/security-policy.yaml. Check for: SQL injection patterns, XSS vectors, hardcoded secrets, weak cryptography, unvalidated input. Generate violations.json with file, line, severity, description." \
            --context-file ".github/agent-orchestration.yaml" \
            --output "/tmp/baseline-violations.json"
          
          echo "baseline_completed=true" >> $GITHUB_OUTPUT
          echo "✓ Baseline analysis complete"
      
      # STAGE 2: COMPLIANCE ENFORCEMENT
      - name: "Stage 2: Compliance Policy Enforcement"
        id: compliance
        if: steps.baseline.outputs.baseline_completed == 'true'
        run: |
          echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
          echo "STAGE 2: Compliance Enforcer Agent"
          echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
          
          gh copilot agent run "compliance-enforcer" \
            --prompt "Review violations from baseline scan (/tmp/baseline-violations.json) against .github/policies/security-policy.yaml compliance rules. Determine: should PR be blocked? Which violations are critical? What approvals required? Output compliance-decision.json with merge_allowed, blocking_violations, required_approvals." \
            --input-file "/tmp/baseline-violations.json" \
            --context-file ".github/policies/security-policy.yaml" \
            --output "/tmp/compliance-decision.json"
          
          echo "compliance_completed=true" >> $GITHUB_OUTPUT
          echo "✓ Compliance check complete"
      
      # STAGE 3: REMEDIATION & AUTO-FIX
      - name: "Stage 3: Remediation Proposer Agent"
        id: remediation
        if: steps.compliance.outputs.compliance_completed == 'true'
        run: |
          echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
          echo "STAGE 3: Remediation Proposer Agent"
          echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
          
          gh copilot agent run "remediation-proposer" \
            --prompt "Based on violations (/tmp/baseline-violations.json) and compliance decision (/tmp/compliance-decision.json), create detailed remediation steps and auto-generate fix PR. Generate fixes for: SQL injection (use parameterized queries), XSS (add escaping), secrets (move to .env), weak crypto (upgrade to bcrypt), unvalidated input (add validation). Output fix PR details." \
            --input-files "/tmp/baseline-violations.json,/tmp/compliance-decision.json" \
            --auto-pr "true" \
            --pr-config ".github/agent-orchestration.yaml" \
            --output "/tmp/remediation-result.json"
          
          echo "remediation_completed=true" >> $GITHUB_OUTPUT
          echo "✓ Remediation proposals complete"
      
      # POLICY VERDICT & FEEDBACK
      - name: "Determine Policy Verdict"
        id: verdict
        run: |
          echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
          echo "POLICY VERDICT"
          echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
          
          # Check compliance decision
          if jq -e '.merge_allowed' /tmp/compliance-decision.json >/dev/null 2>&1; then
            VERDICT="APPROVED"
            echo "✓ All security policies PASSED"
          else
            VERDICT="BLOCKED"
            echo "✗ Security policies FAILED - Merge BLOCKED"
          fi
          
          echo "verdict=$VERDICT" >> $GITHUB_OUTPUT
      
      # POST COMMENT TO PR
      - name: "Post Agent Findings to PR"
        if: always()
        uses: actions/github-script@v6
        with:
          github-token: ${{ secrets.GITHUB_TOKEN }}
          script: |
            const fs = require('fs');
            const baseline = JSON.parse(fs.readFileSync('/tmp/baseline-violations.json', 'utf8'));
            const compliance = JSON.parse(fs.readFileSync('/tmp/compliance-decision.json', 'utf8'));
            
            let comment = `## 🔐 Security Policy Check Results\n\n`;
            comment += `### Stage 1: Baseline Analysis\n`;
            comment += `- Violations Found: **${baseline.violations?.length || 0}**\n`;
            comment += `- Critical: **${baseline.critical_count || 0}** | High: **${baseline.high_count || 0}** | Medium: **${baseline.medium_count || 0}**\n\n`;
            
            comment += `### Stage 2: Compliance Enforcement\n`;
            comment += compliance.merge_allowed 
              ? `✓ **Policy Status: PASSED** - Merge allowed\n`
              : `✗ **Policy Status: BLOCKED** - Merge blocked due to violations\n`;
            
            if (baseline.violations?.length > 0) {
              comment += `\n### Violations Detected\n\`\`\`\n`;
              baseline.violations.slice(0, 5).forEach(v => {
                comment += `${v.file}:${v.line} | ${v.severity} | ${v.type}\n`;
              });
              comment += `\`\`\`\n`;
            }
            
            comment += `\n### Stage 3: Remediation\n`;
            comment += `- Automated fix PR created: ✓\n`;
            comment += `- Review suggested fixes and merge when ready\n`;
            
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: comment
            });
      
      # BLOCK MERGE IF NEEDED
      - name: "Block Merge on Policy Violation"
        if: steps.verdict.outputs.verdict == 'BLOCKED'
        run: |
          echo "::error::Security policy violations detected. Merge blocked."
          exit 1
      
      - name: "Approve for Merge"
        if: steps.verdict.outputs.verdict == 'APPROVED'
        run: |
          echo "::notice::All security policies passed ✓"

EOF

cat .github/workflows/security-policy-check.yml
```

---

### Step 4: Test Policy Enforcement

**Objective**: Trigger the multi-agent workflow on a PR.

Create a test branch with a policy violation:

```bash
# Create test branch
git checkout -b test/policy-violation-xss

# Create a file with an XSS vulnerability (intentional)
cat > templates/vulnerable-feature.html << 'EOF'
{% extends "base.html" %}

{% block content %}
<div class="new-feature">
  <h1>User Feedback</h1>
  
  <!-- VIOLATION: XSS - innerHTML without escaping -->
  <div id="comments">
    {{ user_comment }}  ← User input rendered directly!
  </div>
  
  <script>
    // VIOLATION: Unsafe DOM manipulation
    document.getElementById('comments').innerHTML = userInput;
  </script>
</div>
{% endblock %}
EOF

# Also add a SQL injection vulnerability to trigger blocking
cat > app_update.py << 'EOF'
# VIOLATION: SQL Injection
@app.route('/search')
def search():
    query = f"SELECT * FROM trails WHERE name = '{request.args.get('q')}'"  # DANGEROUS!
    results = db.execute(query)
    return results
EOF

# Commit and push
git add .
git commit -m "feat: Add new feedback feature with search

NOTE: This commit intentionally contains security violations for Exercise 4 testing"

git push origin test/policy-violation-xss
```

**Create PR via GitHub:**

```bash
# Create PR
gh pr create \
  --title "feat: Add user feedback feature" \
  --body "This PR adds a new user feedback tracking system with search functionality.

## Changes
- New templates/vulnerable-feature.html
- Search endpoint in app.py

## Testing
- Tested locally

Note: This is a test PR for Exercise 4 policy enforcement" \
  --head test/policy-violation-xss \
  --base main
```

**Wait for workflow to execute:**

```bash
# Watch workflow run
gh run list --workflow security-policy-check.yml --limit 1

# View workflow results
gh run view <run-id> --log
```

---

### Step 5: Review Agent Analysis & Blocking

**Objective**: Observe multi-agent orchestration in action.

Expected workflow execution:

```
STAGE 1: Baseline Security Checker
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✓ Scanning templates/vulnerable-feature.html
✗ XSS violation found: innerHTML without escaping (line 12)
✓ Scanning app_update.py
✗ SQL Injection violation found: f-string SQL query (line 4)
━ Result: 2 violations found (1 CRITICAL, 1 HIGH)

STAGE 2: Compliance Enforcer
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✓ Checking violations against security-policy.yaml
✗ CRITICAL violation: SQL_INJECTION (blocks merge)
✗ HIGH violation: XSS_VULNERABLE (requires approval)
━ Decision: MERGE BLOCKED due to CRITICAL violation
━ Required Actions: Fix violations + security approval needed

STAGE 3: Remediation Proposer
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✓ Generating fixes for violations
✓ Creating auto-fix PR...
✓ PR #XX: "[SECURITY] Auto-fix: XSS + SQL Injection"
━ Suggested Fixes:
  - Line 12: Add |safe filter and use Jinja2 auto-escape
  - Line 4: Use parameterized query with db.execute()
```

**Check PR status:**

```bash
# Get PR details
gh pr view <pr-number>

# Expected status: "DRAFT" created by remediation agent
# With comment from security-bot showing violations
```

---

### Step 6: Review Agent Comment & Fix PR

**Objective**: Examine automated feedback and proposed fixes.

Expected PR comment from agents:

```
## 🔐 Security Policy Check Results

### Stage 1: Baseline Analysis
- Violations Found: **2**
- Critical: **1** | High: **1** | Medium: **0**

### Stage 2: Compliance Enforcement
✗ **Policy Status: BLOCKED** - Merge blocked due to violations

### Violations Detected
```
templates/vulnerable-feature.html:12 | HIGH | XSS_VULNERABLE
app_update.py:4 | CRITICAL | SQL_INJECTION
```

### Stage 3: Remediation
- Automated fix PR created: PR #XX-fix
- Review suggested fixes and merge when ready

---

### Fix PR Details:

```bash
# View the auto-created fix PR
gh pr view <fix-pr-number>

# Expected content:
# Title: [SECURITY] Auto-fix: XSS + SQL Injection
# 
# Changes:
# - templates/vulnerable-feature.html: Changed to use |escape filter
# - app_update.py: Updated to use parameterized queries
```

---

### Step 7: Document Exercise Completion

**Objective**: Create comprehensive audit of multi-agent orchestration.

```bash
gh issue create \
  --title "[SECURITY AUDIT] Exercise 4: SDLC Multi-Agent Orchestration" \
  --label "security,review-exercise" \
  --body "## Exercise 4: SDLC Security Policy Agents Complete

### Mission: Enterprise Security Automation
Status: ✓ COMPLETE

### Multi-Agent Orchestration Summary

#### Agent 1: Baseline Security Checker
- Purpose: SAST + pattern detection
- Findings: 2 violations (1 CRITICAL, 1 HIGH)
- Execution Time: ~12 seconds
- Output: baseline-violations.json

#### Agent 2: Compliance Enforcer  
- Purpose: Policy validation + enforcement
- Decision: MERGE BLOCKED (CRITICAL violation)
- Required Actions: Fix violations + security approval
- Execution Time: ~8 seconds
- Output: compliance-decision.json

#### Agent 3: Remediation Proposer
- Purpose: Auto-generate fixes
- Action: Created fix PR #XX-fix
- Suggestions: 2 specific remediation steps for each violation
- Execution Time: ~35 seconds
- Output: PR created with fixes

### Policy Enforcement Demonstrated

✓ **Blocking**: Prevented merge due to CRITICAL violations  
✓ **Automation**: Auto-created fix PR without manual intervention  
✓ **Audit Trail**: Complete record of findings and decisions  
✓ **Composability**: 3 agents working sequentially with data sharing  
✓ **Efficiency**: <60 seconds for complete orchestration  

### GitHub Actions Integration

✓ Triggered on: Pull request to main branch  
✓ Workflow file: .github/workflows/security-policy-check.yml  
✓ Stages: 3 sequential agent stages  
✓ PR Comment: Automated findings posted  
✓ Merge Control: Blocks on CRITICAL violations  

### Policies Enforced

✓ SQL Injection prevention (parameterized queries)  
✓ XSS prevention (template escaping)  
✓ Secret detection (hardcoded credentials)  
✓ Weak cryptography check (MD5/SHA1 blocking)  
✓ Input validation requirement  

### Key Learnings

1. **Multi-Agent Orchestration**: Agents work sequentially with defined dependencies
2. **Data Flow**: Violations flow from analyzer → enforcer → remediator
3. **Policy as Code**: security-policy.yaml defines all rules
4. **Automation Scale**: Entire SDLC security from commit detection to fix PR
5. **Production Ready**: GitHub Actions integration for enterprise deployment

### Violations Detected in Test PR

| File | Line | Type | Severity | Status |
|------|------|------|----------|--------|
| app_update.py | 4 | SQL_INJECTION | CRITICAL | Fixed in PR #XX-fix |
| vulnerable-feature.html | 12 | XSS_VULNERABLE | HIGH | Fixed in PR #XX-fix |

### Remediation Status

- Fix PR Created: ✓ PR #XX-fix
- Both violations addressed: ✓
- Merge blocked until approved: ✓
- Security team notified: ✓

### Orchestration Flow Chart

```
PR Created (test/policy-violation-xss)
              ↓
         ┌─────────┐
         │ STAGE 1 │  Baseline Security Checker
         │ (12s)   │  → Finds 2 violations
         └────┬────┘
              ↓
         ┌─────────┐
         │ STAGE 2 │  Compliance Enforcer
         │ (8s)    │  → Blocks merge (CRITICAL)
         └────┬────┘
              ↓
         ┌─────────┐
         │ STAGE 3 │  Remediation Proposer
         │ (35s)   │  → Creates fix PR
         └────┬────┘
              ↓
    MERGE BLOCKED + FIX PR CREATED
    (Total execution: ~55 seconds)
```

### Next Steps

1. Review auto-generated fix PR (#XX-fix)
2. Approve merge of original PR only after fixes applied
3. Verify no regressions after merge

### Enterprise Application

This pattern enables:
- **Compliance as Code**: All requirements in YAML
- **Automated Enforcement**: Every PR automatically checked
- **Scalability**: Same agents work for any repository
- **Audit Trail**: Complete history of all checks
- **Developer Experience**: Fast feedback, suggested fixes

---
Generated by Exercise 4: SDLC Security Policy Agents  
Timestamp: 2026-02-20 11:15:00 UTC  
Agents Involved: 3  
Total Execution Time: ~55 seconds  
Violations Detected: 2  
Fix PRs Created: 1  
Merge Status: BLOCKED (until violations fixed)
"
```

---

## ✅ Acceptance Criteria

- [ ] Created `.github/policies/security-policy.yaml` with comprehensive rules
- [ ] Created `.github/agent-orchestration.yaml` with multi-agent pipeline
- [ ] Created `.github/workflows/security-policy-check.yml` GitHub Actions workflow
- [ ] Triggered workflow on test PR with intentional violations
- [ ] All 3 agents executed successfully in sequence
- [ ] Violations correctly identified and reported
- [ ] PR correctly blocked due to CRITICAL violation
- [ ] Auto-remediation PR created with suggested fixes
- [ ] Agent executed <60 seconds total
- [ ] Documented complete orchestration flow

---

## 🖼️ Expected Final Output

```
✓ Security Policy Orchestration Complete
✓ Stage 1: 2 violations found
✓ Stage 2: Merge blocked (CRITICAL found)
✓ Stage 3: Fix PR created
✓ Total Time: 54 seconds
✓ All agents executed successfully
```

---

## 🎓 Advanced Concepts Demonstrated

### 1. Agent Orchestration Pattern
```
Agent A → Agent B → Agent C
(Sequential with data passing)
```

### 2. Policy-Driven Enforcement
```
YAML Policy → Agent Enforcement → Merge Control
```

### 3. SDLC Integration
```
Developer → Git Push → Security Agents → Auto-Fix → Merge Gate
```

---

## 📚 Resources

- [Multi-Agent Patterns](./resources/agents-reference.md)
- [GitHub Actions Security](./resources/reference.md)
- [Policy YAML Specification](./resources/agents-reference.md)

---

## 🎯 Workshop Completion!

Congratulations! You've completed all 5 exercises of the SecureTrails Security Workshop.

### What You've Learned

✅ **Exercise 0**: Set up secure development environment  
✅ **Exercise 1**: Use agents for vulnerability discovery  
✅ **Exercise 2**: Integrate MCP for supply chain security  
✅ **Exercise 3**: Deploy agents with chaining capability  
✅ **Exercise 4**: Orchestrate agents for organization-wide SDLC security  

### Skills Acquired

- GitHub Copilot CLI usage
- Custom agent deployment (SDK)
- MCP integration
- Agent chaining and composition
- Multi-agent orchestration
- GitHub Actions integration
- Security policy enforcement
- Automated remediation
- Production security workflows

### Take-Home

1. Clone the pattern to your organization's repos
2. Customize `.github/policies/security-policy.yaml`
3. Adapt agents for your specific security requirements
4. Scale to all repositories in your organization

---

**🏆 Workshop Complete!**

**Total Time**: ~120 minutes  
**Exercises**: 5/5 ✓  
**Agents Deployed**: 6  
**GitHub Actions Workflows**: 1  
**Security Policies**: 1 comprehensive policy file  
**Vulnerabilities Blocked**: Unlimited (automated)  

---

**Next**: Apply these patterns to your own repositories and customize for your organization's security requirements.

See you next workshop! 🚀
