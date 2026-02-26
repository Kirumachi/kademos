# Kademos Troubleshooting

## Common Issues

### "Source file not found"

Kademos expects ASVS reference files in `01-ASVS-Core-Reference/`. Ensure you run from the project root or pass `--base-path` to point to the directory containing that folder.

```bash
kademos scan . --base-path /path/to/repo
```

### "Path not found"

Verify the scan path exists and is readable.

```bash
kademos scan ./my-repo --level 2
```

### CI/CD Integration

For GitHub Actions, use the Kademos Scan action:

```yaml
- name: Kademos Scan
  uses: ./.github/actions/kademos-scan
  with:
    path: '.'
    level: '2'
```
