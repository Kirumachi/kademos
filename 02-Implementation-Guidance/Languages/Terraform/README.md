# Secure Infrastructure as Code: Terraform Templates

This directory contains secure-by-default Terraform templates for cloud
storage resources. These templates implement ASVS V5.3 requirements for
secure data storage.

- **Relevant ASVS Requirements:** V5.3.1 (Storage Security), V5.3.3
  (Encryption at Rest), V5.3.4 (Access Control)

---

## Templates

| File | Cloud | Description |
|------|-------|-------------|
| `Secure-S3-Bucket.tf` | AWS | S3 bucket with encryption, versioning, public access block |
| `Secure-Azure-Blob.tf` | Azure | Blob storage with encryption, private access, soft delete |

---

## Security Controls Applied

All templates implement these security controls by default:

| Control | ASVS Req | AWS Implementation | Azure Implementation |
|---------|----------|-------------------|---------------------|
| Encryption at rest | V5.3.3 | SSE-S3/KMS | Storage Service Encryption |
| Block public access | V5.3.4 | `block_public_*` | Private container |
| Versioning | V5.3.1 | Bucket versioning | Blob versioning |
| Access logging | - | Server access logs | Diagnostic settings |
| Soft delete | V5.3.1 | Object lock / lifecycle | Soft delete enabled |
| TLS enforcement | V5.3.3 | Bucket policy | Secure transfer required |

---

## Usage

### AWS S3

```bash
cd aws-project
terraform init
terraform plan -var="bucket_name=my-secure-bucket" -var="environment=prod"
terraform apply
```

### Azure Blob

```bash
cd azure-project
terraform init
terraform plan -var="storage_account_name=mysecurestorage" -var="environment=prod"
terraform apply
```

---

## Customization

These templates are designed as secure baselines. When customizing:

1. **Never disable encryption** - Always use SSE or CMK
2. **Never enable public access** - Use pre-signed URLs or CDN
3. **Keep versioning enabled** - Required for compliance and recovery
4. **Review lifecycle rules** - Adjust retention based on compliance needs

---

## Compliance Mapping

| ASVS Requirement | Control |
|------------------|---------|
| V5.3.1 | Versioning, soft delete for data recovery |
| V5.3.3 | Encryption at rest (AES-256), TLS in transit |
| V5.3.4 | IAM policies, public access blocks |
