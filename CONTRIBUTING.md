# Contributing to PCOS

Thank you for your interest in contributing to PCOS! This document provides guidelines and instructions for contributing.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
- [Development Setup](#development-setup)
- [Pull Request Process](#pull-request-process)
- [Style Guide](#style-guide)

## Code of Conduct

This project adheres to a Code of Conduct. By participating, you are expected to uphold this code. Please report unacceptable behavior to the project maintainers.

## How Can I Contribute?

### Reporting Bugs

- Check existing issues to avoid duplicates
- Use the bug report template
- Include detailed steps to reproduce
- Include system information (OS, Python version, Node version)

### Suggesting Features

- Use the feature request template
- Explain the use case
- Consider the impact on existing functionality

### Submitting Code

- Fork the repository
- Create a feature branch
- Make your changes
- Add tests if applicable
- Submit a pull request

## Development Setup

### Backend (Python)

```bash
# Clone the repository
git clone https://github.com/yaox2689-max/pcos.git
cd pcos

# Install dependencies with uv
uv sync

# Set up environment variables
cp .env.example .env
# Edit .env with your API keys

# Run the backend
uv run uvicorn runtime.main:app --port 8001 --reload
```

### Frontend (Next.js)

```bash
cd frontend

# Install dependencies
npm install

# Run development server
npm run dev
```

### Running Tests

```bash
# Backend tests
python -m pytest tests/ -v

# Identity experiment
python identity_experiment.py
```

## Pull Request Process

1. **Fork and Clone**: Fork the repo and clone your fork
2. **Create Branch**: `git checkout -b feature/your-feature`
3. **Make Changes**: Implement your changes
4. **Test**: Ensure all tests pass
5. **Commit**: Use conventional commits (see below)
6. **Push**: Push to your fork
7. **PR**: Create a pull request with clear description

### Commit Messages

We use [Conventional Commits](https://www.conventionalcommits.org/):

```
feat: add new feature
fix: bug fix
docs: documentation changes
style: formatting, missing semicolons, etc.
refactor: code refactoring
test: adding tests
chore: maintenance tasks
```

Examples:
```
feat: add value conflict visualization
fix: resolve similarity calculation bug
docs: update API documentation
```

## Style Guide

### Python

- Follow PEP 8
- Use type hints
- Write docstrings for public functions
- Maximum line length: 100 characters

### TypeScript/React

- Use TypeScript for all new code
- Follow ESLint configuration
- Use functional components with hooks
- Use Tailwind CSS for styling

### YAML

- Use 2-space indentation
- Add comments for complex structures
- Keep files under 500 lines

## Project Structure

```
pcos/
├── pcos/                    # Schema and configuration
│   ├── identity.yaml        # Identity schema
│   ├── world_model.yaml     # World model schema
│   └── ...
├── runtime/                 # Backend runtime
│   ├── services/            # Core services
│   ├── routers/             # API routes
│   └── ...
├── frontend/                # Next.js frontend
│   ├── app/                 # Pages
│   ├── components/          # React components
│   └── ...
├── research/                # Analysis and findings
└── tests/                   # Test files
```

## Questions?

Feel free to open an issue for any questions about contributing.

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
