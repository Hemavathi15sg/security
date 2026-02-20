# SecureTrails Security Workshop

## 🎯 Workshop Overview

Welcome to the **SecureTrails Co. Security Audit** — a hands-on 2-hour workshop where you'll act as a security analyst team reviewing a vulnerable web application using GitHub Copilot agents, CLI, MCP, and custom security agents.

### The Scenario

SecureTrails Co. is a hiking trail booking platform preparing for launch. Your mission: **discover and report security vulnerabilities before they reach production**. You'll use cutting-edge AI agents to automate security review, dependency scanning, secret detection, and policy enforcement—demonstrating how to integrate security into the entire SDLC.

---

## 📋 Workshop Structure (120 minutes)

| Time | Exercise | Focus | Tools |
|------|----------|-------|-------|
| 0-5 min | **Intro** | Narrative setup, goals | N/A |
| 5-15 min | **[Exercise 0: Prerequisites](./0-prereqs.md)** | Environment setup | VS Code, Copilot Extension, Copilot CLI |
| 15-35 min | **[Exercise 1: Agent Security Review](./1-agent-security-review.md)** | Discover vulnerabilities | Copilot Coding Agent, CLI |
| 35-55 min | **[Exercise 2: MCP & Supply Chain](./2-mcp-supply-chain.md)** | Dependency analysis | MCP, Custom agents |
| 55-75 min | **[Exercise 3: Secret Scanner](./3-secret-scanner-agent.md)** | Secret detection, agent chaining | Custom agents, SDK |
| 75-115 min | **[Exercise 4: SDLC Policies](./4-sdlc-policy-agents.md)** | Multi-agent orchestration | Agent chaining, workflows |
| 115-120 min | **Wrap-up** | Review, next steps | N/A |

---

## 🚀 Quick Start

### Local VS Code Setup
```bash
# 1. Clone the workshop repo
git clone <workshop-repo-url>
cd security-workshop

# 2. Open in VS Code
code .

# 3. Follow Exercise 0 for environment setup
```

**Prerequisites**:
- VS Code installed on your machine
- GitHub Copilot extension installed in VS Code
- GitHub CLI (`gh`) installed locally
- Python 3.9+ installed

---

## 📚 Learning Outcomes

By the end of this workshop, you will:

✅ **Discover vulnerabilities** using AI-powered security analysis agents  
✅ **Understand agent chaining** — composing multiple agents to solve complex problems  
✅ **Integrate MCP (Model Context Protocol)** for external tool access (CVE databases, GitHub APIs)  
✅ **Deploy custom security agents** via Copilot SDK  
✅ **Orchestrate multi-agent workflows** for automated SDLC security policies  
✅ **Apply security best practices** to your own repositories  

---

## 🎯 Exercises Overview

### Exercise 0: Prerequisites (10 min)
**Objective**: Set up environment with Copilot CLI and access to SecureTrails repo.

[▶️ Start Exercise 0](./0-prereqs.md)

---

### Exercise 1: GitHub Agent Security Review (20 min)
**Objective**: Use Copilot Agent to discover 7 planted vulnerabilities (SQL injection, XSS, hardcoded secrets, etc.).

**Tools**: `gh copilot explain`, `gh copilot suggest`  
**Expected findings**: ≥5 security issues  

[▶️ Start Exercise 1](./1-agent-security-review.md)

---

### Exercise 2: MCP & Dependency Supply Chain (20 min)
**Objective**: Map vulnerable dependencies and generate SBOM using MCP integration.

**Tools**: GitHub MCP, custom `dependency-supply-chain-scout` agent  
**Expected findings**: ≥5 vulnerable packages, CVE details  

[▶️ Start Exercise 2](./2-mcp-supply-chain.md)

---

### Exercise 3: Secret Scanner & Agent Chaining (20 min)
**Objective**: Deploy custom secret-detector agent and demonstrate agent-to-agent communication.

**Tools**: Copilot SDK, agent chaining (detector → reporter → remediation)  
**Expected outcome**: Secrets detected, issues auto-created, fixes proposed  

[▶️ Start Exercise 3](./3-secret-scanner-agent.md)

---

### Exercise 4: SDLC Security Policy Agents (25 min)
**Objective**: Implement multi-agent orchestration enforcing organization security policies.

**Tools**: Agent orchestration, policy files, GitHub Actions workflows  
**Expected outcome**: Automated compliance checking, blocking violations, auto-remediation  

[▶️ Start Exercise 4](./4-sdlc-policy-agents.md)

---

## 📖 Resources

- **[Copilot CLI Cheatsheet](./resources/copilot-cheatsheet.md)** — Quick reference for all CLI commands
- **[Agents Reference](./resources/agents-reference.md)** — Details on custom agents and chaining patterns
- **[GitHub Security Best Practices](./resources/reference.md)** — External links and documentation
- **[GitHub Copilot SDK Docs](https://docs.github.com/en/copilot/building-copilot-extensions)**
- **[MCP Documentation](https://modelcontextprotocol.io/)**

---

## ⚡ Quick Commands Reference

```bash
# Setup
gh extension install github/gh-copilot
gh auth login
gh copilot auth

# Analysis
gh copilot explain app.py
gh copilot suggest "Find SQL injection vulnerabilities"

# Agent operations
gh copilot agent register --agent-path ./agents/scanner.py
gh copilot agent orchestrate --config ./agent-orchestration.yaml

# MCP
gh copilot mcp init github   # Initialize GitHub MCP server
```

---

## 📝 Prerequisites

- **VS Code** installed locally (https://code.visualstudio.com/)
- **GitHub Account** with Copilot access
- **GitHub Copilot Extension** for VS Code (installed)
- **GitHub CLI** (`gh`) installed
- **Python 3.9+** (for local development)
- **Node.js 16+** (for sample app dependencies, optional)
- **Git** installed and configured
- Basic understanding of security concepts (helpful but not required)

---

## 📸 Expected Outputs

Throughout the workshop, you'll generate:
- Security audit reports (≥7 vulnerabilities identified)
- Dependency SBOM (Software Bill of Materials)
- Automated GitHub issues with findings
- Pull requests with fixes
- Policy compliance documentation
- Agent execution logs showing reasoning

---

## ❓ Support & Troubleshooting

**Stuck at Exercise 0?** → See [0-prereqs.md Troubleshooting](./0-prereqs.md#troubleshooting)

**Commands not working?** → Check [Copilot CLI Cheatsheet](./resources/copilot-cheatsheet.md)

**Agent issues?** → Refer to [Agents Reference Guide](./resources/agents-reference.md)

---

## 🎓 After the Workshop

### Extend Your Learning
- Integrate these agents into your own GitHub repositories
- Create custom security policies specific to your organization
- Combine agents for different security contexts (PCI-DSS, HIPAA, SOC 2)

### Share & Collaborate
- Fork the agents and customize for your team
- Document your security policies in `.github/security-policy.yaml`
- Set up automated security workflows using the patterns learned

---

## 📊 Workshop Success Metrics

✅ All 5 exercises completed  
✅ Vulnerabilities documented in GitHub issues  
✅ Agent findings understood and reproduced  
✅ Custom agents extended or modified  
✅ Multi-agent orchestration demonstrated  

---

**Ready?** Start with [Exercise 0: Prerequisites](./0-prereqs.md) →

---

*Last Updated: February 2026*  
*Workshop Duration: 2 hours | Difficulty: Intermediate | Participants: 1-20*
