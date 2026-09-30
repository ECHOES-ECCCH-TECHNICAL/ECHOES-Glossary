# Glossary conversion scripts

This directory contains the scripts used, or previously used, to transform the ECHOES glossary source data into SKOS/RDF Turtle.

## Recommended converter

### `csv_to_skos.py`

`csv_to_skos.py` converts the repository's `working_version.csv` directly to a Turtle (`.ttl`) file. It uses only the Python standard library and does not require an intermediate YAML file.

From the repository root, run:

```bash
python3 scripts/csv_to_skos.py working_version.csv /tmp/echoes_glossary.ttl
```

For a reviewed release, replace the temporary output path with an appropriately versioned file under `Published_versions/`. Do not overwrite an existing published release.

The converter:

- recognizes the current multiline CSV headers, including the existing `skos:prefeLabel@it` typo;
- maps each row to a `skos:Concept`;
- writes English and Italian preferred labels and definitions with language tags;
- combines the two source columns into a textual `dct:source` value;
- links each concept to its top-level category with `skos:broader`;
- generates each category as a SKOS top concept with `skos:narrower` links;
- uses `https://vocabs.ilc4clarin.ilc.cnr.it/vocabularies/echoes/` as the default base URI;
- detects missing required fields, duplicate English labels, and generated-URI collisions;
- reports missing translations and sources as warnings.

The input and output paths are required positional arguments. Scheme metadata and the base URI can be overridden:

```bash
python3 scripts/csv_to_skos.py \
  working_version.csv \
  /tmp/echoes_glossary.ttl \
  --title "ECHOES Glossary v.1.0" \
  --description "Glossary of terms for the ECHOES and related projects." \
  --creator "Participants in the ECHOES project" \
  --base-uri "https://vocabs.ilc4clarin.ilc.cnr.it/vocabularies/echoes/"
```

The script performs structural checks on the CSV but does not perform full SHACL or SKOS quality validation. A release should also be parsed with an RDF parser and reviewed before publication.

## Legacy converters

### `xls2SKOS.py`

This is the first stage of the original conversion process. It reads the active worksheet of a hard-coded Excel (`.xlsx`) file with `openpyxl`, maps seven columns by position, constructs a SKOS-like graph, and writes that graph as YAML.

Its current `__main__` block refers to paths under `/home/ubuntu/`, so it cannot be run against this repository without editing the script. It also does not read `working_version.csv`.

External packages used by this legacy script:

- `openpyxl`
- `PyYAML`

### `YAML2RDFTutle.py`

This is the second stage of the original conversion process. It reads the YAML produced by `xls2SKOS.py` and writes Turtle manually. The filename retains the original `Tutle` spelling.

Its current `__main__` block also uses hard-coded `/home/ubuntu/` paths. In addition, it treats every plain YAML string as an RDF URI. This is incorrect for textual values such as `dcterms:source`, which must be serialized as RDF literals. The script should therefore be considered historical and should not be used for a new release without correction.

External package used by this legacy script:

- `PyYAML`

## Conversion paths

The recommended path is:

```text
working_version.csv -> csv_to_skos.py -> Turtle
```

The historical path was:

```text
Excel workbook -> xls2SKOS.py -> YAML -> YAML2RDFTutle.py -> Turtle
```
