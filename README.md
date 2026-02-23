# 🔐 Security Workshop: GitHub Ecosystem from GHAS to Custom Detection
## A Complete, Honest Guide to Modern Security Automation

**Duration**: 2 hours  
**Level**: Intermediate  
**Audience**: Developers interested in security, security teams, platform engineers  
**Format**: Hands-on exercises with real vulnerable code

---

## 🎯 What You'll Learn

This workshop shows you the **actual, working** GitHub security ecosystem:

### How Real Security Automation Works
- ✅ What GitHub GHAS does (and doesn't do)
- ✅ How Copilot CLI adds conversational context
- ✅ When to build custom security tools
- ✅ How to orchestrate everything together
- ✅ Real-world cost-benefit analysis

### NOT Theoretical
Unlike many security workshops, this is:
- **Real code**: SecureTrails contains actual OWASP vulnerabilities
- **Real tools**: GitHub GHAS, Copilot CLI, GitHub Actions (all working)
- **Real patterns**: Professional team workflows
- **Real costs**: No aspirational frameworks—just what works in 2026

---

## 🏗️ Architecture at a Glance

```
TIER 1: GITHUB NATIVE (Built-in GitHub Services - NOT .py files)
├─ CodeQL (SQL injection, XSS detection)
├─ Secret Scanning (hardcoded credentials)
└─ Dependabot (vulnerable packages)
   → Automatic. Free. Always running. Runs on GitHub servers.

TIER 2: INTERACTIVE ANALYSIS (Your Team - Access via CLI)
├─ Copilot CLI (conversational security review)
└─ Security team uses to prioritize & recommend fixes
   → Human expertise via CLI. Requires Copilot license.

TIER 3: CUSTOM EXTENSION (Your .py Files - What YOU Build)
├─ Python security detection scripts (.github/agents/*.py)
├─ Domain-specific vulnerability patterns
└─ Runs in CI/CD pipeline
   → Your specialized rules. You write and maintain these files.

TIER 4: ORCHESTRATION (GitHub Actions Workflow)
├─ GitHub Actions (chains everything together)
├─ Calls GHAS (native)
├─ Calls your .py detection scripts
├─ Creates issues from findings
├─ Blocks PRs on critical severity
└─ Reports to security dashboard
   → Integration layer. Glues everything.
```

**IMPORTANT**: GitHub GHAS is NOT .py files. Custom detection tools ARE .py files.

---

## 📚 Workshop Structure

| Exercise | Duration | Topic | What You Do | Tools |
|----------|----------|-------|-----------|-------|
| **0** | 10 min | Prerequisites | Clone repo, setup auth, verify tools | gh, git, Python |
| **1** | 20 min | GitHub NATIVE | Enable CodeQL, Secrets, Dependabot | GitHub GHAS |
| **2** | 20 min | Conversational Analysis | Use Copilot CLI for interactive review | Copilot CLI |
| **3** | 20 min | Custom Tools | Build Python security detector | Python |
| **4** | 20 min | Integration | Create GitHub Actions workflow | GitHub Actions |
| **5** | 20 min | Real-World | Deploy complete ecosystem, see it work | All tools |
| | **2 hrs** | **TOTAL** | | |

---

## 📋 Exercise Map

- **[Exercise 0: Prerequisites](docs/0-prereqs.md)** - Setup & verification
- **[Exercise 1: GitHub NATIVE Security](docs/1-github-native-security.md)** - GHAS fundamentals
- **[Exercise 2: Copilot CLI Interactive](docs/2-copilot-cli-interactive.md)** - Conversational analysis
- **[Exercise 3: Custom Detection Tools](docs/3-custom-detection-tools.md)** - Build Python scanners
- **[Exercise 4: GitHub Actions Integration](docs/4-github-actions-integration.md)** - Orchestrate tools
- **[Exercise 5: Real-World Ecosystem](docs/5-real-world-ecosystem.md)** - Production deployment

---

## 🎭 The SecureTrails Scenario

Throughout this workshop, you're working with **SecureTrails Co.**—a fictional trail booking platform.

### Context
- 15 developers building Flask + React + Python backend
- Running on AWS, deployed via GitHub Actions
- Public GitHub repository
- Needs OWASP compliance

### The Vulnerabilities
The SecureTrails app intentionally contains 7 OWASP vulnerabilities:
- SQL Injection (database layer)
- Cross-Site Scripting (web templates)
- Broken Authentication (session handling)
- Insecure Access Control (permissions)
- Insecure Deserialization (data processing)
- Vulnerable Dependencies (requirements.txt)
- Security Misconfiguration (debug mode)

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
# 1. Clone this repo
git clone https://github.com/YOUR_USERNAME/security-workshop.git
cd security-workshop

# 2. Start Exercise 0
open docs/0-prereqs.md

# 3. Follow the exercises in order
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
