#!/usr/bin/env python3
"""
Baseline Security Checker Agent
SAST (Static Application Security Testing) agent for SecureTrails
"""

import sys
import json
import re
from pathlib import Path

class SecurityPattern:
    """Define security vulnerability patterns"""
    
    PATTERNS = {
        'SQL_INJECTION': [
            r'f["\']SELECT.*WHERE.*{',  # F-string SQL
            r'query.*format\(',  # Format-based SQL
            r'\.execute\(.*\+.*\)',  # String concatenation
        ],
        'XSS_VULNERABLE': [
            r'innerHTML\s*=',  # Unsafe innerHTML
            r'\.html\(',  # Jinja2 without escape
            r'eval\(',  # eval usage
        ],
        'HARDCODED_SECRETS': [
            r'(API_KEY|PASSWORD|TOKEN|SECRET)\s*=\s*["\'][^"\']',
            r'(JWT_SECRET|PRIVATE_KEY)\s*=',
        ],
        'WEAK_CRYPTO': [
            r'md5\(',
            r'sha1\(',
            r'hashlib\.md5',
        ],
    }

    @classmethod
    def find_violations(cls, content, file_ext):
        """Find security violations in code"""
        violations = []
        
        for vuln_type, patterns in cls.PATTERNS.items():
            for pattern in patterns:
                for match in re.finditer(pattern, content, re.IGNORECASE):
                    line_num = content[:match.start()].count('\n') + 1
                    violations.append({
                        'type': vuln_type,
                        'line': line_num,
                        'match': match.group()[:50],
                    })
        
        return violations

class BaselineChecker:
    """Main agent for baseline security checking"""
    
    def __init__(self, repo_path):
        self.repo_path = Path(repo_path)
        self.violations = []
    
    def scan_files(self):
        """Scan all code files for vulnerabilities"""
        for file_path in self.repo_path.rglob('*'):
            if file_path.is_file() and file_path.suffix in ['.py', '.js', '.html']:
                if 'venv' not in str(file_path) and '.git' not in str(file_path):
                    self._scan_file(file_path)
    
    def _scan_file(self, file_path):
        """Scan individual file"""
        try:
            with open(file_path, 'r') as f:
                content = f.read()
            
            violations = SecurityPattern.find_violations(content, file_path.suffix)
            
            for v in violations:
                self.violations.append({
                    'file': str(file_path.relative_to(self.repo_path)),
                    'line': v['line'],
                    'severity': self._get_severity(v['type']),
                    'type': v['type'],
                    'description': self._get_description(v['type']),
                })
        except Exception as e:
            pass
    
    def _get_severity(self, vuln_type):
        critical = ['SQL_INJECTION', 'HARDCODED_SECRETS']
        return 'CRITICAL' if vuln_type in critical else 'HIGH'
    
    def _get_description(self, vuln_type):
        descriptions = {
            'SQL_INJECTION': 'User input in SQL query - potential SQL injection',
            'XSS_VULNERABLE': 'Unescaped HTML rendering - potential XSS',
            'HARDCODED_SECRETS': 'Hardcoded credentials in source code',
            'WEAK_CRYPTO': 'Weak cryptographic function usage',
        }
        return descriptions.get(vuln_type, 'Security vulnerability detected')
    
    def generate_report(self):
        """Generate JSON report"""
        return {
            'violations': self.violations,
            'summary': {
                'total': len(self.violations),
                'critical': sum(1 for v in self.violations if v['severity'] == 'CRITICAL'),
                'high': sum(1 for v in self.violations if v['severity'] == 'HIGH'),
            }
        }

if __name__ == '__main__':
    checker = BaselineChecker('.')
    checker.scan_files()
    report = checker.generate_report()
    print(json.dumps(report, indent=2))
    sys.exit(0)
