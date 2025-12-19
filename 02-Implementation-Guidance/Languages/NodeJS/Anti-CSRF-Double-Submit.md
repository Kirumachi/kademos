# Secure Coding Pattern: CSRF Protection (Node.js/Express)

This guide provides the approved method for implementing Cross-Site Request
Forgery (CSRF) protection in Node.js applications using the Double Submit
Cookie pattern, suitable for stateless APIs and SPAs.

- **Relevant ASVS Requirements:** V3.5.1 (Anti-forgery tokens), V3.5.2
  (Token validation)
- **Related Pattern:** `../../Patterns/Anti-CSRF-Implementation.md`

---

## Principle: Double Submit Cookie Pattern

For stateless applications (SPAs with JWT authentication), the Double Submit
Cookie pattern provides CSRF protection without server-side session storage:

1. Server generates a cryptographically random token
2. Token is sent in both a cookie AND expected in a custom header
3. On each request, server verifies both values match
4. Attackers cannot read cross-origin cookies, so they cannot forge the header

---

## Implementation

### Dependencies

```bash
npm install express cookie-parser crypto
```

### Complete Implementation

```javascript
// csrf-protection.js
// ASVS V3.5.1, V3.5.2: Double Submit Cookie CSRF protection

const express = require('express');
const crypto = require('crypto');
const cookieParser = require('cookie-parser');

const app = express();
app.use(express.json());
app.use(cookieParser());

// Configuration
const CSRF_COOKIE_NAME = 'XSRF-TOKEN';
const CSRF_HEADER_NAME = 'X-XSRF-TOKEN';
const TOKEN_LENGTH = 32;

// Cookie options for CSRF token
const CSRF_COOKIE_OPTIONS = {
  httpOnly: false,    // Must be readable by JavaScript
  secure: process.env.NODE_ENV === 'production',
  sameSite: 'strict', // Prevents cross-site cookie sending
  maxAge: 3600000,    // 1 hour
  path: '/'
};

/**
 * Generates a cryptographically secure random token.
 * ASVS V3.5.1: Tokens must be unpredictable.
 */
function generateCsrfToken() {
  return crypto.randomBytes(TOKEN_LENGTH).toString('hex');
}

/**
 * Timing-safe comparison to prevent timing attacks.
 * ASVS V3.5.2: Token comparison must be secure.
 */
function secureCompare(a, b) {
  if (typeof a !== 'string' || typeof b !== 'string') {
    return false;
  }
  if (a.length !== b.length) {
    return false;
  }
  return crypto.timingSafeEqual(Buffer.from(a), Buffer.from(b));
}

/**
 * Middleware to set CSRF token cookie.
 * Call this on initial page load or after authentication.
 */
function setCsrfToken(req, res, next) {
  const token = generateCsrfToken();
  res.cookie(CSRF_COOKIE_NAME, token, CSRF_COOKIE_OPTIONS);
  req.csrfToken = token;
  next();
}

/**
 * Middleware to validate CSRF token on state-changing requests.
 * ASVS V3.5.1: All state-changing requests must be protected.
 */
function validateCsrfToken(req, res, next) {
  // Skip validation for safe methods
  const safeMethods = ['GET', 'HEAD', 'OPTIONS'];
  if (safeMethods.includes(req.method)) {
    return next();
  }

  const cookieToken = req.cookies[CSRF_COOKIE_NAME];
  const headerToken = req.headers[CSRF_HEADER_NAME.toLowerCase()];

  // Both tokens must be present
  if (!cookieToken || !headerToken) {
    return res.status(403).json({
      error: 'CSRF token missing',
      code: 'CSRF_TOKEN_MISSING'
    });
  }

  // ASVS V3.5.2: Tokens must match (timing-safe comparison)
  if (!secureCompare(cookieToken, headerToken)) {
    return res.status(403).json({
      error: 'CSRF token invalid',
      code: 'CSRF_TOKEN_INVALID'
    });
  }

  next();
}

// Apply CSRF validation globally to all routes
app.use(validateCsrfToken);

// Endpoint to get a new CSRF token (call after login)
app.get('/api/csrf-token', setCsrfToken, (req, res) => {
  res.json({ message: 'CSRF token set in cookie' });
});

// Protected endpoint example
app.post('/api/profile', (req, res) => {
  // This endpoint is protected by validateCsrfToken middleware
  res.json({ message: 'Profile updated successfully' });
});

app.put('/api/settings', (req, res) => {
  res.json({ message: 'Settings updated successfully' });
});

app.delete('/api/account', (req, res) => {
  res.json({ message: 'Account deleted' });
});

module.exports = {
  app,
  setCsrfToken,
  validateCsrfToken,
  generateCsrfToken,
  secureCompare
};
```

---

## Frontend Integration

```javascript
// frontend-csrf.js
// Client-side code to include CSRF token in requests

/**
 * Reads CSRF token from cookie.
 */
function getCsrfToken() {
  const match = document.cookie.match(/XSRF-TOKEN=([^;]+)/);
  return match ? match[1] : null;
}

/**
 * Fetch wrapper that automatically includes CSRF token.
 */
async function secureFetch(url, options = {}) {
  const csrfToken = getCsrfToken();

  const headers = {
    ...options.headers,
    'Content-Type': 'application/json'
  };

  // Add CSRF token for state-changing requests
  if (!['GET', 'HEAD', 'OPTIONS'].includes(options.method?.toUpperCase())) {
    headers['X-XSRF-TOKEN'] = csrfToken;
  }

  return fetch(url, { ...options, headers, credentials: 'same-origin' });
}

// Usage example
async function updateProfile(data) {
  const response = await secureFetch('/api/profile', {
    method: 'POST',
    body: JSON.stringify(data)
  });
  return response.json();
}
```

---

## Security Controls Summary

| ASVS Req | Control | Implementation |
|----------|---------|----------------|
| V3.5.1 | Anti-forgery tokens | 32-byte random token |
| V3.5.2 | Token validation | `crypto.timingSafeEqual` |
| V3.5.3 | Cookie attributes | `SameSite=Strict`, `Secure` |

---

## Testing

```javascript
// test-csrf.js
const request = require('supertest');
const { app } = require('./csrf-protection');

describe('CSRF Protection', () => {
  let csrfToken;

  beforeEach(async () => {
    // Get a valid CSRF token
    const res = await request(app).get('/api/csrf-token');
    const cookies = res.headers['set-cookie'];
    const match = cookies[0].match(/XSRF-TOKEN=([^;]+)/);
    csrfToken = match[1];
  });

  it('rejects POST without CSRF token', async () => {
    const res = await request(app)
      .post('/api/profile')
      .send({ name: 'Test' });
    expect(res.status).toBe(403);
    expect(res.body.code).toBe('CSRF_TOKEN_MISSING');
  });

  it('rejects POST with invalid CSRF token', async () => {
    const res = await request(app)
      .post('/api/profile')
      .set('Cookie', `XSRF-TOKEN=${csrfToken}`)
      .set('X-XSRF-TOKEN', 'invalid-token')
      .send({ name: 'Test' });
    expect(res.status).toBe(403);
    expect(res.body.code).toBe('CSRF_TOKEN_INVALID');
  });

  it('accepts POST with valid CSRF token', async () => {
    const res = await request(app)
      .post('/api/profile')
      .set('Cookie', `XSRF-TOKEN=${csrfToken}`)
      .set('X-XSRF-TOKEN', csrfToken)
      .send({ name: 'Test' });
    expect(res.status).toBe(200);
  });

  it('allows GET requests without CSRF token', async () => {
    const res = await request(app).get('/api/csrf-token');
    expect(res.status).toBe(200);
  });
});
```

---

## Common Mistakes to Avoid

| Mistake | Risk | Mitigation |
|---------|------|------------|
| Using predictable tokens | Token guessing | Use `crypto.randomBytes` |
| String comparison for tokens | Timing attacks | Use `timingSafeEqual` |
| `HttpOnly` cookie | JS cannot read token | Set `httpOnly: false` |
| Missing `SameSite` | Cross-site requests | Set `SameSite: Strict` |
| CSRF on GET requests | Unnecessary overhead | Skip safe methods |
| Exposing token in URL | Token leakage via Referer | Use header only |
