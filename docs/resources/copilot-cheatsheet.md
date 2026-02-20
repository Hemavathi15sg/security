# Copilot CLI Cheatsheet

Quick reference for all GitHub Copilot CLI commands used in the workshop.

---

## 🔐 Authentication

### Login to GitHub
```bash
gh auth login
# Follow prompts:
# → Web protocol (HTTPS or SSH)
# → Authorize browser
```

### Authenticate Copilot Specifically
```bash
gh copilot auth
# Enables Copilot agent access
```

### Check Authentication Status
```bash
gh auth status
# Shows current account and token scopes
```

### Logout
```bash
gh auth logout
```

---

## 📝 Basic Commands

### Get Help
```bash
gh copilot --help
gh copilot explain --help
gh copilot suggest --help
```

### Check Version
```bash
gh copilot --version
```

---

## 🔍 Code Analysis (Exercises 1-2)

### Explain Code (understand what it does)
```bash
gh copilot explain <file>

# Examples:
gh copilot explain app.py
gh copilot explain requirements.txt
gh copilot explain templates/login.html
```

**When prompted, provide a specific analyzing request:**
```
Analyze this Flask application for security vulnerabilities. 
Identify: 1) SQL injection risks, 2) Auth flaws, 3) Hardcoded 
credentials, 4) Session issues, 5) CORS misconfigurations.
```

---

### Suggest Solutions (get recommendations)
```bash
gh copilot suggest "<task description>"

# Examples:
gh copilot suggest "Find SQL injection vulnerabilities in Flask"
gh copilot suggest "Identify XSS vectors in HTML templates"
gh copilot suggest "Check for exposed API keys in .env.example"
gh copilot suggest "Analyze requirements.txt for vulnerable packages"
```

---

## 🤖 Agent Commands (Exercises 2-4)

### List Available Agents
```bash
gh copilot agent list
gh copilot agent list --verbose
```

### Register a Custom Agent
```bash
gh copilot agent register --agent-path .github/agents/scanner.py
gh copilot agent register \
  --agent-path .github/agents/secret-detector.py \
  --name "secret-detector-enforcer" \
  --description "Detects exposed credentials" \
  --triggers "pre-commit,pre-push" \
  --chaining-enabled true
```

### Run/Invoke an Agent
```bash
gh copilot agent run <agent-name> --prompt "<instructions>"

# Examples:
gh copilot agent run dependency-supply-chain-scout \
  --prompt "Analyze requirements.txt and generate SBOM with CVE info"

gh copilot agent run secret-detector-enforcer \
  --prompt "Scan all files for hardcoded secrets"

gh copilot agent run baseline-checker \
  --prompt "Find SQL injection and XSS in modified files"
```

### Agent with Input/Output Files
```bash
gh copilot agent run <agent-name> \
  --prompt "<prompt>" \
  --input-file "input.json" \
  --output "output.json" \
  --verbose
```

### Agent with Context
```bash
gh copilot agent run <agent-name> \
  --prompt "<prompt>" \
  --context-file ".github/policies/security-policy.yaml"
```

---

## 🔗 MCP Commands (Exercise 2)

### Initialize MCP Server
```bash
gh copilot mcp init <server-type>

# Examples:
gh copilot mcp init github    # GitHub MCP server
gh copilot mcp init git       # Git MCP server
```

### List Available MCP Tools
```bash
gh copilot mcp tools list
```

### Check MCP Status
```bash
gh copilot mcp status
```

### Configure MCP (create config file)
```bash
mkdir -p .copilot
cat > .copilot/mcp-config.json << 'EOF'
{
  "servers": {
    "github": {
      "url": "npx",
      "args": ["@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_TOKEN": "<token>"
      }
    }
  }
}
EOF
```

---

## 🚀 Orchestration Commands (Exercise 4)

### Run Agent Orchestration
```bash
gh copilot agent orchestrate \
  --config .github/agent-orchestration.yaml \
  --pr <pr-number>

# Example with verbose logging:
gh copilot agent orchestrate \
  --config .github/agent-orchestration.yaml \
  --pr 42 \
  --verbose \
  --log-level debug
```

### Validate Orchestration Config
```bash
gh copilot agent orchestrate --validate \
  --config .github/agent-orchestration.yaml
```

---

## 📋 Extension Management

### Install Copilot Extension
```bash
gh extension install github/gh-copilot
```

### Upgrade Copilot Extension
```bash
gh extension upgrade github/gh-copilot
```

### List Installed Extensions
```bash
gh extension list
```

### Check Extension Version
```bash
gh extension list | grep copilot
```

### Force Reinstall
```bash
gh extension install github/gh-copilot --force
```

---

## 🔧 Workflow Debugging

### Check if Copilot is responding
```bash
gh copilot suggest "Say hello"
```

### Test agent registration
```bash
gh copilot agent list
```

### Debug agent execution
```bash
gh copilot agent run <agent-name> \
  --prompt "<prompt>" \
  --verbose \
  --log-level debug
```

### Check agent logs
```bash
gh copilot agent logs <agent-name>
```

---

## 📚 Common Workflows

### Exercise 1: Quick Security Review
```bash
# Step 1
gh copilot explain app.py

# Step 2 (when prompted)
# Paste: "Analyze for SQL injection, XSS, auth flaws, hardcoded secrets"

# Step 3
gh copilot suggest "Review templates/trails.html for XSS vulnerabilities"

# Step 4
gh copilot suggest "Check requirements.txt for known CVEs"
```

### Exercise 2: Supply Chain Analysis
```bash
# Step 1: Initialize MCP
gh copilot mcp init github

# Step 2: Query advisories
gh copilot suggest "Use GitHub MCP to find CVEs in requirements.txt"

# Step 3: Run agent
gh copilot agent run dependency-supply-chain-scout \
  --prompt "Generate SBOM with CVE details for all dependencies"

# Step 4: Auto-fix
gh copilot agent run remediation-proposer \
  --prompt "Create PR to update all vulnerable packages"
```

### Exercise 3: Secret Detection
```bash
# Step 1: Register agent
gh copilot agent register --agent-path .github/agents/secret-detector.py

# Step 2: Test with deliberate secret
# (Add secret to file)

# Step 3: Commit (triggers pre-commit hook)
git commit -m "test"

# Expected: Commit blocked, issue created, PR generated
```

### Exercise 4: Multi-Agent Orchestration
```bash
# Step 1: Validate config
gh copilot agent orchestrate --validate \
  --config .github/agent-orchestration.yaml

# Step 2: Run orchestration
gh copilot agent orchestrate \
  --config .github/agent-orchestration.yaml \
  --pr <pr-number>

# Expected: 3 agents run sequentially, PR commented
```

---

## 🎯 Tips & Tricks

### Longer Prompts
For complex prompts, use `@prompt` syntax or separate file:
```bash
gh copilot agent run security-analyzer \
  --prompt-file analysis-request.txt
```

### Save Output for Later Review
```bash
gh copilot agent run detector \
  --prompt "scan files" \
  --output findings.json > execution.log 2>&1
```

### Test Agent Before Production
```bash
# Use --dry-run flag (if supported)
gh copilot agent run checker \
  --prompt "analyze code" \
  --dry-run
```

### Chain Agents Manually
```bash
# Run Agent 1, save output
gh copilot agent run agent1 \
  --prompt "analyze" \
  --output /tmp/out1.json

# Pass to Agent 2
gh copilot agent run agent2 \
  --prompt "review findings" \
  --input-file /tmp/out1.json \
  --output /tmp/out2.json
```

---

## ❌ Common Issues & Solutions

### Issue: "gh: extension not found: copilot"
```bash
# Solution
gh extension install github/gh-copilot
gh copilot --version
```

### Issue: "authorization required"
```bash
# Solution
gh auth logout
gh auth login
gh copilot auth
```

### Issue: "Agent not found"
```bash
# Solution
gh copilot agent list  # Verify agent registered
gh copilot agent register --agent-path <path>  # Re-register
```

### Issue: "No response from agent"
```bash
# Solution
gh copilot agent run <name> --verbose --log-level debug
```

### Issue: "Pre-commit hook not running"
```bash
# Solution
pre-commit install
pre-commit run --all-files
```

---

## 📖 Related Documentation

- **Copilot CLI Official**: https://docs.github.com/en/copilot/github-copilot-cli
- **Copilot SDK Docs**: https://docs.github.com/en/copilot/building-copilot-extensions
- **MCP Protocol**: https://modelcontextprotocol.io/
- **GitHub Copilot Home**: https://github.com/features/copilot

---

## 🎓 Workshop Reference

**Used in Exercise 0**: Authentication commands  
**Used in Exercise 1**: `explain`, `suggest`  
**Used in Exercise 2**: MCP commands, agent run  
**Used in Exercise 3**: Agent registration, chaining  
**Used in Exercise 4**: Orchestration commands  

---

*Last Updated: February 2026*
