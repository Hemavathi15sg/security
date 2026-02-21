#!/usr/bin/env python3
"""
Remediation Proposer Agent
Analyzes SBOM and generates secure dependency updates with detailed remediation plans
"""

import json
import sys
from pathlib import Path
from datetime import datetime


class RemediationProposer:
    """Agent for proposing security remediations based on SBOM analysis"""
    
    def __init__(self):
        self.name = "remediation-proposer"
        self.version = "1.0.0"
        self.description = "Generates secure dependency updates and remediation plans"
    
    def load_sbom(self, sbom_file: str = "sbom-report.json") -> dict:
        """Load SBOM from file"""
        sbom_path = Path(sbom_file)
        
        if not sbom_path.exists():
            # Try alternate locations
            for alt_path in ["sbom.json", "../sbom-report.json", "../../sbom-report.json"]:
                if Path(alt_path).exists():
                    sbom_path = Path(alt_path)
                    break
        
        if not sbom_path.exists():
            return {"error": f"SBOM file not found: {sbom_file}"}
        
        with open(sbom_path, 'r') as f:
            return json.load(f)
    
    def generate_secure_requirements(self, sbom: dict) -> str:
        """Generate requirements.txt with secure versions"""
        
        if "error" in sbom:
            return sbom["error"]
        
        packages = sbom.get("packages", [])
        
        requirements = []
        for pkg in packages:
            name = pkg.get("name")
            recommended = pkg.get("recommended_version")
            if name and recommended:
                requirements.append(f"{name}=={recommended}")
        
        return "\n".join(requirements) + "\n"
    
    def propose_remediation(self, sbom_file: str = "sbom-report.json") -> dict:
        """Main method to generate complete remediation proposal"""
        
        sbom = self.load_sbom(sbom_file)
        
        if "error" in sbom:
            return sbom
        
        packages = sbom.get("packages", [])
        summary = sbom.get("summary", {})
        
        # Generate outputs
        requirements = self.generate_secure_requirements(sbom)
        
        return {
            "requirements_secure": requirements,
            "summary": {
                "total_packages_updated": len(packages),
                "total_cves_fixed": summary.get("total_vulnerabilities", 0),
                "risk_before": summary.get("risk_level", "UNKNOWN"),
                "risk_after": "LOW"
            },
            "packages": [
                {
                    "name": pkg["name"],
                    "old_version": pkg["version"],
                    "new_version": pkg["recommended_version"],
                    "cves_fixed": len(pkg.get("vulnerabilities", []))
                }
                for pkg in packages
            ],
            "status": "success"
        }


def main():
    """CLI entry point"""
    agent = RemediationProposer()
    
    # Check if reading from stdin or command line
    if not sys.stdin.isatty():
        data = json.loads(sys.stdin.read())
        sbom_file = data.get("sbom_file", "sbom-report.json")
    else:
        sbom_file = sys.argv[1] if len(sys.argv) > 1 else "sbom-report.json"
    
    remediation = agent.propose_remediation(sbom_file)
    print(json.dumps(remediation, indent=2))


if __name__ == "__main__":
    main()
