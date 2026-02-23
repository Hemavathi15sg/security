# Exercise 3: Custom Detection Tools - Build Your Own Security Scanners
## When GitHub GHAS Isn't Enough

**Duration**: 20 minutes  
**Type**: ⭐⭐⭐⭐ Practical construction  
**Focus**: Create specialized security detection scripts

---

## 🎯 Learning Objectives

✅ Understand when custom tools are needed  
✅ Build a Python security detection script from scratch  
✅ Define custom detection patterns for your domain  
✅ Integrate output with GitHub (JSON format)  
✅ See how this fits into the ecosystem (not a magic "agent framework")

---

## 📋 Scenario

**GitHub GHAS covers standard vulnerabilities:**
- SQL injection ✅
- XSS ✅  
- Weak cryptography ✅
- Known vulnerable packages ✅

**GitHub GHAS MISSES domain-specific risks:**
❌ Business logic flaws (booking system allowing double-booking)  
❌ Configuration issues (debug mode left on in production)  
❌ API contract violations  
❌ Custom authentication bypasses  

**This Exercise:**  
Build a detector for SecureTrails' specific risk: **insecure comparison operators in access control**.

```python
# Vulnerable pattern to detect
if user_id == admin_id:  # Should be "is" for Python objects
if password_input == stored_password:  # Timing attack vulnerability
```

---

## 🔨 Step 1: Understand the Problem

Review the issue in SecureTrails code:

```bash
grep -r "==" apps/securetrails-vulnerable/app.py | head -10
```

Look for patterns like:

```python
# BAD: Timing attack vulnerability
if user_password == stored_password:
    login_user()

# BAD: Type confusion
if user_id == admin_id:  # Could match different types
    grant_admin()

# GOOD: Safe comparison
import hmac
if hmac.compare_digest(user_password, stored_password):
    login_user()
```

---

## 🛠️ Step 2: Create a Detection Script

Create a new file: `.github/agents/access-control-detector.py`

```python
#!/usr/bin/env python3
"""
Custom Security Detector: Insecure Access Control Patterns
Scans for dangerous == comparisons in security contexts
"""

import re
import json
import sys
from pathlib import Path

class AccessControlDetector:
    def __init__(self, repo_root):
        self.repo_root = Path(repo_root)
        self.findings = []
        
        # Patterns that indicate security-sensitive == comparisons
        self.dangerous_patterns = [
            # Direct password comparison
            (r'if\s+\w+_password\s*==', 'Timing attack: Direct password comparison'),
            (r'password.*==.*password', 'Timing attack: Direct password comparison'),
            
            # Type confusion in admin checks  
            (r'if\s+\w+_id\s*==\s*admin_id', 'Type confusion: ID comparison without type check'),
            (r'if\s+\w+\s*==\s*["\']\w+["\']\s*:', 'String comparison without escaping'),
            
            # Token/session validation
            (r'if\s+\w+_token\s*==\s*\w+_token', 'Timing attack: Token comparison'),
        ]
        
    def scan_file(self, filepath):
        """Scan a single file for dangerous patterns"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                lines = f.readlines()
        except:
            return
        
        for line_num, line in enumerate(lines, 1):
            # Skip comments and non-Python files
            if not filepath.suffix == '.py':
                continue
            if line.strip().startswith('#'):
                continue
                
            for pattern, risk in self.dangerous_patterns:
                if re.search(pattern, line):
                    self.findings.append({
                        'file': str(filepath.relative_to(self.repo_root)),
                        'line': line_num,
                        'code': line.strip(),
                        'risk': risk,
                        'severity': 'CRITICAL',
                        'riskType': 'InsecureComparison'
                    })
    
    def scan_directory(self):
        """Scan all Python files in repo"""
        for py_file in self.repo_root.rglob('*.py'):
            # Skip virtual environments and caches
            if 'venv' in str(py_file) or '__pycache__' in str(py_file):
                continue
            self.scan_file(py_file)
    
    def generate_report(self):
        """Output findings as JSON"""
        report = {
            'tool': 'AccessControlDetector',
            'scanTime': '2026-01-20T10:00:00Z',
            'totalFindings': len(self.findings),
            'critical': len([f for f in self.findings if f['severity'] == 'CRITICAL']),
            'findings': self.findings
        }
        return report

if __name__ == '__main__':
    # Run from repo root
    repo_root = sys.argv[1] if len(sys.argv) > 1 else '.'
    
    detector = AccessControlDetector(repo_root)
    detector.scan_directory()
    report = detector.generate_report()
    
    # Output JSON
    print(json.dumps(report, indent=2))
    
    # Exit with code based on findings
    sys.exit(1 if report['critical'] > 0 else 0)
```

---

## 🚀 Step 3: Test Your Scanner

Run the detector on SecureTrails:

```bash
python .github/agents/access-control-detector.py apps/securetrails-vulnerable
```

**Expected output:**

```json
{
  "tool": "AccessControlDetector",
  "scanTime": "2026-01-20T10:00:00Z",
  "totalFindings": 3,
  "critical": 3,
  "findings": [
    {
      "file": "app.py",
      "line": 67,
      "code": "if user_password == stored_password:",
      "risk": "Timing attack: Direct password comparison",
      "severity": "CRITICAL",
      "riskType": "InsecureComparison"
    },
    {
      "file": "app.py",
      "line": 142,
      "code": "if user_id == admin_id:",
      "risk": "Type confusion: ID comparison without type check",
      "severity": "CRITICAL",
      "riskType": "InsecureComparison"
    }
  ]
}
```

**Check exit code:**

```bash
python .github/agents/access-control-detector.py apps/securetrails-vulnerable
echo "Exit code: $?"  # Should be 1 (critical findings found)
```

---

## 🎯 Step 4: Add Fix Recommendations

Enhance your detector to suggest fixes:

```python
def suggest_fix(self, finding):
    """Generate fix recommendations"""
    if 'password' in finding['code'].lower():
        return {
            'recommendation': 'Use constant-time comparison',
            'example': 'import hmac\nif hmac.compare_digest(user_pwd, stored_pwd):',
            'reason': 'Prevents timing attacks'
        }
    elif 'id' in finding['code'].lower():
        return {
            'recommendation': 'Use type-safe comparison',
            'example': 'if int(user_id) == int(admin_id) and isinstance(user_id, int):',
            'reason': 'Prevents type confusion attacks'
        }
    return {'recommendation': 'Review security context'}
```

Add to your findings:

```python
finding['fix'] = self.suggest_fix(finding)
```

---

## 📊 Step 5: Integration Points

Your custom detector integrates with the ecosystem at different levels:

### A. Local Development
```bash
# Developer runs pre-commit hook
python .github/agents/access-control-detector.py ./
```

### B. GitHub Actions Workflow
```yaml
- name: Run Custom Security Detector
  run: python .github/agents/access-control-detector.py ./
  continue-on-error: false  # Fail if findings
  
- name: Report Findings
  if: failure()
  run: |
    # Parse JSON output
    # Create GitHub issues
    # Annotation on PR
```

### C. Data Passing Between Tools
```bash
# GHAS finds: SQL injection
# Custom tool finds: Insecure comparison
# GitHub Actions: Combines into single security report

findings=$(python access-control-detector.py .)
echo "$findings" > /tmp/custom-security-report.json

# Pass to next step
echo "FINDINGS=$findings" >> $GITHUB_ENV
```

---

## ✅ Key Differences: Custom Tools vs GHAS

| Aspect | GHAS | Custom Tool |
|--------|------|------------|
| **Setup** | Enabled in settings | Write Python script + add to Actions |
| **Rules** | Fixed by GitHub | You define patterns |
| **Updates** | GitHub maintains | You maintain |
| **Speed** | Fast (native) | Slower (scripted) |
| **Accuracy** | High (proven) | In your control |
| **Use when** | Standard vulns | Domain-specific risks |

---

## 🔗 Honest Truth

**This is NOT an "Agent Framework"**

What you built:
- ✅ Python script that scans code
- ✅ Regex/logic-based pattern matching
- ✅ JSON output for integration
- ✅ Exit code for CI/CD decisions

What it's NOT:
- ❌ No LLM reasoning
- ❌ No autonomous decision-making
- ❌ No "agent" orchestration
- ❌ No external API calls
- ❌ No learning/adaptation

**It's a PURPOSE-BUILT SECURITY SCANNER.**

You use this when:
- ❌ GitHub GHAS can't detect it
- ❌ You need business logic validation
- ❌ You need compliance checking

The "agent" part comes later when you chain this with Copilot CLI (interactive) + GitHub Actions (orchestration).

---

## 🎁 Bonus: Add Severity Scoring

Enhance findings with business impact:

```python
def calculate_severity(finding):
    """Map technical risk to business impact"""
    if 'password' in finding['code'].lower():
        return {
            'severity': 'CRITICAL',
            'businessImpact': 'User account takeover',
            'exploitDifficulty': 'EASY',
            'firstResponderAction': 'Block PR until fixed'
        }
    elif 'admin' in finding['code'].lower():
        return {
            'severity': 'CRITICAL', 
            'businessImpact': 'Privilege escalation',
            'exploitDifficulty': 'EASY',
            'firstResponderAction': 'Block release until fixed'
        }
```

---

## ✅ Acceptance Criteria

- [ ] Created `access-control-detector.py` script
- [ ] Script successfully scans directory
- [ ] Detects insecure `==` patterns
- [ ] Outputs valid JSON
- [ ] Exit code 1 when findings found, 0 when clean
- [ ] Ran against SecureTrails and found vulnerabilities
- [ ] Understand when to build custom tools
- [ ] Understand this is NOT a magic framework

---

## 🚀 Next Steps

**Exercise 4**: GitHub Actions Integration
- Automate running GHAS + custom detector + Copilot analysis
- Chain together finding → report → issue → PR block

**Exercise 5**: Real-World Ecosystem
- Deploy all components
- See them working together

---

## 📚 Reference

- [RegEx Patterns for Security](https://owasp.org/www-community/Regular_expression_Denial_of_Service_-_ReDoS)
- [Python Security Best Practices](https://python.readthedocs.io/en/latest/library/hmac.html)
- [GitHub Actions: Custom Actions](https://docs.github.com/en/actions/creating-actions/about-custom-actions)

---

**⏱️ Time**: 20 min | **Exercises**: 3/5 ✓

---

## 💡 Real-World Patterns You Can Extend

Copy and modify this for YOUR security concerns:

```python
# API contract violations
r'requests\.get\(.*\)\.json\(\)'  # No timeout

# Configuration issues  
r'DEBUG\s*=\s*True'  # Debug mode enabled
r'SECRET_KEY\s*=\s*["\']secret["\']\s*'  # Hardcoded key

# Logging secrets
r'print.*password'  # Password in logs
r'logger.*token'  # Token in logs

# Missing security headers
r'return.*response'  # Missing HSTS
```

This is how professional security tools are built.
