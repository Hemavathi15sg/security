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

## 📖 Key Concepts

**GitHub Advanced Security (GHAS)**
- CodeQL: Static analysis for code vulnerabilities
- Secret Scanning: Detects hardcoded credentials
- Dependabot: Identifies vulnerable packages

**Copilot CLI**
- Interactive security analysis
- Multi-turn conversations about findings
- Create issues directly via GitHub MCP

**Custom Agents**
- Copilot CLI `/agents` system
- Fix documentation guides
- Reusable across team

**GitHub Actions**
- Automated security workflows
- Continuous scanning
- Remediation tracking

---

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

*Last Updated: February 2026*

---

## 🚀 Getting Started

### Prerequisites

```bash
# 1. GitHub CLI
gh auth login

# 2. Copilot CLI
copilot --version           # Should show 0.0.414 or newer
copilot /login              # Authenticate

# 3. Python 3.8+
python3 --version
```

### Quick Start

```bash
# 1. Clone the VULNERABLE APP (this is what you'll audit)
git clone https://github.com/Hemavathi15sg/securetrails-workshop.git
cd securetrails-workshop

# 2. Set up Python environment
python -m venv venv
source venv/bin/activate  # or: venv\Scripts\activate (Windows)
pip install -r requirements.txt

# 3. In ANOTHER terminal, access the WORKSHOP exercises
# (Or reference docs from the workshop repo)
```

---

## 💰 Real Implementation: ROI Calculation

**Your Company**: 15 developers

| Aspect | Manual Review | GitHub Ecosystem |
|--------|----------------|------------------|
| **Setup Cost** | $100K/yr (security engineer) | $17K/yr (tools + setup) |
| **Vulnerabilities Caught** | ~70% | ~95% |
| **Developer Time Freed** | 0 hours | 90 hours/week |
| **ROI** | Baseline | 580% savings |

---

## 📊 What Gets Done in Real-Time

As you progress through exercises, your repository ACTUALLY CHANGES:

| After Exercise | Repository State |
|---|---|
| Ex 0 | ✅ Auth setup, tools verified |
| Ex 1 | ✅ GitHub GHAS enabled, findings appear |
| Ex 2 | ✅ (Local) Used Copilot CLI for analysis |
| Ex 3 | ✅ Custom detector added to `.github/agents/` |
| Ex 4 | ✅ GitHub Actions workflow created & running |
| Ex 5 | ✅ Complete ecosystem working end-to-end |

---

## 📁 Repository Structure

```
docs/
├── 0-prereqs.md .................................... Prerequisites
├── 1-github-native-security.md ................... GHAS fundamentals
├── 2-copilot-cli-interactive.md ................. Conversational analysis
├── 3-custom-detection-tools.md .................. Python detectors
├── 4-github-actions-integration.md .............. Orchestration
└── 5-real-world-ecosystem.md ..................... Production deployment

apps/securetrails-vulnerable/
├── app.py ......................................... Flask backend
├── templates/ ..................................... HTML templates
├── static/js/ ..................................... JavaScript
└── requirements.txt ............................... Vulnerable packages

.github/
├── workflows/
│   └── security-pipeline.yml ..................... Automated workflow
└── agents/
    ├── access-control-detector.py ............... Custom detector
    └── (other security tools)
```

---

## ✅ Success Criteria

By the end of the 2-hour workshop, you should:

- [ ] Understand what GitHub GHAS is and when to use it
- [ ] Have used Copilot CLI for interactive security analysis
- [ ] Built a custom Python security detector
- [ ] Created a GitHub Actions workflow
- [ ] Seen the complete ecosystem working end-to-end
- [ ] Know which tool to use for different scenarios
- [ ] Can replicate this in your own repositories
- [ ] Understand trade-offs (automation vs. accuracy vs. cost)

---

## 🎓 Key Concepts

### GitHub GHAS (Built-in GitHub Services - NOT .py files)
**What**: Automated vulnerability detection built into GitHub  
**Included**: CodeQL, Secret Scanning, Dependabot  
**Where**: Runs on GitHub servers, not in your .github/agents/  
**Cost**: Included in GitHub Pro ($21/mo)  
**Files**: NONE - these are GitHub services, not code you write  
**When to use**: Start here—catches 95% of common vulns automatically

### Copilot CLI (Interactive Tool - Access via Terminal)
**What**: Conversational AI for security analysis  
**How to use**: `copilot` command in terminal  
**Cost**: Copilot license ($10-20/mo per user)  
**Files**: NONE - it's a service you access, not code you write  
**When to use**: For prioritization and architectural decisions

### Custom Detection Tools (Your Python Scripts - ARE .py files)
**What**: Python security scripts YOU create and maintain  
**Where**: `.github/agents/` (your repository)  
**Files**: YES - you write these as .py files  
**Cost**: Developer time  
**Examples**: `access-control-detector.py`, `secret-detector.py`  
**When to use**: When GitHub GHAS can't detect YOUR domain risks

### GitHub Actions (Integration Layer - Orchestration)
**What**: CI/CD workflow that chains everything  
**Where**: `.github/workflows/` (your repository)  
**Files**: YES - you write `.yml` files  
**Cost**: Free (2,000 min/month included)  
**When to use**: Chain GHAS + Copilot + custom tools together

---

## 📞 Support & Questions

### During Workshop
- Check exercise README for explicit steps
- Use Copilot CLI `/help` for commands
- Ask facilitator for clarification

### GitHub-specific
- [GitHub Security Docs](https://docs.github.com/code-security)
- [GitHub Actions Docs](https://docs.github.com/actions)

### Security Concepts
- [OWASP Top 10](https://owasp.org/Top10/)
- [CWE Top 25](https://cwe.mitre.org/top25/)

---

## 🎬 Choose Your Path

### Path A: Understand GitHub's Security (50 min)
1. Exercise 0: Prerequisites
2. Exercise 1: GitHub NATIVE Security
3. Exercise 5: Real-World

### Path B: Use Copilot for Security (80 min)
1. Exercise 0: Prerequisites
2. Exercise 1: GitHub NATIVE
3. Exercise 2: Copilot CLI
4. Exercise 5: Real-World

### Path C: Build Custom Tools (100 min)
1. Exercise 0: Prerequisites
2. Exercise 1: GitHub NATIVE
3. Exercise 3: Custom Tools
4. Exercise 4: GitHub Actions
5. Exercise 5: Real-World

### Path D: Complete Workshop (120 min)
All exercises in order. Recommended.

---

## 🚀 Deploy to Your Project

After the workshop:

1. Copy workflow: `.github/workflows/security-pipeline.yml`
2. Copy detectors: `.github/agents/*.py`
3. Enable GHAS: Settings → Code Security
4. Train your team: Share SECURITY.md
5. Monitor: Review issues weekly

---

**⏱️ Duration**: 2 hours | **Hands-on**: 100% | **Real code**: 100% | **Working tools**: 100%

**[▶️ Next Step: Exercise 0 - Prerequisites](docs/0-prereqs.md)**
