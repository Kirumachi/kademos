# Secure Coding Pattern: CSRF Protection

This guide provides the approved method for implementing Cross-Site Request
Forgery (CSRF) protection in our applications.

- **Relevant ASVS Requirement:** V3.5.1, V3.5.2

---

## Principle: Synchronizer Token Pattern

All state-changing requests (e.g., `POST`, `PUT`, `DELETE`) must be protected
by a unique, unpredictable token that is tied to the user's session. This is
known as the **Synchronizer (or Anti-CSRF) Token Pattern**.

The general flow is:

1. The server generates a unique, random token for a user session.
2. The server embeds this token in a hidden field in HTML forms. For SPA/API
   clients, it's sent in a custom HTTP header or cookie.
3. When the user submits the form or makes an API call, the token is sent
   back to the server.
4. The server validates that the submitted token matches the one associated
   with the user's session before processing the request.

---

## Implementation by Application Type

### 1. Stateful Web Applications (Server-Side Sessions)

Use the built-in CSRF protection provided by your web framework. **Do not
build your own.**

- **Java (Spring Security):** CSRF protection is enabled by default. Ensure
  it is not disabled. The token is automatically added to the model for
  Thymeleaf/JSP forms. For AJAX calls, ensure the frontend sends the token
  in the `X-XSRF-TOKEN` header.
- **Python (Django):** Use the `{% csrf_token %}` template tag in all
  `<form>` elements that use an internal URL. Ensure the `CsrfViewMiddleware`
  is enabled.
- **Ruby on Rails:** `protect_from_forgery` is enabled by default in
  `ApplicationController`.

### 2. Stateless Applications (SPAs with APIs)

For stateless applications using tokens like JWTs, the **Double Submit
Cookie** pattern is the approved method.

1. **On Login:** The server generates a random, unpredictable string for
   the CSRF token. It returns this token in two places:
   - In the JWT payload (inside the `csrf` claim).
   - In a separate `HttpOnly=false`, `Secure=true`, `SameSite=Strict` cookie
     (e.g., `XSRF-TOKEN`).
2. **On Subsequent Requests:** Your frontend JavaScript reads the token from
   the cookie and includes it in a custom HTTP header (e.g., `X-CSRF-Token`).
3. **On Server:** The API backend must validate the request by:
   - Decoding the JWT to get the `csrf` claim.
   - Reading the `X-CSRF-Token` header.
   - **Verifying that the two values are identical.** If they are not, the
     request must be rejected with a `403 Forbidden` error.

---

## Common Mistakes to Avoid

- **Using CSRF tokens for `GET` requests:** CSRF protection is only for
  state-changing requests.
- **Leaking the token:** Ensure the token is not logged or exposed in URLs.
- **Incorrect cookie flags:** For the Double Submit pattern, the cookie must
  not be `HttpOnly` so that JavaScript can read it, but it should be `Secure`
  and `SameSite=Strict`.
