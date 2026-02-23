# Exercise 3: Create Custom Agents - Generate Fix Guides Using Copilot CLI
## Building Domain-Specific Vulnerability Fixes

**Duration**: 20 minutes  
**Type**: ⭐⭐⭐⭐ Agent creation  
**Focus**: Use Copilot CLI to CREATE custom agents (.md guides) for fixing vulnerabilities

---

## 🎯 Learning Objectives

✅ Understand what a "custom agent" is (fix documentation)  
✅ Use Copilot CLI to GENERATE fix guides  
✅ Create `.md` agent files for SecureTrails vulnerabilities  
✅ Document step-by-step remediation processes  
✅ Build a library of custom agents for your domain  

---

## 📖 What is a Custom Agent?

**In this workshop, a "Custom Agent" is:**
- A `.md` file that documents HOW to fix a specific vulnerability
- Created using Copilot CLI prompts
- Contains step-by-step remediation instructions
- Stored in `.github/agents/` as reference guides
- Used by developers to understand AND fix issues

**NOT**:
- Pre-built Python scripts (we don't use those)
- Automated executables
- Magic frameworks

**Simply**: Intelligent documentation for fixing security issues.

---

## 📋 The Vulnerability We Found

From Exercise 1 (GitHub GHAS), we detected:

```
🔴 CRITICAL: SQL Injection in database query layer
File: apps/securetrails-vulnerable/app.py
Line: ~47
Issue: User input directly concatenated into SQL query
```

Example vulnerable code:
```python
user_input = request.args.get('location')
query = f"SELECT * FROM trails WHERE location = '{user_input}'"
database.execute(query)  # VULNERABLE!
```

**Now**: Use Copilot CLI to CREATE a fix guide (custom agent).

---

## 🚀 Step 1: Launch Copilot CLI

```bash
copilot
```

You'll see:
```
Welcome to GitHub Copilot CLI
Type your prompt and press Enter for analysis
/help for commands | /exit to quit
```

---

## 🛠️ Step 2: Create SQL Injection Fix Agent

Ask Copilot CLI to generate a fix guide:

```
I'm a lead dev at SecureTrails (Flask/Python app) and we just got flagged by GitHub GHAS 
for SQL injection in our database layer. 

Here's what we found:
- File: app.py, Line 47
- The problem: User input from request.args is directly concatenated into SQL queries
- Example: `query = f"SELECT * FROM trails WHERE location = '{user_input}'"`
- This breaks our authentication AND lets attackers dump the entire database

I need to create a remediation guide for our team (2 seniors, 1 junior). 

Create a structured, implementable guide that covers:
1. What's the risk? (make it real - what could attackers actually DO?)
2. Root cause analysis (where in our code?)
3. Step-by-step fix process (how exactly do we change the code?)
4. Before/After code examples (show Python SQLAlchemy AND raw MySQLdb patterns)
5. Testing strategy (how do we VERIFY it's fixed, including injection payloads to try?)
6. Gotchas & common mistakes (what could go wrong during refactor?)
7. Timeline (how long should this take?)

Make it something we can literally hand to a developer and say 'go fix this' without 
needing a security consultant holding their hand the whole time.
```

**Copilot responds** with structured remediation guide:

```markdown
# SQL Injection Fix Guide - SecureTrails Database Layer

## Executive Summary
SQL Injection is a CRITICAL vulnerability allowing attackers to:
- Extract all database records
- Modify or delete data
- Escalate privileges

**Risk Level**: CRITICAL
**Effort**: 2-4 hours
**Impact**: Prevents remote code execution

## Root Cause
User input from `request.args.get('location')` is directly interpolated into SQL queries.
The string formatting operator (`f"..."`) does NOT sanitize input.

## Remediation Steps

### Step 1: Identify All Vulnerable Query Points
```bash
grep -r "f\"SELECT" apps/securetrails-vulnerable/
grep -r "f'SELECT" apps/securetrails-vulnerable/
grep -r "query = f" apps/securetrails-vulnerable/
```

### Step 2: Understand Parameterized Queries
Parameterized queries separate SQL code from data:
```python
# VULNERABLE - String interpolation
query = f"SELECT * FROM users WHERE id = {user_id}"

# SAFE - Parameterized query
query = "SELECT * FROM users WHERE id = ?"
cursor.execute(query, (user_id,))
```

The `?` is a placeholder. User_id is passed separately, so it's treated as DATA, not code.

### Step 3: Fix the Code

**BEFORE (Vulnerable)**:
```python
@app.route('/api/trails')
def search_trails():
    location = request.args.get('location')
    query = f"SELECT * FROM trails WHERE location = '{location}'"
    results = db.execute(query)
    return jsonify(results)
```

**AFTER (Secure)**:
```python
@app.route('/api/trails')
def search_trails():
    location = request.args.get('location')
    query = "SELECT * FROM trails WHERE location = ?"
    results = db.execute(query, (location,))
    return jsonify(results)
```

### Step 4: Test the Fix

**Test with normal input**:
```bash
curl "http://localhost:5000/api/trails?location=Colorado"
# Should return trails in Colorado
```

**Test with SQL injection payload**:
```bash
curl "http://localhost:5000/api/trails?location=Colorado' OR '1'='1"
# Should return NO trails (or error)
# BEFORE fix: Would return ALL trails
# AFTER fix: Safely handles the quote as a string
```

### Step 5: Code Review Checklist
- [ ] All user input queries use parameterized queries
- [ ] No f-string SQL query construction
- [ ] No string concatenation in queries
- [ ] Tests confirm injection attempts fail safely
- [ ] Security team approval

### Step 6: Deploy
1. Merge PR after security review
2. Deploy to staging first
3. Run integration tests
4. Monitor production logs for errors

## Common Pitfalls to Avoid
❌ Sanitizing input with string escaping (doesn't work reliably)
❌ Using only for user input (ALL external input needs parameterization)
❌ Mixing parameterized and non-parameterized queries

## Success Criteria
✅ No SQL injection test payloads succeed
✅ All legitimate queries work correctly
✅ GitHub GHAS reports 0 SQL injection findings
✅ Security team approval obtained
```

---

## 📝 Step 3: Save the Agent Guide

Save what Copilot generated as a custom agent:

**File**: `.github/agents/sql-injection-fix-guide.md`

**Content**: (Paste Copilot's entire response)

This is your first **custom agent** - a domain-specific fix guide created by Copilot CLI.

---

## 🔄 Step 4: Create More Custom Agents - Domain-Specific Remediations

Repeat for other vulnerabilities found by GHAS:

### Agent 2: Authentication & Authorization Fix

Ask Copilot CLI:
```
Our SecureTrails Flask app has a broken authentication issue flagged by GitHub GHAS.
The problem: We're not validating user permissions on data modifications.

Specifically:
- User A can modify User B's trail bookings by changing a URL parameter
- Sessions exist but aren't checked on state-changing operations (PUT, DELETE, POST)
- Example: DELETE /booking/123 should verify the logged-in user OWNS booking 123

Create a fix guide that covers:
1. Why this is a CRITICAL business risk (attackers can book/cancel other users' trips)
2. Root cause (session handling vs permission validation)
3. How to implement proper authorization checks in Flask decorators
4. Before/After code showing vulnerable endpoint vs secure endpoint
5. How to test permission boundaries (which operations should succeed/fail for different users)
6. Common mistakes (hardcoding IDs, forgetting session checks, etc)

Include realistic Python patterns we can use. Our team uses Flask-Login, so show that pattern.
This should be implementable in 1-2 days for an experienced developer.
```

Save as: `.github/agents/authentication-fix-guide.md`

### Agent 3: XSS Prevention Fix

Ask Copilot CLI:
```
GitHub GHAS flagged XSS vulnerabilities in our Jinja2 templates where user-submitted 
trail comments and descriptions are rendered without HTML escaping.

The risk: Attackers inject JavaScript that runs in OTHER users' browsers 
(stealing cookies, redirecting to malware, etc)

Create a remediation guide:
1. How does XSS happen in Jinja2? (what's the specific template pattern we're using wrong?)
2. Why is this dangerous for SecureTrails specifically? (we store user comments)
3. How to fix templates - Jinja2 escaping patterns and when to use autoescape
4. Before/After template examples
5. Content Security Policy headers we should add to app.py
6. Testing - how to verify XSS payloads are now neutralized (include test payloads)
7. Performance implications of escaping (is there any?)

We're already escaping in SOME places inconsistently, so explain when escaping is needed 
vs when it's not. Show the safe defaults.
```

Save as: `.github/agents/xss-fix-guide.md`

### Agent 4: Dependency Security Fix

Ask Copilot CLI:
```
Our requirements.txt has flagged vulnerabilities in dependencies (Flask 1.1.2 → 2.3.0, 
Jinja2 2.11 → 3.1.0, requests 2.28.0 → older).

We need a process for safely upgrading without breaking the application.

Create a guide:
1. What are the risks of upgrading vs NOT upgrading dependencies?
2. Breaking changes to watch for between Flask 1.x and 2.x
3. Testing strategy (unit tests? integration tests? manual?)
4. Rollback plan if something breaks
5. Step-by-step upgrade process (in what order should we upgrade?)
6. How to verify no regression after upgrade
7. Documentation update checklist

We have a 2-hour regression test window before the next deploy.
```

Save as: `.github/agents/dependency-update-guide.md`

---

## ✅ Your Custom Agent Library

After this exercise, you'll have:

```
.github/agents/
├── sql-injection-fix-guide.md .............. Fix SQL injection
├── authentication-fix-guide.md ............ Fix auth issues
├── xss-fix-guide.md ...................... Fix XSS vulnerabilities
└── dependency-update-guide.md ............ Safe dependency updates
```

**These are your CUSTOM AGENTS** - Copilot-generated fix guides for YOUR domain.

---

## 🎯 Key Insight: Custom Agents = Smart Documentation

**What custom agents do**:
- ✅ Explain WHAT vulnerability exists (why GitHub flagged it)
- ✅ Explain WHY it's dangerous (business impact)
- ✅ Show BEFORE/AFTER code examples
- ✅ Provide step-by-step fix instructions
- ✅ Include testing strategies
- ✅ Prevent developers from making mistakes

**What they DON'T do**:
- ❌ Automatically fix code (that's developer's job)
- ❌ Run as background services
- ❌ Execute code
- ❌ Bypass manual review

**They guide, not automate.**

---

## 💡 Using Custom Agents in Workflow

In Exercise 4 (GitHub Actions), we'll:

1. GHAS finds vulnerability → Creates issue
2. Issue links to custom agent (fix guide)
3. Developer reads agent guide
4. Developer applies fixes following guide
5. Re-runs GHAS to verify fix
6. Issue closes when fixed

---

## ✅ Acceptance Criteria

- [ ] Used Copilot CLI to create at least 1 custom agent
- [ ] Saved agent as `.md` file in `.github/agents/`
- [ ] Agent includes: Problem, Why it's bad, Before/After code, Fix steps
- [ ] Agent is formatted for easy developer reading
- [ ] Created minimum 2 agents (one required, one bonus)
- [ ] Understand agents are documentation, not code execution
- [ ] Can explain how agents will be used in GitHub Actions

---

## 📚 Agent Best Practices

When creating custom agents via Copilot CLI:

1. **Be Specific**: Include exact file names and line numbers from GHAS findings
2. **Show Examples**: Include actual before/after code
3. **Step-by-Step**: Number each action clearly
4. **Add Testing**: How to verify the fix works
5. **Link to Standards**: Reference OWASP, CWE where applicable
6. **Include Effort**: Time estimate for developers
7. **Add Validation**: Checklist to verify completion

---

## 🚀 Next Steps

**Exercise 4**: GitHub Actions Integration
- Connect GHAS findings → Custom agent guides → Developer workflow
- Automate issue creation with agent links
- Track remediation progress

---

**⏱️ Time**: 20 min | **Exercises**: 3/5 ✓

**You just created your FIRST custom agent using Copilot CLI!**
