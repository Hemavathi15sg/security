#!/usr/bin/env python3
"""
Secret Detector Enforcer Agent
Detects and reports exposed credentials
"""

import re
import json
import sys
from pathlib import Path

class SecretDetector:
    """Detect exposed secrets in code"""
    
    PATTERNS = {
        'API_KEY': r'API_KEY\s*=?\s*["\']([a-zA-Z0-9_\-]{20,})["\']',
        'AWS_KEY': r'AKIA[0-9A-Z]{16}',
        'GITHUB_TOKEN': r'ghp_[0-9a-zA-Z]{36}',
        'DATABASE_PASSWORD': r'postgres://[^:]+:([^@]+)@',
        'JWT_SECRET': r'JWT_SECRET\s*=\s*["\']([^"\']{10,})["\']',
        'PRIVATE_KEY': r'-----BEGIN.*PRIVATE KEY-----',
    }
    
    def __init__(self):
        self.secrets = []
    
    def scan_directory(self, path='.'):
        """Scan all files for secrets"""
        for file_path in Path(path).rglob('*'):
            if file_path.is_file() and self._should_scan(file_path):
                self._scan_file(file_path)
    
    def _should_scan(self, file_path):
        """Determine if file should be scanned"""
        excluded = {'venv', '.git', '__pycache__', 'node_modules'}
        if any(excluded_dir in file_path.parts for excluded_dir in excluded):
            return False
        
        extensions = {'.py', '.js', '.html', '.env', '.txt', '.md'}
        return file_path.suffix in extensions
    
    def _scan_file(self, file_path):
        """Scan a single file"""
        try:
            content = file_path.read_text(errors='ignore')
            
            for secret_type, pattern in self.PATTERNS.items():
                for match in re.finditer(pattern, content):
                    line_num = content[:match.start()].count('\n') + 1
                    self.secrets.append({
                        'file': str(file_path),
                        'line': line_num,
                        'type': secret_type,
                        'severity': 'CRITICAL',
                    })
        except Exception:
            pass
    
    def generate_report(self):
        """Generate detection report"""
        return {
            'secrets_found': len(self.secrets),
            'details': self.secrets,
            'status': 'BLOCK_COMMIT' if self.secrets else 'ALLOW'
        }

if __name__ == '__main__':
    detector = SecretDetector()
    detector.scan_directory()
    report = detector.generate_report()
    print(json.dumps(report, indent=2))
    
    if report['secrets_found'] > 0:
        sys.exit(1)  # Block commit
    sys.exit(0)
