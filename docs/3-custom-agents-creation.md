# Exercise 3: Create Custom Agents Using Copilot CLI
## Using Built-in Agent Management System

**Duration**: 20 minutes  
**Type**: ⭐⭐⭐⭐ Agent creation  
**Focus**: Use Copilot CLI's `/agents` system to create custom agents

---

## 🎯 Learning Objectives

✅ Launch Copilot CLI and access the Agent menu  
✅ Use Copilot CLI's built-in `/agents` management  
✅ Create domain-specific agents for vulnerabilities  
✅ Understand agent structure and documentation  
✅ Build a library of custom agents for SecureTrails  

---

## 📖 What is a Custom Agent?

**In Copilot CLI, a "Custom Agent" is:**
- A reusable instruction set for fixing specific vulnerabilities
- Managed through Copilot CLI's interactive menu
- Can be invoked to guide developers through remediation
- Tailored to your domain/application
- Persistent within your Copilot CLI environment

---

## 🚀 Step 1: Launch Copilot CLI and Access Agent Menu

In your terminal, run:

```bash
npx @github/copilot
```

You'll see the Copilot CLI interface. To access custom agents, look for the **"Custom Agents"** section or type:

```bash
/agents
```

**You'll see this menu:**

![Copilot Custom Agents Menu](./images/copilot-custom-agents-menu.png)

Available options:
- **1. Create new agent...** ← Select this to create SQL injection agent
- **2. Learn more about custom agents** - Get info about agent structure

---

## 🛠️ Step 2: Create SQL Injection Fix Agent

Select option **1. Create new agent...**

**Copilot prompts you:**

```
Agent name: sql-injection-fix-guide
Agent description: Remediation guide for SQL injection vulnerabilities in Flask apps
```

Enter details:

```
Name: sql-injection-fix-guide
Description: Step-by-step guide to fix SQL injection in SecureTrails Flask database queries

Then Copilot asks for the agent content/instructions:

Instructions to include:
- Our app uses Flask with SQLite/MySQL
- Vulnerability: User input directly concatenated into SQL queries (app.py line ~47)
- The issue: query = f"SELECT * FROM trails WHERE location = '{user_input}'"
- Need: parameterized queries, before/after examples, testing approach
- Target audience: 2 senior devs, 1 junior
- Include: Common mistakes, timeline, success criteria
```

**Copilot creates the agent** and shows success:

![Agent Generation Successful](./images/copilot-agent-success.png)

**You'll see:**
- ✅ Agent generation successful!
- Name: sql-injection-remediation-guide
- Instructions: 6,662 chars
- The agent is 41KB with complete examples, test cases, and timeline

---

## 🔧 Step 2.5: Configure Agent Tools

Copilot asks: **"Which tools should this agent have access to?"**

![Agent Tools Selection](./images/copilot-agent-tools-selection.png)

**Options:**
- **1. All tools** ← Select this (agent can use all Copilot capabilities)
- **2. Select by category...** (customize tool access)

Select **"All tools"** for full agent capabilities.

---

## ✅ Step 3: Agent Saved Successfully

Copilot confirms:

![Agent Saved to Repository](./images/copilot-agent-saved.png)

**You'll see:**
```
Created agent at .github\agents\sql-injection-remediation-guide.agent.md
```

**This means:**
- ✅ Agent automatically saved to `.github/agents/` folder
- ✅ File format: `.agent.md` (Copilot's agent format)
- ✅ Agent is now persistent in your repository
- ✅ Can be referenced in GitHub Actions (Exercise 4)

---

## 📝 Step 4: Select Your Custom Agent

After agent is created, Copilot shows the agent selection menu:

![Select Custom Agent](./images/agent%20selection.png)

**You'll see:**
```
Selected custom agent: sql-injection-remediation-guide

Select Agent:
> 1. Default (deselect current agent)
  2. sql-injection-remediation-guide (current)

Manage Agents:
  3. Create new agent...
  4. Learn more about custom agents
```

Your agent is now **selected and active**. The agent responds with tailored guidance:

![Custom Agent Fixes Response](./images/custom%20agent.png)

**The agent delivers:**
- ✅ References your specific app (SecureTrails)
- ✅ Points to exact line numbers and vulnerabilities
- ✅ Provides step-by-step fixes
- ✅ Shows before/after code examples
- ✅ Includes testing strategy
- ✅ Tailored to your team (senior devs, juniors)

---

## 💬 Step 5: Ask Your Questions to the Agent

Now you can ask security questions and get tailored responses:

**Example questions:**

```bash
# Ask the agent about your specific problem:
"How would we fix line 47 in app.py?"

# Or:
"What's the step-by-step process to patch this SQL injection?"

# Or:
"Show me the before/after code for this vulnerability"
```

The agent responds with step-by-step guidance tailored to your team's needs.

---

## 🔄 Step 6: Create More Agents (Repeat for 3 Remaining)

Follow the **exact same workflow** for the remaining vulnerabilities:

1. **Create new agent** → Enter name, description, instructions
2. **Select tools** → Choose "All tools"
3. **Confirm** → Agent saved to `.github/agents/`
4. **Select agent** → Choose from menu (optional - can switch agents)
5. **Use agent** → Ask security questions

### Agent 2: Authentication & Authorization Fix

```
Name: authentication-fix-guide
Description: Secure user permission validation in Flask endpoints

Content: 
- Problem: DELETE /booking/123 doesn't verify ownership
- User A can modify User B's bookings via URL parameter
- Need: Flask decorator for authorization checks
- Include: session validation, permission testing, common mistakes
```

---

### Agent 3: XSS Prevention Fix

```
Name: xss-fix-guide
Description: HTML escaping and XSS prevention in Jinja2 templates

Content:
- Problem: User comments rendered without HTML escaping
- Templates use {{ user_input }} directly
- Need: Jinja2 autoescape, CSP headers
- Include: before/after templates, testing payloads
```

---

### Agent 4: Dependency Security Fix

```
Name: dependency-update-guide
Description: Safe upgrade path for vulnerable Python packages

Content:
- Problem: Flask 1.1.2 (vulnerable) → 2.3.0 (breaking changes)
- Need: Testing strategy, rollback plan, upgrade order
- Include: regression tests, documentation updates
```

---

## ✅ Your Custom Agent Library

---

## 📋 Reference: Copilot CLI Commands

When you're in the Copilot CLI interactive session (`npx @github/copilot -i`), you can use these slash commands:

```
Available Commands:
/version     - Show Copilot CLI version
/help        - Display help information
/agents      - Manage custom agents (CREATE, LIST, EDIT, DELETE)
/clear       - Clear conversation history
/exit        - Exit the interactive session
```

**Most important for this exercise**: `/agents` - opens the agent management menu where you:
- Create new agents
- List existing agents
- Edit agent instructions
- Delete agents you no longer need

---

## ✨ After This Exercise

Your agents are available in Copilot CLI:

```
Copilot CLI /agents menu:
├── sql-injection-fix-guide
├── authentication-fix-guide
├── xss-fix-guide
└── dependency-update-guide
```

**These are managed directly by Copilot CLI** - no file management needed.

---

## 💡 Key Insight: Managed Agents vs Manual Files

**Copilot CLI's built-in agents:**
- ✅ Managed through interactive menu
- ✅ Persistent in your Copilot environment
- ✅ Can be referenced in conversations
- ✅ Reusable across projects
- ✅ No manual file creation

**NOT** `.md` files in `.github/agents/` - those are for GitHub Actions integration (Exercise 4).

---

## 🎯 Using Agents in Conversations

Once agents are created, you can reference them:

```bash
# In Copilot CLI:
"Using the sql-injection-fix-guide agent, how would we fix line 47 in app.py?"

# Or:
"Walk me through the authentication-fix-guide agent for our booking endpoint"
```

Copilot uses your agent knowledge to guide you through fixes.

---

## ✅ Acceptance Criteria

- [ ] Launched Copilot CLI successfully
- [ ] Accessed the `/agents` menu  
- [ ] Created at least 1 custom agent (SQL injection)
- [ ] Created all 4 custom agents (SQL, Auth, XSS, Dependencies)
- [ ] Each agent has name, description, and content
- [ ] Can reference agents in Copilot conversations
- [ ] Understand Copilot CLI agent management system

---

## 🚀 Next Exercise

**Exercise 4**: GitHub Actions Integration
- Export agents as documentation
- Link to GitHub issues
- Automate GHAS → Issue → Agent workflow

---

**⏱️ Time**: 20 min | **Exercises**: 3/6 ✓

**Custom agents are now persistent in your Copilot CLI environment!**

---
