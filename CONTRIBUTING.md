# Contributing to the ASVS Compliance Starter Kit

First off, thank you for considering contributing! This project thrives on
community involvement, and every contribution helps make our applications
more secure. Whether you're correcting a typo, improving a template, or
adding a new secure coding pattern, your input is valuable.

This document provides guidelines to ensure that contributing to this
repository is a smooth and positive experience for everyone.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
- [Your First Contribution](#your-first-contribution)
- [Submitting Changes](#submitting-changes-the-pull-request-process)
- [Development Setup & Style Guides](#development-setup--style-guides)

## Code of Conduct

To ensure a welcoming and inclusive environment, we have adopted a Code of
Conduct that we expect all contributors to adhere to. Please read the
`CODE_OF_CONDUCT.md` file to understand what actions will and will not be
tolerated.

## How Can I Contribute?

There are many ways to contribute to the project. Here are a few to get you
started:

- **Reporting Bugs:** Find something wrong with a script, a template, or a
  document? [Open an issue][new-issue] and select the **Bug report**
  template.
- **Suggesting Enhancements:** Have an idea for a new template or a better
  secure coding pattern? [Open an issue][new-issue] and select the
  **Feature request** template.
- **Pull Requests:** If you're ready to contribute code or documentation,
  we welcome your pull requests. See the Pull Request Process below for
  details.

[new-issue]: https://github.com/kaademos/asvs-compliance-starter-kit/issues/new/choose

## Your First Contribution

Unsure where to begin? A great place to start is by looking for issues
tagged with `good first issue` or `help wanted`. These are typically
well-defined tasks that are a great introduction to the project's workflow.

You can also contribute by:

- Improving the documentation in any of the `.md` files.
- Adding a secure coding example for a language you're familiar with.
- Adding a new verification test for a specific ASVS requirement.

## Submitting Changes: The Pull Request Process

1. **Fork the repository** to create your own copy of the project.

2. **Clone your fork** to your local machine.

3. **Create a new branch** from the `develop` branch for your changes.

   ```sh
   # Branch off from the develop branch
   git checkout develop
   git pull origin develop

   # Create your new feature or fix branch
   # Good branch names: feat/add-python-csrf-pattern or fix/typo-in-readme
   git checkout -b <your-branch-name>
   ```

4. **Make your changes** locally, adhering to the Style Guides.

5. **Commit your changes** using a clear and descriptive commit message.
   We follow the [Conventional Commits][conv-commits] specification.

   ```sh
   # Examples of good commit messages:
   git commit -m "feat: Add new decision template for V5 File Handling"
   git commit -m "docs: Clarify instructions in the main README.md"
   git commit -m "fix: Correct field name in V8 Authorization template"
   ```

6. **Push your branch** to your forked repository.

   ```sh
   git push origin <your-branch-name>
   ```

7. **Open a Pull Request** to the `develop` branch of the main repository.
   Please fill out the pull request template with a clear description of
   your changes. The project maintainers will review your PR, provide
   feedback, and merge it when it's ready.

## Development Setup & Style Guides

To ensure consistency across the project, we use automated checks in our CI
pipeline. To avoid issues, please adhere to the following guidelines.

### Local Setup

Before committing, you can run formatters locally to ensure your changes
will pass our checks.

```sh
# Example for Prettier (if used in the project)
npm install --global prettier
prettier --write .
```

### Style Guides

- **Markdown:** Use clear, concise language. Use Prettier-compatible
  formatting. Our CI pipeline will check this automatically.
- **JSON:** Ensure any JSON files are well-formatted and valid. Our CI
  pipeline will also check this.
- **Code (Scripts, Tests):** Follow standard conventions for the language
  you are writing in. Add comments to explain complex logic.

---

Thank you again for your interest in making this starter kit better!

[conv-commits]: https://www.conventionalcommits.org/en/v1.0.0/
