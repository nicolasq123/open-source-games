"""Read and search the upstream and supplemental open-source games catalog."""

import argparse
import re
import sys
from pathlib import Path
from urllib.request import urlopen


README_URL = "https://raw.githubusercontent.com/bobeff/open-source-games/main/README.md"
REFERENCES = Path(__file__).resolve().parents[1] / "references"
SNAPSHOT = REFERENCES / "catalog.md"
GITHUB_ADDITIONS = REFERENCES / "github-games.md"
GITHUB_REPOSITORY = re.compile(r"https?://(?:www\.)?github\.com/([\w.-]+/[\w.-]+)", re.IGNORECASE)
SECTION_HEADING = re.compile(r"^##[ \t]+(.+)$", re.MULTILINE)
NON_GAME_SECTIONS = {"table of contents", "other lists"}
LIST_ITEM = re.compile(r"^[ \t]*[-*+][ \t]+")
ENTRY_BOUNDARY = re.compile(r"(?=^[ \t]*[-*+][ \t]+|^#{3,6}[ \t]+)", re.MULTILINE)


def read_catalog(snapshot=False):
    if not snapshot:
        try:
            with urlopen(README_URL, timeout=15) as response:
                return response.read().decode("utf-8-sig")
        except (OSError, UnicodeError) as error:
            print(f"Unable to read live catalog ({error}). Using bundled snapshot.", file=sys.stderr)

    return SNAPSHOT.read_text(encoding="utf-8-sig")


def game_sections(readme):
    parts = SECTION_HEADING.split(readme)
    return {
        heading.strip(): body.strip("\r\n")
        for heading, body in zip(parts[1::2], parts[2::2])
        if heading.strip().casefold() not in NON_GAME_SECTIONS
    }


def read_github_additions(readme):
    report = GITHUB_ADDITIONS.read_text(encoding="utf-8-sig")
    introduction = SECTION_HEADING.split(report, maxsplit=1)[0].strip()
    seen = {repo.casefold().removesuffix(".git") for repo in GITHUB_REPOSITORY.findall(readme)}
    sections = {}
    for heading, body in game_sections(report).items():
        kept = []
        for entry in ENTRY_BOUNDARY.split(body):
            match = GITHUB_REPOSITORY.search(entry)
            if not LIST_ITEM.match(entry) or match is None:
                continue
            repo = match[1].casefold().removesuffix(".git")
            if repo in seen:
                continue
            seen.add(repo)
            kept.append(entry.strip())
        if kept:
            sections[heading] = "\n\n".join(kept)
    return introduction, sections


def merge_sections(upstream, additions):
    sections = upstream.copy()
    for heading, extra in additions.items():
        if heading in sections:
            sections[heading] += "\n\n" + extra
        else:
            sections[heading] = extra
    return sections


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("category", nargs="?", help="Exact game category heading")
    parser.add_argument("--all", action="store_true", help="Print the complete catalog in scope")
    parser.add_argument(
        "--scope", choices=("all", "upstream", "github"),
        help="Select both catalogs, the upstream README, or the curated GitHub additions",
    )
    parser.add_argument("--find", metavar="TEXT", help="Find entries containing a literal name or term")
    parser.add_argument(
        "--match", action="append", default=[], metavar="REGEX",
        help="Find candidate entries outside the selected category; may be repeated",
    )
    source = parser.add_mutually_exclusive_group()
    source.add_argument("--snapshot", action="store_true", help="Use the bundled upstream catalog")
    source.add_argument("--readme", type=Path, help="Use a different local upstream catalog file")
    args = parser.parse_args()
    scope = args.scope or ("upstream" if args.readme else "all")
    if args.all and (args.category or args.find or args.match):
        parser.error("--all cannot be combined with a category, --find or --match")

    terms = args.match
    if args.find:
        terms = [*terms, re.escape(args.find)]

    try:
        patterns = [re.compile(term, re.IGNORECASE) for term in terms]
        readme = (
            args.readme.read_text(encoding="utf-8-sig")
            if args.readme
            else read_catalog(args.snapshot)
        )
        introduction, additions = ("", {}) if scope == "upstream" else read_github_additions(readme)
    except (OSError, UnicodeError, re.error) as error:
        parser.exit(1, f"{error}\n")

    if args.all:
        if scope != "github":
            sys.stdout.write(readme)
        if scope != "upstream" and (additions or scope == "github"):
            if scope == "all":
                sys.stdout.write("\n\n")
            report = [introduction]
            report.extend(f"## {heading}\n\n{body}" for heading, body in additions.items())
            sys.stdout.write("\n\n".join(report) + "\n")
        return

    upstream = game_sections(readme)
    sections = additions if scope == "github" else merge_sections(upstream, additions)
    if not sections and scope != "github":
        parser.exit(1, "No game categories found in the README.\n")

    selected = None
    if args.category:
        names = {name.casefold(): name for name in sections}
        selected = names.get(args.category.strip().casefold())
        if selected is None:
            parser.error(f"Unknown category {args.category!r}. Available: {', '.join(sections)}")
        print(f"## {selected}\n\n{sections[selected]}")

    if patterns:
        found = False
        for heading, body in sections.items():
            if heading == selected:
                continue
            matches = [
                entry.rstrip()
                for entry in ENTRY_BOUNDARY.split(body)
                if LIST_ITEM.match(entry) and any(pattern.search(entry) for pattern in patterns)
            ]
            if matches:
                found = True
                print(f"\n## Keyword matches in {heading}\n")
                print("\n\n".join(matches))
        if not found:
            print("No matching entries.", file=sys.stderr)
    elif selected is None:
        print("\n".join(sections))


if __name__ == "__main__":
    main()
