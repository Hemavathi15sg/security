# Exercise 0: Prerequisites & Environment Setup (Local VS Code)

**Duration**: 10 minutes  
**Expected Time to Complete**: 10 min

---

## 🎯 Learning Objectives

By the end of this exercise, you will:

✅ Set up VS Code with GitHub Copilot extension  
✅ Install and authenticate GitHub Copilot CLI locally  
✅ Clone the SecureTrails vulnerable application  
✅ Configure local Python environment  
✅ Verify that Copilot agents can access your repository  

---

## 📖 Scenario Context

You've been brought on as a security analyst at SecureTrails Co. Your first task: **prepare your local development environment for a comprehensive security audit**. You need VS Code with Copilot, Copilot CLI, access to the vulnerable app repository, and confirmation that all tools are ready for automated security analysis.

---

## 🔧 Step-by-Step Setup

### Step 1: Verify & Install Prerequisites

Before starting, ensure you have these installed:

```bash
# Check VS Code
code --version
# Expected: Should output version (e.g., 1.85.0)

# Check Python
python --version
# or
python3 --version
# Expected: Python 3.9+

# Check Git
git --version
# Expected: git version 2.x or higher

# Check GitHub CLI
gh --version
# Expected: gh version 2.x.x
```

**If any are missing**:
```bash
# Install VS Code: https://code.visualstudio.com/

# Install Python: https://www.python.org/ (or via Homebrew/Chocolatey)

# Install Git: https://git-scm.com/

# Install GitHub CLI: https://cli.github.com/
```

---

### Step 2: Install GitHub Copilot Extension in VS Code

Open VS Code and install the official Copilot extension:

1. **Open VS Code Extensions:**
   - Press `Ctrl+Shift+X` (Windows) or `Cmd+Shift+X` (Mac)
   - Or: Click **Extensions** icon on left sidebar

2. **Search for "GitHub Copilot":**
   - Type "GitHub Copilot" in search box
   - Look for extension by **GitHub** (official)

3. **Install the Extension:**
   - Click **Install** on the official GitHub Copilot extension
   - Wait for installation to complete

4. **Verify Installation:**
   - You should see a "GitHub Copilot" icon in the bottom-right status bar
   - Or check Extensions → Installed for "GitHub Copilot"

**Expected Screen:**
```
Extensions Marketplace
┌─────────────────────────────┐
│ GitHub Copilot              │
│ by GitHub                   │
│ ★★★★★ (450K ratings)        │
│ [Install] │ [Version: x.x.x] │
│                              │
│ AI-powered code completion  │
│ Your AI pair programmer     │
└─────────────────────────────┘
```

---

### Step 3: Install GitHub Copilot CLI Locally

Open a terminal on your machine and run:

```bash
# Install Copilot CLI extension (if not already installed)
gh extension install github/gh-copilot

# Or upgrade if already installed
gh extension upgrade github/gh-copilot

# Verify installation
gh copilot --version
```

**Expected Output:**
```
gh-copilot/1.x.x (or newer)
```

**Troubleshooting:**
```bash
# If gh command not found, ensure GitHub CLI is installed
# Then try:
/usr/local/bin/gh extension install github/gh-copilot

# On Windows, use PowerShell or Command Prompt:
gh extension install github/gh-copilot
```

---

### Step 4: Authenticate with GitHub

Authenticate both GitHub CLI and Copilot:

```bash
# Authenticate GitHub CLI (if not already done)
gh auth login
```

**Follow prompts:**
- What is your preferred protocol for Git operations? → **HTTPS**
- Authenticate Git with your GitHub credentials? → **Y**
- How would you like to authenticate GitHub CLI? → **Login with a web browser**
- (Browser opens - click Authorize)

**Verify authentication:**
```bash
# Check GitHub CLI status
gh auth status

# Check Copilot CLI access
gh copilot --version
```

**Expected Output:**
```
Logged in to github.com with account <your-username>
  - Active account: true
  - Git operations: HTTPS
  - Token: gho_***...
  - Scopes: repo, workflow, gist, read:org
```

---

### Step 5: Clone SecureTrails Repository

Open terminal in your machine and clone:

```bash
# Clone the SecureTrails vulnerable app
git clone https://github.com/<your-org>/securetrails-vulnerable.git
cd securetrails-vulnerable

# Verify directory structure
ls -la
```

**Expected Directory Structure:**
```
securetrails-vulnerable/
├── app.py                    # Flask backend (vulnerable)
├── requirements.txt          # Python dependencies
├── templates/
│   ├── login.html           # Contains XSS vulnerability
│   ├── trails.html          # Contains IDOR vulnerability
│   └── admin.html           # Contains broken auth
├── static/js/
│   └── app.js               # Client-side injection points
├── .env.example             # Contains exposed secrets
├── Dockerfile               # Security misconfiguration
├── database.db              # SQLite with test data
└── .github/
    ├── copilot-instructions.md
    └── workflows/
        └── security-checks.yml
```

---

### Step 6: Open Project in VS Code

From the terminal:

```bash
# Open the project in VS Code
code .
```

Or from VS Code:
- Click **File** → **Open Folder**
- Navigate to `securetrails-vulnerable` folder
- Click **Open**

**VS Code should open with the project loaded**. Verify you can see:
- File explorer on left showing the directory structure
- GitHub Copilot icon in status bar (bottom-right)

---

### Step 7: Set Up Python Virtual Environment

In VS Code terminal (`` Ctrl+` ``):

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Mac/Linux:
source venv/bin/activate

# On Windows (PowerShell):
venv\Scripts\Activate.ps1

# On Windows (Command Prompt):
venv\Scripts\activate.bat

# Verify activation (should show (venv) in prompt)
```

**Install dependencies:**
```bash
# Install Python packages
pip install -r requirements.txt

# Verify Flask installation
pip list | grep Flask
```

**Expected Output:**
```
Flask                1.1.0
requests             2.24.0
SQLAlchemy           1.3.0
```

*(Note: These are intentionally outdated versions with known vulnerabilities)*

---

### Step 8: Configure VS Code for Copilot

1. **Open VS Code Settings:**
   - Press `Ctrl+,` (Windows) or `Cmd+,` (Mac)
   - Or: Click **File** → **Preferences** → **Settings**

2. **Search for Copilot settings:**
   - In the search box, type "Copilot"
   - Enable these settings:
     - ✓ **Copilot: Enable** (should be checked)
     - ✓ **Copilot: Inline Suggest: Enable** (auto-complete)

3. **Create VS Code terminal in project:**
   - Press `` Ctrl+` `` to open integrated terminal
   - Verify prompt shows project directory

**Expected Screen:**
```
VS Code
┌─────────────────────────────────┐
│ ✓ GitHub Copilot Extension      │
│ ✓ Terminal open (Python venv)   │
│ ✓ File explorer showing repo    │
│ $ (venv) project-name>          │
└─────────────────────────────────┘
```

---

### Step 9: Test Copilot CLI Access

In VS Code terminal, verify Copilot CLI works:

```bash
# Test Copilot CLI version
gh copilot --version

# Test Copilot with a simple explanation
gh copilot explain app.py
```

**When prompted, provide a test analysis request:**
```
Analyze this Flask application for security vulnerabilities. 
Identify: SQL injection risks, auth flaws, hardcoded credentials.
```

**Expected:**
- Copilot responds with code analysis
- No authorization errors
- Can explain code structure and find issues

---

### Step 10: Verify Python Path in VS Code

VS Code should use the virtual environment Python:

1. **Open Command Palette:** `Ctrl+Shift+P` (Windows) or `Cmd+Shift+P` (Mac)
2. **Search and select:** "Python: Select Interpreter"
3. **Choose:** `./venv/bin/python` (the virtual environment)

**Verify in terminal:**
```bash
# Check which Python is active
which python
# or on Windows:
where python

# Should show path to virtual environment
```

---

## ✅ Acceptance Criteria

Verify your setup by checking these items:

- [ ] VS Code installed and running
- [ ] GitHub Copilot extension installed in VS Code
- [ ] `gh copilot --version` returns a version number (terminal)
- [ ] `gh auth status` shows authenticated account (terminal)
- [ ] SecureTrails repository cloned locally
- [ ] Project opened in VS Code
- [ ] Python venv created and activated
- [ ] Dependencies installed (`pip list` shows Flask, requests, etc.)
- [ ] Python interpreter set to venv in VS Code
- [ ] `gh copilot explain app.py` works (returns analysis)

**All checkboxes complete?** → You're ready for Exercise 1! ✅

---

## 🆘 Troubleshooting

### Issue: GitHub Copilot extension not working in VS Code
```bash
# Make sure it's installed
# Go to VS Code Extensions → Search "GitHub Copilot"
# Install the official one by GitHub

# Restart VS Code
Code → File → Reload Window (or Ctrl+R)
```

### Issue: `gh: extension not found: copilot`
```bash
# Update GitHub CLI first
gh upgrade

# Then install Copilot extension
gh extension install github/gh-copilot

# If still failing:
gh extension list  # Show installed extensions
```

### Issue: `Permission denied` on repository clone
```bash
# Ensure SSH key is configured
gh auth ssh-key add ~/.ssh/id_ed25519

# Or use HTTPS with token
git clone https://github.com/<org>/securetrails-vulnerable.git
# Enter GitHub username and Personal Access Token as password
```

### Issue: Python venv not activating in VS Code
```bash
# On Windows PowerShell (if execution policy blocks it):
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Then try again:
venv\Scripts\Activate.ps1

# Verify activation (should show (venv) in terminal prompt)
```

### Issue: Python interpreter not showing in VS Code
```bash
# Open Command Palette: Ctrl+Shift+P
# Type: Python: Select Interpreter
# Choose: ./venv/bin/python (the one with venv path)

# Verify in terminal
python --version  # Should show Python 3.9+
```

### Issue: `gh copilot` command returns "not found"
```bash
# Check if gh extension is installed
gh extension list

# If not listed, install it
gh extension install github/gh-copilot

# Check installation directory
ls ~/.config/gh/extensions/  # On Mac/Linux
# Or
%APPDATA%\GitHub CLI\extensions  # On Windows
```

### Issue: "Authorization required" error
```bash
# Re-authenticate GitHub CLI
gh auth logout
gh auth login
# Follow the prompts

# Verify authentication
gh auth status
```

---

## 📚 Resources

- **[GitHub Copilot Extension](https://marketplace.visualstudio.com/items?itemName=GitHub.copilot)** — VS Code Marketplace
- **[Copilot CLI Documentation](https://docs.github.com/en/copilot/github-copilot-cli/about-github-copilot-cli)**
- **[VS Code setup guide](https://code.visualstudio.com/docs/setup/setup-overview)**
- **[GitHub CLI reference](https://cli.github.com/manual/)**
- **[Python virtual environments](https://docs.python.org/3/tutorial/venv.html)**

---

## ✨ Quick Reference

**VS Code Keyboard Shortcuts:**
- Open terminal: `` Ctrl+` ``
- Open command palette: `Ctrl+Shift+P`
- Open file explorer: `Ctrl+Shift+E`
- Open extensions: `Ctrl+Shift+X`
- Select Python interpreter: `Ctrl+Shift+P` → "Python: Select Interpreter"

**Essential Commands:**
```bash
# Activate virtual environment
source venv/bin/activate          # Mac/Linux
venv\Scripts\activate.bat         # Windows (Command Prompt)
venv\Scripts\Activate.ps1         # Windows (PowerShell)

# Test Copilot CLI
gh copilot --version
gh copilot explain app.py

# Check Python
python --version
pip list
```

---

## 🎯 Ready for Next Step?

Once all acceptance criteria are met, proceed to:

### **[Exercise 1: GitHub Agent Security Review](./1-agent-security-review.md)** →

This exercise will use the Copilot CLI to discover the first set of vulnerabilities in the SecureTrails application.

---

**⏱️ Time Elapsed**: ~10 minutes  
**Next Exercise**: Exercise 1 (20 min)
