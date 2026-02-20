# GitHub Copilot Instructions for SecureTrails

This file guides Copilot agents on security patterns and vulnerabilities in the codebase.

## Codebase Overview
- Backend: Flask (Python)
- Frontend: HTML + Vanilla JavaScript
- Database: SQLite

## Known Vulnerabilities (For Training Purposes)

### SQL Injection Points
- `app.py:45` - Login query with f-string
- `app.py:100` - Trail view query
- `app.py:125` - Search functionality

### XSS Vulnerabilities
- `templates/login.html:15` - Error message rendering
- `templates/trails.html:18` - Comment rendering
- `static/js/app.js:8` - innerHTML usage

### Authentication Issues
- Hardcoded JWT secret in app.py:12
- MD5 password hashing (deprecated)
- Missing session validation

### Configuration Issues
- CORS allows all origins
- Debug mode enabled in production
- Hardcoded database path

## Analysis Patterns

When analyzing this code:
1. Look for string interpolation in SQL queries (SQL injection)
2. Check HTML rendering for unescaped output (XSS)
3. Identify hardcoded credentials
4. Verify password hashing methods
5. Check CORS and security headers

## Files to Analyze
- Security concerns primarily in: app.py, templates/*, static/js/app.js
- Configuration in: .env.example, requirements.txt
