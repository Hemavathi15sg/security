# Exercise 2: Copilot CLI - Interactive Security Analysis
## Real-Time Conversational Code Review

**Duration**: 20 minutes  
**Type**: ⭐⭐⭐ Interactive analysis  
**Focus**: Copilot CLI (`copilot` shell) for conversational security review

---

## 🎯 Learning Objectives

✅ Launch Copilot CLI interactive shell  
✅ Use real-time prompts to analyze code security  
✅ Have multi-turn conversation about vulnerabilities  
✅ Get contextual, reasoning-based analysis (not just pattern matching)  
✅ See how AI augments GitHub's native scanning  

---

## 📖 Scenario

**GitHub GHAS detected vulnerabilities in securetrails-workshop.**  
**Now: Why do they exist? How serious? What's the best fix?**

This is where **Copilot CLI's conversational capability** adds value:
- Interactive discussion about findings
- Contextual reasoning about impact
- Follow-up questions about architecture
- Trade-off analysis for fixes

GitHub GHAS = Automated detection  
Copilot CLI = Human-like reasoning

---

## 🚀 Step 1: Launch Copilot CLI

Open terminal and run:

```bash
npx @github/copilot
```

**You'll see this interactive shell:**

![Copilot CLI Interface](./images/copilotversion.png)

**Available commands:**
- Type your prompt and press Enter
- `/help` - Show available commands
- `/exit` - Close Copilot

---

## 💬 Step 2: First Prompt - Overview Analysis

Run this command with your initial security assessment request:

```bash
npx @github/copilot -i "I'm reviewing a Flask web application called SecureTrails - a trail booking platform. I need a quick security assessment. Can you help me identify:

1. The top 3 CRITICAL vulnerabilities that would most likely affect a booking app like this
2. What's the real-world business impact if an attacker exploited each?
3. What architectural patterns or practices would prevent these specific issues?

The app has:
- Backend logic in app.py (Flask routes, database queries)
- HTML templates with user-generated content
- JavaScript on the frontend
- Python dependencies in requirements.txt

What are the biggest red flags I should look for?"
```

**Copilot responds** with contextual overview:

```
## Security Review: SecureTrails Application

### CRITICAL Risk #1: SQL Injection in User Input Handling
**Severity**: CRITICAL - Remote Code Execution possible
**Location**: app.py database query layer
**Issue**: User input from requests directly interpolated into SQL queries
**Business Impact**: Attacker can extract all user data, modify bookings, escalate privileges
**Fix Pattern**: Use parameterized queries (ORM layer, prepared statements)
**Time to Fix**: 2-4 hours

### CRITICAL Risk #2: Insufficient Authentication 
**Severity**: CRITICAL
**Issue**: Session handling doesn't validate user permissions on state changes
**Business Impact**: Users can book/cancel other users' trails, modify reservations
**Fix Pattern**: Implement role-based access control, validate user_id in every mutation
**Time to Fix**: 4-6 hours

### CRITICAL Risk #3: Cross-Site Scripting (XSS) in User Comments
**Severity**: CRITICAL  
**Location**: Trail detail pages render user comments without escaping
**Business Impact**: Attackers can run JavaScript in other users' browsers
**Fix Pattern**: Auto-escape HTML in template rendering

These three risks compound each other...
```

---

## 🔍 Step 3: Create Issue & Try Fixing It

Based on Copilot's analysis, use Copilot CLI to create a GitHub issue directly through GitHub's MCP.

### Create Issue Using Copilot CLI

Ask Copilot to create the GitHub issue for you:

```bash
npx @github/copilot -i "I need you to create a GitHub issue in my repository (Hemavathi15sg/securetrails-workshop) for the SQL injection vulnerability we just discussed.

Please create an issue with:
- Title: 'fix(security): SQL Injection - Parameterize database queries'
- Description: Include the vulnerability summary, the vulnerable code location, and the fix approach
- Labels: security, critical, bug
- Assignees: (optional - leave empty)

Make the description clear enough that any developer can understand the fix needed."
```

**Copilot will:**
1. ✅ Create the issue in your GitHub repository
2. ✅ Format the title and description professionally
3. ✅ Add appropriate labels (security, critical)
4. ✅ Return the issue URL and number

**Example Issue Created:**

```
Title: fix(security): SQL Injection - Parameterize database queries
Issue #47
Description:
## Vulnerability
Location: app.py, trails search endpoint (line 47)
Type: SQL Injection

## Current Code (Vulnerable)
User input directly concatenated into SQL queries:
query = f"SELECT * FROM trails WHERE location = '{user_input}'"

## Risk
- Attackers can extract all database records
- Can modify or delete data
- Possible privilege escalation

## Fix
Use parameterized queries - pass user input as separate parameter, not in SQL string:
query = "SELECT * FROM trails WHERE location = ?"
db.execute(query, (user_input,))

## Priority
CRITICAL - Fix immediately
```

---

### Try the Fix

Implement the before/after code fix in your local branch

```python
# BEFORE (Vulnerable - App.py line 47)
def search_trails():
    user_input = request.args.get('location')
    query = f"SELECT * FROM trails WHERE location = '{user_input}'"
    results = database.execute(query)
    return jsonify(results)

# AFTER (Fixed - Using parameterized query)
def search_trails():
    user_input = request.args.get('location')
    query = "SELECT * FROM trails WHERE location = ?"
    results = database.execute(query, (user_input,))
    return jsonify(results)
```

**Key change:**
- ❌ Bad: `f"SELECT * FROM trails WHERE location = '{user_input}'"`
- ✅ Good: `"SELECT * FROM trails WHERE location = ?"` + `(user_input,)`

The database driver treats the parameter as DATA, not SQL code, preventing injection.

---

## 🎓 Why This Matters

**Copilot CLI provides 3 things GitHub GHAS can't:**

1. **Explanation**: Not just "SQL injection found" but *why* it matters
2. **Context**: Multi-turn conversation about your app architecture
3. **Guidance**: Step-by-step fix recommendations tailored to your codebase

---

## ✅ Acceptance Criteria

- [ ] Launched Copilot CLI interactive session
- [ ] Asked initial security assessment question
- [ ] Had follow-up conversation about findings
- [ ] Created GitHub issue from analysis
- [ ] Attempted before/after code fix
- [ ] Understood why parameterized queries prevent SQL injection

---

## 🚀 Next Steps

**Exercise 3**: Create Custom Agents
- Custom agents = fix guides that any developer can follow
- Repeat this "analyze → fix" process consistently across your team

---

**⏱️ Time**: 20 min | **Exercises**: 2/6 ✓
