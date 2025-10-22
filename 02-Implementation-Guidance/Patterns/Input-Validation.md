# Secure Coding Pattern: Server-Side Input Validation

## Overview

Input validation is a foundational, non-negotiable step in building secure applications. The principle is simple: **never trust data that originates from an external system**. All input must be assumed "tainted" until it has been successfully validated. Proper validation can eliminate a vast number of vulnerabilities, including injection attacks and cross-site scripting (XSS).

Input can originate from many sources, all of which must be treated as untrusted:
* User-submitted forms (text fields, hidden fields, file uploads)
* URL parameters and query strings
* HTTP headers and cookies
* API responses from third-party systems
* Data retrieved from a database (if it wasn't validated before being stored)

* **Relevant ASVS Requirements:** V2.1.1 (Validation Documentation), V2.2.1 (Input Validation), V2.2.2 (Trusted Service Layer Validation)

---

## Principle 1: Always Validate on the Server-Side (ASVS V2.2.2)

Client-side validation (using JavaScript) is excellent for user experience but provides **zero security**. An attacker can easily bypass it using browser developer tools or a web proxy.

Therefore, **all security-critical validation must be performed at a trusted, server-side layer of the application.** This is the only way to ensure that malicious or malformed data is never processed by your business logic.

---

## Principle 2: Use Allow-List Validation (ASVS V2.2.1)

The most effective validation strategy is to use an **allow-list** (whitelisting). This means defining a strict set of rules for what is *allowed* and rejecting everything else. The alternative, a block-list, is fundamentally flawed and must not be used.

| Method | Description | Security Risk |
| :--- | :--- | :--- |
| **Allow-List (✅ Recommended)** | Specifies exactly what is permitted (e.g., "accept only characters `a-z`, `0-9`, and hyphen, with a length of 5-10"). | **Low risk.** Unexpected and malicious data is rejected by default. |
| **Block-List (❌ Forbidden)** | Tries to specify what is *not* allowed (e.g., "block `<script>` tags and single quotes"). | **High risk.** It is practically impossible to create a perfect block-list. Attackers will always find bypasses (e.g., using different encodings). |

---

## 1. Validation Strategy

For every piece of untrusted input, you should perform the following steps on the server-side:

1.  **Canonicalize:** If the application supports multiple character sets or encodings, convert all input to a single, standard format (e.g., UTF-8) *before* validation. This prevents attackers from using alternate encodings to bypass your checks.
2.  **Validate Data:** Check the input against a strict definition of what is valid.
    * **Type:** Is it the correct data type (integer, string, boolean)?
    * **Length:** Is it within the required minimum and maximum length?
    * **Format:** Does it match the expected pattern (e.g., a regex for a UUID or email)?
    * **Range:** Is the number within an acceptable range?
3.  **Handle Failure:** If validation fails for any reason, **reject the input** and return a generic error message to the user.

---

## 2. Implementation Using Frameworks

Always prefer to use the validation libraries built into your framework (e.g., Java's `jakarta.validation`, Python's `WTForms` or `Pydantic`). They are well-tested and designed to prevent common mistakes.

### Code Example (Python using Regex)

In Python, the built-in `re` module is excellent for enforcing allow-list patterns. This example demonstrates validating a simple product ID.

```python
import re

def is_valid_product_id(product_id: str) -> bool:
    """
    ASVS V2.2.1: Validates that a product_id is a 10-character alphanumeric string.
    This is an example of strict, allow-list validation.
    """
    # 1. Check the data type.
    if not isinstance(product_id, str):
        return False

    # 2. Define the allow-list pattern: must be exactly 10 alphanumeric characters.
    pattern = re.compile("^[a-zA-Z0-9]{10}$")

    # 3. Use re.fullmatch() to ensure the ENTIRE string conforms to the pattern.
    if re.fullmatch(pattern, product_id):
        return True
    
    return False

# --- Usage Example (in a server-side function) ---
valid_id = "PROD123456"
invalid_id = "<script>" # Will be rejected because it doesn't match the allow-list.

print(f"'{valid_id}': {is_valid_product_id(valid_id)}")         # Output: True
print(f"'{invalid_id}': {is_valid_product_id(invalid_id)}") # Output: False
```

### Code Example (Java using Jakarta Bean Validation)

Modern Java frameworks use annotations to declaratively enforce validation rules. This is the preferred approach as it's clean, reusable, and integrates directly into the framework.

```java
// Using Jakarta Bean Validation (common in Spring Boot, Quarkus, etc.)

import jakarta.validation.constraints.NotBlank;

import jakarta.validation.constraints.Pattern;

import jakarta.validation.constraints.Size;

// This is a Data Transfer Object (DTO) that represents incoming data.

public class CreateUserRequest {

    @NotBlank(message \= "Username cannot be blank.")

    @Size(min \= 5, max \= 20, message \= "Username must be between 5 and 20 characters.")

    @Pattern(regexp \= "^\[a-zA-Z0-9\_\]+$", message \= "Username can only contain letters, numbers, and underscores.")

    // ASVS V2.2.1: This combination of annotations defines a strict allow-list for the username.

    private String username;

    // ... other fields like email, password etc. with their own validation annotations ...

    // Getters and setters

    public String getUsername() {

        return username;

    }

    public void setUsername(String username) {

        this.username \= username;

    }

}
```

**ASVS V2.2.2: How it works in a framework like Spring Boot**

1. You would use this `CreateUserRequest` class as a parameter in your REST Controller.

2. By adding the `@Valid` annotation, the framework automatically runs these validation checks on the server-side before your controller method is even executed.

3. If validation fails, it throws an exception which you can handle to return a 400 Bad Request.This enforces validation at the trusted service layer.

---

## 3. Common Mistakes to Avoid

| Mistake | Description & Risk | Mitigation |
| :---- | :---- | :---- |
| **Trusting the Client** | Relying on JavaScript validation for security. An attacker can easily turn it off or send a request directly to your API endpoint. | **Always** perform the same or stricter validation on the server-side. |
| **Using a Block-List** | Trying to filter out bad characters like `<` or `'`. This is a flawed strategy that attackers can almost always bypass with different encodings or variations. | **Always** use an allow-list. Define what is good and reject everything else. |
| **Incomplete Validation** | Only checking for one property (e.g., length) but not others (e.g., character set). This leaves gaps for attackers to exploit. | Your validation should be comprehensive: check type, length, format, and range. |
| **Verbose Error Messages** | Returning errors like "Invalid character `<` at position 1" can help an attacker reverse-engineer your validation logic. | Return generic error messages to the user (e.g., "Invalid input for field 'username'"), while logging the detailed error on the server for debugging. |
