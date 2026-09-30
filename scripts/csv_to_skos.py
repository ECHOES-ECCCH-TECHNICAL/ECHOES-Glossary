#!/usr/bin/env python3
"""Convert the ECHOES working glossary CSV directly to SKOS/Turtle."""

from __future__ import annotations

import argparse
import csv
import re
import sys
import unicodedata
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path


DEFAULT_BASE_URI = "https://vocabs.ilc4clarin.ilc.cnr.it/vocabularies/echoes/"


@dataclass(frozen=True)
class Concept:
    label_en: str
    definition_en: str
    term_source: str
    definition_source: str
    label_it: str
    definition_it: str
    category: str
    local_name: str


HEADER_ALIASES = {
    "label_en": {"skos:preflabel@en"},
    "definition_en": {"skos:definition@en"},
    "term_source": {"dcterms:sourcepart1"},
    "definition_source": {"dcterms:sourcepart2"},
    # The working CSV currently contains the typo "prefeLabel".
    "label_it": {"skos:preflabel@it", "skos:prefelabel@it"},
    "definition_it": {"skos:definition@it"},
    # Each row contains its broader/top-level category despite the current header name.
    "category": {"skos:hastopconcept", "skos:broader"},
}


def normalize_header(value: str) -> str:
    """Normalize line breaks, spaces, case, and a possible BOM in CSV headers."""
    value = value.lstrip("\ufeff")
    return re.sub(r"\s+", "", value).casefold()


def resolve_columns(fieldnames: list[str]) -> dict[str, str]:
    normalized = {normalize_header(name): name for name in fieldnames}
    resolved: dict[str, str] = {}

    for logical_name, aliases in HEADER_ALIASES.items():
        matches = [normalized[alias] for alias in aliases if alias in normalized]
        if not matches:
            expected = ", ".join(sorted(aliases))
            raise ValueError(
                f"Missing column for {logical_name!r}; expected one of: {expected}"
            )
        if len(matches) > 1:
            raise ValueError(
                f"Ambiguous columns for {logical_name!r}: {', '.join(matches)}"
            )
        resolved[logical_name] = matches[0]

    return resolved


def clean(value: str | None) -> str:
    return (value or "").strip()


def make_local_name(label: str) -> str:
    """Create a stable, prefixed-name-safe identifier from an English label."""
    ascii_label = (
        unicodedata.normalize("NFKD", label)
        .encode("ascii", "ignore")
        .decode("ascii")
    )
    local_name = re.sub(r"\s+", "_", ascii_label.strip())
    local_name = re.sub(r"[^A-Za-z0-9_-]", "", local_name)
    local_name = re.sub(r"_+", "_", local_name).strip("_")

    if not local_name:
        raise ValueError(f"Cannot create a URI identifier from label {label!r}")
    if local_name[0].isdigit() or local_name[0] == "-":
        local_name = f"concept_{local_name}"
    return local_name


def turtle_literal(value: str, language: str | None = None) -> str:
    escaped = (
        value.replace("\\", "\\\\")
        .replace('"', '\\"')
        .replace("\r", "\\r")
        .replace("\n", "\\n")
        .replace("\t", "\\t")
    )
    suffix = f"@{language}" if language else ""
    return f'"{escaped}"{suffix}'


def prefixed(local_name: str) -> str:
    return f"echoes:{local_name}"


def source_literal(term_source: str, definition_source: str) -> str:
    return (
        f"Source of term: {term_source}; "
        f"source of definition: {definition_source}"
    )


def write_resource(
    lines: list[str],
    subject: str,
    rdf_type: str,
    properties: list[tuple[str, list[str]]],
) -> None:
    properties = [(predicate, values) for predicate, values in properties if values]
    lines.append(f"{subject} a {rdf_type} ;")
    for property_index, (predicate, values) in enumerate(properties):
        separator = ",\n        "
        rendered_values = separator.join(values)
        terminator = " ." if property_index == len(properties) - 1 else " ;"
        lines.append(f"    {predicate} {rendered_values}{terminator}")
    lines.append("")


def read_concepts(input_path: Path) -> tuple[list[Concept], list[str]]:
    warnings: list[str] = []
    concepts: list[Concept] = []
    labels_seen: dict[str, int] = {}
    uris_seen: dict[str, str] = {}

    with input_path.open("r", encoding="utf-8-sig", newline="") as stream:
        reader = csv.DictReader(stream)
        if reader.fieldnames is None:
            raise ValueError("The CSV has no header row")
        columns = resolve_columns(reader.fieldnames)

        for row_number, row in enumerate(reader, start=2):
            values = {key: clean(row[column]) for key, column in columns.items()}

            required = ("label_en", "definition_en", "category")
            missing = [name for name in required if not values[name]]
            if missing:
                raise ValueError(
                    f"Row {row_number} is missing required field(s): {', '.join(missing)}"
                )

            label_key = values["label_en"].casefold()
            if label_key in labels_seen:
                raise ValueError(
                    f"Duplicate English label {values['label_en']!r} in rows "
                    f"{labels_seen[label_key]} and {row_number}"
                )
            labels_seen[label_key] = row_number

            local_name = make_local_name(values["label_en"])
            if local_name in uris_seen:
                raise ValueError(
                    f"URI collision: {values['label_en']!r} and "
                    f"{uris_seen[local_name]!r} both map to {local_name!r}"
                )
            uris_seen[local_name] = values["label_en"]

            if not values["label_it"]:
                warnings.append(
                    f"row {row_number} ({values['label_en']}): missing Italian preferred label"
                )
            if not values["definition_it"]:
                warnings.append(
                    f"row {row_number} ({values['label_en']}): missing Italian definition"
                )
            if not values["term_source"]:
                warnings.append(
                    f"row {row_number} ({values['label_en']}): missing term source"
                )
            if not values["definition_source"]:
                warnings.append(
                    f"row {row_number} ({values['label_en']}): missing definition source"
                )

            concepts.append(Concept(local_name=local_name, **values))

    return concepts, warnings


def build_turtle(
    concepts: list[Concept],
    base_uri: str,
    title: str,
    description: str,
    creator: str,
) -> str:
    if not base_uri.endswith(("/", "#")):
        base_uri += "/"

    categories: dict[str, list[Concept]] = defaultdict(list)
    category_names: dict[str, str] = {}
    for concept in concepts:
        category_local_name = make_local_name(concept.category)
        previous = category_names.setdefault(category_local_name, concept.category)
        if previous != concept.category:
            raise ValueError(
                f"Category URI collision: {previous!r} and {concept.category!r}"
            )
        categories[category_local_name].append(concept)

    lines = [
        "@prefix dct: <http://purl.org/dc/terms/> .",
        f"@prefix echoes: <{base_uri}> .",
        "@prefix skos: <http://www.w3.org/2004/02/skos/core#> .",
        "",
    ]

    for concept in sorted(concepts, key=lambda item: item.label_en.casefold()):
        labels = [turtle_literal(concept.label_en, "en")]
        if concept.label_it:
            labels.append(turtle_literal(concept.label_it, "it"))

        definitions = [turtle_literal(concept.definition_en, "en")]
        if concept.definition_it:
            definitions.append(turtle_literal(concept.definition_it, "it"))

        properties: list[tuple[str, list[str]]] = []
        if concept.term_source or concept.definition_source:
            properties.append(
                (
                    "dct:source",
                    [
                        turtle_literal(
                            source_literal(
                                concept.term_source, concept.definition_source
                            )
                        )
                    ],
                )
            )
        properties.extend(
            [
                ("skos:broader", [prefixed(make_local_name(concept.category))]),
                ("skos:definition", definitions),
                ("skos:inScheme", ["echoes:"]),
                ("skos:prefLabel", labels),
            ]
        )
        write_resource(
            lines, prefixed(concept.local_name), "skos:Concept", properties
        )

    for category_local_name in sorted(
        categories, key=lambda key: category_names[key].casefold()
    ):
        category_label = category_names[category_local_name]
        narrower = [
            prefixed(concept.local_name)
            for concept in sorted(
                categories[category_local_name],
                key=lambda item: item.label_en.casefold(),
            )
        ]
        write_resource(
            lines,
            prefixed(category_local_name),
            "skos:Concept",
            [
                ("skos:inScheme", ["echoes:"]),
                ("skos:narrower", narrower),
                ("skos:prefLabel", [turtle_literal(category_label, "en")]),
                ("skos:topConceptOf", ["echoes:"]),
            ],
        )

    top_concepts = [
        prefixed(local_name)
        for local_name in sorted(
            categories, key=lambda key: category_names[key].casefold()
        )
    ]
    write_resource(
        lines,
        "echoes:",
        "skos:ConceptScheme",
        [
            ("dct:creator", [turtle_literal(creator, "en")]),
            ("dct:description", [turtle_literal(description, "en")]),
            ("dct:title", [turtle_literal(title, "en")]),
            ("skos:hasTopConcept", top_concepts),
        ],
    )

    return "\n".join(lines)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Convert the ECHOES glossary CSV directly to SKOS/Turtle."
    )
    parser.add_argument("input_csv", type=Path, help="path to working_version.csv")
    parser.add_argument("output_ttl", type=Path, help="path for the generated Turtle")
    parser.add_argument(
        "--base-uri",
        default=DEFAULT_BASE_URI,
        help=f"concept scheme base URI (default: {DEFAULT_BASE_URI})",
    )
    parser.add_argument("--title", default="ECHOES Glossary")
    parser.add_argument(
        "--description",
        default="Glossary of terms for the ECHOES and related projects.",
    )
    parser.add_argument("--creator", default="Participants in the ECHOES project")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        concepts, warnings = read_concepts(args.input_csv)
        turtle = build_turtle(
            concepts,
            base_uri=args.base_uri,
            title=args.title,
            description=args.description,
            creator=args.creator,
        )
        args.output_ttl.parent.mkdir(parents=True, exist_ok=True)
        args.output_ttl.write_text(turtle, encoding="utf-8")
    except (OSError, ValueError, csv.Error) as error:
        print(f"error: {error}", file=sys.stderr)
        return 1

    print(f"Generated {args.output_ttl} with {len(concepts)} concepts.")
    category_count = len({concept.category for concept in concepts})
    print(f"Top concepts: {category_count}")
    for warning in warnings:
        print(f"warning: {warning}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
