# Contributing

Contributions are welcome, and they are greatly appreciated! Every little bit helps, and credit will always be given.

You can contribute in many ways:

## Types of Contributions

### Report Bugs

Report bugs at https://github.com/HAEdwin/entity_broadcaster/issues.

If you are reporting a bug, please include:

- Your operating system name and version.
- Any details about your local setup that might be helpful in troubleshooting.
- Detailed steps to reproduce the bug.
- Home Assistant version and Entity Broadcaster version.

### Fix Bugs

Look through the GitHub issues for bugs. Anything tagged with "bug" and "help wanted" is open to whoever wants to implement it.

### Implement Features

Look through the GitHub issues for features. Anything tagged with "enhancement" and "help wanted" is open to whoever wants to implement it.

### Write Documentation

Entity Broadcaster could always use more documentation, whether as part of the official Entity Broadcaster docs, in docstrings, or even on the web in blog posts, articles, and such.

### Submit Feedback

The best way to send feedback is to file an issue at https://github.com/HAEdwin/entity_broadcaster/issues.

If you are proposing a feature:

- Explain in detail how it would work.
- Keep the scope as narrow as possible, to make it easier to implement.
- Remember that this is a volunteer-driven project, and that contributions are welcome.

## Get Started!

Ready to contribute? Here's how to set up `entity_broadcaster` for local development.

1. Fork the `entity_broadcaster` repo on GitHub.
2. Clone your fork locally:
   ```bash
   git clone git@github.com:your_name_here/entity_broadcaster.git
   ```
3. Install your local copy into a virtualenv or use it directly in your Home Assistant development environment.
4. Create a branch for local development:
   ```bash
   git checkout -b name-of-your-bugfix-or-feature
   ```
5. Make your changes locally.
6. Test your changes with Home Assistant.
7. Commit your changes and push your branch to GitHub:
   ```bash
   git add .
   git commit -m "Your detailed description of your changes."
   git push origin name-of-your-bugfix-or-feature
   ```
8. Submit a pull request through the GitHub website.

## Pull Request Guidelines

Before you submit a pull request, check that it meets these guidelines:

1. The pull request should include tests if applicable.
2. If the pull request adds functionality, the docs should be updated.
3. The pull request should work for Python 3.11+ and Home Assistant 2023.1+.
4. Check that your code follows the project's coding standards.

## Code Standards

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guidelines
- Use type hints where appropriate
- Include docstrings for functions and classes
- Keep functions focused and small
- Use meaningful variable and function names

## Testing

- Test your changes with a real Home Assistant installation
- Verify that the UDP broadcasting works correctly
- Test both the config flow and options flow
- Ensure error handling works as expected
- Test with different entity types and configurations

## Code of Conduct

Please note that this project is released with a Contributor Code of Conduct. By participating in this project you agree to abide by its terms.
