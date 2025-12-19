# Secure Coding Pattern: Input Validation (Python/FastAPI with Pydantic)

This guide provides the approved method for implementing server-side input
validation in Python applications using FastAPI and Pydantic.

- **Relevant ASVS Requirements:** V2.1.1 (Validation Documentation), V2.2.1
  (Input Validation), V2.2.2 (Trusted Service Layer Validation)
- **Related Pattern:** `../../Patterns/Input-Validation.md`

---

## Principle: Declarative Allow-List Validation

Pydantic provides type-safe, declarative validation that enforces allow-list
rules at the API boundary. All validation occurs on the server-side before
any business logic executes.

Key benefits:

- Type coercion and validation in one step
- Automatic error messages without leaking implementation details
- Reusable validators across endpoints
- Integration with OpenAPI documentation

---

## Implementation

### Dependencies

```bash
pip install fastapi pydantic uvicorn
```

### Complete Implementation

```python
# input_validation.py
# ASVS V2.2.1, V2.2.2: Server-side input validation with Pydantic

import re
from typing import Optional
from datetime import date
from enum import Enum

from fastapi import FastAPI, HTTPException, status
from pydantic import (
    BaseModel,
    Field,
    field_validator,
    model_validator,
    EmailStr,
    constr,
    conint,
)

app = FastAPI()


# ASVS V2.2.1: Define allowed values using enums
class UserRole(str, Enum):
    USER = "user"
    ADMIN = "admin"
    MODERATOR = "moderator"


class CreateUserRequest(BaseModel):
    """
    User creation request with strict validation.
    ASVS V2.2.1: All fields have explicit allow-list constraints.
    """

    # Username: 3-20 chars, alphanumeric + underscore only
    username: constr(min_length=3, max_length=20, pattern=r"^[a-zA-Z0-9_]+$") = Field(
        ...,
        description="Username (3-20 chars, alphanumeric and underscore only)",
        examples=["john_doe"]
    )

    # Email: validated format
    email: EmailStr = Field(
        ...,
        description="Valid email address",
        examples=["user@example.com"]
    )

    # Password: minimum length enforced (additional checks in validator)
    password: constr(min_length=12, max_length=128) = Field(
        ...,
        description="Password (12-128 chars)"
    )

    # Age: bounded integer
    age: conint(ge=13, le=120) = Field(
        ...,
        description="Age (13-120)"
    )

    # Role: strict enum validation
    role: UserRole = Field(
        default=UserRole.USER,
        description="User role"
    )

    # Optional field with validation
    phone: Optional[constr(pattern=r"^\+?[1-9]\d{1,14}$")] = Field(
        default=None,
        description="Phone number in E.164 format"
    )

    @field_validator("password")
    @classmethod
    def validate_password_strength(cls, v: str) -> str:
        """
        ASVS V2.1.1: Password must meet complexity requirements.
        """
        errors = []

        if not re.search(r"[A-Z]", v):
            errors.append("uppercase letter")
        if not re.search(r"[a-z]", v):
            errors.append("lowercase letter")
        if not re.search(r"\d", v):
            errors.append("digit")
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", v):
            errors.append("special character")

        if errors:
            raise ValueError(f"Password must contain: {', '.join(errors)}")

        return v

    @field_validator("username")
    @classmethod
    def validate_username_not_reserved(cls, v: str) -> str:
        """
        ASVS V2.2.1: Block reserved usernames.
        """
        reserved = {"admin", "root", "system", "null", "undefined"}
        if v.lower() in reserved:
            raise ValueError("This username is not available")
        return v

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "username": "john_doe",
                    "email": "john@example.com",
                    "password": "SecureP@ssw0rd!",
                    "age": 25,
                    "role": "user"
                }
            ]
        }
    }


class ProductSearchRequest(BaseModel):
    """
    Product search with validated query parameters.
    ASVS V2.2.1: Strict allow-list validation for search inputs.
    """

    query: constr(min_length=1, max_length=100, strip_whitespace=True) = Field(
        ...,
        description="Search query"
    )

    # Pagination with safe defaults and limits
    page: conint(ge=1, le=1000) = Field(
        default=1,
        description="Page number"
    )

    page_size: conint(ge=1, le=100) = Field(
        default=20,
        description="Results per page"
    )

    # Sort field must be from allow-list
    sort_by: Optional[str] = Field(
        default="relevance",
        description="Sort field"
    )

    @field_validator("sort_by")
    @classmethod
    def validate_sort_field(cls, v: str) -> str:
        """
        ASVS V2.2.1: Allow-list for sort fields prevents injection.
        """
        allowed = {"relevance", "price", "name", "date", "rating"}
        if v not in allowed:
            raise ValueError(f"sort_by must be one of: {', '.join(allowed)}")
        return v

    @field_validator("query")
    @classmethod
    def sanitize_query(cls, v: str) -> str:
        """
        Remove potentially dangerous characters from search query.
        """
        # Remove null bytes and control characters
        sanitized = re.sub(r"[\x00-\x1f\x7f]", "", v)
        return sanitized


class DateRangeRequest(BaseModel):
    """
    Date range with cross-field validation.
    """

    start_date: date
    end_date: date

    @model_validator(mode="after")
    def validate_date_range(self):
        """
        ASVS V2.2.1: Cross-field validation for logical constraints.
        """
        if self.end_date < self.start_date:
            raise ValueError("end_date must be after start_date")

        # Limit range to prevent DoS via large queries
        max_days = 365
        if (self.end_date - self.start_date).days > max_days:
            raise ValueError(f"Date range cannot exceed {max_days} days")

        return self


# API Endpoints

@app.post("/api/users", status_code=status.HTTP_201_CREATED)
async def create_user(user: CreateUserRequest):
    """
    ASVS V2.2.2: Validation happens at the trusted service layer.
    If we reach this point, all input has been validated.
    """
    # Business logic here - input is guaranteed valid
    return {
        "message": "User created",
        "username": user.username,
        "email": user.email
    }


@app.get("/api/products/search")
async def search_products(params: ProductSearchRequest):
    """
    Search products with validated parameters.
    """
    return {
        "query": params.query,
        "page": params.page,
        "page_size": params.page_size,
        "sort_by": params.sort_by
    }


@app.post("/api/reports")
async def generate_report(date_range: DateRangeRequest):
    """
    Generate report for validated date range.
    """
    return {
        "start": date_range.start_date.isoformat(),
        "end": date_range.end_date.isoformat()
    }
```

---

## Security Controls Summary

| ASVS Req | Control | Implementation |
|----------|---------|----------------|
| V2.1.1 | Documented validation | Pydantic Field descriptions |
| V2.2.1 | Allow-list validation | `constr`, `conint`, enums, regex |
| V2.2.2 | Server-side validation | FastAPI automatic validation |

---

## Testing

```python
# test_input_validation.py
import pytest
from fastapi.testclient import TestClient
from input_validation import app

client = TestClient(app)


class TestUserCreation:
    """ASVS V2.2.1: Input validation tests."""

    def test_valid_user_creation(self):
        response = client.post("/api/users", json={
            "username": "valid_user",
            "email": "test@example.com",
            "password": "SecureP@ssw0rd!",
            "age": 25
        })
        assert response.status_code == 201

    def test_rejects_short_username(self):
        response = client.post("/api/users", json={
            "username": "ab",  # Too short
            "email": "test@example.com",
            "password": "SecureP@ssw0rd!",
            "age": 25
        })
        assert response.status_code == 422

    def test_rejects_invalid_username_chars(self):
        response = client.post("/api/users", json={
            "username": "user<script>",  # Invalid characters
            "email": "test@example.com",
            "password": "SecureP@ssw0rd!",
            "age": 25
        })
        assert response.status_code == 422

    def test_rejects_reserved_username(self):
        response = client.post("/api/users", json={
            "username": "admin",  # Reserved
            "email": "test@example.com",
            "password": "SecureP@ssw0rd!",
            "age": 25
        })
        assert response.status_code == 422

    def test_rejects_weak_password(self):
        response = client.post("/api/users", json={
            "username": "valid_user",
            "email": "test@example.com",
            "password": "weakpassword",  # No uppercase, digit, special
            "age": 25
        })
        assert response.status_code == 422

    def test_rejects_invalid_age(self):
        response = client.post("/api/users", json={
            "username": "valid_user",
            "email": "test@example.com",
            "password": "SecureP@ssw0rd!",
            "age": 5  # Below minimum
        })
        assert response.status_code == 422


class TestProductSearch:
    """ASVS V2.2.1: Search parameter validation."""

    def test_rejects_invalid_sort_field(self):
        response = client.get("/api/products/search", params={
            "query": "test",
            "sort_by": "'; DROP TABLE products;--"  # SQL injection attempt
        })
        assert response.status_code == 422

    def test_rejects_excessive_page_size(self):
        response = client.get("/api/products/search", params={
            "query": "test",
            "page_size": 10000  # Exceeds limit
        })
        assert response.status_code == 422
```

---

## Common Mistakes to Avoid

| Mistake | Risk | Mitigation |
|---------|------|------------|
| Trusting client validation | JS validation bypassed | Pydantic validates server-side |
| Dynamic sort/filter fields | SQL/NoSQL injection | Use allow-list validators |
| No length limits | DoS via large payloads | Use `constr(max_length=...)` |
| Verbose error details | Information disclosure | Use generic error messages |
| Missing cross-field validation | Logic bypass | Use `model_validator` |
