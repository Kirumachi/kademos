# Secure Coding Pattern: Effective Security Logging and Monitoring

## Overview

Security logging is a critical **detective control**. While debug logs help you fix bugs, security logs create a forensic audit trail to help incident responders determine what happened during a security event, trace it to the source, and prevent it from happening again.

This guide focuses on logging events relevant to the application's security, such as authentication, access control, and critical transactions. These logs must be structured, protected, and contain sufficient context to be fed into a Security Information and Event Management (SIEM) system for monitoring and alerting.

* **Relevant ASVS Requirements:** V16.2 (General Logging), V16.3 (Security Events), V16.4 (Log Protection)

---

## Principle: Log for Incident Response

When writing a security log, ask yourself: "If I were responding to an alert at 3 AM, would this log entry give me enough information to understand what happened?"

Your logs must be:
* **Actionable:** Capture specific, high-fidelity events that can trigger alerts.
* **Context-Rich:** Contain enough metadata to trace an event back to a source user and IP address.
* **Structured:** Use a machine-readable format like **JSON** to allow for easy parsing, searching, and analysis.

---

## 1. What to Log: Key Security Events

The application must log every security-critical action. The following events are considered the baseline for effective monitoring.

| Event Category | Description & Requirement | ASVS Support |
| :--- | :--- | :--- |
| **Authentication Events** | Log every successful and failed login attempt. Log any activity indicative of brute-force attacks. | **V16.3.1** |
| **Authorization Failures** | Log all attempts to access data, pages, features, or records for which the user is not authorized (access denied). This is critical for detecting IDOR attempts. | **V16.3.2** |
| **Account & Identity Changes** | Log password reset attempts, successful password changes, and any modifications to a user's sensitive profile information (e.g., email address). | **V16.3.1** |
| **High-Risk Transactions** | Log the initiation and outcome of critical business functions, such as payment processing, funds transfers, or changes to user permissions. | **V16.3.3** |
| **System & Security Failures**| Log all unhandled exceptions and failures in security controls (e.g., validation errors, cryptography failures). | **V16.3.4** |

---

## 2. Anatomy of a Good Security Log Event (ASVS V16.2.1)

Every security log entry should be a structured JSON object containing a consistent set of fields:

* **Timestamp:** The exact time the event occurred, in **UTC format**.
* **Source IP Address:** The IP address of the client that initiated the request.
* **User Identifier:** The username or unique ID of the authenticated user.
* **Event Type / ID:** A consistent, unique identifier for the event (e.g., `USER_LOGIN_FAILURE`).
* **Outcome:** The result of the event (e.g., `SUCCESS`, `FAILURE`).
* **Description:** A human-readable message describing the event.
* **Contextual Details:** A nested object containing any other relevant data (e.g., the ID of the resource being accessed).

---

## 3. Implementation Examples

### Python (Structured JSON Logging)

This example uses Python's standard `logging` library with a custom JSON formatter to create context-rich, machine-readable logs.

```python
import logging
import json
from datetime import datetime, timezone

class JsonFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            "timestamp": datetime.fromtimestamp(record.created, tz=timezone.utc).isoformat(),
            "level": record.levelname,
            "message": record.getMessage(),
            **(record.__dict__.get("extra_info", {})),
        }
        return json.dumps(log_record)

# Configure a specific logger for security events
security_logger = logging.getLogger("security_events")
handler = logging.StreamHandler()
handler.setFormatter(JsonFormatter())
security_logger.addHandler(handler)
security_logger.setLevel(logging.INFO)

def log_auth_failure(username, source_ip):
    # ASVS V16.3.1: Log failed authentication with rich context.
    log_details = {
        "event_type": "USER_LOGIN_FAILURE",
        "outcome": "FAILURE",
        "source_ip": source_ip,
        "user_id": username,
    }
    security_logger.warning(
        f"Failed login attempt for user '{username}'.",
        extra={"extra_info": log_details}
    )
```
### Java (Using SLF4J with Logback/Logstash)

In the Java ecosystem, structured logging is often achieved using libraries like SLF4J with a Logstash encoder to produce JSON.

```java
// Conceptual example in a Spring Boot service
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.slf4j.MDC; // Mapped Diagnostic Context for structured data

@Service
public class AuthenticationService {
    private static final Logger securityLogger = LoggerFactory.getLogger("security");

    public boolean login(String username, String password, String sourceIp) {
        // ... authentication logic ...

        if (!isSuccess) {
            // ASVS V16.3.1: Use MDC to add structured context to the log event.
            // The Logstash/JSON encoder will automatically include these fields.
            MDC.put("eventType", "USER_LOGIN_FAILURE");
            MDC.put("outcome", "FAILURE");
            MDC.put("sourceIp", sourceIp);
            MDC.put("userId", username);
            
            securityLogger.warn("Failed login attempt for user.");

            MDC.clear(); // Clean up the context for the next request
            return false;
        }
        // ... log success ...
        return true;
    }
}
```

### C# (.NET Core with Serilog)

Serilog is a popular library in the .NET world for creating structured logs that can be easily sent to various sinks (like a console, file, or SIEM).

```C#
// In your Program.cs or Startup.cs to configure Serilog
using Serilog;
using Serilog.Formatting.Json;

Log.Logger = new LoggerConfiguration()
    .WriteTo.Console(new JsonFormatter()) // Configure to output JSON
    .CreateLogger();

// --- In your controller or service ---
using Microsoft.AspNetCore.Mvc;

public class AccountController : ControllerBase
{
    private readonly ILogger<AccountController> _logger;

    public AccountController(ILogger<AccountController> logger)
    {
        _logger = logger;
    }

    [HttpPost("login")]
    public IActionResult Login([FromBody] LoginModel model)
    {
        // ... authentication logic ...
        
        if (!isSuccess)
        {
            // ASVS V16.3.1: Serilog uses message templates with properties
            // to create structured log events.
            _logger.LogWarning(
                "Failed login attempt for user {UserId} from IP {SourceIp}",
                model.Username, HttpContext.Connection.RemoteIpAddress);
            
            return Unauthorized();
        }

        return Ok();
    }
}
```
-----

## 4. Common Mistakes to Avoid

| Mistake | Description & Risk | Mitigation |
| :--- | :--- | :--- |
| **Logging Sensitive Data** | Writing passwords, full session tokens, API keys, or PII to logs. If logs are compromised, this data is stolen, violating **ASVS V16.2.5**. | **Never log secrets.** Mask, redact, or hash sensitive values. Do not log entire request bodies or data objects by default. |
| **Not Logging Failures** | Only logging successful events. Failed logins or access control checks are often the first sign of an attack. | Prioritize logging **failures** for authentication and authorization events, as required by **ASVS V16.3.1** and **V16.3.2**. |
| **Using Unstructured Text** | Writing plain text strings like `"Login failed"`. This is difficult to parse, search, and alert on automatically. | Log in a structured format like **JSON**. This allows for reliable querying and alerting in a SIEM. |
| **Insufficient Context** | Logging `"Access Denied"` without including the user ID, source IP, and the resource they tried to access. The log is useless for investigation. | Ensure every security log entry contains the "who, what, when, and where" as defined in the "Anatomy" section (**ASVS V16.2.1**). |
| **Allowing Log Injection** | Directly embedding user input into a log message. An attacker could inject newlines (`\n`) and fake log entries to mislead investigators. | Use a structured logging library that treats user input as data, not as part of the log message format (**ASVS V16.4.1**). |