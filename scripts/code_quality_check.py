#!/usr/bin/env python3
"""
Android & Flutter Code Quality & Security Checker
Performs static analysis on Kotlin (.kt) and Dart (.dart) files.
"""

import sys
import os
import re
from pathlib import Path


SECURITY_RULES = [
    {
        "id": "CWE-798",
        "name": "Hardcoded Secrets / API Keys",
        "severity": "HIGH",
        "pattern": re.compile(
            r'(api[_-]?key|secret[_-]?key|auth[_-]?token|password)\s*[:=]\s*["\']([A-Za-z0-9_\-\.]{12,})["\']',
            re.IGNORECASE
        ),
        "recommendation": "Move secrets to BuildConfig, local.properties, or CI/CD environment variables."
    },
    {
        "id": "CWE-312",
        "name": "Cleartext Shared Preferences",
        "severity": "MEDIUM",
        "pattern": re.compile(
            r'(getSharedPreferences|SharedPreferences\.getInstance)\(',
            re.IGNORECASE
        ),
        "recommendation": "Use EncryptedSharedPreferences (Android) or flutter_secure_storage (Flutter) for sensitive data."
    },
    {
        "id": "CWE-319",
        "name": "Cleartext HTTP Connection",
        "severity": "HIGH",
        "pattern": re.compile(r'["\']http://[a-zA-Z0-9\.\-_]+'),
        "recommendation": "Enforce HTTPS traffic. Configure NetworkSecurityConfig to disallow cleartext traffic."
    },
    {
        "id": "QUALITY-001",
        "name": "GlobalScope Usage in Coroutines",
        "severity": "MEDIUM",
        "pattern": re.compile(r'GlobalScope\.(launch|async)'),
        "recommendation": "Use lifecycleScope, viewModelScope, or a structured CoroutineScope."
    },
    {
        "id": "QUALITY-002",
        "name": "Uncontrolled Empty Catch Block",
        "severity": "LOW",
        "pattern": re.compile(r'catch\s*\([^\)]+\)\s*\{\s*\}'),
        "recommendation": "Log or gracefully handle errors; do not swallow exceptions silently."
    },
    {
        "id": "QUALITY-003",
        "name": "Unsafe Null Assertion Operator",
        "severity": "LOW",
        "pattern": re.compile(r'[a-zA-Z0-9_\)]![\.\(]'),
        "recommendation": "Avoid force-unwrapping (!); use safe calls (?.) or pattern matching."
    },
    {
        "id": "QUALITY-004",
        "name": "Non-Lifecycle-Aware Flow Collection in Compose",
        "severity": "MEDIUM",
        "pattern": re.compile(r'\.collectAsState\(\s*\)'),
        "recommendation": "Use collectAsStateWithLifecycle() to stop Flow collection when app is in the background."
    },
    {
        "id": "QUALITY-005",
        "name": "Hardcoded Color Literal in UI Code",
        "severity": "LOW",
        "pattern": re.compile(r'Color\s*\(\s*0x[0-9a-fA-F]{6,8}\s*\)'),
        "recommendation": "Use MaterialTheme.colorScheme or colorResource() to support dynamic theming."
    }
]


def audit_file(file_path: Path):
    issues = []
    try:
        content = file_path.read_text(errors="ignore")
    except Exception as e:
        return issues

    lines = content.splitlines()
    for line_idx, line in enumerate(lines, start=1):
        # Skip commented lines
        stripped = line.strip()
        if stripped.startswith("//") or stripped.startswith("/*") or stripped.startswith("*"):
            continue

        for rule in SECURITY_RULES:
            if rule["pattern"].search(line):
                issues.append({
                    "file": str(file_path),
                    "line": line_idx,
                    "code": line.strip()[:100],
                    "rule_id": rule["id"],
                    "name": rule["name"],
                    "severity": rule["severity"],
                    "recommendation": rule["recommendation"]
                })
    return issues


def scan_directory(target: Path):
    results = []
    extensions = {".kt", ".dart", ".java"}

    for root, _, files in os.walk(target):
        for f in files:
            p = Path(root) / f
            if p.suffix in extensions:
                file_issues = audit_file(p)
                results.extend(file_issues)
    return results


def main():
    target = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd()
    if not target.exists():
        print(f"Error: Path '{target}' does not exist.")
        sys.exit(1)

    print(f"🔍 Scanning '{target}' for Android & Flutter code quality and security issues...\n")
    issues = scan_directory(target) if target.is_dir() else audit_file(target)

    if not issues:
        print("✅ No security vulnerabilities or critical code quality issues detected! Score: 100/100")
        return

    high_count = sum(1 for i in issues if i["severity"] == "HIGH")
    med_count = sum(1 for i in issues if i["severity"] == "MEDIUM")
    low_count = sum(1 for i in issues if i["severity"] == "LOW")

    score = max(0, 100 - (high_count * 20 + med_count * 10 + low_count * 3))

    print(f"📊 Audit Summary: {len(issues)} issues found (Score: {score}/100)")
    print(f"   🔴 High: {high_count} | 🟡 Medium: {med_count} | 🔵 Low: {low_count}\n")

    for idx, item in enumerate(issues, start=1):
        print(f"[{idx}] {item['severity']} - {item['rule_id']}: {item['name']}")
        print(f"    File: {item['file']}:{item['line']}")
        print(f"    Code: {item['code']}")
        print(f"    Fix:  {item['recommendation']}\n")


if __name__ == "__main__":
    main()
