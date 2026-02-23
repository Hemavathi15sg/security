# Exercise 3: Secret Detection (Credential Leak Prevention)

**Duration**: 15 minutes  
**Level**: ⭐⭐ Intermediate  

---

## 🎯 Learning Objectives

✅ Run secret detection agent  
✅ Understand credential leak risks  
✅ Identify hardcoded secrets using regex + entropy analysis  

---

## 📖 Scenario

Prevent accidental API key/password commits. Run a secret detection agent to find hardcoded credentials before they reach the repository.

---

## 🚀 Run the Agent

### Step 1: Execute Secret Detector

```bash
cd apps/securetrails-vulnerable
python ../../.github/agents/secret-detector.py
```

This scans all files for:
- Hardcoded API keys (AWS, GitHub, etc.)
- Database passwords
- JWT secrets  
- Private keys
- Entropy-based detection (random strings that look like secrets)

**Example output:**
```
SECRETS FOUND
=============

CRITICAL:
1. JWT_SECRET in app.py:12
   Pattern: JWT_SECRET = 'super-secret-key-12345'
   Fix: Move to environment variable

2. Database password in .env.example:3
   Pattern: postgres://user:PASSWORD123@localhost
   Fix: Use .env (never commit real credentials)

Exit code: 1 (secrets found = block commit)
```

---

## 🛠️ Agent Deep Dive: secret-detector.py

### How Credential Detection Works

```bash
# View agent source
cat .github/agents/secret-detector.py | head -80
```

**Two detection methods:**

**Method 1: Pattern Matching (Regex)**
```python
PATTERNS = {
    'API_KEY': r'[a-z0-9]{20,}',           # Long random strings
    'JWT_SECRET': r'JWT_SECRET\s*=',       # Direct secret names
    'DB_PASSWORD': r'password["\']?\s*[:=]',  # Credential patterns
    'AWS_KEY': r'AKIA[0-9A-Z]{16}',       # AWS key format
}
```

**Method 2: Entropy Analysis**
```python
def calculate_entropy(string):
    """If string looks random = likely a secret"""
    entropy = 0
    for char in set(string):
        frequency = string.count(char) / len(string)
        entropy -= frequency * log2(frequency)
    return entropy

# High entropy (>= 4.0) = suspicious = likely secret
if entropy > 4.0:
    flag_as_secret()
```

### Real Example From SecureTrails

```python
# Found in app.py:12
JWT_SECRET = 'super-secret-key-12345'  ← Pattern match: JWT_SECRET =

# Found in .env.example:3  
db_password = 'postgres://user:PASSWORD123@...'  ← Pattern match: password

# Also catches random-looking entropy
api_key = 'sk_live_51234567890abcdefghijklmnopqrstuv'  ← High entropy
```

### Hands-On: Add New Secret Patterns

```bash
# Edit the agent
code .github/agents/secret-detector.py

# Find PATTERNS dict and add:
'GITHUB_TOKEN': r'ghp_[A-Za-z0-9_]{36}',     # GitHub Personal Access Token
'STRIPE_KEY': r'sk_live_[A-Za-z0-9]{24}',   # Stripe live key
```

Test your changes:

```bash
python .github/agents/secret-detector.py

# Should now catch GitHub tokens and Stripe keys
python .github/agents/secret-detector.py | grep -E "GITHUB_TOKEN|STRIPE"
```

---

Notice the agent found:
- ✅ Hardcoded JWT secret
- ✅ DB password in .env.example  
- ✅ AWS credentials pattern
- ✅ Private key exposed

**Exit code mapping:**
- `1` = Secrets found (should block CI/CD)
- `0` = Clean (safe to proceed)

---

### Step 3: Create Issue

```bash
gh issue create \
  --title "[SECURITY] Exercise 3: Hardcoded Secrets Found" \
  --label "security,exercise" \
  --body "## Secret Detection Results

Agent found 2 CRITICAL hardcoded secrets:

1. JWT Secret in app.py:12
2. DB Password in .env.example:3

All credentials must be moved to environment variables.
Never commit real credentials to version control."
```

---

## ✅ Acceptance Criteria

- [ ] Ran `python .github/agents/secret-detector.py`
- [ ] Found ≥2 CRITICAL secrets (JWT, DB password)
- [ ] Understood exit codes (1=secrets, 0=clean)
- [ ] Created GitHub issue with findings
- [ ] Understood how agents detect credentials

---

## 📚 Resources

- [OWASP Secret Management](https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html)  
- [How to Identify Secrets](./resources/reference.md)

---

**⏱️ Time**: 15 min | **Exercises**: 4/5
