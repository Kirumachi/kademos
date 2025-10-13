# Using ASVS as Functional Security Requirements

## The "Why": Shifting from Testing to Building

The official OWASP ASVS is written primarily as a set of **verification checks** (e.g., "Verify that..."). This language is perfect for security testers and auditors who are assessing an application after it has been built.

However, for developers, architects, and AppSec engineers working within the Software Development Lifecycle (SDLC), it's far more effective to frame these checks as proactive **functional requirements** (e.g., "The application shall...").

This starter kit provides a complete set of the ASVS 5.0 standard, pre-translated into this developer-friendly format.

### Benefits of This Approach

* **Clarity for Developers:** A requirement like "The application shall use parameterized queries" is a direct, actionable instruction for an engineer.
* **Backlog-Ready:** These functional requirements can be directly converted into user stories, tasks, or tickets in a project management tool like Jira or Azure DevOps.
* **Test-Driven Security:** A clear functional requirement makes it easier for QA and security teams to write corresponding automated test cases.

## How to Use These Files

The translated requirements can be found in the `01-ASVS-Core-Reference/Functional-Requirements/` directory.

You can use these files to:
1.  Determine the applicable ASVS Level for your project using the `Level-Definitions.md` guide.
2.  Select the corresponding `ASVS-Functional-Requirements-L[1|2].json` file.
3.  Use a script or tool to parse this JSON file and import the requirements directly into your project's backlog as security stories.
4.  Reference these requirements in your `Decision-Templates` to justify your design choices.

### How the Files are Structured

The functional requirement files are **cumulative**. This means that the file for a higher level also includes all requirements from the lower levels.

* **`ASVS-Functional-Requirements-L1.json`**: Contains all Level 1 requirements.
* **`ASVS-Functional-Requirements-L2.json`**: Contains all Level 1 **and** Level 2 requirements.
* **`ASVS-Functional-Requirements-L3.json`**: Contains all Level 1, 2, **and** 3 requirements.

This makes it easy to grab the single file that matches your project's target level and get a complete checklist.
