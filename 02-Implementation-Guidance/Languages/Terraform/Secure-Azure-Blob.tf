# Secure Azure Blob Storage Configuration
# ASVS V5.3: Secure-by-default storage configuration
#
# This template creates an Azure Storage Account with:
# - Encryption at rest (Microsoft-managed or CMK)
# - Private access only (no public blob access)
# - Soft delete enabled
# - Versioning enabled
# - HTTPS-only access
# - Minimum TLS version 1.2

terraform {
  required_version = ">= 1.0.0"
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = ">= 3.0.0"
    }
  }
}

provider "azurerm" {
  features {
    key_vault {
      purge_soft_delete_on_destroy = false
    }
  }
}

# Variables
variable "resource_group_name" {
  description = "Name of the resource group"
  type        = string
}

variable "location" {
  description = "Azure region for resources"
  type        = string
  default     = "eastus"
}

variable "storage_account_name" {
  description = "Name of the storage account (must be globally unique)"
  type        = string

  validation {
    condition     = can(regex("^[a-z0-9]{3,24}$", var.storage_account_name))
    error_message = "Storage account name must be 3-24 characters, lowercase letters and numbers only."
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

variable "container_name" {
  description = "Name of the blob container"
  type        = string
  default     = "secure-data"
}

variable "soft_delete_retention_days" {
  description = "Number of days to retain soft-deleted blobs"
  type        = number
  default     = 30

  validation {
    condition     = var.soft_delete_retention_days >= 1 && var.soft_delete_retention_days <= 365
    error_message = "Soft delete retention must be between 1 and 365 days."
  }
}

variable "enable_customer_managed_key" {
  description = "Use customer-managed key for encryption"
  type        = bool
  default     = false
}

# Resource Group (if not existing)
resource "azurerm_resource_group" "storage" {
  name     = var.resource_group_name
  location = var.location

  tags = {
    Environment = var.environment
    Security    = "ASVS-V5.3-Compliant"
    ManagedBy   = "Terraform"
  }
}

# ASVS V5.3: Secure Storage Account
resource "azurerm_storage_account" "secure_storage" {
  name                = var.storage_account_name
  resource_group_name = azurerm_resource_group.storage.name
  location            = azurerm_resource_group.storage.location

  # Use Standard_GRS for production (geo-redundant)
  account_tier             = "Standard"
  account_replication_type = var.environment == "prod" ? "GRS" : "LRS"
  account_kind             = "StorageV2"

  # ASVS V5.3.3: Enforce HTTPS and minimum TLS 1.2
  enable_https_traffic_only = true
  min_tls_version           = "TLS1_2"

  # ASVS V5.3.4: Disable public blob access
  allow_nested_items_to_be_public = false
  public_network_access_enabled   = true # Set to false if using Private Endpoints

  # ASVS V5.3.3: Enable infrastructure encryption (double encryption)
  infrastructure_encryption_enabled = var.environment == "prod"

  # Shared access key is required for some operations but should be rotated
  shared_access_key_enabled = true

  # ASVS V5.3.1: Blob properties for versioning and soft delete
  blob_properties {
    versioning_enabled = true

    delete_retention_policy {
      days = var.soft_delete_retention_days
    }

    container_delete_retention_policy {
      days = var.soft_delete_retention_days
    }

    change_feed_enabled = var.environment == "prod"
  }

  # Network rules - restrict access
  network_rules {
    default_action = "Deny"
    bypass         = ["AzureServices", "Logging", "Metrics"]
    ip_rules       = [] # Add allowed IPs here
    # virtual_network_subnet_ids = []  # Add VNet subnet IDs here
  }

  tags = {
    Environment = var.environment
    Security    = "ASVS-V5.3-Compliant"
    ManagedBy   = "Terraform"
  }
}

# ASVS V5.3.4: Private container (no public access)
resource "azurerm_storage_container" "secure_container" {
  name                  = var.container_name
  storage_account_name  = azurerm_storage_account.secure_storage.name
  container_access_type = "private" # Never use "blob" or "container"
}

# Advanced Threat Protection (optional but recommended for prod)
resource "azurerm_advanced_threat_protection" "storage" {
  count              = var.environment == "prod" ? 1 : 0
  target_resource_id = azurerm_storage_account.secure_storage.id
  enabled            = true
}

# Diagnostic settings for logging (requires Log Analytics workspace)
# Uncomment and configure if you have a Log Analytics workspace
#
# resource "azurerm_monitor_diagnostic_setting" "storage" {
#   name                       = "storage-diagnostics"
#   target_resource_id         = "${azurerm_storage_account.secure_storage.id}/blobServices/default"
#   log_analytics_workspace_id = var.log_analytics_workspace_id
#
#   enabled_log {
#     category = "StorageRead"
#   }
#
#   enabled_log {
#     category = "StorageWrite"
#   }
#
#   enabled_log {
#     category = "StorageDelete"
#   }
#
#   metric {
#     category = "Transaction"
#     enabled  = true
#   }
# }

# Outputs
output "storage_account_id" {
  description = "The ID of the storage account"
  value       = azurerm_storage_account.secure_storage.id
}

output "storage_account_name" {
  description = "The name of the storage account"
  value       = azurerm_storage_account.secure_storage.name
}

output "primary_blob_endpoint" {
  description = "The primary blob endpoint"
  value       = azurerm_storage_account.secure_storage.primary_blob_endpoint
}

output "container_name" {
  description = "The name of the blob container"
  value       = azurerm_storage_container.secure_container.name
}

output "security_controls" {
  description = "Security controls applied to this storage account"
  value = {
    encryption                 = "Microsoft-managed (AES-256)"
    infrastructure_encryption  = var.environment == "prod" ? "Enabled (double encryption)" : "Disabled"
    public_blob_access         = "Disabled"
    container_access           = "Private"
    https_only                 = "Enforced"
    min_tls_version            = "TLS 1.2"
    versioning                 = "Enabled"
    soft_delete_blob           = "${var.soft_delete_retention_days} days"
    soft_delete_container      = "${var.soft_delete_retention_days} days"
    advanced_threat_protection = var.environment == "prod" ? "Enabled" : "Disabled"
    network_default_action     = "Deny"
  }
}

# Connection string (sensitive - use Azure Key Vault in production)
output "primary_connection_string" {
  description = "The primary connection string for the storage account"
  value       = azurerm_storage_account.secure_storage.primary_connection_string
  sensitive   = true
}
