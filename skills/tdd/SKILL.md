---
name: tdd
description: Test-driven development workflow for implementing or refactoring code with tests-first, Red-Green-Refactor, and coverage targets. Use when the user asks for TDD, tests-first, write failing tests before code, or mentions /tdd.
---

# TDD

## Overview

Apply a strict tests-first workflow: define interfaces, write failing tests, implement minimal code, refactor safely, and keep coverage targets.

## Workflow

1. Clarify scope and risk
   - Restate the feature/bug and identify key edge cases.
   - Confirm environment/test runner if unclear.

2. Define interfaces/types
   - Specify public APIs, inputs/outputs, and error behavior.
   - If existing code dictates signatures, align with current patterns.

3. Write failing tests (RED)
   - Cover normal cases, edge cases, and regressions.
   - Run tests to confirm failure.

4. Implement minimal code (GREEN)
   - Add the smallest change that makes tests pass.
   - Re-run tests and confirm success.

5. Refactor (REFACTOR)
   - Improve clarity/perf while keeping tests green.
   - Re-run tests.

6. Coverage and quality gate
   - Target **80%+** coverage overall.
   - Target **100%** for financial/auth/security/critical logic.
   - If coverage tooling is missing, propose the minimal setup.

## Output Expectations

- Show the RED/GREEN/REFACTOR sequence explicitly.
- Call out any assumptions or missing test tooling.
- Ask before expanding scope beyond the requested behavior.
