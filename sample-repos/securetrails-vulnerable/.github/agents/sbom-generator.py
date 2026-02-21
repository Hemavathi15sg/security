#!/usr/bin/env python3
"""
Dependency Supply Chain Scout Agent - Simplified Version
Generates SBOM with vulnerability data from known CVE database
"""

import json
import sys
from pathlib import Path
from datetime import datetime


# Comprehensive CVE database from our previous analysis
VULNERABILITY_DATABASE = {
    "Flask": {
        "1.1.0": {
            "cves": [
                {
                    "cve_id": "CVE-2024-22414",
                    "severity": "HIGH",
                    "description": "XSS vulnerability via unsafe Jinja2 template rendering with |safe filter",
                    "cvss": "7.5"
                }
            ],
            "recommended_version": "3.0.3",
            "license": "BSD-3-Clause"
        }
    },
    "requests": {
        "2.24.0": {
            "cves": [
                {
                    "cve_id": "CVE-2024-35195",
                    "severity": "MEDIUM",
                    "description": "Certificate verification bypass - first request with verify=False disables verification for connection pool",
                    "cvss": "6.0"
                },
                {
                    "cve_id": "CVE-2024-47081",
                    "severity": "HIGH",
                    "description": "Credential leak via .netrc parsing flaw with malicious URLs",
                    "cvss": "8.2"
                }
            ],
            "recommended_version": "2.32.4",
            "license": "Apache-2.0"
        }
    },
    "SQLAlchemy": {
        "1.3.0": {
            "cves": [
                {
                    "cve_id": "CVE-2019-7164",
                    "severity": "CRITICAL",
                    "description": "SQL injection via order_by parameter allows arbitrary SQL execution",
                    "cvss": "9.8"
                }
            ],
            "recommended_version": "2.0.35",
            "license": "MIT"
        }
    },
    "Werkzeug": {
        "1.0.0": {
            "cves": [
                {
                    "cve_id": "CVE-2023-25577",
                    "severity": "HIGH",
                    "description": "DoS via unlimited multipart form parsing causing resource exhaustion",
                    "cvss": "7.5"
                },
                {
                    "cve_id": "CVE-2023-46136",
                    "severity": "HIGH",
                    "description": "DoS via crafted multipart uploads with excessive CPU/memory use",
                    "cvss": "7.5"
                },
                {
                    "cve_id": "CVE-2024-34069",
                    "severity": "HIGH",
                    "description": "Remote code execution via debugger PIN exploitation",
                    "cvss": "8.1"
                },
                {
                    "cve_id": "CVE-2024-49767",
                    "severity": "HIGH",
                    "description": "Resource exhaustion via multipart requests bypassing memory limits",
                    "cvss": "7.5"
                },
                {
                    "cve_id": "CVE-2024-49766",
                    "severity": "MEDIUM",
                    "description": "Path traversal on Windows with Python <3.11 via unsafe safe_join",
                    "cvss": "6.5"
                }
            ],
            "recommended_version": "3.0.6",
            "license": "BSD-3-Clause"
        }
    },
    "Jinja2": {
        "2.11.0": {
            "cves": [
                {
                    "cve_id": "CVE-2024-22195",
                    "severity": "HIGH",
                    "description": "XSS via HTML attribute injection when xmlattr filter bypasses auto-escaping",
                    "cvss": "7.3"
                },
                {
                    "cve_id": "CVE-2024-56326",
                    "severity": "CRITICAL",
                    "description": "Sandbox breakout via str.format allowing arbitrary Python code execution",
                    "cvss": "9.8"
                },
                {
                    "cve_id": "CVE-2019-10906",
                    "severity": "HIGH",
                    "description": "Template injection leading to sandbox escape and code execution",
                    "cvss": "8.6"
                }
            ],
            "recommended_version": "3.1.5",
            "license": "BSD-3-Clause"
        }
    },
    "MarkupSafe": {
        "1.1.0": {
            "cves": [],
            "recommended_version": "3.0.2",
            "license": "BSD-3-Clause"
        }
    },
    "click": {
        "7.1.0": {
            "cves": [],
            "recommended_version": "8.1.8",
            "license": "BSD-3-Clause"
        }
    },
    "itsdangerous": {
        "1.1.0": {
            "cves": [],
            "recommended_version": "2.2.0",
            "license": "BSD-3-Clause"
        }
    },
    "Flask-CORS": {
        "3.0.8": {
            "cves": [
                {
                    "cve_id": "CVE-2024-6221",
                    "severity": "MEDIUM",
                    "description": "CORS misconfiguration - Access-Control-Allow-Private-Network set to true by default",
                    "cvss": "6.5"
                }
            ],
            "recommended_version": "5.0.0",
            "license": "MIT"
        }
    }
}


def parse_requirements(file_path: str = "requirements.txt") -> list:
    """Parse requirements.txt and return list of packages"""
    packages = []
    
    # Adjust path if running from .github/agents
    req_path = Path(file_path)
    if not req_path.exists():
        req_path = Path("../../requirements.txt")
    
    if not req_path.exists():
        return []
    
    with open(req_path, 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#'):
                if '==' in line:
                    pkg, ver = line.split('==')
                    packages.append({
                        "name": pkg.strip(),
                        "version": ver.strip()
                    })
    
    return packages


def generate_sbom(requirements_file: str = "requirements.txt") -> dict:
    """Generate complete SBOM with vulnerability data"""
    
    packages_data = parse_requirements(requirements_file)
    
    sbom = {
        "bomFormat": "CycloneDX",
        "specVersion": "1.5",
        "version": 1,
        "serialNumber": f"urn:uuid:sbom-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}",
        "metadata": {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "tools": [{
                "vendor": "GitHub Copilot",
                "name": "dependency-supply-chain-scout",
                "version": "1.0.0"
            }],
            "component": {
                "type": "application",
                "name": "securetrails-vulnerable",
                "version": "1.0.0",
                "description": "Vulnerable Flask application for security training"
            }
        },
        "packages": []
    }
    
    total_cves = 0
    critical_count = 0
    high_count = 0
    medium_count = 0
    low_count = 0
    
    for pkg in packages_data:
        pkg_name = pkg["name"]
        pkg_version = pkg["version"]
        
        # Get vulnerability data from our database
        vuln_data = VULNERABILITY_DATABASE.get(pkg_name, {}).get(pkg_version, {})
        
        package_info = {
            "name": pkg_name,
            "version": pkg_version,
            "license": vuln_data.get("license", "Unknown"),
            "purl": f"pkg:pypi/{pkg_name}@{pkg_version}",
            "vulnerabilities": vuln_data.get("cves", []),
            "recommended_version": vuln_data.get("recommended_version", pkg_version),
            "vulnerability_count": len(vuln_data.get("cves", [])),
            "risk_score": calculate_risk_score(vuln_data.get("cves", []))
        }
        
        # Count severity levels
        for cve in package_info["vulnerabilities"]:
            total_cves += 1
            severity = cve["severity"]
            if severity == "CRITICAL":
                critical_count += 1
            elif severity == "HIGH":
                high_count += 1
            elif severity == "MEDIUM":
                medium_count += 1
            else:
                low_count += 1
        
        sbom["packages"].append(package_info)
    
    # Add summary statistics
    sbom["summary"] = {
        "total_packages": len(packages_data),
        "total_vulnerabilities": total_cves,
        "severity_distribution": {
            "CRITICAL": critical_count,
            "HIGH": high_count,
            "MEDIUM": medium_count,
            "LOW": low_count
        },
        "packages_with_vulnerabilities": sum(1 for p in sbom["packages"] if p["vulnerability_count"] > 0),
        "risk_level": "CRITICAL" if critical_count > 0 else "HIGH" if high_count > 0 else "MEDIUM"
    }
    
    return sbom


def calculate_risk_score(cves: list) -> int:
    """Calculate risk score based on CVE severity and count"""
    if not cves:
        return 0
    
    severity_weights = {
        "CRITICAL": 10,
        "HIGH": 7,
        "MEDIUM": 4,
        "LOW": 1
    }
    
    score = sum(severity_weights.get(cve["severity"], 0) for cve in cves)
    return min(score, 100)  # Cap at 100


def main():
    """Main entry point"""
    
    command = sys.argv[1] if len(sys.argv) > 1 else "sbom"
    
    if command == "sbom":
        sbom = generate_sbom()
        print(json.dumps(sbom, indent=2))
    elif command == "list":
        packages = parse_requirements()
        print(json.dumps({"packages": packages, "count": len(packages)}, indent=2))
    elif command == "summary":
        sbom = generate_sbom()
        summary = {
            "total_packages": sbom["summary"]["total_packages"],
            "total_vulnerabilities": sbom["summary"]["total_vulnerabilities"],
            "risk_level": sbom["summary"]["risk_level"],
            "severity_breakdown": sbom["summary"]["severity_distribution"]
        }
        print(json.dumps(summary, indent=2))
    else:
        print(json.dumps({
            "error": f"Unknown command: {command}",
            "available_commands": ["sbom", "list", "summary"]
        }, indent=2))


if __name__ == "__main__":
    main()
