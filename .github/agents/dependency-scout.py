#!/usr/bin/env python3
"""
Dependency Supply Chain Scout Agent
Analyzes dependencies for Known CVEs
"""

import json
import sys
from pathlib import Path

class DependencyScout:
    """Agent for scanning dependencies"""
    
    # Known vulnerable packages (for demonstration)
    KNOWN_VULNS = {
        'Flask': {
            '1.1.0': [
                {'id': 'CVE-2021-21342', 'severity': 'CRITICAL', 'description': 'Werkzeug RCE'},
                {'id': 'CVE-2021-21409', 'severity': 'HIGH', 'description': 'Development reloader RCE'},
            ],
            'latest': '2.3.2'
        },
        'requests': {
            '2.24.0': [
                {'id': 'CVE-2021-33503', 'severity': 'MEDIUM', 'description': 'URL parsing issue'},
            ],
            'latest': '2.28.1'
        },
        'SQLAlchemy': {
            '1.3.0': [
                {'id': 'CVE-2021-XXXXX', 'severity': 'HIGH', 'description': 'SQL injection vectors'},
            ],
            'latest': '2.0.8'
        },
    }
    
    def __init__(self):
        self.sbom = {'packages': [], 'summary': {}}
    
    def parse_requirements(self):
        """Parse requirements.txt"""
        req_file = Path('requirements.txt')
        packages = []
        
        if req_file.exists():
            for line in req_file.read_text().split('\n'):
                line = line.strip()
                if line and not line.startswith('#'):
                    parts = line.split('==')
                    if len(parts) == 2:
                        packages.append({'name': parts[0], 'version': parts[1]})
        
        return packages
    
    def check_vulnerabilities(self, packages):
        """Check each package for known vulnerabilities"""
        for pkg in packages:
            name = pkg['name']
            version = pkg['version']
            
            vulns = []
            if name in self.KNOWN_VULNS:
                if version in self.KNOWN_VULNS[name]:
                    vulns = self.KNOWN_VULNS[name][version]
            
            self.sbom['packages'].append({
                'name': name,
                'version': version,
                'vulnerabilities': vulns,
                'recommended_version': self.KNOWN_VULNS.get(name, {}).get('latest', version),
            })
    
    def generate_sbom(self):
        """Generate Software Bill of Materials"""
        packages = self.parse_requirements()
        self.check_vulnerabilities(packages)
        
        critical = sum(1 for p in self.sbom['packages'] 
                      for v in p.get('vulnerabilities', []) 
                      if v.get('severity') == 'CRITICAL')
        
        self.sbom['summary'] = {
            'total_packages': len(packages),
            'with_vulnerabilities': sum(1 for p in self.sbom['packages'] 
                                       if p.get('vulnerabilities')),
            'critical': critical,
        }
        
        return self.sbom

if __name__ == '__main__':
    scout = DependencyScout()
    sbom = scout.generate_sbom()
    print(json.dumps(sbom, indent=2))
    sys.exit(0)
