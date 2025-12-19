# Secure S3 Bucket Configuration
# ASVS V5.3: Secure-by-default storage configuration
#
# This template creates an S3 bucket with:
# - Server-side encryption (SSE-S3 or KMS)
# - Public access blocked
# - Versioning enabled
# - Access logging
# - TLS-only access policy

terraform {
  required_version = ">= 1.0.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">= 5.0.0"
    }
  }
}

# Variables
variable "bucket_name" {
  description = "Name of the S3 bucket"
  type        = string

  validation {
    condition     = can(regex("^[a-z0-9][a-z0-9.-]{1,61}[a-z0-9]$", var.bucket_name))
    error_message = "Bucket name must be 3-63 characters, lowercase, and DNS-compliant."
  }
}

variable "environment" {
  description = "Environment name (e.g., prod, staging, dev)"
  type        = string
  default     = "dev"

  validation {
    condition     = contains(["dev", "staging", "prod"], var.environment)
    error_message = "Environment must be dev, staging, or prod."
  }
}

variable "enable_kms_encryption" {
  description = "Use KMS encryption instead of SSE-S3"
  type        = bool
  default     = false
}

variable "kms_key_arn" {
  description = "ARN of KMS key for encryption (required if enable_kms_encryption is true)"
  type        = string
  default     = null
}

variable "log_bucket_name" {
  description = "Name of the bucket for access logs (optional)"
  type        = string
  default     = null
}

variable "retention_days" {
  description = "Number of days to retain non-current versions"
  type        = number
  default     = 90
}

# Data source for current AWS account
data "aws_caller_identity" "current" {}

# Main S3 bucket
# ASVS V5.3.1: Secure storage configuration
resource "aws_s3_bucket" "secure_bucket" {
  bucket = var.bucket_name

  tags = {
    Environment = var.environment
    Security    = "ASVS-V5.3-Compliant"
    ManagedBy   = "Terraform"
  }
}

# ASVS V5.3.4: Block ALL public access
resource "aws_s3_bucket_public_access_block" "secure_bucket" {
  bucket = aws_s3_bucket.secure_bucket.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

# ASVS V5.3.3: Server-side encryption
resource "aws_s3_bucket_server_side_encryption_configuration" "secure_bucket" {
  bucket = aws_s3_bucket.secure_bucket.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm     = var.enable_kms_encryption ? "aws:kms" : "AES256"
      kms_master_key_id = var.enable_kms_encryption ? var.kms_key_arn : null
    }
    bucket_key_enabled = var.enable_kms_encryption
  }
}

# ASVS V5.3.1: Versioning for data recovery
resource "aws_s3_bucket_versioning" "secure_bucket" {
  bucket = aws_s3_bucket.secure_bucket.id

  versioning_configuration {
    status = "Enabled"
  }
}

# Lifecycle rules for version management
resource "aws_s3_bucket_lifecycle_configuration" "secure_bucket" {
  bucket = aws_s3_bucket.secure_bucket.id

  rule {
    id     = "cleanup-old-versions"
    status = "Enabled"

    noncurrent_version_expiration {
      noncurrent_days = var.retention_days
    }

    noncurrent_version_transition {
      noncurrent_days = 30
      storage_class   = "STANDARD_IA"
    }

    abort_incomplete_multipart_upload {
      days_after_initiation = 7
    }
  }
}

# Access logging (if log bucket is provided)
resource "aws_s3_bucket_logging" "secure_bucket" {
  count = var.log_bucket_name != null ? 1 : 0

  bucket        = aws_s3_bucket.secure_bucket.id
  target_bucket = var.log_bucket_name
  target_prefix = "${var.bucket_name}/logs/"
}

# ASVS V5.3.3: Bucket policy enforcing TLS-only access
resource "aws_s3_bucket_policy" "secure_bucket" {
  bucket = aws_s3_bucket.secure_bucket.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid       = "EnforceTLS"
        Effect    = "Deny"
        Principal = "*"
        Action    = "s3:*"
        Resource = [
          aws_s3_bucket.secure_bucket.arn,
          "${aws_s3_bucket.secure_bucket.arn}/*"
        ]
        Condition = {
          Bool = {
            "aws:SecureTransport" = "false"
          }
        }
      },
      {
        Sid       = "EnforceMinTLSVersion"
        Effect    = "Deny"
        Principal = "*"
        Action    = "s3:*"
        Resource = [
          aws_s3_bucket.secure_bucket.arn,
          "${aws_s3_bucket.secure_bucket.arn}/*"
        ]
        Condition = {
          NumericLessThan = {
            "s3:TlsVersion" = "1.2"
          }
        }
      }
    ]
  })

  depends_on = [aws_s3_bucket_public_access_block.secure_bucket]
}

# Outputs
output "bucket_id" {
  description = "The ID of the S3 bucket"
  value       = aws_s3_bucket.secure_bucket.id
}

output "bucket_arn" {
  description = "The ARN of the S3 bucket"
  value       = aws_s3_bucket.secure_bucket.arn
}

output "bucket_domain_name" {
  description = "The domain name of the S3 bucket"
  value       = aws_s3_bucket.secure_bucket.bucket_domain_name
}

output "security_controls" {
  description = "Security controls applied to this bucket"
  value = {
    encryption        = var.enable_kms_encryption ? "KMS" : "SSE-S3"
    public_access     = "Blocked"
    versioning        = "Enabled"
    tls_required      = "Yes (TLS 1.2+)"
    logging           = var.log_bucket_name != null ? "Enabled" : "Disabled"
    version_retention = "${var.retention_days} days"
  }
}
