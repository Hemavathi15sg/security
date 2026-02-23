# Exercise 4: GitHub Actions Integration - Orchestrate Your Security Ecosystem
## Combining GHAS + Copilot CLI + Custom Tools

**Duration**: 20 minutes  
**Type**: ⭐⭐⭐⭐⭐ Full automation  
**Focus**: Chain tools together into automated workflows

---

## 🎯 Learning Objectives

✅ Create a GitHub Actions workflow  
✅ Run GHAS (native), Copilot CLI, and custom tools in sequence  
✅ Parse findings and decide on actions  
✅ Create GitHub issues from security findings  
✅ Block PRs based on severity  

---

## 📋 Scenario

**We've built three independent tools:**
- Exercise 1: GitHub GHAS (native automated scanning)
- Exercise 2: Copilot CLI (interactive conversational analysis)
- Exercise 3: Custom detectors (domain-specific patterns)

**Now: Chain them together**

```
Push Code
    ↓
Run GHAS (auto - detects SQLi, XSS, weak crypto)
    ↓
Run Custom Detector (detects insecure ==, debug flags)
    ↓
Invoke Copilot CLI (analyzes + prioritizes findings)
    ↓
Create GitHub Issues (for each finding)
    ↓
Block PR if CRITICAL severity
    ↓
Generate Security Summary
```

---

## 🏗️ Step 1: Create GitHub Actions Workflow

Create: `.github/workflows/security-pipeline.yml`

```yaml
name: Security Pipeline
on:
  pull_request:
    branches: [ main ]
  push:
    branches: [ main ]

jobs:
  security-scan:
    runs-on: ubuntu-latest
    
    steps:
      # Step 1: Checkout code
      - name: Checkout
        uses: actions/checkout@v4
        
      # Step 2: Enable GitHub GHAS (automatic)
      # Already enabled in Settings → Code Security
      # This workflow will detect CodeQL, Dependabot, Secret Scanning results
      
      - name: Wait for GitHub GHAS Results
        run: |
          echo "GitHub GHAS is running in background..."
          echo "CodeQL scanning for: SQL injection, XSS, weak crypto"
          echo "Secret Scanning checking for: hardcoded credentials"
          echo "Dependabot checking for: vulnerable packages"
      
      # Step 3: Set up Python for custom scanning
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      # Step 4: Run custom detector
      - name: Run Custom Detector
        id: custom-scan
        run: |
          python .github/agents/access-control-detector.py . > custom-findings.json 2>&1 || true
          cat custom-findings.json
        continue-on-error: true
      
      # Step 5: Parse findings
      - name: Parse Security Findings
        id: parse-findings
        run: |
          python3 << 'EOF'
          import json
          import sys
          
          # Load custom findings
          try:
              with open('custom-findings.json', 'r') as f:
                  custom = json.load(f)
          except:
              custom = {'findings': []}
          
          # Count by severity
          critical = len([f for f in custom.get('findings', []) if f.get('severity') == 'CRITICAL'])
          
          print(f"CRITICAL findings: {critical}")
          print(f"Total findings: {len(custom.get('findings', []))}")
          
          # Output for next steps
          with open('findings-summary.json', 'w') as f:
              json.dump({
                  'critical_count': critical,
                  'total_count': len(custom.get('findings', [])),
                  'findings': custom.get('findings', [])
              }, f)
          
          sys.exit(1 if critical > 0 else 0)
          EOF
        continue-on-error: true
      
      # Step 6: Invoke Copilot CLI for analysis (optional in CI)
      - name: Copilot CLI Analysis
        if: always()
        run: |
          echo "In production, invoke Copilot CLI with findings..."
          echo "For now, showing simulated analysis output:"
          
          # Simulated Copilot response
          cat << 'ANALYSIS'
          ## Security Analysis Results
          
          **CRITICAL**: 2 findings in access control
          - Timing attack in password comparison (app.py:67)
          - Type confusion in admin check (app.py:142)
          
          **Recommendation**: Fix before merge
          **Time estimate**: 2-4 hours
          **Priority**: Block PR until fixed
          ANALYSIS
        continue-on-error: true
      
      # Step 7: Create Issues from Findings
      - name: Create GitHub Issues
        if: always()
        run: |
          python3 << 'EOF'
          import json
          import subprocess
          import os
          
          # Read findings
          try:
              with open('findings-summary.json', 'r') as f:
                  summary = json.load(f)
          except:
              exit(0)
          
          # Create issue for each CRITICAL finding
          for finding in summary.get('findings', []):
              if finding.get('severity') == 'CRITICAL':
                  title = f"🔴 CRITICAL: {finding['risk']}"
                  body = f"""## Security Finding

**Type**: {finding.get('riskType')}
**Severity**: CRITICAL
**Location**: {finding['file']}:{finding['line']}
**Code**: \`\`\`
{finding['code']}
\`\`\`

**Issue**: {finding['risk']}

**Fix**: Use secure comparison methods (hmac.compare_digest for passwords, proper type checking for IDs)

**Assignee**: Security team
**Label**: security, critical
"""
                  
                  # Create issue (simulated)
                  print(f"[ISSUE] {title}")
                  print(f"[BODY] {body[:100]}...")
          
          EOF
        continue-on-error: true
      
      # Step 8: Block PR if CRITICAL
      - name: PR Gate - Security Check
        id: security-gate
        run: |
          python3 << 'EOF'
          import json
          
          try:
              with open('findings-summary.json', 'r') as f:
                  summary = json.load(f)
          except:
              exit(0)
          
          critical_count = summary.get('critical_count', 0)
          
          if critical_count > 0:
              print(f"❌ BLOCKED: {critical_count} CRITICAL security finding(s)")
              print("Fix findings and push again to retry security checks")
              exit(1)
          else:
              print("✅ PASSED: No CRITICAL findings")
              exit(0)
          EOF
      
      # Step 9: Generate Summary Report
      - name: Security Summary
        if: always()
        run: |
          python3 << 'EOF'
          import json
          
          summary = {
              "github_ghas": {
                  "status": "running",
                  "components": ["CodeQL", "Secret Scanning", "Dependabot"]
              },
              "custom_detectors": {
                  "access_control": "completed"
              },
              "overall_status": "checking..."
          }
          
          print("=" * 50)
          print("SECURITY SCAN SUMMARY")
          print("=" * 50)
          print(json.dumps(summary, indent=2))
          EOF
```

---

## 🚀 Step 2: Understand the Workflow Stages

The workflow has 3 key decision points:

### Stage 1: Detection Phase
- GitHub GHAS runs automatically (background)
- Custom detectors run and parse output
- Findings stored as JSON

### Stage 2: Analysis Phase  
- Copilot CLI invoked with findings (optional in CI)
- Severity determined
- Issues created for CRITICAL findings

### Stage 3: Gate Phase
- If any CRITICAL: Block PR ❌
- If only WARNING/INFO: Allow PR ✅
- Report generated

---

## 📊 Step 3: Data Flow Between Tools

Visual representation of how findings flow:

```
┌─────────────────────┐
│  GitHub.com         │
│  (GHAS Background)  │
│  - CodeQL           │
│  - Secrets Scan     │
│  - Dependabot       │
└──────────┬──────────┘
           │
           ├─→ findings.json (GitHub API)
           │
┌──────────▼──────────┐
│  Custom Detectors   │
│  (.py scripts)      │
│  - access-control   │
│  - compliance       │
└──────────┬──────────┘
           │
           ├─→ custom-findings.json
           │
┌──────────▼──────────┐
│  Copilot CLI        │
│  (Conversational)   │
│  - Prioritize       │
│  - Recommend        │
└──────────┬──────────┘
           │
           ├─→ analysis.json
           │
┌──────────▼──────────┐
│  GitHub Actions     │
│  - Create Issues    │
│  - Block PR         │
│  - Report           │
└─────────────────────┘
```

Each tool:
- **Takes** findings as input
- **Adds** context/analysis
- **Produces** JSON output
- **Passes** to next tool

---

## ✅ Step 4: Add PR Comment with Results

Enhance workflow to comment on PR:

```yaml
      - name: Comment PR with Security Review
        if: always()
        uses: actions/github-script@v6
        with:
          script: |
            const fs = require('fs');
            const summary = JSON.parse(fs.readFileSync('findings-summary.json', 'utf8'));
            
            let comment = '## 🔒 Security Scan Results\n\n';
            
            if (summary.critical_count > 0) {
              comment += `⚠️ **${summary.critical_count} CRITICAL finding(s)** detected\n`;
              comment += '- [ ] Review security issues\n';
              comment += '- [ ] Fix vulnerabilities\n';
              comment += '- [ ] Push fix commit\n\n';
            } else {
              comment += '✅ **No CRITICAL findings** - Ready to merge\n\n';
            }
            
            comment += `**Total findings**: ${summary.total_count}\n`;
            
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: comment
            });
```

---

## 🎯 Step 5: Test the Workflow

Trigger the workflow:

```bash
# Option A: Push to main (if workflow is active)
git push origin main

# Option B: Create a test PR
git checkout -b test/security-check
echo "# Test" >> README.md
git add README.md
git commit -m "Test security workflow"
git push origin test/security-check
# Then open PR on GitHub
```

**Check workflow results:**
1. Go to repo → Actions
2. Click latest run
3. Review "security-scan" job
4. See all 9 steps execute
5. View PR comment with results

---

## 💡 Step 6: Extend for Your Needs

### A. Add Slack Notifications
```yaml
- name: Notify Slack
  if: always()
  run: |
    curl -X POST ${{ secrets.SLACK_WEBHOOK }} \
      -H 'Content-type: application/json' \
      -d '{
        "text": "Security scan completed",
        "blocks": [{"type": "section", "text": {"type": "mrkdwn", "text": "*CRITICAL*: 2 findings"}}]
      }'
```

### B. Deploy Only if Safe
```yaml
  deploy:
    needs: security-scan
    if: needs.security-scan.outputs.passed == 'true'
    runs-on: ubuntu-latest
    steps:
      - run: echo "Deploying to production..."
```

### C. Generate Compliance Report
```yaml
- name: Compliance Report
  run: |
    python3 << 'EOF'
    # Export to compliance database
    # Update security dashboard
    # Archive findings for audit
    EOF
```

---

## ✅ Acceptance Criteria

- [ ] Created `.github/workflows/security-pipeline.yml`
- [ ] Workflow has all 9 steps
- [ ] Can trigger manually or on PR
- [ ] Runs GHAS detection
- [ ] Runs custom detector
- [ ] Parses findings
- [ ] Creates issues for CRITICAL
- [ ] Blocks PR if needed
- [ ] Comments on PR with results
- [ ] Understand data flow between tools

---

## 🔗 Key Insight: Orchestration ≠ Agent Framework

What you've built:
- ✅ Automated workflow
- ✅ Tool chaining
- ✅ Decision logic
- ✅ Conditional execution

What it ISN'T:
- ❌ No autonomous agents
- ❌ No learning
- ❌ No self-modifying behavior
- ❌ No external agents running

**It's PURPOSE-BUILT ORCHESTRATION.**

This is how enterprise security actually works:
- GitHub GHAS = Detection layer
- Custom tools = Domain layer
- Copilot CLI = Analysis layer
- GitHub Actions = Integration layer

---

## 🚀 Next Steps

**Exercise 5**: Real-World Ecosystem
- Deploy to real repository
- See it catch actual vulnerabilities
- Understand when to use each component

---

## 📚 Reference

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [YAML Syntax](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions)
- [GitHub Script Action](https://github.com/actions/github-script)
- [Workflow Examples](https://github.com/actions/starter-workflows)

---

**⏱️ Time**: 20 min | **Exercises**: 4/5 ✓

**Progress**: You now understand the complete security ecosystem:
- ✅ GitHub GHAS (what's built-in)
- ✅ Copilot CLI (conversational analysis)
- ✅ Custom Tools (your extensions)
- ✅ GitHub Actions (orchestration)
