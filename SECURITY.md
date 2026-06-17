# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 0.2.x   | ✅ Active support  |
| 0.1.x   | ⚠️ Security fixes only |
| < 0.1   | ❌ No longer supported |

## Reporting a Vulnerability

If you discover a security vulnerability in PCOS, please report it responsibly.

### How to Report

1. **Do NOT** open a public GitHub issue for security vulnerabilities
2. Email security concerns to: [your-email@example.com]
3. Include the following information:
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if any)

### What to Expect

- **Acknowledgment**: Within 48 hours
- **Initial Assessment**: Within 1 week
- **Fix Timeline**: Depends on severity
  - Critical: Within 1 week
  - High: Within 2 weeks
  - Medium: Within 1 month
  - Low: Next release

### Disclosure Policy

- We will work with you to understand and fix the issue
- We will credit you in the security advisory (unless you prefer anonymity)
- We will not take legal action against researchers who report vulnerabilities responsibly

## Security Best Practices

When using PCOS:

1. **API Keys**: Never commit API keys to version control
2. **Environment Variables**: Use `.env` files (already in `.gitignore`)
3. **Dependencies**: Keep dependencies updated
4. **Network**: Run the API server behind a reverse proxy in production
5. **Data**: Decision data contains sensitive personal information - protect it

## Security Features

- API keys are loaded from environment variables only
- No API keys are logged or stored in decision records
- SQLite database is local by default
- CORS is configured for development (restrict in production)

## Contact

For security concerns: [your-email@example.com]

For general questions: Use [GitHub Discussions](https://github.com/yaox2689-max/pcos/discussions)
