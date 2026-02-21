# Custom Security Agents - Documentation

This directory contains custom GitHub Copilot agents for security analysis and remediation.

## Available Agents

### 1. 🔍 SBOM Generator (`sbom-generator.py`)
**Purpose**: Generate Software Bill of Materials with vulnerability analysis

**Features**:
- Parses requirements.txt
- Generates CycloneDX 1.5 format SBOM
- Includes CVE data for all packages
- Provides severity ratings and risk scores
- Includes recommended update versions

**Usage**:
```bash
# Generate complete SBOM with vulnerabilities
python .github/agents/sbom-generator.py sbom

# Get summary only
python .github/agents/sbom-generator.py summary

# List packages
python .github/agents/sbom-generator.py list
```

**Output**: `sbom-report.json` with detailed vulnerability information

---

### 2. 🛡️ Remediation Proposer (`remediation-proposer.py`)
**Purpose**: Propose security remediation updates based on SBOM analysis

**Features**:
- Loads SBOM report
- Generates secure requirements.txt
- Creates detailed change summary
- Identifies breaking changes
- Provides risk assessment

**Usage**:
```bash
# Generate remediation proposal from SBOM
python .github/agents/remediation-proposer.py sbom-report.json

# With custom SBOM file
python .github/agents/remediation-proposer.py path/to/sbom.json
```

**Output**: JSON with:
- `requirements_secure`: Updated dependency versions
- `summary`: CVEs fixed, risk reduction
- `packages`: Detailed change list per package

---

### 3. 🔎 Dependency Scout (`dependency-scout.py`)
**Purpose**: Scan dependencies using OSV API for real-time vulnerability data

**Features**:
- Scans Python dependencies
- Queries OSV vulnerability database
- Generates SBOM
- Checks live vulnerability data
- Provides detailed security reports

**Usage**:
```bash
# Full scan with vulnerability checking
python .github/agents/dependency-scout.py scan

# Generate SBOM only
python .github/agents/dependency-scout.py sbom

# List dependencies
python .github/agents/dependency-scout.py list
```

**Requirements**: `pip install requests`

---

## Complete Workflow

### Step 1: Generate SBOM
```bash
python .github/agents/sbom-generator.py sbom > sbom-report.json
```

### Step 2: Review Vulnerabilities
```bash
python .github/agents/sbom-generator.py summary
```

### Step 3: Generate Remediation
```bash
python .github/agents/remediation-proposer.py sbom-report.json > remediation.json
```

### Step 4: Extract Secure Requirements
```bash
python .github/agents/remediation-proposer.py sbom-report.json | jq -r '.requirements_secure' > requirements-secure.txt
```

### Step 5: Apply Updates
```bash
pip install -r requirements-secure.txt
```

---

## Integration Examples

### GitHub Actions Workflow

```yaml
name: Security Scan
on: [push, pull_request]

jobs:
  security-scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.12'
      
      - name: Generate SBOM
        run: python .github/agents/sbom-generator.py sbom > sbom-report.json
      
      - name: Upload SBOM
        uses: actions/upload-artifact@v4
        with:
          name: sbom
          path: sbom-report.json
      
      - name: Check for Critical CVEs
        run: |
          CRITICAL=$(python .github/agents/sbom-generator.py summary | jq '.severity_distribution.CRITICAL')
          if [ "$CRITICAL" -gt 0 ]; then
            echo "❌ Found $CRITICAL critical vulnerabilities"
            exit 1
          fi
```

### Pre-commit Hook

```bash
#!/bin/bash
# .git/hooks/pre-commit

echo "🔍 Scanning dependencies for vulnerabilities..."
python .github/agents/sbom-generator.py summary

CRITICAL=$(python .github/agents/sbom-generator.py summary | jq -r '.severity_distribution.CRITICAL')

if [ "$CRITICAL" -gt 0 ]; then
    echo "❌ Cannot commit: $CRITICAL critical vulnerabilities found"
    echo "Run: python .github/agents/remediation-proposer.py"
    exit 1
fi

echo "✅ No critical vulnerabilities detected"
```

---

## Agent Registry

| Agent | Command | Input | Output |
|-------|---------|-------|--------|
| sbom-generator | `sbom` | requirements.txt | sbom-report.json |
| sbom-generator | `summary` | requirements.txt | JSON summary |
| remediation-proposer | (default) | sbom-report.json | Remediation JSON |
| dependency-scout | `scan` | requirements.txt | Vulnerability report |

---

## CVE Database

All agents use a comprehensive CVE database including:
- **Critical**: CVE-2019-7164 (SQLAlchemy), CVE-2024-56326 (Jinja2)
- **High**: 8 CVEs across Flask, Werkzeug, requests, Jinja2
- **Medium**: 3 CVEs in Werkzeug, Flask-CORS, requests

Database last updated: 2026-02-21

---

## Notes

- Agents do NOT require external dependencies by default (except dependency-scout)
- All vulnerability data is embedded for offline use
- SBOM format: CycloneDX 1.5 (industry standard)
- Compatible with security scanning tools like Grype, Trivy, etc.

---

**Created by**: GitHub Copilot Security Workshop  
**Version**: 1.0.0  
**Last Updated**: 2026-02-21
