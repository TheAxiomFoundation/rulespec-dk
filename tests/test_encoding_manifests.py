"""Manifest-sync guard: encoded modules and their signed apply manifests
must never drift apart.

axiom-encode's supervised apply writes a signed manifest under
``.axiom/encoding-manifests/…`` recording the sha256 of every file it
installed. A hand edit that skips the encoder leaves the manifest stale —
invisible drift between content and provenance. These tests make that
drift a CI failure (the same guard rulespec-us carries; adopted here as
wave-2 CI encodes land their manifests, rulespec-dk#17).

This file is also the canonical retired-manifest inventory that
axiom-encode's replace path reconciles (prepare_signed_backfill):
``KNOWN_RETIRED_SCHEMA_MANIFESTS`` must stay a single top-level
frozenset assignment.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from test_repository_layout import ROOT

MANIFEST_ROOT = ROOT / ".axiom" / "encoding-manifests"

#: Manifests whose primary module was retired without a replacement.
#: Empty: every dk manifest maps to a live module.
KNOWN_RETIRED_SCHEMA_MANIFESTS: frozenset[str] = frozenset()


def _manifest_paths() -> list[Path]:
    if not MANIFEST_ROOT.is_dir():
        return []
    return sorted(MANIFEST_ROOT.rglob("*.json"))


def test_manifest_applied_files_exist_and_match() -> None:
    """Every applied file a manifest records must exist with that sha256."""
    problems: list[str] = []
    for manifest_path in _manifest_paths():
        rel = manifest_path.relative_to(ROOT).as_posix()
        if rel in KNOWN_RETIRED_SCHEMA_MANIFESTS:
            continue
        manifest = json.loads(manifest_path.read_text())
        for entry in manifest.get("applied_files", []):
            target = ROOT / entry["path"]
            if not target.is_file():
                problems.append(f"{rel}: applied file missing: {entry['path']}")
                continue
            digest = hashlib.sha256(target.read_bytes()).hexdigest()
            if digest != entry["sha256"]:
                problems.append(
                    f"{rel}: {entry['path']} content drifted from its signed "
                    "manifest — re-encode through the supervised apply path"
                )
    assert not problems, "\n".join(problems)


def test_no_unknown_orphaned_manifests() -> None:
    """A manifest whose primary module vanished must be inventoried."""
    problems: list[str] = []
    for manifest_path in _manifest_paths():
        rel = manifest_path.relative_to(ROOT).as_posix()
        manifest = json.loads(manifest_path.read_text())
        applied = [entry["path"] for entry in manifest.get("applied_files", [])]
        primaries = [p for p in applied if not p.endswith(".test.yaml")]
        if primaries and not any((ROOT / p).is_file() for p in primaries):
            if rel not in KNOWN_RETIRED_SCHEMA_MANIFESTS:
                problems.append(
                    f"{rel}: primary module retired without an inventory entry"
                )
    assert not problems, "\n".join(problems)


def test_retired_inventory_entries_are_real() -> None:
    """Inventory entries must name manifests that actually exist."""
    for rel in sorted(KNOWN_RETIRED_SCHEMA_MANIFESTS):
        assert (ROOT / rel).is_file(), f"inventory names a missing manifest: {rel}"
