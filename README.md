# Security Pipeline Demo

CI/CD pipeline with comprehensive security scanning using SonarQube, Bandit, Trivy, and OSV Scanner.

## Security Scanners

| Scanner | Purpose | What it Scans |
|---------|---------|---------------|
| **Bandit** | Python security linter | Hardcoded secrets, SQL injection, command injection, weak crypto |
| **Trivy** | Vulnerability scanner | Dependencies, filesystem, misconfigurations |
| **OSV Scanner** | Open Source Vulnerabilities | Known CVEs in dependencies via OSV database |
| **SonarQube** | Code quality & security | Code smells, bugs, vulnerabilities, coverage |

## Setup

### Prerequisites

- Python 3.12+
- GitHub repository with Actions enabled
- (Optional) SonarQube server or SonarCloud account

### Local Development

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run tests
pytest tests/ -v --cov=src

# Run Bandit locally
bandit -r src/ -f txt
```

### GitHub Secrets Required

For SonarQube integration, add these secrets to your repository:

| Secret | Description |
|--------|-------------|
| `SONAR_TOKEN` | SonarQube authentication token |
| `SONAR_HOST_URL` | SonarQube server URL (e.g., `https://sonarcloud.io`) |

**To add secrets:**
1. Go to Repository → Settings → Secrets and variables → Actions
2. Click "New repository secret"
3. Add each secret

## Pipeline Triggers

The security pipeline runs on:
- Push to `main` branch
- Pull requests to `main` branch

## Pipeline Jobs

```
┌─────────────┐
│    test     │ ← Run pytest with coverage
└──────┬──────┘
       │
       ▼
┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐
│   bandit    │  │    trivy    │  │ osv-scanner │  │  sonarqube  │
└──────┬──────┘  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘
       │                │                │                │
       └────────────────┴────────────────┴────────────────┘
                                │
                                ▼
                       ┌─────────────────┐
                       │ security-summary│
                       └─────────────────┘
```

## Reports

After each run, artifacts are available:
- `coverage-report` - HTML and XML coverage reports
- `bandit-report` - JSON and text security findings
- `trivy-report` - JSON and SARIF vulnerability reports
- `osv-report` - JSON dependency vulnerabilities

## Sample Code

The `src/app.py` contains intentional security issues for testing:
- SQL injection vulnerability
- Weak hashing (MD5)
- Command injection
- Hardcoded credentials

These demonstrate how each scanner detects different vulnerability types.

## Customization

### Adjust Severity Levels

In `.github/workflows/security-scan.yml`:

```yaml
# Trivy - change severity threshold
severity: 'CRITICAL,HIGH,MEDIUM'

# Bandit - change confidence/severity
bandit -r src/ -ll -ii  # -ll = low severity, -ii = low confidence
```

### Add More Scanners

Additional scanners to consider:
- **Safety** - Python dependency checker
- **Semgrep** - Multi-language static analysis
- **Snyk** - Dependency and container scanning
- **CodeQL** - GitHub's semantic code analysis

## Project Structure

```
security-pipeline/
├── .github/
│   └── workflows/
│       └── security-scan.yml    # CI pipeline
├── src/
│   ├── __init__.py
│   └── app.py                   # Sample application
├── tests/
│   ├── __init__.py
│   └── test_app.py              # Unit tests
├── .gitignore
├── README.md
├── requirements.txt
└── sonar-project.properties     # SonarQube config
```
