#!/usr/bin/env python3
"""
Android & Flutter Codebase Inspector
Scans target directory to identify platform, dependencies, package name, and architecture.
"""

import os
import sys
import json
import re
from pathlib import Path


def inspect_android(root_path: Path) -> dict:
    info = {
        "is_android": False,
        "build_system": None,
        "package_name": None,
        "dependencies": [],
        "detected_arch": "Unknown",
        "has_compose": False,
        "has_hilt": False
    }

    gradle_files = list(root_path.glob("**/build.gradle*"))
    manifests = list(root_path.glob("**/AndroidManifest.xml"))

    if not gradle_files and not manifests:
        return info

    info["is_android"] = True
    info["build_system"] = "Gradle (KTS)" if any(f.name.endswith(".kts") for f in gradle_files) else "Gradle (Groovy)"

    # Inspect manifest for package name
    for m in manifests:
        content = m.read_text(errors="ignore")
        pkg_match = re.search(r'package="([^"]+)"', content)
        if pkg_match:
            info["package_name"] = pkg_match.group(1)
            break

    # Inspect gradle files for dependencies
    dep_keywords = {
        "compose": "Jetpack Compose",
        "hilt": "Dagger Hilt",
        "koin": "Koin",
        "retrofit": "Retrofit",
        "room": "Room DB",
        "navigation-compose": "Navigation Compose",
        "lifecycle-viewmodel": "Jetpack ViewModel"
    }

    found_deps = set()
    for g in gradle_files:
        content = g.read_text(errors="ignore")
        for key, name in dep_keywords.items():
            if key in content.lower():
                found_deps.add(name)

    info["dependencies"] = sorted(list(found_deps))
    info["has_compose"] = "Jetpack Compose" in found_deps
    info["has_hilt"] = "Dagger Hilt" in found_deps

    # Arch heuristic
    kt_files = list(root_path.glob("**/*.kt"))
    has_vm = any("ViewModel" in f.name for f in kt_files)
    has_usecase = any("UseCase" in f.name for f in kt_files)
    has_presenter = any("Presenter" in f.name for f in kt_files)
    has_intent = any("Intent" in f.name or "Reducer" in f.name for f in kt_files)

    if has_usecase:
        info["detected_arch"] = "Clean Architecture"
    elif has_intent:
        info["detected_arch"] = "MVI"
    elif has_vm:
        info["detected_arch"] = "MVVM"
    elif has_presenter:
        info["detected_arch"] = "MVP"

    return info


def inspect_flutter(root_path: Path) -> dict:
    info = {
        "is_flutter": False,
        "app_name": None,
        "dependencies": [],
        "state_management": [],
        "detected_arch": "Unknown"
    }

    pubspec = root_path / "pubspec.yaml"
    if not pubspec.exists():
        for p in root_path.glob("**/pubspec.yaml"):
            pubspec = p
            break

    if not pubspec.exists():
        return info

    info["is_flutter"] = True
    content = pubspec.read_text(errors="ignore")

    name_match = re.search(r"^name:\s*([a-zA-Z0-9_-]+)", content, re.MULTILINE)
    if name_match:
        info["app_name"] = name_match.group(1)

    state_libs = {
        "flutter_bloc": "BLoC",
        "flutter_riverpod": "Riverpod",
        "provider": "Provider",
        "get": "GetX",
        "mobx": "MobX"
    }

    found_state = []
    for key, name in state_libs.items():
        if key in content:
            found_state.append(name)
    info["state_management"] = found_state

    # Arch heuristic
    dart_files = list(root_path.glob("**/*.dart"))
    has_features_dir = any("features" in str(f) for f in dart_files)
    has_usecase = any("usecase" in f.name.lower() for f in dart_files)
    has_bloc = any("bloc" in f.name.lower() or "cubit" in f.name.lower() for f in dart_files)

    if has_features_dir and has_usecase:
        info["detected_arch"] = "Clean Architecture (Feature-First)"
    elif has_features_dir:
        info["detected_arch"] = "Feature-First"
    elif has_bloc:
        info["detected_arch"] = "BLoC Architecture"
    elif any("viewmodel" in f.name.lower() for f in dart_files):
        info["detected_arch"] = "MVVM"

    return info


def main():
    target = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd()
    if not target.exists():
        print(f"Error: Path '{target}' does not exist.")
        sys.exit(1)

    android_info = inspect_android(target)
    flutter_info = inspect_flutter(target)

    report = {
        "scanned_path": str(target.resolve()),
        "android": android_info,
        "flutter": flutter_info
    }

    print(json.dumps(report, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
