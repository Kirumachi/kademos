# Secure Coding Pattern: Access Control (Preventing IDOR / BOLA)

## Overview

**Insecure Direct Object Reference (IDOR)**, a specific type of **Broken
Object Level Authorization (BOLA)**, is a critical and common vulnerability.
It occurs when an application uses an identifier from a user (like a URL
parameter) to directly access a resource without verifying if that user is
actually authorized to access *that specific resource*.

The core principle to prevent IDOR is simple: **For every request that
accesses a private resource, the server must perform an explicit
authorization check to verify that the currently authenticated user is
authorized to interact with that specific record.**

- **Relevant ASVS Requirements:** V8.2.2 (Data-Specific Access), V8.3.1
  (Enforcement at a Trusted Service Layer)

---

## Vulnerability Scenario

IDOR vulnerabilities typically exploit predictable identifiers. Consider an
application that lets a user view their invoice via a URL like this:

`https://app.example.com/api/invoices?invoiceId=101`

A malicious user, after authenticating, can simply change the identifier
in the URL:

`https://app.example.com/api/invoices?invoiceId=102`

If the application only checks that the user is logged in but **fails to
verify that the current user owns invoice #102**, it will display the other
user's private information. This is a classic IDOR data breach.

---

## Principle: Enforce Data-Specific Access on the Server

To prevent IDOR (ASVS V8.2.2 & V8.3.1), every data access operation on the
server must be filtered not just by the object's ID, but also by the user's
identity.

This check must happen at a **trusted service layer** (your backend code),
as any client-side checks can be bypassed. The logic is simple: "Does this
object's `owner_id` match the `current_user_id`?"

### Pseudocode Example

This illustrates the fundamental logic difference between insecure and
secure code.

#### Insecure Pseudocode

```text
function retrieve_invoice_insecure(current_user, requested_invoice_id):
    # INSECURE: The query only uses the ID from the URL.
    # It never checks who owns the invoice.
    invoice = database.get_invoice_by_id(requested_invoice_id)
    return invoice  # Returns the invoice, regardless of who owns it.
```

#### Secure Pseudocode

```text
function retrieve_invoice_secure(current_user, requested_invoice_id):
    # 1. Fetch the resource using the user-provided ID.
    invoice = database.get_invoice_by_id(requested_invoice_id)

    if invoice is None:
        return error_404  # Treat as not found

    # 2. EXPLICIT AUTHORIZATION CHECK (The Core Defense)
    if (invoice.owner_id == current_user.id):
        # User is authorized, so return the resource.
        return invoice
    else:
        # User is not the owner. Deny access.
        # Return a generic error to prevent leaking information.
        return error_403_or_404
```

---

## Implementation Examples

### Java (Spring Boot with JPA/Spring Data)

In a Spring application, the ownership check should be part of your
repository query. This is the most efficient and secure way to enforce
the rule at the database level.

```java
// In your InvoiceRepository.java interface
import org.springframework.data.jpa.repository.JpaRepository;
import java.util.Optional;

public interface InvoiceRepository extends JpaRepository<Invoice, Long> {
    /**
     * ASVS V8.2.2: This query is the secure way to fetch an object.
     * It finds an invoice ONLY IF the ID matches AND the owner's
     * username matches the currently authenticated principal's name.
     */
    Optional<Invoice> findByIdAndOwnerUsername(Long id, String username);
}

// --- In your InvoiceService.java ---
@Service
public class InvoiceService {
    @Autowired
    private InvoiceRepository invoiceRepository;

    public Invoice getInvoiceForCurrentUser(Long invoiceId) {
        // ASVS V8.3.1: The check is enforced in the trusted service layer.
        String currentUsername = SecurityContextHolder.getContext()
            .getAuthentication().getName();

        // The repository query handles both finding and authorization.
        return invoiceRepository
            .findByIdAndOwnerUsername(invoiceId, currentUsername)
            .orElseThrow(() -> new ResourceNotFoundException(
                "Invoice not found or access denied."));
    }
}
```

### C# (.NET with Entity Framework)

In ASP.NET Core, the logic is very similar. The ownership check is added
directly into the LINQ query against the database context.

```csharp
// In your InvoicesController.cs
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using System.Security.Claims;

[ApiController]
[Route("api/[controller]")]
public class InvoicesController : ControllerBase
{
    private readonly ApplicationDbContext _context;

    public InvoicesController(ApplicationDbContext context)
    {
        _context = context;
    }

    [HttpGet("{id}")]
    public async Task<ActionResult<Invoice>> GetInvoice(int id)
    {
        // Get the current user's ID from their claims.
        var currentUserId = User.FindFirstValue(ClaimTypes.NameIdentifier);

        // ASVS V8.2.2 & V8.3.1: The LINQ query securely filters by BOTH
        // the invoice ID and the current user's ID.
        var invoice = await _context.Invoices
            .Where(i => i.Id == id && i.OwnerUserId == currentUserId)
            .FirstOrDefaultAsync();

        if (invoice == null)
        {
            // Return a generic "Not Found" to prevent leaking information
            // about which invoice IDs exist.
            return NotFound();
        }

        return Ok(invoice);
    }
}
```

## Common Mistakes to Avoid

| Mistake | Risk | Mitigation |
| :--- | :--- | :--- |
| **Security by Obscurity** | UUIDs still vulnerable | Check ownership always |
| **Checking Only Writes** | Reads expose data | Check all operations |
| **Leaking Internal IDs** | Exposes system info | Use DTOs, minimal data |

**Details:**

- **Security by Obscurity:** Assuming that using long, non-sequential
  identifiers like UUIDs is sufficient protection. While harder to guess,
  a leaked UUID is just as vulnerable as an integer if there is no ownership
  check. Always enforce the explicit ownership check.
- **Checking Only Write Actions:** Developers sometimes only protect "write"
  operations (POST, PUT, DELETE) but forget to add the same checks to "read"
  operations (GET). Authorization must be verified for every single request.
- **Leaking Internal Identifiers:** Returning excessive data in API responses
  (like internal `owner_id` fields) can give an attacker information they
  can use to map out your system. Use DTOs to control what data is exposed.
