# SecureTrails - Workshop Sample Application

This is an intentionally vulnerable application designed for security training.

## Setup

```bash
python database.py
python app.py
```

## Vulnerabilities (Intentional for Training)

This application contains 7 primary vulnerabilities:

1. **SQL Injection** - User input in SQL queries
2. **XSS** - Unescaped HTML rendering
3. **Hardcoded Secrets** - JWT and API keys in code
4. **Weak Cryptography** - MD5 password hashing
5. **Broken Authentication** - Missing session validation
6. **IDOR** - Direct object references without authorization
7. **Security Misconfiguration** - Debug mode, CORS *, exposed credentials

Use with Copilot agents to discover and fix each vulnerability.
