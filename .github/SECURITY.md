# Security Policy

## Our Commitment

As a project dedicated to providing security guidance, the integrity and accuracy of our content are paramount. We are committed to ensuring that the templates, code examples, and patterns within the ASVS Compliance Starter Kit represent current security best practices. We deeply appreciate the community's efforts in helping us maintain the quality and security of this resource.

## Scope of this Policy

This security policy applies to potential vulnerabilities found within the **content of this repository**. A vulnerability in this context could include, but is not limited to:

* **Insecure Code Examples:** A code snippet in a `Patterns` or `Verification-Tests` document that contains a security flaw.
* **Flawed Security Guidance:** A recommendation in a `Decision-Templates` or pattern file that is outdated, incorrect, or promotes an insecure practice.
* **Repository Configuration Issues:** A vulnerability in the repository's CI/CD workflows or dependencies (e.g., a vulnerable GitHub Action).

## Reporting a Vulnerability

**Please do not report security vulnerabilities through public GitHub issues.** We ask that you report them privately so we can address the issue before it is widely known.

### Preferred Method: Email

Please send a detailed report to **[kirumachi@proton.me](mailto:kirumachi@proton.me)** with the subject line "SECURITY: Vulnerability in asvs-compliance-starter-kit".

A good report should include:
* A clear description of the flawed guidance or code.
* The full path to the file(s) involved.
* A description of the potential security impact if a user were to implement the flawed guidance.
* Your recommendation for a fix.

### Alternative Method: GitHub Private Reporting

You can also use GitHub's private vulnerability reporting feature, which can be found on the "Security" tab of the repository.

### Our Process

After receiving a report, we will:
1.  Acknowledge receipt of your report within 48 hours.
2.  Investigate and validate the issue.
3.  Work to correct the flawed content in the `develop` branch.
4.  Merge the fix into `main` and credit you for the discovery (unless you wish to remain anonymous).

We thank you for your help in making this project a trusted resource for the security community.
