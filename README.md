# ECHOES Glossary

## Description of the Glossary

The **ECHOES Glossary** establishes a shared conceptual framework for the ECHOES project and may also support alignment across the wider ECCCH project family. Its purpose is not to replace the many vocabularies, thesauri, ontologies, and other semantic artefacts already used in the Cultural Heritage domain. Instead, it aims to improve terminological clarity across interdisciplinary work.

The glossary functions as a **semantic alignment tool**. It supports consistency in internal collaboration, reduces ambiguity, improves mutual understanding among project partners, and facilitates knowledge transfer beyond the project’s boundaries.

The first published pool contains **73 terms** selected according to their relevance to the project objectives, their recurrence in project documentation and discussions, and their potential ambiguity across disciplinary contexts. Particular attention was given to foundational, methodological, and cross-domain concepts that require harmonisation.

For the first release, terms include definitions and lexicalisations in **English** and **Italian**. Additional languages and terms are planned for future releases. See: `[INSERT LINK TO ROADMAP OR ISSUE TRACKER]`.

The terms were first gathered in a working spreadsheet and collaboratively validated by project members. The spreadsheet was then transformed into a SKOS model and converted into a Turtle `.ttl` file for publication.

## SKOS Modelling

The ECHOES Glossary is modelled using **SKOS — Simple Knowledge Organization System**. SKOS is a W3C standard for representing knowledge organisation systems such as glossaries, thesauri, taxonomies, classification schemes, and subject heading systems in a machine-readable and interoperable way.

In the ECHOES Glossary model, each row of the working spreadsheet corresponds to one `skos:Concept`.

The core SKOS elements used in the model are:

| Spreadsheet field     | SKOS/RDF property     | Description                                                      |
| --------------------- | --------------------- | ---------------------------------------------------------------- |
| English term          | `skos:prefLabel @en`  | Preferred label of the concept in English                        |
| Term source           | `dcterms:source`      | Source from which the term was identified                        |
| English definition    | `skos:definition @en` | Definition of the concept in English                             |
| Definition source URL | `dcterms:source`      | Source of the English definition                                 |
| Italian term          | `skos:prefLabel @it`  | Preferred label of the concept in Italian                        |
| Italian definition    | `skos:definition @it` | Definition of the concept in Italian                             |
| Type of term          | `skos:broader`        | Broader semantic category used to organise the concept hierarchy |

Source attribution is handled through `dcterms:source`. The source of the term and the source of the definition are kept distinct in the working spreadsheet and then concatenated in the RDF output to ensure traceability and transparency.

Concepts are organised hierarchically using `skos:broader` relations. Instead of creating separate concept schemes for different disciplinary areas, each term is linked to one of three overarching domains:

1. **Cultural Heritage**
2. **Information Science and Data Management**
3. **Other relevant topics**

The SKOS file also includes metadata such as title, authors, and abstract to describe the resource.

## Publication in Skosmos

The ECHOES Glossary is published on the SKOSMOS instance maintained by the **CNR Institute for Computational Linguistics “A. Zampolli” (CNR-ILC)**, the leading member of **CLARIN-IT**.

## Overview of the Repository

This repository contains the source files, published versions, and current version of the ECHOES Glossary.

```text
.
├── README.md
├── current/
│   └── [CURRENT_VERSION_FILE].ttl
├── published-versions/
│   ├── [VERSION_1].ttl
│   ├── [VERSION_2].ttl
│   └── ...
├── scripts/
│   └── [SCRIPT_NAME]
└── source/
    └── [WORKING_SPREADSHEET]
```

### Main files and folders

| Path                                 | Description                                                                             |
| ------------------------------------ | --------------------------------------------------------------------------------------- |
| `README.md`                          | Documentation for the repository and the ECHOES Glossary.                               |
| `current/`                           | Contains the most recent version of the glossary in SKOS/Turtle format.                 |
| `current/[CURRENT_VERSION_FILE].ttl` | The current version of the ECHOES Glossary used for publication.                        |
| `published-versions/`                | Archive of previously published glossary releases.                                      |
| `published-versions/[VERSION].ttl`   | Versioned SKOS/Turtle files corresponding to earlier releases.                          |
| `source/`                            | Contains the working source data, such as the spreadsheet used to prepare the glossary. |
| `scripts/`                           | Contains scripts used to transform the spreadsheet into SKOS/Turtle format.             |

## Contributing to the Glossary

We welcome contributions that improve the ECHOES Glossary. Contributions should follow a clear and structured process to ensure consistency, quality, and traceability.

You can contribute by:

- adding new terms;
- improving or clarifying definitions;
- correcting unclear or duplicate concepts;
- adding or revising translations;
- improving sources or documentation.

All changes must be proposed via **GitHub issues** or **pull requests** and must be approved before being included in the glossary.

## Licence

`[INSERT LICENCE INFORMATION]`

## Citation

To cite the ECHOES Glossary, please use:

```text
[INSERT RECOMMENDED CITATION]
```

## Credits

The ECHOES Glossary was developed within the ECHOES project through collaborative work by project members.

The glossary is modelled using SKOS, the W3C Simple Knowledge Organization System.

Publication is supported through the Skosmos platform and the Skosmos instance maintained by the CNR Institute for Computational Linguistics “A. Zampolli” (CNR-ILC), leading member of CLARIN-IT.
