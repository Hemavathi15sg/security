# 🔐 SecureTrails - GitHub Security Workshop

![Duration: 2 Hours](https://img.shields.io/badge/Duration-2%20Hours-blue)
![Level: Intermediate](https://img.shields.io/badge/Level-Intermediate-orange)
![GitHub](https://img.shields.io/badge/GitHub-Security-green)

---

## 📖 The Story

Welcome to **SecureTrails**, a popular travel booking and trail management platform! Founded in 2018, our platform connects millions of adventure enthusiasts with curated hiking, trekking, and adventure trails worldwide.

However, our security posture has been neglected. GitHub's Advanced Security scans have recently flagged critical vulnerabilities in our codebase:

- 🔴 **SQL Injection** in our database query layer
- 🔴 **Broken Authentication** in user permission validation
- 🔴 **Hardcoded Secrets** in environment files
- 🔴 **Vulnerable Dependencies** in our Python packages

As a newly hired Security Engineer at SecureTrails, your mission is to **audit, analyze, and remediate these vulnerabilities** using GitHub's complete security ecosystem. We need to secure our platform before the peak season when millions of users rely on us.

---

## 🎯 Workshop Objectives

By the end of this 2-hour workshop, you will:

✅ Understand GitHub's native security features (GHAS, CodeQL, Secret Scanning, Dependabot)  
✅ Use Copilot CLI for interactive vulnerability analysis  
✅ Create custom security agents to guide fix remediation  
✅ Automate security workflows with GitHub Actions  
✅ Deploy a complete, repeatable security strategy  

---

## 🛠️ Prerequisites

### Required Tools

- **Visual Studio Code** (latest version)
- **GitHub Copilot CLI** (`npx @github/copilot`)
- **GitHub CLI** (`gh` v2.0+)
- **Git** (v2.40+)

### Authentication

- **GitHub Account** (with Copilot access)
- **GitHub Authentication** (`gh auth login`)

### Access

- Clone of **SecureTrails** vulnerable app: `https://github.com/Hemavathi15sg/securetrails-workshop`

---

## 📚 Workshop Exercises

| # | Exercise | Duration | Level | Focus | What You'll Do |
|---|----------|----------|-------|-------|---|
| 0 | [Prerequisites & Setup](./docs/0-prereqs.md) | 10 min | ⭐ | Setup | Install tools, authenticate with GitHub |
| 1 | [GitHub NATIVE Security (GHAS)](./docs/1-github-native-security.md) | 20 min | ⭐⭐ | Detection | Enable GHAS, review CodeQL findings, secrets, Dependabot alerts |
| 2 | [Copilot CLI - Interactive Analysis](./docs/2-copilot-cli-interactive.md) | 20 min | ⭐⭐⭐ | Analysis | Use Copilot CLI to analyze vulnerabilities, create GitHub issues |
| 3 | [Create Custom Agents](./docs/3-custom-agents-creation.md) | 20 min | ⭐⭐⭐⭐ | Documentation | Build fix guides using Copilot CLI `/agents` system |
| 4 | [GitHub Actions Integration](./docs/4-github-actions-orchestration.md) | 20 min | ⭐⭐⭐⭐ | Automation | Orchestrate GHAS → Issues → Agents → Workflows |
| 5 | [Real-World Ecosystem](./docs/5-real-world-ecosystem.md) | 20 min | ⭐⭐⭐⭐⭐ | Deployment | Deploy complete security strategy end-to-end |

---

## 📚 Related Resources

- [GitHub Advanced Security Docs](https://docs.github.com/en/enterprise-cloud@latest/code-security)
- [Copilot CLI Documentation](https://docs.github.com/en/copilot/github-copilot-cli/about-github-copilot-cli)
- [GitHub CodeQL](https://codeql.github.com/)
- [Dependabot Alerts](https://docs.github.com/en/code-security/dependabot)
- [Secret Scanning](https://docs.github.com/en/code-security/secret-scanning)

---

**Ready to secure SecureTrails?** 

## [→ Start with Exercise 0: Prerequisites & Setup](./docs/0-prereqs.md)

---

