# Contributing to the SecureTrails Security Workshop

Thank you for your interest in contributing! This document provides guidelines for contributing to this workshop.

## How to Contribute

### 1. Report Issues

Found a problem or have a suggestion?

**[Create an Issue](https://github.com/Hemavathi15sg/security/issues)**

Include:
- Clear description of the issue
- Steps to reproduce (if applicable)
- Expected vs actual behavior
- Your environment (OS, Python version, Copilot version)

### 2. Improve Documentation

Found a typo or unclear explanation?

1. Fork the repository
2. Create a descriptive branch: `docs/fix-prereqs-clarity`
3. Make your improvements
4. Submit a Pull Request

Focus areas:
- Exercise clarity and step-by-step instructions
- Troubleshooting guidance
- Resource links and references

### 3. Enhance Agents

Want to improve the security agents?

1. Navigate to [`.github/agents/`](./.github/agents/)
2. Review existing agents: baseline-checker, dependency-scout, secret-detector
3. Propose improvements via:
   - New detection patterns
   - Better severity classification
   - Additional vulnerability types
   - Performance optimizations

### 4. Add New Exercises

Have an idea for an additional exercise?

1. Create a branch: `feature/exercise-5-custom-agents`
2. Follow the [Exercise Template](./docs/EXERCISE-TEMPLATE.md)
3. Ensure consistency with existing exercises
4. Include:
   - Clear objectives
   - Step-by-step instructions
   - Expected output examples
   - Links to resources

---

## Contribution Guidelines

### Code Quality

- **Python agents**: Follow [PEP 257](https://www.python.org/dev/peps/pep-0257/) docstring conventions
- **Markdown docs**: Use consistent formatting and headers
- **YAML workflows**: Use consistent indentation (2 spaces)

### Testing

Before submitting:

```bash
# Test exercises locally
cd docs/
# Follow each exercise step-by-step

# Test agents
python .github/agents/baseline-checker.py
python .github/agents/dependency-scout.py
python .github/agents/secret-detector.py
```

### Commit Messages

Use clear, descriptive commit messages:

```
docs: Clarify Exercise 1 vulnerability walkthrough

- Add line number references to vulnerable code
- Explain SQL injection attack scenario
- Link to OWASP reference material
```

### Pull Request Process

1. Fork and create a feature branch
2. Make your changes
3. Update relevant documentation
4. Ensure no breaking changes
5. Submit PR with description of changes
6. Address review feedback

---

## Workshop Improvement Areas

### High Priority

- [ ] Additional vulnerability detection patterns in agents
- [ ] More real-world scenario variations
- [ ] Advanced troubleshooting guides
- [ ] Performance optimization for large repositories

### Medium Priority

- [ ] Video walkthroughs for each exercise
- [ ] Automated testing for agents
- [ ] Support for additional programming languages
- [ ] Integration examples with popular tools (SonarQube, etc.)

### Low Priority

- [ ] Translations to other languages
- [ ] Additional visualization tools
- [ ] Extended agent ecosystem

---

## Questions or Discussions?

Have questions about the workshop?

**[Start a Discussion](https://github.com/Hemavathi15sg/security/discussions)**

Topics welcome:
- How to adapt for your org
- Custom agent development
- Integration patterns
- Learning experiences

---

## Conduct

Be respectful and constructive. We're all here to learn!

---

## Recognition

Contributors will be recognized in:
- [CONTRIBUTORS.md](./CONTRIBUTORS.md)
- GitHub repository contributors list
- Workshop release notes

---

Thank you for making this workshop better! 🙏
