# ECHOES Glossary

## Description of the Glossary

The **ECHOES Glossary** establishes a shared conceptual framework for the ECHOES project and may also support alignment across the wider ECCCH project family. Its purpose is not to replace the many vocabularies, thesauri, ontologies, and other semantic artefacts already used in the Cultural Heritage domain. Instead, it aims to improve terminological clarity across interdisciplinary work.

The glossary functions as a **semantic alignment tool**. It supports consistency in internal collaboration, reduces ambiguity, improves mutual understanding among project partners, and facilitates knowledge transfer beyond the project’s boundaries.

The first published pool contains **73 terms** selected according to their relevance to the project objectives, their recurrence in project documentation and discussions, and their potential ambiguity across disciplinary contexts. Particular attention was given to foundational, methodological, and cross-domain concepts that require harmonisation.

For the first release, terms include definitions and lexicalisations in **English** and **Italian**. Additional languages and terms are planned for future releases. See: `[INSERT LINK TO ROADMAP OR ISSUE TRACKER]`.

The terms were first gathered in a working spreadsheet and collaboratively validated by project members. The spreadsheet was then transformed into a SKOS model and converted into a Turtle `.ttl` file for publication.

## SKOS Modelling

The ECHOES Glossary is modelled using **SKOS — Simple Knowledge Organisation System**. SKOS is a W3C standard for representing knowledge organisation systems such as glossaries, thesauri, taxonomies, classification schemes, and subject heading systems in a machine-readable and interoperable way.

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
├── [working_version]
├── published-versions/
│   ├── [VERSION_1].ttl
│   ├── [VERSION_2].ttl
│   └── ...
├── scripts/
│   └── [csv2SKOS]
│   └── [YAML2RDFTutle]
└── source/
    └── [WORKING_SPREADSHEET]
```

### Main files and folders

| Path                                 | Description                                                                             |
| ------------------------------------ | --------------------------------------------------------------------------------------- |
| `README.md`                          | Documentation for the repository and the ECHOES Glossary.                               |
| `working version.csv`                | The working version of the glossary used exclusively for collaboration.                 |
| `published-versions/`                | Folder of previously published glossary releases.                                      |
| `published-versions/[VERSION].ttl`   | Versioned SKOS/Turtle files corresponding to earlier releases.                          |
| `source/`                            | Contains the working source data, such as the spreadsheet used to prepare the glossary. |
| `scripts/`                           | Contains scripts used to transform the spreadsheet into SKOS/Turtle format.             |

## Contributing to the Glossary

We welcome contributions that improve the ECHOES Glossary. Contributions should follow a clear and structured process to ensure consistency, quality, and traceability.

You can contribute by:

 * Proposing candidate terms;
 * improving or clarifying definitions;
 * correcting unclear or duplicate concepts;
 * adding or revising translations;
 * improving sources or documentation.

> [!NOTE]
> Please note that while the repository is public, this would only allow collaborators to preview the content and consider improvements to definitions, terms, domain concepts, and related content. However, suggestions or proposed changes should still be submitted through **GitHub Issues**, which would remain the required channel for collecting, discussing, and approving proposals. Once approved, changes would be implemented through **pull requests** before being included in the glossary.

### General Change Workflow

Use this workflow for new terms, definition changes, source corrections, and hierarchy changes.

1. **Open an issue**
   Describe the proposed change, the term concerned, the reason for the change, and any relevant sources.

2. **Review and assignment**
   An administrator reviews the issue and assigns it to the appropriate person for review.

3. **Validation**
   The proposal is checked for accuracy, consistency with the glossary, and reliability of sources.

4. **Implementation**
   Once approved, the change is made through a pull request.

5. **Merge**
   An administrator reviews and merges the approved pull request into the current version.

### Translation Workflow

Use this workflow for adding or correcting translations.

1. **Open a translation issue**
   Include the term, the language, the current translation if available, the proposed translation, and a short explanation.

2. **Assign to Language Reviewer**
   The issue is assigned to the Language Reviewer responsible for that language.

3. **Language validation**
   The Language Reviewer checks linguistic accuracy, terminology consistency, and conceptual equivalence.

4. **Implementation**
   After approval, the translation is added or corrected through a pull request.

5. **Merge**
   An administrator merges the validated change into the current version.

### New Term Workflow

Use this workflow when proposing a new glossary term.

1. **Propose the term**
   Open an issue with the term, definition, source, and reason for inclusion.

2. **Conceptual review**
   Administrators check whether the term is relevant and does not duplicate an existing concept.

3. **SKOS placement**
   The term is assigned to the appropriate broader category:

   * Cultural Heritage;
   * Information Science and Data Management;
   * Other topics of interest.

4. **Translation review**
   Required translations are added and checked by the relevant Language Reviewers.

5. **Publication**
   Once validated, the term is added to the current version and included in the next published release.

### Working with Files

* The **working version** contains the latest editable version of the glossary.
* The **published versions** folder contains stable releases and should not be edited directly.
* Small changes can be made using GitHub’s online editor.
* Larger changes should be made locally using a branch and pull request.

### Requesting to Become a Language Reviewer

Contributors who want to review translations for a specific language can open an issue with:

* the language they want to support;
* their relevant experience;
* a short explanation of their interest.

## Licence

`[INSERT LICENCE INFORMATION]`

## Citation

To cite the ECHOES Glossary, please use:

```text
[INSERT RECOMMENDED CITATION]
```

## Credits

The ECHOES Glossary was developed within the ECHOES project through collaborative work by project members.

The glossary is modelled using SKOS, the W3C Simple Knowledge Organisation System.

Publication is supported through the SKOSMOS platform and the SKOSMOS instance maintained by the CNR Institute for Computational Linguistics “A. Zampolli” (CNR-ILC), executive member of CLARIN-IT.
