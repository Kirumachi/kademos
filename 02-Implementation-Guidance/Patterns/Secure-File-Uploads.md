# Secure Coding Pattern: Secure File Uploads

## Overview

File upload functionality is an extremely high-risk feature. Every file uploaded by a user must be treated as hostile, as it could contain malware, a web shell for remote code execution, or be crafted to cause a denial-of-service (DoS) attack.

Proper file handling is a critical defense for any application. It requires a multi-layered validation strategy and secure storage configurations to protect against server compromise, data breaches, and the spread of viruses.

* **Relevant ASVS Requirements:** V5.2.1 (File Size), V5.2.2 (File Type/Content), V5.3.1 (Execution), V5.3.2 (Path Traversal)

---

## Principle: A Multi-Layered Defense

A secure file upload process involves three distinct stages, all performed on the server-side. Never trust any information provided by the client, including the filename, extension, or `Content-Type` header.

| ASVS Requirement | Principle | Mitigation Technique |
| :--- | :--- | :--- |
| **V5.2.1** | **Size Validation** | Restrict the maximum file size to prevent DoS attacks. |
| **V5.2.2** | **Type Validation** | Use an allow-list for extensions and verify the file's actual type using its "magic bytes." |
| **V5.3.2** | **Path Traversal Prevention** | Never use a user-provided filename for storage. Generate a new, random filename and store it in a non-executable location. |
| **V5.4.3** | **Malware Prevention** | Scan files for malware before making them available to other users. |

---

## 1. Implementation Strategy

### A. Strict Validation on the Server

If any of these server-side checks fail, the file must be rejected immediately.

1.  **Enforce File Size Limit:** Reject any file that exceeds a predefined maximum size.
2.  **Validate File Extension:** Check the extension against a strict **allow-list** of permitted types (e.g., `['.jpg', '.png']`).
3.  **Verify Magic Bytes:** Read the file's initial bytes to confirm its content actually matches its extension. A file named `avatar.jpg` could be a malicious script.
4.  **Scan for Malware:** Pass the validated file to an antivirus or malware scanner.

### B. Secure Storage

1.  **Store Files Outside the Web Root:** Never save uploaded files to a directory that the web server can execute (e.g., `/var/www/uploads`). The preferred approach is to use a separate object store like Amazon S3 or Azure Blob Storage.
2.  **Generate a Random Filename:** Do not use the user-provided filename. Generate a new, random identifier (e.g., a UUID) for the stored file to prevent path traversal attacks.

---

## 2. Code Examples

### Java (Spring Boot)

This example shows a service method for storing a file securely, combining multiple validation steps.

```java
import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;
import java.io.InputStream;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.nio.file.StandardCopyOption;
import java.util.UUID;
import org.apache.tika.Tika; // Apache Tika for magic byte detection

@Service
public class FileStorageService {

    // ASVS V5.3.2: Store files in a configured, non-web-accessible path.
    private final Path rootLocation = Paths.get("/var/secure_uploads");
    private final long MAX_FILE_SIZE = 5 * 1024 * 1024; // 5MB

    public String store(MultipartFile file) {
        try {
            // ASVS V5.2.1: Check file size.
            if (file.getSize() > MAX_FILE_SIZE) {
                throw new StorageException("Failed to store file: size exceeds limit.");
            }

            // ASVS V5.2.2: Validate file type using magic bytes with Apache Tika.
            Tika tika = new Tika();
            String detectedType = tika.detect(file.getInputStream());
            if (!isValidMimeType(detectedType)) {
                 throw new StorageException("File validation failed: Invalid content type.");
            }

            // ASVS V5.3.2: Generate a new, random filename.
            String extension = getFileExtension(file.getOriginalFilename());
            String newFilename = UUID.randomUUID().toString() + extension;

            // TODO: Pass the file to a malware scanner here.

            // Copy the file to the secure storage location.
            Path destinationFile = this.rootLocation.resolve(newFilename).normalize().toAbsolutePath();
            try (InputStream inputStream = file.getInputStream()) {
                Files.copy(inputStream, destinationFile, StandardCopyOption.REPLACE_EXISTING);
            }
            
            // Return the new filename to be stored in the database.
            return newFilename;

        } catch (Exception e) {
            throw new StorageException("Failed to store file.", e);
        }
    }
    
    private boolean isValidMimeType(String mimeType) {
        // Use a strict allow-list for MIME types.
        return "image/jpeg".equals(mimeType) || "image/png".equals(mimeType);
    }
    
    private String getFileExtension(String filename) {
        return filename.substring(filename.lastIndexOf("."));
    }
}
```
### C# (.NET Core)

This example shows an action method in an ASP.NET Core controller for handling a file upload.

```c#
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Http;
using System.IO;
using System.Threading.Tasks;
using System;

[ApiController]
[Route("api/[controller]")]
public class UploadController : ControllerBase
{
    // ASVS V5.3.2: Path should be configured outside the web root (wwwroot).
    private readonly string _uploadPath = "/var/secure_uploads";
    private const long _maxFileSize = 5 * 1024 * 1024; // 5MB
    private readonly string[] _allowedExtensions = { ".jpg", ".png" };

    [HttpPost]
    public async Task<IActionResult> Upload(IFormFile file)
    {
        // ASVS V5.2.1: Check file size.
        if (file.Length > _maxFileSize)
        {
            return BadRequest("File size exceeds the limit.");
        }

        var extension = Path.GetExtension(file.FileName).ToLowerInvariant();

        // ASVS V5.2.2: Use a strict allow-list for extensions.
        if (string.IsNullOrEmpty(extension) || !_allowedExtensions.Contains(extension))
        {
            return BadRequest("Invalid file type.");
        }

        // TODO: Add magic byte validation here using a library or custom logic.
        // TODO: Pass the file stream to a malware scanner.

        try
        {
            // ASVS V5.3.2: Generate a unique filename to prevent overwrites and path traversal.
            var newFileName = $"{Guid.NewGuid()}{extension}";
            var fullPath = Path.Combine(_uploadPath, newFileName);

            // Ensure the directory exists.
            Directory.CreateDirectory(_uploadPath);

            using (var stream = new FileStream(fullPath, FileMode.Create))
            {
                await file.CopyToAsync(stream);
            }

            // Return a reference to the new file.
            return Ok(new { FileName = newFileName });
        }
        catch (Exception)
        {
            return StatusCode(500, "An error occurred during file upload.");
        }
    }
}
```

## 3. Common Mistakes to Avoid

| Mistake | Description & Risk | Mitigation |
| :--- | :--- | :--- |
| **Trusting Client-Provided Info** | Relying on the `Content-Type` header or the filename extension sent by the client. Both can be easily faked by an attacker. | **Always verify the file's actual content** on the server using its binary header data (magic bytes). |
| **Using a Block-List** | Attempting to ban dangerous extensions (e.g., `.exe`, `.php`). Attackers constantly find new extensions or bypass methods. | Only permit specific file types and extensions defined in a strict **allow-list**. |
| **Storing in the Web Root** | Placing files in a public directory (e.g., `wwwroot/uploads/`) where the web server might try to execute them if misinterpreted. | Store files in a separate, **non-web-accessible directory** or a dedicated object store that lacks execution privileges. |
| **Using the Original Filename** | Accepting a user-provided filename like `../../system.ini` risks path traversal attacks, allowing an attacker to overwrite critical system files. | **Generate a new, unique, random filename** (like a UUID) for every file saved to the server. |