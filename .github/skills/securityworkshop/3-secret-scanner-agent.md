# Exercise 3: Secret Scanner & Agent Chaining

**Duration**: 20 minutes  
**Expected Time to Complete**: 20 min

---

## 🎯 Learning Objectives

By the end of this exercise, you will:

✅ Deploy a custom `secret-detector-enforcer` agent via Copilot SDK  
✅ Understand **agent chaining** — agents calling other agents  
✅ Implement credential leak prevention workflows  
✅ Experience automated issue creation and remediation  
✅ Learn SDK patterns for agent composition  

---

## 📖 Scenario Context

Critical Risk: **"Someone might accidentally commit an API key or database password!"**

You need to prevent credential leaks before they reach the repository. Your solution: Build a multi-agent workflow where:
1. Secrets are detected on git push
2. Commit is blocked  
3. Issue is auto-created
4. Remediation PR is generated

This demonstrates **agent chaining** — the power of composable AI agents working together.

---

## 🔍 Task Overview

You'll:
1. Deploy `secret-detector-enforcer` agent (SDK-based)
2. Understand agent-to-agent communication
3. Test with intentionally hardcoded secret
4. Watch agent chain execute automatically
5. Review issue and fix PR created by agents

---

## 📋 Step-by-Step Instructions

### Step 1: Deploy Secret-Detector Agent Using Copilot SDK

**Objective**: Install and register the custom secret-detector agent.

First, verify the agent file exists:

```bash
cd securetrails-vulnerable

# List available agents in .github/agents/
ls -la .github/agents/

# Expected files:
# - secret-detector.py (MAIN AGENT)
# - issue-reporter.py (HELPER AGENT - called by secret-detector)
# - remediation-proposer.py (HELPER AGENT - created fix PRs)
```

**Initialize the agent using Copilot SDK:**

```bash
# Register the secret-detector agent
gh copilot agent register \
  --agent-path .github/agents/secret-detector.py \
  --name "secret-detector-enforcer" \
  --description "Detects and prevents credential leaks in git commits" \
  --triggers "pre-commit,pre-push" \
  --chaining-enabled true
```

**Expected output:**
```
✓ Agent Registered: secret-detector-enforcer
✓ Location: .github/agents/secret-detector.py
✓ Triggers: pre-commit, pre-push
✓ Chaining: Enabled (can call other agents)
✓ Status: Active
```

---

### Step 2: Understanding Agent Chaining Architecture

**Objective**: Learn how agents communicate and pass context.

The agent chain for this exercise:

```
┌─────────────────────────────────────────────────────────────┐
│ TRIGGER: Developer runs `git push`                          │
└──────────────────────────────┬──────────────────────────────┘
                               ↓
┌──────────────────────────────────────────────────────────────┐
│ AGENT 1: secret-detector-enforcer                            │
│ ─────────────────────────────────────────────────────────────│
│ Task: Scan files for credential patterns                    │
│ Methods:                                                     │
│  - Regex matching (AWS_KEY, API_KEY, DATABASE_URL, etc.)    │
│  - Entropy analysis (high-entropy random strings)           │
│  - File extension scanning (.env, .pem, .key)               │
│ Output: {found_secrets: [{file, line, type, snippet}]}      │
└──────────────────────────────┬──────────────────────────────┘
                               ↓
                    ┌──────────────────┐
                    │ Secrets Found?   │
                    └────┬─────────┬───┘
                         │ YES     │ NO
                    ┌────▼─┐   ┌──▼────┐
                    │CHAIN │   │ALLOW  │
                    │AGENTS│   │PUSH   │
                    └────┬─┘   └───────┘
                         ↓
                    ┌──────────────────────────────────────────┐
                    │ AGENT 2: issue-reporter                  │
                    │ ───────────────────────────────────────  │
                    │ Input: Shared context from Agent 1       │
                    │ Task: Create GitHub issue with findings  │
                    │ Output: GitHub Issue #XX created         │
                    └──────────────────┬───────────────────────┘
                                       ↓
                    ┌──────────────────────────────────────────┐
                    │ AGENT 3: remediation-proposer            │
                    │ ───────────────────────────────────────  │
                    │ Input: Issue details + secret locations  │
                    │ Task: Generate fix PR                    │
                    │ Output: PR #YY with remediation          │
                    └──────────────────────────────────────────┘
```

**Key Concept — Context Passing Between Agents:**

```python
# Pseudo-code showing how agents share context:

# Agent 1 finds secrets
findings = {
    "secrets_found": [
        {
            "file": "app.py",
            "line": 12,
            "type": "JWT_SECRET",
            "pattern_matched": "JWT_SECRET = '...'",
            "severity": "CRITICAL"
        }
    ],
    "timestamp": "2026-02-20T...",
    "commit": "abc123"
}

# Agent 2 receives findings as input
issue_created = agent2.run(input=findings)

# Agent 3 receives results from Agent 2
fix_pr_created = agent3.run(input=issue_created, context=findings)
```

---

### Step 3: Set Up Pre-Commit Hook for Testing

**Objective**: Configure the agent to run before commits are made.

Create pre-commit configuration:

```bash
# Install pre-commit framework
pip install pre-commit

# Create .pre-commit-config.yaml
cat > .pre-commit-config.yaml << 'EOF'
repos:
  - repo: local
    hooks:
      - id: copilot-secret-scan
        name: Copilot Secret Scanner
        entry: python .github/agents/secret-detector.py
        language: system
        stages: [commit]
        always_run: true
        pass_filenames: false
        verbose: true
        
  - repo: local
    hooks:
      - id: copilot-issue-reporter
        name: Copilot Issue Reporter
        entry: python .github/agents/issue-reporter.py
        language: system
        stages: [commit]
        always_run: true
        pass_filenames: false
        depend: [copilot-secret-scan]
EOF

# Install the hooks
pre-commit install --stages commit,push
```

---

### Step 4: Test Agent Chain with Intentional Secret

**Objective**: Deliberately commit a secret to trigger the agent chain.

Create a test file with hardcoded secret:

```bash
# Create a file (deliberately) with exposed credential
cat > test-secret-exposure.txt << 'EOF'
# This is a test case for Exercise 3
# DO NOT use this file in production

API_KEY=sk_live_51234567890abcdefghijklmnopqrstuv
DATABASE_URL=postgres://user:$ecure_p@ssw0rd@db.example.com:5432/trails
AWS_ACCESS_KEY_ID=AKIAIOSFODNN7EXAMPLE
GITHUB_TOKEN=ghp_aB3CdEf9ghI0jKlMn1OpQrStUvWxYz2A

# Note: All above are intentionally exposed for testing
EOF
```

**Attempt to commit (this will trigger agent chain):**

```bash
git add test-secret-exposure.txt
git commit -m "Test: Add secret exposure for Exercise 3"
```

**Expected behavior — Agent chain executes:**

1. **Pre-commit hook runs secret-detector agent:**
   ```
   ✓ Scanning files for secrets...
   ✓ Found 4 credential patterns
   ✗ BLOCKING commit: Secrets detected
   
   Blocked Secrets:
   - test-secret-exposure.txt:4 | Type: API_KEY | Entropy: 94%
   - test-secret-exposure.txt:5 | Type: DATABASE_URL (password)
   - test-secret-exposure.txt:6 | Type: AWS_ACCESS_KEY_ID
   - test-secret-exposure.txt:7 | Type: GITHUB_TOKEN
   ```

2. **Agent chains to issue-reporter:**
   ```
   ✓ Creating GitHub issue...
   ✓ Issue #47 created: "🚨 Secret Exposure Detected"
   ✓ Labels applied: security, secrets, autoremediation
   ✓ Assignee: @security-team
   ```

3. **Agent chains to remediation-proposer:**
   ```
   ✓ Generating remediation workflow...
   ✓ PR #48 created: "security: Remove exposed secrets"
   ✓ Suggested fixes:
     - Remove sensitive values from code
     - Create .env template
     - Update .gitignore
   ```

**Commit is BLOCKED:**
```
✗ Commit failed due to security policy violations
  Issue created: #47 (assign to yourself to begin remediation)
  Proposed fix: PR #48 (review and merge to resolve)
→ Use `git reset HEAD test-secret-exposure.txt` to unstage
```

---

### Step 5: Review Created GitHub Issue

**Objective**: Verify the auto-generated issue contains proper context.

Check the issue created by issue-reporter agent:

```bash
# List recent security issues
gh issue list --label security --limit 5

# Read the auto-created issue
gh issue view #47
```

**Expected issue content:**

```
🚨 Secret Exposure Detected
=========================

## Severity: CRITICAL ⚠️

### Summary
Pre-commit hook detected exposed credentials before commit.
Agent Analysis Complete | Automatic remediation proposed

### Detected Secrets

| File | Line | Type | Pattern | Risk |
|------|------|------|---------|------|
| test-secret-exposure.txt | 4 | API_KEY | sk_live_... | CRITICAL |
| test-secret-exposure.txt | 5 | DATABASE_URL | postgres://...pwd | CRITICAL |
| test-secret-exposure.txt | 6 | AWS_ACCESS_KEY | AKIA... | CRITICAL |
| test-secret-exposure.txt | 7 | GITHUB_TOKEN | ghp_... | CRITICAL |

### Security Implications
- All 4 credentials must be considered COMPROMISED
- Immediate rotation required
- Review git history for previous exposure

### Remediation Status
✓ Automatic fix PR proposed: #48
✓ Review suggested solution
✓ Rotate all exposed credentials
✓ Update .gitignore patterns

### Agent Analysis
- Tool: secret-detector-enforcer
- Detection Method: Entropy + regex patterns
- Confidence: 100% (literal patterns matched)
- Execution Time: 2.3s

### Next Steps
1. Review PR #48 for proposed fixes
2. Approve and merge PR if acceptable
3. Rotate all exposed credentials immediately
4. Verify no other exposure in history: 
   \`\`\`bash
   git log -p --all -S 'sk_live_5' -- .
   \`\`\`

Generated by Exercise 3: Secret Detector Enforcer Agent
Triggered at: 2026-02-20 10:45:00 UTC
```

---

### Step 6: Review Remediation PR

**Objective**: Examine the auto-generated fix from remediation-proposer agent.

```bash
# View the remediation PR
gh pr view #48
```

**Expected PR content:**

```
security: Remove exposed secrets and enforce best practices

### What This PR Does
✓ Removes all hardcoded secrets
✓ Creates .env.example template (safe values)
✓ Updates .gitignore to exclude .env
✓ Adds pre-commit secret scanning
✓ Documents credential rotation process

### Changes
- test-secret-exposure.txt → DELETED (contained exposed secrets)
- .env.example → CREATED (template with sanitized values)
- .gitignore → UPDATED (added .env, .pem, *.key)
- .pre-commit-config.yaml → UPDATED (secret scanning)

### Diff Summary
```
 diff --git a/test-secret-exposure.txt b/test-secret-exposure.txt
 deleted file mode 100644
 index 1234567..0000000
 +++ /dev/null
 @@ -1,8 +0,0 @@
 -API_KEY=sk_live_51234567890abcdefghijklmnopqrstuv
 -DATABASE_URL=postgres://user:$ecure_p@ssw0rd@...
 -...

 diff --git a/.env.example b/.env.example
 new file mode 100644
 index 0000000..abc1234
 --- /dev/null
 +++ b/.env.example
 @@ -0,0 +1,10 @@
 +# SecureTrails Environment Variables
 +# Copy to .env and fill in actual values
 +
 +API_KEY=your_api_key_here
 +DATABASE_URL=postgres://user:password@localhost:5432/trails
 +AWS_ACCESS_KEY_ID=your_aws_key_here
 +GITHUB_TOKEN=your_github_token_here
 +JWT_SECRET=your_jwt_secret_here
```

### Checklist
- [x] Secrets removed from all files
- [x] .env.example created with safe template
- [x] .gitignore updated to exclude sensitive files
- [x] No new secrets introduced
- [x] Pre-commit hooks configured
- [x] All imports still work (tested locally)

### Credential Rotation Required
After merging, IMMEDIATELY rotate:
1. API_KEY (revoke old key in provider dashboard)
2. DATABASE_URL credentials (reset DB password)
3. AWS_ACCESS_KEY_ID (deactivate, create new key pair)
4. GITHUB_TOKEN (delete token, create new one)

**Rationale**: These credentials were in git history and may be visible in backups/forks.

### Agent Note
Generated by Exercise 3 — Automated secret remediation
This PR was created automatically after secrets were detected.
```

---

### Step 7: Implement the Fix

**Objective**: Merge the remediation PR to enforce best practices.

```bash
# Approve and merge the PR
gh pr review #48 --approve

# Merge the PR
gh pr merge #48 --merge

# Verify changes applied
git pull origin main

# Confirm files updated
ls -la .env.example
cat .gitignore | grep -E "\.env|\.key|\.pem"
```

---

### Step 8: Verify Agent Chaining Worked

**Objective**: Document the complete agent chain execution.

Create a summary issue:

```bash
gh issue create \
  --title "[SECURITY AUDIT] Exercise 3: Agent Chaining Demonstration" \
  --label "security,review-exercise" \
  --body "## Exercise 3: Secret Scanner & Agent Chaining Complete

### Mission: Prevent Credential Leaks
Status: ✓ COMPLETE

### Agent Chain Execution Summary

#### Phase 1: Detection (Agent 1)
- Agent: secret-detector-enforcer
- Trigger: git commit attempt
- Action: Scanned files for credential patterns
- Result: ✓ Found 4 exposed secrets
  - API_KEY (sk_live_...)
  - DATABASE_URL (postgres://user:password@...)
  - AWS_ACCESS_KEY_ID
  - GITHUB_TOKEN
- Status: **Commit BLOCKED** (prevented exposure)

#### Phase 2: Issue Creation (Agent 2)
- Agent: issue-reporter
- Input: Findings from Agent 1
- Action: Created GitHub issue with full context
- Result: ✓ Issue #47 created
- Context Passed: File paths, line numbers, patterns, severity
- Status: **Issue auto-created and labeled**

#### Phase 3: Remediation (Agent 3)
- Agent: remediation-proposer
- Input: Issue context from Agent 2
- Action: Generated comprehensive fix
- Result: ✓ PR #48 created
  - Removed exposed secrets
  - Created .env.example template
  - Updated .gitignore
  - Added pre-commit blocking
- Status: **Fix PR auto-created and ready**

### Agent Chaining Benefits Demonstrated

✓ **Composition**: Agents work together toward solution
✓ **Context Passing**: Each agent receives relevant findings
✓ **Automation**: Complete workflow requires no manual intervention
✓ **Scalability**: Same pattern can be extended with more agents
✓ **Efficiency**: From detection to fix in <10 seconds

### Security Improvements Implemented

✓ Pre-commit secrets scanning (prevents future exposure)
✓ GitHub issue tracking (audit trail)
✓ Automated remediation (consistent fixes)
✓ .gitignore enforcement (protection)
✓ .env template pattern (best practice)

### Key Learnings

1. **Agent Chaining Pattern**: Agent A → Agent B → Agent C workflow
2. **Context Sharing**: How agents pass findings between each other
3. **Trigger Integration**: Pre-commit hooks activate agent pipeline
4. **SDK Usage**: Copilot SDK enables custom agent deployment
5. **Automation**: Multi-step security workflow fully automated

### Credentials Exposed (Action Required)

⚠️ **Note**: If any of these were real, they must be rotated immediately:
- API_KEY: Revoke in provider dashboard
- DATABASE: Reset password
- AWS Keys: Deactivate, create new pair
- GitHub Token: Delete, create new token

Since these are test credentials from exercise, no real rotation needed.

### Files Modified by Agents

- test-secret-exposure.txt: ✗ DELETED
- .env.example: ✓ CREATED
- .gitignore: ✓ UPDATED  
- .pre-commit-config.yaml: ✓ ENHANCED

### Next Exercise

In Exercise 4, you'll scale this to organization-level security policies with multi-agent orchestration enforcing SDLC-wide compliance.

---
Generated by Exercise 3: Secret Scanner & Agent Chaining  
Timestamp: 2026-02-20 10:45:00 UTC
Agents Involved: 3 (detector, reporter, remediation-proposer)
Chains Executed: 1 complete chain
Success Rate: 100%
"
```

---

## ✅ Acceptance Criteria

- [ ] `secret-detector-enforcer` agent deployed via SDK
- [ ] Agent triggers on `git commit`/`pre-push`
- [ ] Created test file with hardcoded secrets
- [ ] Commit blocked when secrets detected
- [ ] Agent 1 detected all 4 secrets
- [ ] Agent 2 (issue-reporter) auto-created GitHub issue
- [ ] Agent 3 (remediation-proposer) auto-created fix PR
- [ ] Agent chaining completed end-to-end
- [ ] Issue and PR reviewed and documented

---

## 🖼️ Expected Output

```
Pre-commit Hook Execution:
===========================
✓ Running secret-detector-enforcer...
✗ BLOCKED: 4 secrets found
✓ Creating issue...
✓ Issue #47 created
✓ Creating fix PR...
✓ PR #48 created
→ Review suggested remediation
```

---

## 🆘 Troubleshooting

### Issue: Pre-commit hook not triggering
```bash
# Verify installation
pre-commit validate-config
pre-commit install

# Test manually
pre-commit run --all-files
```

### Issue: Agent not chaining to next agent
```bash
# Check agent registration
gh copilot agent list --verbose

# Verify chaining enabled
gh copilot agent register --agent-path .github/agents/secret-detector.py --chaining-enabled true
```

### Issue: Issue/PR not created
```bash
# Check agent logs
gh copilot agent run secret-detector-enforcer --verbose --log-level debug

# Verify GitHub token has correct scopes
gh auth status
```

---

## 📚 Resources

- [Copilot SDK Documentation](https://docs.github.com/en/copilot/building-copilot-extensions)
- [Agent Chaining Patterns](./resources/agents-reference.md)
- [Secret Detection Techniques](./resources/reference.md)
- [Pre-commit Framework](https://pre-commit.com/)

---

## 🎯 Key Concepts Learned

### Agent Chaining
```
Agent A finds → Agent B reports → Agent C fixes
```

### SDK Pattern
```python
agent = CopilotAgent(name="detector")
agent.chain_to("reporter")
agent.chain_to("remediation-proposer")
```

### Context Passing
Agents automatically share findings through context files/APIs

---

## 📌 Next Steps

Excellent progress! You now understand:
- ✅ Custom agent deployment
- ✅ Agent-to-agent communication
- ✅ Automated incident response
- ✅ Multi-step security workflows

### Final Challenge: Exercise 4

In **[Exercise 4: SDLC Security Policy Agents](./4-sdlc-policy-agents.md)**, you'll:
- Build **multi-agent orchestration** across entire SDLC
- Enforce **organization-wide security policies**
- Integrate with **GitHub Actions**
- Demonstrate **production-ready deployment**

**Ready?** → **[Exercise 4: SDLC Policy Agents →](./4-sdlc-policy-agents.md)**

---

**⏱️ Time Elapsed**: ~60 minutes cumulative  
**Exercises Completed**: 4/5 ✓
