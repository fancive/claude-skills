---
description: Run E2E tests using Claude in Chrome. Real browser automation with screenshots and GIF recording.
---

# /e2e

Run end-to-end browser tests using Claude in Chrome.

## Prerequisites

- Claude in Chrome extension installed
- Browser tab available

## Usage

```bash
/e2e test login flow on https://example.com
/e2e verify search works on current page
/e2e record checkout flow with GIF
```

## What It Does

1. Opens browser tab (or uses current)
2. Executes test steps (navigate, click, fill, verify)
3. Takes screenshots at each step
4. Records GIF (optional)
5. Generates test report

## Example

```
/e2e test login flow on https://myapp.com

Agent will:
1. Navigate to https://myapp.com/login
2. Find and fill email input
3. Find and fill password input
4. Click login button
5. Verify redirect to dashboard
6. Screenshot each step
7. Generate report
```

## Output

```
E2E Test: Login Flow
Status: ✅ PASS

Steps:
1. ✅ Navigate to /login
2. ✅ Fill email field
3. ✅ Fill password field
4. ✅ Click login button
5. ✅ Verify dashboard loaded

Screenshots: artifacts/e2e-login-*.png
Recording: artifacts/e2e-login.gif
```

## Options

| Flag | Description |
|------|-------------|
| `--record` | Record test as GIF |
| `--verbose` | Show detailed step output |
| `--continue-on-fail` | Don't stop on first failure |

## Test Patterns

```bash
/e2e test login flow           # Auth testing
/e2e test search for "query"   # Search testing
/e2e test form submission      # Form testing
/e2e verify element exists     # Element check
/e2e record user journey       # Full flow with GIF
```

## Artifacts

```
artifacts/
├── e2e-{test}-step-1.png
├── e2e-{test}-step-2.png
├── e2e-{test}.gif
└── e2e-{test}-report.md
```

## vs Playwright

| /e2e (Chrome) | Playwright |
|---------------|------------|
| Real-time execution | Generates test files |
| Visual feedback | Headless by default |
| One-off testing | Repeatable CI/CD |
| Immediate results | Scripted automation |

Use `/e2e` for exploratory testing and quick verification.
Use Playwright for CI/CD integration.
