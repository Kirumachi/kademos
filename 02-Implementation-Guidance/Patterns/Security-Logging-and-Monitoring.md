# Secure Coding Pattern: Effective Security Logging and Monitoring

## Overview

Security logging is a critical **detective control**. While debug logs help
you fix bugs, security logs create a forensic audit trail to help incident
responders determine what happened during a security event, trace it to the
source, and prevent it from happening again.

This guide focuses on logging events relevant to the application's security,
such as authentication, access control, and critical transactions. These
logs must be structured, protected, and contain sufficient context to be fed
into a Security Information and Event Management (SIEM) system for
monitoring and alerting.

- **Relevant ASVS Requirements:** V16.2 (General Logging), V16.3 (Security
  Events), V16.4 (Log Protection)

---

## Principle: Log for Incident Response

When writing a security log, ask yourself: "If I were responding to an
alert at 3 AM, would this log entry give me enough information to understand
what happened?"

Your logs must be:

- **Actionable:** Capture specific, high-fidelity events that can trigger
  alerts.
- **Context-Rich:** Contain enough metadata to trace an event back to a
  source user and IP address.
- **Structured:** Use a machine-readable format like **JSON** to allow for
  easy parsing, searching, and analysis.

---

## 1. What to Log: Key Security Events

The application must log every security-critical action. The following
events are considered the baseline for effective monitoring.

| Event Category | Description | ASVS |
| :--- | :--- | :--- |
| **Authentication** | Log successful and failed login attempts | V16.3.1 |
| **Authorization Failures** | Log access denied to data/pages | V16.3.2 |
| **Account Changes** | Log password resets, profile changes | V16.3.1 |
| **High-Risk Transactions** | Log payments, permission changes | V16.3.3 |
| **System Failures** | Log unhandled exceptions, control failures | V16.3.4 |

---

## 2. Anatomy of a Good Security Log Event (ASVS V16.2.1)

Every security log entry should be a structured JSON object containing a
consistent set of fields:

- **Timestamp:** The exact time the event occurred, in **UTC format**.
- **Source IP Address:** The IP address of the client that initiated the
  request.
- **User Identifier:** The username or unique ID of the authenticated user.
- **Event Type / ID:** A consistent, unique identifier for the event
  (e.g., `USER_LOGIN_FAILURE`).
- **Outcome:** The result of the event (e.g., `SUCCESS`, `FAILURE`).
- **Description:** A human-readable message describing the event.
- **Contextual Details:** A nested object containing any other relevant
  data (e.g., the ID of the resource being accessed).

---

## 3. Implementation Examples

### Python (Structured JSON Logging)

This example uses Python's standard `logging` library with a custom JSON
formatter to create context-rich, machine-readable logs.

```python
import logging
import json
from datetime import datetime, timezone

class JsonFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            "timestamp": datetime.fromtimestamp(
                record.created, tz=timezone.utc).isoformat(),
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

In the Java ecosystem, structured logging is often achieved using libraries
like SLF4J with a Logstash encoder to produce JSON.

```java
// Conceptual example in a Spring Boot service
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.slf4j.MDC; // Mapped Diagnostic Context for structured data

@Service
public class AuthenticationService {
    private static final Logger securityLogger =
        LoggerFactory.getLogger("security");

    public boolean login(String username, String password, String sourceIp) {
        // ... authentication logic ...

        if (!isSuccess) {
            // ASVS V16.3.1: Use MDC to add structured context.
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

Serilog is a popular library in the .NET world for creating structured logs
that can be easily sent to various sinks (like a console, file, or SIEM).

```csharp
// In your Program.cs or Startup.cs to configure Serilog
using Serilog;
using Serilog.Formatting.Json;

Log.Logger = new LoggerConfiguration()
    .WriteTo.Console(new JsonFormatter())
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
            _logger.LogWarning(
                "Failed login for user {UserId} from IP {SourceIp}",
                model.Username, HttpContext.Connection.RemoteIpAddress);

            return Unauthorized();
        }

        return Ok();
    }
}
```

---

## 4. Common Mistakes to Avoid

| Mistake | Risk | Mitigation |
| :--- | :--- | :--- |
| **Logging Sensitive Data** | Data breach | Never log secrets |
| **Not Logging Failures** | Missed attacks | Log auth failures |
| **Unstructured Text** | Hard to parse | Use JSON format |
| **Insufficient Context** | Useless for investigation | Include who/what/when |
| **Log Injection** | Fake log entries | Use structured logging |

**Details:**

- **Logging Sensitive Data:** Writing passwords, session tokens, API keys,
  or PII to logs. If logs are compromised, this data is stolen (ASVS
  V16.2.5). Never log secrets. Mask, redact, or hash sensitive values.
- **Not Logging Failures:** Only logging successful events. Failed logins
  or access control checks are often the first sign of an attack. Prioritize
  logging failures for authentication and authorization (V16.3.1, V16.3.2).
- **Using Unstructured Text:** Writing plain text strings like "Login
  failed". This is difficult to parse, search, and alert on automatically.
  Log in a structured format like JSON.
- **Insufficient Context:** Logging "Access Denied" without including the
  user ID, source IP, and resource they tried to access. Ensure every
  security log entry contains the "who, what, when, and where" (V16.2.1).
- **Allowing Log Injection:** Directly embedding user input into a log
  message. An attacker could inject newlines and fake log entries to mislead
  investigators. Use a structured logging library (V16.4.1).
