# Secure Coding Pattern: Secure File Uploads (Node.js/Express)

This guide provides the approved method for implementing secure file upload
functionality in Node.js applications using Express and Multer.

- **Relevant ASVS Requirements:** V5.2.1 (File Size), V5.2.2 (File Type),
  V5.3.1 (Execution), V5.3.2 (Path Traversal)
- **Related Pattern:** `../../Patterns/Secure-File-Uploads.md`

---

## Principle: Defense in Depth

File uploads are a high-risk feature. Every uploaded file must be treated as
potentially malicious. This implementation uses multiple layers of validation:

1. **Size limits** enforced at the middleware level
2. **File type validation** using magic bytes (not just extension)
3. **Secure storage** with randomized filenames outside web root
4. **Content scanning** integration point for antivirus

---

## Implementation

### Dependencies

```bash
npm install express multer file-type uuid
```

| Package | Purpose |
|---------|---------|
| `express` | Web framework |
| `multer` | Multipart form handling |
| `file-type` | Magic byte detection |
| `uuid` | Secure filename generation |

### Complete Implementation

```javascript
// secure-upload.js
// ASVS V5.2, V5.3: Secure file upload implementation

const express = require('express');
const multer = require('multer');
const { fileTypeFromBuffer } = require('file-type');
const { v4: uuidv4 } = require('uuid');
const path = require('path');
const fs = require('fs').promises;

const app = express();

// ASVS V5.3.2: Store files outside the web root
const UPLOAD_DIR = process.env.UPLOAD_DIR || '/var/secure_uploads';

// ASVS V5.2.1: Maximum file size (5MB)
const MAX_FILE_SIZE = 5 * 1024 * 1024;

// ASVS V5.2.2: Allowed MIME types (strict allow-list)
const ALLOWED_MIME_TYPES = new Set([
  'image/jpeg',
  'image/png',
  'image/gif',
  'application/pdf'
]);

// ASVS V5.2.2: Map MIME types to allowed extensions
const MIME_TO_EXT = {
  'image/jpeg': '.jpg',
  'image/png': '.png',
  'image/gif': '.gif',
  'application/pdf': '.pdf'
};

// Configure multer for memory storage (validate before saving)
const upload = multer({
  storage: multer.memoryStorage(),
  limits: {
    fileSize: MAX_FILE_SIZE,
    files: 1
  }
});

/**
 * Validates file content using magic bytes.
 * ASVS V5.2.2: Never trust client-provided Content-Type or extension.
 */
async function validateFileType(buffer) {
  const type = await fileTypeFromBuffer(buffer);

  if (!type) {
    return { valid: false, error: 'Unable to determine file type' };
  }

  if (!ALLOWED_MIME_TYPES.has(type.mime)) {
    return { valid: false, error: 'File type not allowed' };
  }

  return { valid: true, mime: type.mime, ext: MIME_TO_EXT[type.mime] };
}

/**
 * Generates a secure, random filename.
 * ASVS V5.3.2: Prevents path traversal by never using user input.
 */
function generateSecureFilename(extension) {
  return `${uuidv4()}${extension}`;
}

/**
 * Saves file to secure storage location.
 * ASVS V5.3.2: Ensures file is stored outside web-accessible paths.
 */
async function saveFile(buffer, filename) {
  await fs.mkdir(UPLOAD_DIR, { recursive: true });

  const filePath = path.join(UPLOAD_DIR, filename);

  // Verify the resolved path is within UPLOAD_DIR (path traversal defense)
  const resolvedPath = path.resolve(filePath);
  if (!resolvedPath.startsWith(path.resolve(UPLOAD_DIR))) {
    throw new Error('Invalid file path');
  }

  await fs.writeFile(resolvedPath, buffer);
  return resolvedPath;
}

// File upload endpoint
app.post('/api/upload', upload.single('file'), async (req, res) => {
  try {
    if (!req.file) {
      return res.status(400).json({ error: 'No file provided' });
    }

    // ASVS V5.2.2: Validate file type using magic bytes
    const validation = await validateFileType(req.file.buffer);
    if (!validation.valid) {
      return res.status(400).json({ error: validation.error });
    }

    // ASVS V5.3.2: Generate secure filename
    const secureFilename = generateSecureFilename(validation.ext);

    // TODO: Integration point for malware scanning
    // await scanForMalware(req.file.buffer);

    // Save file to secure location
    const savedPath = await saveFile(req.file.buffer, secureFilename);

    // Return only the filename, not the full path
    res.status(201).json({
      message: 'File uploaded successfully',
      filename: secureFilename
    });

  } catch (error) {
    console.error('Upload error:', error.message);
    res.status(500).json({ error: 'File upload failed' });
  }
});

// Error handler for multer errors
app.use((error, req, res, next) => {
  if (error instanceof multer.MulterError) {
    if (error.code === 'LIMIT_FILE_SIZE') {
      return res.status(400).json({ error: 'File size exceeds limit' });
    }
    return res.status(400).json({ error: 'File upload error' });
  }
  next(error);
});

module.exports = { app, validateFileType, generateSecureFilename };
```

---

## Security Controls Summary

| ASVS Req | Control | Implementation |
|----------|---------|----------------|
| V5.2.1 | File size limit | `multer.limits.fileSize` |
| V5.2.2 | Type validation | `file-type` magic bytes |
| V5.3.1 | No execution | Store outside web root |
| V5.3.2 | Path traversal | UUID filename + path validation |

---

## Testing

```javascript
// test-upload.js
const request = require('supertest');
const { app } = require('./secure-upload');

describe('Secure File Upload', () => {
  it('rejects files exceeding size limit', async () => {
    const largeBuffer = Buffer.alloc(6 * 1024 * 1024); // 6MB
    const res = await request(app)
      .post('/api/upload')
      .attach('file', largeBuffer, 'large.jpg');
    expect(res.status).toBe(400);
  });

  it('rejects files with invalid magic bytes', async () => {
    const fakeJpg = Buffer.from('not a real image');
    const res = await request(app)
      .post('/api/upload')
      .attach('file', fakeJpg, 'fake.jpg');
    expect(res.status).toBe(400);
  });

  it('rejects disallowed file types', async () => {
    // Valid PNG magic bytes but testing allow-list
    const res = await request(app)
      .post('/api/upload')
      .attach('file', Buffer.from('MZ...'), 'malware.exe');
    expect(res.status).toBe(400);
  });
});
```

---

## Common Mistakes to Avoid

| Mistake | Risk | Mitigation |
|---------|------|------------|
| Trusting `Content-Type` header | File type spoofing | Use magic byte validation |
| Using original filename | Path traversal, overwrites | Generate UUID filename |
| Storing in `public/` or `static/` | Code execution | Store outside web root |
| No size limit | DoS via large files | Set `multer.limits.fileSize` |
| Block-list for extensions | Bypass via new extensions | Use strict allow-list |
