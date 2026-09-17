#!/usr/bin/env python3
"""Update managed firmware release links in README.md."""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import tempfile
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Any, Callable
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
README_PATH = ROOT / "README.md"
MANIFEST_PATH = ROOT / "firmware-archive.json"
REFERENCE_PATTERN = re.compile(r"^\[(?P<id>[qz]\d+)\]:\s+(?P<url>\S+)$", re.MULTILINE)
GITHUB_HOST = "github.com"
API_ROOT = "https://api.github.com"
EXPECTED_STATIC_REFERENCES = {"z00", "z01"}
EXPECTED_MANAGED_COUNTS = {"qmk": 15, "zmk": 30}
RELEASES_PER_PAGE = 30
MAX_RELEASE_PAGES = 3


@dataclass(frozen=True)
class SourceSpec:
    repository: str
    tag_pattern: re.Pattern[str]
    reference_pattern: re.Pattern[str]
    asset_name: Callable[[str, str], str]


SOURCES = {
    "qmk": SourceSpec(
        repository="ergohaven/vial-qmk",
        tag_pattern=re.compile(r"^(\d+)\.(\d+)\.(\d+)$"),
        reference_pattern=re.compile(r"^q\d+$"),
        asset_name=lambda tag, key: f"{tag}_{key}.uf2",
    ),
    "zmk": SourceSpec(
        repository="ergohaven/ergohaven-zmk",
        tag_pattern=re.compile(r"^(\d{4})\.(\d{2})\.(\d{2})$"),
        reference_pattern=re.compile(r"^z\d+$"),
        asset_name=lambda _tag, key: key,
    ),
}


class ArchiveError(RuntimeError):
    """A safe, user-facing archive update failure."""


def version_tuple(source: str, tag: str) -> tuple[int, int, int] | None:
    match = SOURCES[source].tag_pattern.fullmatch(tag)
    if not match:
        return None
    version = tuple(map(int, match.groups()))
    if source == "zmk":
        try:
            date(*version)
        except ValueError:
            return None
    return version


def load_manifest() -> tuple[dict[str, dict[str, str]], dict[str, str]]:
    try:
        data = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise ArchiveError(f"cannot read {MANIFEST_PATH.name}: {error}") from error

    if not isinstance(data, dict) or set(data) != {"managed", "static"}:
        raise ArchiveError("manifest must contain exactly 'managed' and 'static'")

    managed = data["managed"]
    static = data["static"]
    if not isinstance(managed, dict) or set(managed) != set(SOURCES):
        raise ArchiveError("manifest managed sources must be exactly qmk and zmk")
    if not isinstance(static, dict) or set(static) != EXPECTED_STATIC_REFERENCES:
        raise ArchiveError("manifest static references must be exactly z00 and z01")

    all_ids: set[str] = set()
    for source, spec in SOURCES.items():
        mapping = managed[source]
        if not isinstance(mapping, dict) or not mapping:
            raise ArchiveError(f"manifest source {source} must contain references")
        if len(mapping) != EXPECTED_MANAGED_COUNTS[source]:
            raise ArchiveError(
                f"manifest source {source} must contain {EXPECTED_MANAGED_COUNTS[source]} references"
            )
        for reference, key in mapping.items():
            if not isinstance(reference, str) or not spec.reference_pattern.fullmatch(reference):
                raise ArchiveError(f"invalid {source} reference: {reference!r}")
            if reference in all_ids:
                raise ArchiveError(f"duplicate manifest reference: {reference}")
            if not isinstance(key, str) or not re.fullmatch(r"[a-z0-9][a-z0-9_.-]*", key):
                raise ArchiveError(f"invalid asset key for {reference}")
            all_ids.add(reference)

    for reference, url in static.items():
        if reference in all_ids or not isinstance(url, str):
            raise ArchiveError(f"invalid static reference: {reference}")
        all_ids.add(reference)

    return managed, static


def read_references(readme: str) -> dict[str, str]:
    references: dict[str, str] = {}
    for match in REFERENCE_PATTERN.finditer(readme):
        reference = match.group("id")
        if reference in references:
            raise ArchiveError(f"duplicate README reference: {reference}")
        references[reference] = match.group("url")
    return references


def parse_download_url(source: str, tag: str, expected_asset: str, value: str) -> bool:
    spec = SOURCES[source]
    parsed = urlparse(value)
    parts = parsed.path.strip("/").split("/")
    expected_path = [*spec.repository.split("/"), "releases", "download", tag, expected_asset]
    return (
        parsed.scheme == "https"
        and parsed.netloc == GITHUB_HOST
        and not parsed.params
        and not parsed.query
        and not parsed.fragment
        and parts == expected_path
    )


def validate_readme(
    readme: str,
    managed: dict[str, dict[str, str]],
    static: dict[str, str],
) -> tuple[dict[str, str], dict[str, str]]:
    references = read_references(readme)
    expected_ids = set(static)
    for mapping in managed.values():
        expected_ids.update(mapping)
    if set(references) != expected_ids:
        missing = sorted(expected_ids - set(references))
        unexpected = sorted(set(references) - expected_ids)
        raise ArchiveError(f"README reference set mismatch; missing={missing}, unexpected={unexpected}")

    current_tags: dict[str, str] = {}
    for source, mapping in managed.items():
        spec = SOURCES[source]
        tags: set[str] = set()
        for reference, key in mapping.items():
            value = references[reference]
            parsed = urlparse(value)
            parts = parsed.path.strip("/").split("/")
            if len(parts) != 6:
                raise ArchiveError(f"invalid release URL for {reference}")
            tag = parts[4]
            expected_asset = spec.asset_name(tag, key)
            if version_tuple(source, tag) is None or not parse_download_url(source, tag, expected_asset, value):
                raise ArchiveError(f"invalid managed URL for {reference}")
            tags.add(tag)
        if len(tags) != 1:
            raise ArchiveError(f"{source} references must use one release cohort")
        current_tags[source] = tags.pop()

    for reference, expected_url in static.items():
        if references[reference] != expected_url:
            raise ArchiveError(f"static reference {reference} changed")

    return references, current_tags


def fetch_releases(source: str) -> list[dict[str, Any]]:
    repository = SOURCES[source].repository
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "ergohaven-keymap-hub-firmware-archive",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    token = os.environ.get("GITHUB_TOKEN", "").strip()
    if token:
        headers["Authorization"] = f"Bearer {token}"

    releases: list[dict[str, Any]] = []
    for page in range(1, MAX_RELEASE_PAGES + 1):
        url = (
            f"{API_ROOT}/repos/{repository}/releases"
            f"?per_page={RELEASES_PER_PAGE}&page={page}"
        )
        request = Request(url, headers=headers)
        try:
            with urlopen(request, timeout=30) as response:
                release_page = json.load(response)
        except (HTTPError, URLError, TimeoutError, json.JSONDecodeError) as error:
            raise ArchiveError(f"GitHub API request failed for {repository}: {error}") from error

        if not isinstance(release_page, list):
            raise ArchiveError(f"GitHub API returned invalid releases for {repository}")
        releases.extend(release for release in release_page if isinstance(release, dict))
        if len(release_page) < RELEASES_PER_PAGE:
            break
    return releases


def trusted_asset_url(source: str, release: dict[str, Any], expected_name: str) -> str | None:
    assets = release.get("assets")
    if not isinstance(assets, list):
        return None
    matches = [asset for asset in assets if isinstance(asset, dict) and asset.get("name") == expected_name]
    if len(matches) != 1:
        return None

    asset = matches[0]
    size = asset.get("size")
    url = asset.get("browser_download_url")
    tag = release.get("tag_name")
    if (
        asset.get("state") != "uploaded"
        or isinstance(size, bool)
        or not isinstance(size, int)
        or size <= 0
        or not isinstance(url, str)
        or not isinstance(tag, str)
        or not parse_download_url(source, tag, expected_name, url)
    ):
        return None
    return url


def select_complete_release(
    source: str,
    mapping: dict[str, str],
    releases: list[dict[str, Any]],
) -> tuple[str, dict[str, str]]:
    candidates: list[tuple[tuple[int, int, int], dict[str, Any]]] = []
    for release in releases:
        if (
            not isinstance(release, dict)
            or release.get("draft") is not False
            or release.get("prerelease") is not False
            or not isinstance(release.get("published_at"), str)
        ):
            continue
        tag = release.get("tag_name")
        parsed_version = version_tuple(source, tag) if isinstance(tag, str) else None
        if parsed_version is not None:
            candidates.append((parsed_version, release))

    for _version, release in sorted(candidates, key=lambda candidate: candidate[0], reverse=True):
        tag = release["tag_name"]
        resolved: dict[str, str] = {}
        for reference, key in mapping.items():
            expected_name = SOURCES[source].asset_name(tag, key)
            url = trusted_asset_url(source, release, expected_name)
            if url is None:
                break
            resolved[reference] = url
        if len(resolved) == len(mapping):
            return tag, resolved

    raise ArchiveError(f"no complete stable {source} release contains all managed assets")


def render_readme(readme: str, replacements: dict[str, str]) -> str:
    def replace(match: re.Match[str]) -> str:
        reference = match.group("id")
        if reference not in replacements:
            return match.group(0)
        return f"[{reference}]: {replacements[reference]}"

    return REFERENCE_PATTERN.sub(replace, readme)


def write_atomic(path: Path, content: str) -> None:
    mode = path.stat().st_mode
    with tempfile.NamedTemporaryFile(
        mode="w",
        encoding="utf-8",
        newline="",
        dir=path.parent,
        prefix=f".{path.name}.",
        delete=False,
    ) as handle:
        handle.write(content)
        temporary = Path(handle.name)
    os.chmod(temporary, mode)
    os.replace(temporary, path)


def update_archive(write: bool) -> int:
    managed, static = load_manifest()
    try:
        readme = README_PATH.read_text(encoding="utf-8")
    except OSError as error:
        raise ArchiveError(f"cannot read {README_PATH.name}: {error}") from error

    _references, current_tags = validate_readme(readme, managed, static)
    replacements: dict[str, str] = {}
    selected_tags: dict[str, str] = {}

    for source, mapping in managed.items():
        selected_tag, resolved = select_complete_release(source, mapping, fetch_releases(source))
        current_version = version_tuple(source, current_tags[source])
        selected_version = version_tuple(source, selected_tag)
        if current_version is None or selected_version is None or selected_version < current_version:
            raise ArchiveError(f"refusing to downgrade {source} from {current_tags[source]} to {selected_tag}")
        selected_tags[source] = selected_tag
        replacements.update(resolved)

    updated = render_readme(readme, replacements)
    validate_readme(updated, managed, static)

    summary = ", ".join(f"{source} {current_tags[source]} -> {selected_tags[source]}" for source in SOURCES)
    if updated == readme:
        print(f"Firmware archive is current: {summary}")
        return 0
    if not write:
        print(f"Firmware archive needs an update: {summary}", file=sys.stderr)
        return 1

    write_atomic(README_PATH, updated)
    print(f"Updated firmware archive: {summary}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true", help="write updated links to README.md")
    mode.add_argument("--check", action="store_true", help="fail when README.md is not current")
    arguments = parser.parse_args()

    try:
        return update_archive(write=arguments.write)
    except ArchiveError as error:
        print(f"error: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
