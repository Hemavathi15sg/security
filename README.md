# 🔐 SecureTrails Security Workshop
## Autonomous AI-Powered Security using GitHub Copilot Agents

![Duration](https://img.shields.io/badge/Duration-2%20Hours-blue)
![Level](https://img.shields.io/badge/Level-Intermediate-orange)
![GitHub Copilot](https://img.shields.io/badge/GitHub%20Copilot-Agents%20%26%20CLI-black)

---

## 📖 The Story

Welcome to **SecureTrails Co.**, a hiking trail booking platform! Founded in 2015, our platform connects outdoor enthusiasts with the most scenic trails worldwide. However, as we prepare for our Series B launch, we've discovered significant security vulnerabilities in our codebase.

As a newly hired **Security Engineer**, your mission is to **discover and document critical vulnerabilities**, demonstrate how AI agents can automate security reviews, and show your team how to integrate continuous security scanning into the SDLC.

**The Challenge:**
- ⚠️ Manual security reviews are slow and error-prone
- ⚠️ New vulnerabilities appear daily in dependencies  
- ⚠️ Teams lack security automation expertise
- ⚠️ Launch is in 2 weeks!

**The Solution:**
- ✅ Deploy autonomous **Copilot Agents** for rapid SAST scanning
- ✅ Use **Model Context Protocol (MCP)** to query CVE databases
- ✅ Chain agents together to solve complex security problems
- ✅ Integrate security directly into **GitHub Workflows**

---

## 🎯 Workshop Objectives

By the end of this 2-hour workshop, you will:

✅ Master **GitHub Copilot agents** for automated security scanning  
✅ Deploy **custom security agents** using Copilot SDK and Python  
✅ Implement **agent chaining** — composing multiple agents to solve complex security problems  
✅ Integrate **Model Context Protocol (MCP)** for external tool access (CVE databases, Git APIs)  
✅ Orchestrate **multi-agent workflows** in GitHub Actions for enterprise security policies  
✅ Apply **security best practices** to your own repositories  

---

## 🛠️ Prerequisites

### Required Tools

- **Visual Studio Code** (latest version)
- **GitHub Copilot** subscription (individual, business, or enterprise)
- **GitHub CLI** (`gh`) v2.30+
- **Git** v2.40+
- **Python** 3.9+
- **Docker Desktop** (optional, for containerization exercises)

### Required VS Code Extensions

- **GitHub Copilot** (`GitHub.copilot`)
- **GitHub Copilot Chat** (`GitHub.copilot-chat`)
- **Python** extension (`ms-python.python`)

### Quick Setup Check

```bash
# Verify tools are installed
code --version          # → 1.85+
gh --version            # → 2.30+
python --version        # → 3.9+
git --version           # → 2.40+

# Install Copilot CLI extension
gh extension install github/gh-copilot

# Authenticate
gh auth login
```

**[▶️ Full Setup Instructions](./docs/0-prereqs.md)**

---

## 📚 Workshop Exercises

| # | Exercise | Duration | Difficulty | Focus | Topic |
|---|----------|----------|-----------|-------|-------|
| **0** | [Prerequisites & Setup](./docs/0-prereqs.md) | 10 min | ⭐ | Environment | Copilot CLI, Python venv, GitHub auth |
| **1** | [AI-Powered Security Review](./docs/1-agent-security-review.md) | 20 min | ⭐⭐ | SAST | Autonomous vulnerability scanning, OWASP detection |
| **2** | [Supply Chain Security](./docs/2-mcp-supply-chain.md) | 20 min | ⭐⭐ | Dependencies | MCP integration, CVE matching, SBOM generation |
| **3** | [Secret Detection & Agents](./docs/3-secret-scanner-agent.md) | 25 min | ⭐⭐⭐ | Agent Chaining | Multi-agent orchestration, pre-commit hooks |
| **4** | [Enterprise Security Policies](./docs/4-sdlc-policy-agents.md) | 25 min | ⭐⭐⭐⭐ | Automation | GitHub Actions, policy enforcement, enterprise workflows |

**Total Workshop Duration**: ~120 minutes

---

## 🚀 Quick Start

### 1. Clone This Repository

```bash
git clone https://github.com/Hemavathi15sg/security.git
cd security
```

### 2. Follow the Setup Guide

```bash
# Start with Exercise 0
code docs/0-prereqs.md
```

### 3. Start with Exercise 1 (or any exercise)

- **Beginners**: Start with [Exercise 0: Prerequisites](./docs/0-prereqs.md)
- **Experienced**: Jump to [Exercise 1: Security Review](./docs/1-agent-security-review.md)

---

## 📁 Repository Structure

```
security/
├── README.md                          ← You are here
├── docs/                              ← All workshop exercises
│   ├── 0-prereqs.md                   ← Environment setup
│   ├── 1-agent-security-review.md     ← SAST scanning
│   ├── 2-mcp-supply-chain.md          ← Dependency scanning
│   ├── 3-secret-scanner-agent.md      ← Agent chaining
│   ├── 4-sdlc-policy-agents.md        ← Enterprise automation
│   ├── resources/                     ← Reference materials
│   │   ├── copilot-cheatsheet.md
│   │   └── agents-reference.md
│   └── images/                        ← Exercise screenshots
├── apps/                              ← Sample vulnerable applications
│   └── securetrails-vulnerable/       ← Flask app (intentionally vulnerable)
├── scripts/                           ← Utility scripts
├── .github/
│   ├── workflows/                     ← GitHub Actions CI/CD
│   └── agents/                        ← Custom security agents
├── .gitignore                         ← Git ignore rules
└── docker-compose.yml                 ← Local environment setup
```

---

## 🎓 Learning Path

### Beginner Path (60 min)
1. ✅ [Exercise 0: Prerequisites](./docs/0-prereqs.md) (10 min)
2. ✅ [Exercise 1: Security Review](./docs/1-agent-security-review.md) (20 min)
3. ✅ [Exercise 2: Supply Chain](./docs/2-mcp-supply-chain.md) (20 min)
4. 📖 Review [Resources & References](./docs/resources/)

### Intermediate Path (100 min)
1. ✅ All Beginner path exercises
2. ✅ [Exercise 3: Secret Detection](./docs/3-secret-scanner-agent.md) (25 min)
3. 📖 Study [Agent Architecture](./docs/resources/agents-reference.md)

### Advanced Path (Full 120 min)
1. ✅ All Intermediate exercises
2. ✅ [Exercise 4: Enterprise Policies](./docs/4-sdlc-policy-agents.md) (25 min)
3. 🔧 Extend agents for your own repositories

---

## 🏗️ Workshop Scenario: SecureTrails Co.

**Application**: Flask backend + JavaScript frontend booking platform

**Vulnerabilities to Discover**:
- SQL Injection (authentication bypass)
- Hardcoded API secrets in source code
- Cross-Site Scripting (XSS) in templates
- Weak password hashing (MD5)
- Insecure Direct Object Reference (IDOR)
- CORS misconfiguration
- Outdated dependencies with known CVEs

**Your Mission**: Find all 7 vulnerabilities using **Copilot Agents** in 20 minutes.

---

## 🤖 GitHub Copilot Agents Used

| Agent | Purpose | Type |
|-------|---------|------|
| **baseline-checker** | SAST scanning for code vulnerabilities | Custom Python |
| **dependency-scout** | CVE detection and dependency analysis | Custom Python |
| **secret-detector** | Credential leak prevention | Custom Python |
| **issue-reporter** | Auto-create GitHub issues | Custom Python |
| **compliance-enforcer** | Security policy enforcement in CI/CD | Custom Python |

**View Custom Agents**: [`.github/agents/`](./.github/agents/)

---

## 📖 Resources & Documentation

### Official Documentation
- 📘 [GitHub Copilot Documentation](https://docs.github.com/en/copilot)
- 📘 [GitHub Copilot CLI Guide](https://docs.github.com/en/copilot/github-copilot-cli/about-github-copilot-cli)
- 📘 [Model Context Protocol (MCP)](https://modelcontextprotocol.io/)

### Workshop Resources
- 📋 [Copilot CLI Cheatsheet](./docs/resources/copilot-cheatsheet.md)
- 🏗️ [Agent Architecture Patterns](./docs/resources/agents-reference.md)
- 🔒 [OWASP Top 10 Reference](https://owasp.org/Top10/)

### Troubleshooting
- 🆘 **[Exercise 0: Troubleshooting Guide](./docs/0-prereqs.md#--troubleshooting)**
- 💬 **GitHub Discussions**: Open an [issue](https://github.com/Hemavathi15sg/security/issues) if you get stuck

---

## 💡 Key Concepts

### What Are GitHub Copilot Agents?

Copilot Agents are **AI-powered autonomous workers** that:
- ✅ Run scheduled or triggered analyses
- ✅ Execute complex multi-step tasks
- ✅ Integrate external tools via MCP
- ✅ Chain together to solve larger problems
- ✅ Report findings to GitHub Issues

### Why Agent Chaining?

**Single Agent**: Finds vulnerabilities  
**Chained Agents**: Find → Report → Remediate → Enforce

This workshop demonstrates the **power of composable AI**.

---

## 🔄 Next Steps After the Workshop

1. **Deploy in Your Repos**: Use these agents in your organization
2. **Customize Agents**: Modify for your tech stack and policies
3. **Integrate CI/CD**: Add to GitHub Actions workflows
4. **Train Your Team**: Host this workshop for your team

---

## 🤝 Contributing

Found an issue or have suggestions? 

- **Report**:  [Create an Issue](https://github.com/Hemavathi15sg/security/issues)
- **Improve**: [Create a PR](https://github.com/Hemavathi15sg/security/pulls)
- **Discuss**: Start a [Discussion](https://github.com/Hemavathi15sg/security/discussions)

---

## 📝 License

This workshop is open source and available under the [MIT License](LICENSE).

---

## 🎯 Ready to Get Started?

### Choose Your Path:

| 👶 Just Started | 🚀 Know the Basics | 🎯 Expert |
|---|---|---|
| [📖 Read the Overview](./docs/) | [🏃 Quick Setup](./docs/0-prereqs.md) | [🔧 Jump to Exercise 3](./docs/3-secret-scanner-agent.md) |
| [⏱️ ~60 min](./docs/0-prereqs.md) | [⏱️ ~90 min](./docs/1-agent-security-review.md) | [⏱️ ~120 min](./docs/4-sdlc-policy-agents.md) |

---

## 📞 Support

- **GitHub Issues**: [Report a problem](https://github.com/Hemavathi15sg/security/issues)
- **GitHub Discussions**: [Ask a question](https://github.com/Hemavathi15sg/security/discussions)
- **Documentation**: [View the docs](./docs/)

---

**Last Updated**: February 2026  
**Workshop Version**: 1.0  
**Copilot Feature**: GitHub Copilot Agents (GA)

---

**[▶️ START EXERCISE 0 →](./docs/0-prereqs.md)**
