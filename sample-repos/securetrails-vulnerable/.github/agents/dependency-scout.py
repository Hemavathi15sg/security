#!/usr/bin/env python3
"""
Dependency Supply Chain Scout Agent
Scans dependencies for known vulnerabilities and generates SBOM (Software Bill of Materials)
"""

import json
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Optional
import requests
from datetime import datetime


class DependencyScout:
    """Agent for scanning dependencies and generating security reports"""
    
    def __init__(self):
        self.name = "dependency-supply-chain-scout"
        self.version = "1.0.0"
        self.description = "Scans dependencies for known vulnerabilities and generates SBOM"
        
    def scan_python_dependencies(self, requirements_file: str = "requirements.txt") -> Dict:
        """Scan Python requirements.txt for vulnerabilities"""
        
        if not Path(requirements_file).exists():
            return {"error": f"{requirements_file} not found"}
        
        dependencies = []
        with open(requirements_file, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    if '==' in line:
                        pkg, ver = line.split('==')
                        dependencies.append({
                            "package": pkg.strip(),
                            "version": ver.strip(),
                            "ecosystem": "PyPI"
                        })
        
        return {
            "dependencies": dependencies,
            "total": len(dependencies),
            "file": requirements_file
        }
    
    def check_vulnerabilities(self, package: str, version: str, ecosystem: str = "PyPI") -> List[Dict]:
        """Check for known vulnerabilities using OSV API"""
        
        osv_url = "https://api.osv.dev/v1/query"
        
        payload = {
            "version": version,
            "package": {
                "name": package,
                "ecosystem": ecosystem
            }
        }
        
        try:
            response = requests.post(osv_url, json=payload, timeout=10)
            if response.status_code == 200:
                data = response.json()
                return data.get("vulns", [])
            return []
        except Exception as e:
            return [{"error": str(e)}]
    
    def generate_sbom(self, requirements_file: str = "requirements.txt") -> Dict:
        """Generate Software Bill of Materials (SBOM) in CycloneDX format"""
        
        scan_result = self.scan_python_dependencies(requirements_file)
        
        if "error" in scan_result:
            return scan_result
        
        sbom = {
            "bomFormat": "CycloneDX",
            "specVersion": "1.5",
            "version": 1,
            "metadata": {
                "timestamp": datetime.utcnow().isoformat() + "Z",
                "tools": [{
                    "vendor": "GitHub Copilot",
                    "name": self.name,
                    "version": self.version
                }],
                "component": {
                    "type": "application",
                    "name": "securetrails-vulnerable",
                    "version": "1.0.0"
                }
            },
            "components": []
        }
        
        for dep in scan_result["dependencies"]:
            component = {
                "type": "library",
                "name": dep["package"],
                "version": dep["version"],
                "purl": f"pkg:pypi/{dep['package']}@{dep['version']}"
            }
            sbom["components"].append(component)
        
        return sbom
    
    def scan_and_report(self, requirements_file: str = "requirements.txt", 
                       check_vulns: bool = True) -> Dict:
        """Complete scan with vulnerability checking"""
        
        scan_result = self.scan_python_dependencies(requirements_file)
        
        if "error" in scan_result:
            return scan_result
        
        report = {
            "scan_timestamp": datetime.utcnow().isoformat() + "Z",
            "agent": self.name,
            "dependencies_scanned": scan_result["total"],
            "vulnerabilities": [],
            "dependencies": []
        }
        
        for dep in scan_result["dependencies"]:
            dep_info = {
                "package": dep["package"],
                "version": dep["version"],
                "ecosystem": dep["ecosystem"],
                "vulnerabilities": []
            }
            
            if check_vulns:
                vulns = self.check_vulnerabilities(
                    dep["package"], 
                    dep["version"], 
                    dep["ecosystem"]
                )
                
                for vuln in vulns:
                    if "error" not in vuln:
                        vuln_summary = {
                            "id": vuln.get("id", "Unknown"),
                            "summary": vuln.get("summary", "No summary available"),
                            "severity": self._extract_severity(vuln),
                            "fixed_versions": self._extract_fixed_versions(vuln)
                        }
                        dep_info["vulnerabilities"].append(vuln_summary)
                        report["vulnerabilities"].append({
                            "package": dep["package"],
                            "version": dep["version"],
                            **vuln_summary
                        })
            
            report["dependencies"].append(dep_info)
        
        report["total_vulnerabilities"] = len(report["vulnerabilities"])
        report["critical_count"] = sum(1 for v in report["vulnerabilities"] 
                                      if v.get("severity", "").upper() == "CRITICAL")
        report["high_count"] = sum(1 for v in report["vulnerabilities"] 
                                  if v.get("severity", "").upper() == "HIGH")
        
        return report
    
    def _extract_severity(self, vuln: Dict) -> str:
        """Extract severity from vulnerability data"""
        if "severity" in vuln:
            if isinstance(vuln["severity"], list) and len(vuln["severity"]) > 0:
                return vuln["severity"][0].get("type", "UNKNOWN")
        return "UNKNOWN"
    
    def _extract_fixed_versions(self, vuln: Dict) -> List[str]:
        """Extract fixed versions from vulnerability data"""
        fixed = []
        if "affected" in vuln:
            for affected in vuln["affected"]:
                if "ranges" in affected:
                    for r in affected["ranges"]:
                        if "events" in r:
                            for event in r["events"]:
                                if "fixed" in event:
                                    fixed.append(event["fixed"])
        return fixed
    
    def run(self, command: str = "scan", **kwargs) -> Dict:
        """Main entry point for the agent"""
        
        if command == "scan":
            return self.scan_and_report(**kwargs)
        elif command == "sbom":
            return self.generate_sbom(**kwargs)
        elif command == "list":
            return self.scan_python_dependencies(**kwargs)
        else:
            return {
                "error": f"Unknown command: {command}",
                "available_commands": ["scan", "sbom", "list"]
            }


def main():
    """CLI entry point"""
    agent = DependencyScout()
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        result = agent.run(command)
    else:
        result = agent.run("scan")
    
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
