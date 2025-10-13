<div align="center">
  
# ASVS Compliance Starter Kit

**A practical, open-source toolkit for integrating the OWASP ASVS 5.0 into your SDLC.**

</div>

<p align="center">
  <a href="LICENSE">
    <img src="https://img.shields.io/github/license/kaademos/asvs-compliance-starter-kit?style=for-the-badge" alt="License">
  </a>
  <a href="https://github.com/kaademos/asvs-compliance-starter-kit/issues">
    <img src="https://img.shields.io/github/issues/kaademos/asvs-compliance-starter-kit?style=for-the-badge&color=brightgreen" alt="Open Issues">
  </a>
  <a href="https://github.com/kaademos/asvs-compliance-starter-kit/pulls">
    <img src="https://img.shields.io/github/issues-pr/kaademos/asvs-compliance-starter-kit?style=for-the-badge&color=9cf" alt="Open Pull Requests">
  </a>
</p>

## 📋 Table of Contents

- [About The Project](#-about-the-project)
- [✨ Key Features](#-key-features)
- [🚀 Getting Started](#-getting-started)
- [📂 Repository Structure](#-repository-structure)
- [🎯 How to Use This Kit](#-how-to-use-this-kit)
- [🤝 Contributing](#-contributing)
- [📜 License](#-license)


## 📖 About The Project

Welcome! This repository provides a set of adaptable templates and documentation based on the **OWASP Application Security Verification Standard (ASVS) 5.0**. Our goal is to offer a practical framework that helps engineering teams of all sizes embed security into their development process from the start.

This is a public, open-source project, free for anyone to use and adapt. We welcome contributions to help make it a valuable resource for the entire community. By using this kit, teams can effectively "shift-left," ensuring security is considered at every stage of the Software Development Lifecycle (SDLC) and empowering them to build secure products by design.

## ✨ Key Features

* **Standardized Templates**: Ready-to-use templates for security decisions and policies.
* **ASVS 5.0 Aligned**: Directly based on the latest OWASP standard.
* **Developer-Friendly Requirements**: We provide the entire ASVS standard pre-translated into actionable functional requirements that can be directly used in development backlogs.
* **Machine-Readable**: Core requirements provided in JSON and CSV for easy automation.
* **Practical Guidance**: Includes secure coding patterns and verification examples.
* **Community Driven**: Open to contributions and improvements from everyone.

## 🚀 Getting Started

1.  **Clone the repository:**
    ```sh
    git clone [https://github.com/kaademos/asvs-compliance-starter-kit.git](https://github.com/kaademos/asvs-compliance-starter-kit.git)
    ```
2.  **Explore the documentation standards:** Start in the `/00-Documentation-Standards/` directory to understand the high-level policies and decision templates.
3.  **Adapt for your project:** Copy the relevant templates and begin integrating them into your project's design and development lifecycle.

## 📂 Repository Structure

The repository is organized into several key directories:

* `📁 00-Documentation-Standards/`
    * Contains high-level policy and decision templates. These are meant to be completed during the design and threat modeling phases of a project.
* `📁 01-ASVS-Core-Reference/`
    * * Houses a tailored, machine-readable version of the ASVS 5.0 standard (JSON, CSV). This is the baseline against which applications can be measured.
* `📁 02-Implementation-Guidance/`
    * Provides practical, developer-focused guidance, including approved libraries, secure coding patterns, and example verification tests for specific ASVS requirements.
* `📁 03-Product-Specific-Files/`
    * A placeholder for teams to link to or store their product-specific ASVS documentation, such as threat models or completed decision templates.
* `📁 04-Documentation-Artifacts/`
    * A central location for storing signed-off or critical security decision artifacts for archival and audit purposes.

## 🎯 How to Use This Kit

### For Product & Engineering Leads

1.  **Define Your Target**: Start in `/00-Documentation-Standards/Level-Definitions.md` to understand which ASVS level applies to your application.
2.  **Document Key Decisions**: Use the templates in `/00-Documentation-Standards/Decision-Templates/` during the design phase to document critical security architecture choices (e.g., authentication strategy, data classification).

### For Developers

1.  **Build Your Security Backlog**: Go to the `/01-ASVS-Core-Reference/Functional-Requirements/` directory. Use the JSON files there as a source of truth for creating security user stories and tasks in your project management system.
2.  **Understand Requirements**: Refer to the baseline functional requirements to see the specific controls required for your application's ASVS level.
3.  **Find Secure Solutions**: Before implementing a requirement, check `/02-Implementation-Guidance/` for approved patterns and libraries.

### For Security & QA Teams

1.  **Automate Verification**: Use the JSON files in `/01-ASVS-Core-Reference/` as input for security testing tools and scripts.
2.  **Write Test Cases**: Use the guidance in `/02-Implementation-Guidance/Verification-Tests/` to create effective tests that map directly to ASVS requirements.

## 🤝 Contributing

Contributions are what make the open-source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

We welcome contributions of all kinds, including:
* Improving documentation
* Adding new implementation guidance or secure coding patterns
* Submitting new templates
* Reporting issues or suggesting new features

To get started, please follow these steps:

1.  Fork the Project
2.  Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3.  Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4.  Push to the Branch (`git push origin feature/AmazingFeature`)
5.  Open a Pull Request

For more details, please see the [CONTRIBUTING](CONTRIBUTING.md).

## 📜 License

This project is licensed under the Apache License 2.0. See the [LICENSE](LICENSE) file for details.
