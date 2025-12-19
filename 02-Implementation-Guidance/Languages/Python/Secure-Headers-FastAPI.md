# Secure Coding Pattern: Security Headers (Python/FastAPI)

This guide provides the approved method for implementing security headers
in Python applications using FastAPI and Starlette middleware.

- **Relevant ASVS Requirements:** V8.1.1 (X-Frame-Options), V14.4.1
  (Content-Type), V14.4.3 (Content-Security-Policy), V14.4.4 (HSTS)
- **Related Pattern:** `../../Patterns/Security-Logging-and-Monitoring.md`

---

## Principle: Defense in Depth via HTTP Headers

Security headers provide an additional layer of defense against common web
attacks. They instruct browsers to enable built-in security features that
protect users from XSS, clickjacking, and other client-side attacks.

---

## Implementation

### Dependencies

```bash
pip install fastapi uvicorn
```

### Complete Implementation

```python
# secure_headers.py
# ASVS V8.1, V14.4: Security headers middleware for FastAPI

from typing import Callable
from fastapi import FastAPI, Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """
    Middleware that adds security headers to all responses.
    ASVS V14.4: HTTP Security Headers
    """

    def __init__(
        self,
        app: ASGIApp,
        content_security_policy: str | None = None,
        enable_hsts: bool = True,
        hsts_max_age: int = 31536000,  # 1 year
        enable_hsts_subdomains: bool = True,
        enable_hsts_preload: bool = False,
        frame_options: str = "DENY",
        content_type_options: bool = True,
        referrer_policy: str = "strict-origin-when-cross-origin",
        permissions_policy: str | None = None,
    ):
        super().__init__(app)
        self.content_security_policy = content_security_policy
        self.enable_hsts = enable_hsts
        self.hsts_max_age = hsts_max_age
        self.enable_hsts_subdomains = enable_hsts_subdomains
        self.enable_hsts_preload = enable_hsts_preload
        self.frame_options = frame_options
        self.content_type_options = content_type_options
        self.referrer_policy = referrer_policy
        self.permissions_policy = permissions_policy

    async def dispatch(
        self, request: Request, call_next: Callable
    ) -> Response:
        response = await call_next(request)

        # ASVS V14.4.3: Content-Security-Policy
        if self.content_security_policy:
            response.headers["Content-Security-Policy"] = (
                self.content_security_policy
            )

        # ASVS V14.4.4: Strict-Transport-Security (HSTS)
        if self.enable_hsts:
            hsts_value = f"max-age={self.hsts_max_age}"
            if self.enable_hsts_subdomains:
                hsts_value += "; includeSubDomains"
            if self.enable_hsts_preload:
                hsts_value += "; preload"
            response.headers["Strict-Transport-Security"] = hsts_value

        # ASVS V8.1.1: X-Frame-Options (clickjacking protection)
        if self.frame_options:
            response.headers["X-Frame-Options"] = self.frame_options

        # ASVS V14.4.1: X-Content-Type-Options (MIME sniffing protection)
        if self.content_type_options:
            response.headers["X-Content-Type-Options"] = "nosniff"

        # Referrer-Policy (information leakage prevention)
        if self.referrer_policy:
            response.headers["Referrer-Policy"] = self.referrer_policy

        # Permissions-Policy (feature restrictions)
        if self.permissions_policy:
            response.headers["Permissions-Policy"] = self.permissions_policy

        # Remove potentially dangerous headers
        response.headers.pop("Server", None)
        response.headers.pop("X-Powered-By", None)

        return response


# Default secure CSP for APIs (restrictive)
DEFAULT_API_CSP = (
    "default-src 'none'; "
    "frame-ancestors 'none'; "
    "base-uri 'none'; "
    "form-action 'none'"
)

# Default CSP for web applications (adjust as needed)
DEFAULT_WEB_CSP = (
    "default-src 'self'; "
    "script-src 'self'; "
    "style-src 'self' 'unsafe-inline'; "
    "img-src 'self' data: https:; "
    "font-src 'self'; "
    "connect-src 'self'; "
    "frame-ancestors 'none'; "
    "base-uri 'self'; "
    "form-action 'self'"
)

# Default Permissions-Policy (restrictive)
DEFAULT_PERMISSIONS_POLICY = (
    "accelerometer=(), "
    "camera=(), "
    "geolocation=(), "
    "gyroscope=(), "
    "magnetometer=(), "
    "microphone=(), "
    "payment=(), "
    "usb=()"
)


def create_secure_app(
    title: str = "Secure API",
    is_api_only: bool = True,
    **kwargs
) -> FastAPI:
    """
    Factory function to create a FastAPI app with security headers.
    ASVS V14.4: Secure by default configuration.
    """
    app = FastAPI(title=title, **kwargs)

    # Select appropriate CSP based on app type
    csp = DEFAULT_API_CSP if is_api_only else DEFAULT_WEB_CSP

    # Add security headers middleware
    app.add_middleware(
        SecurityHeadersMiddleware,
        content_security_policy=csp,
        enable_hsts=True,
        hsts_max_age=31536000,
        enable_hsts_subdomains=True,
        frame_options="DENY",
        content_type_options=True,
        referrer_policy="strict-origin-when-cross-origin",
        permissions_policy=DEFAULT_PERMISSIONS_POLICY,
    )

    return app


# Example usage
app = create_secure_app(title="My Secure API")


@app.get("/api/health")
async def health_check():
    """Health check endpoint with security headers."""
    return {"status": "healthy"}


@app.get("/api/data")
async def get_data():
    """Example endpoint demonstrating secure headers."""
    return {"message": "This response includes security headers"}


# Alternative: Manual middleware addition for existing apps
def add_security_headers(existing_app: FastAPI) -> None:
    """
    Add security headers to an existing FastAPI application.
    Use this when you cannot use the factory function.
    """
    existing_app.add_middleware(
        SecurityHeadersMiddleware,
        content_security_policy=DEFAULT_API_CSP,
        enable_hsts=True,
        frame_options="DENY",
        content_type_options=True,
        referrer_policy="strict-origin-when-cross-origin",
        permissions_policy=DEFAULT_PERMISSIONS_POLICY,
    )
```

---

## Security Headers Reference

| Header | ASVS | Purpose | Recommended Value |
|--------|------|---------|-------------------|
| Content-Security-Policy | V14.4.3 | XSS prevention | See CSP section |
| Strict-Transport-Security | V14.4.4 | Force HTTPS | `max-age=31536000; includeSubDomains` |
| X-Frame-Options | V8.1.1 | Clickjacking | `DENY` |
| X-Content-Type-Options | V14.4.1 | MIME sniffing | `nosniff` |
| Referrer-Policy | - | Info leakage | `strict-origin-when-cross-origin` |
| Permissions-Policy | - | Feature control | Disable unused APIs |

---

## Content-Security-Policy Deep Dive

### For Pure APIs (No HTML)

```text
default-src 'none'; frame-ancestors 'none'; base-uri 'none'; form-action 'none'
```

### For Web Applications

```text
default-src 'self';
script-src 'self';
style-src 'self' 'unsafe-inline';
img-src 'self' data: https:;
font-src 'self';
connect-src 'self' https://api.example.com;
frame-ancestors 'none';
base-uri 'self';
form-action 'self';
upgrade-insecure-requests;
```

### CSP Reporting (Recommended)

```python
# Enable CSP violation reporting
CSP_WITH_REPORTING = (
    "default-src 'self'; "
    "report-uri /api/csp-report; "
    "report-to csp-endpoint"
)

@app.post("/api/csp-report")
async def csp_report(request: Request):
    """Endpoint to receive CSP violation reports."""
    report = await request.json()
    # Log the violation for analysis
    logger.warning(f"CSP Violation: {report}")
    return {"status": "received"}
```

---

## Testing

```python
# test_secure_headers.py
import pytest
from fastapi.testclient import TestClient
from secure_headers import app

client = TestClient(app)


class TestSecurityHeaders:
    """ASVS V14.4: Security header validation tests."""

    def test_csp_header_present(self):
        """ASVS V14.4.3: Content-Security-Policy must be set."""
        response = client.get("/api/health")
        assert "Content-Security-Policy" in response.headers
        assert "default-src" in response.headers["Content-Security-Policy"]

    def test_hsts_header_present(self):
        """ASVS V14.4.4: HSTS header must be set."""
        response = client.get("/api/health")
        assert "Strict-Transport-Security" in response.headers
        hsts = response.headers["Strict-Transport-Security"]
        assert "max-age=" in hsts
        assert "includeSubDomains" in hsts

    def test_frame_options_header(self):
        """ASVS V8.1.1: X-Frame-Options must prevent framing."""
        response = client.get("/api/health")
        assert response.headers.get("X-Frame-Options") == "DENY"

    def test_content_type_options_header(self):
        """ASVS V14.4.1: X-Content-Type-Options must be nosniff."""
        response = client.get("/api/health")
        assert response.headers.get("X-Content-Type-Options") == "nosniff"

    def test_referrer_policy_header(self):
        """Referrer-Policy should limit information leakage."""
        response = client.get("/api/health")
        assert "Referrer-Policy" in response.headers

    def test_no_server_header(self):
        """Server header should be removed to hide technology."""
        response = client.get("/api/health")
        assert "Server" not in response.headers
        assert "X-Powered-By" not in response.headers

    def test_permissions_policy_header(self):
        """Permissions-Policy should restrict browser features."""
        response = client.get("/api/health")
        assert "Permissions-Policy" in response.headers
        pp = response.headers["Permissions-Policy"]
        assert "camera=()" in pp
        assert "microphone=()" in pp
```

---

## Common Mistakes to Avoid

| Mistake | Risk | Mitigation |
|---------|------|------------|
| Missing CSP | XSS attacks | Always set CSP |
| `unsafe-inline` in script-src | XSS via inline scripts | Use nonces or hashes |
| Missing HSTS | Downgrade attacks | Enable HSTS with long max-age |
| `SAMEORIGIN` for frame-options | Allows same-origin framing | Use `DENY` unless framing needed |
| No HSTS preload | First-visit vulnerable | Consider preload for production |
| Exposing Server header | Technology fingerprinting | Remove Server header |
