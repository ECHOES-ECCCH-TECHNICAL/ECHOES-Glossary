#!/usr/bin/env python3
"""
Script per convertire il glossario ECHOES da Excel a SKOS usando YAML
"""

import openpyxl
import yaml
from collections import OrderedDict
import re


def sanitize_uri_component(text):
    """Converte il testo in un componente URI valido"""
    if not text:
        return ""
    # Rimuove spazi extra e newline
    text = re.sub(r'\s+', '_', text.strip())
    # Rimuove caratteri non validi per URI
    text = re.sub(r'[^\w\-_]', '', text)
    return text


def create_concept_uri(label, base_uri="http://echoes-project.eu/skos/"):
    """Crea un URI per un concetto basato sulla sua etichetta"""
    return base_uri + sanitize_uri_component(label)


def create_top_concept_uri(label, base_uri="http://echoes-project.eu/skos/topConcept/"):
    """Crea un URI per un top concept"""
    return base_uri + sanitize_uri_component(label)


def represent_ordereddict(dumper, data):
    """Custom representer per OrderedDict in YAML"""
    return dumper.represent_dict(data.items())


def represent_str(dumper, data):
    """Custom representer per stringhe multilinea in YAML"""
    if '\n' in data or len(data) > 80:
        return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='|')
    return dumper.represent_scalar('tag:yaml.org,2002:str', data)


# Registra i custom representers
yaml.add_representer(OrderedDict, represent_ordereddict)
yaml.add_representer(str, represent_str)


def process_excel_to_skos(excel_path, output_yaml_path):
    """
    Processa il file Excel e genera un file YAML in formato SKOS
    """
    # Carica il workbook
    wb = openpyxl.load_workbook(excel_path)
    ws = wb.active
    
    # Struttura dati SKOS
    skos_data = OrderedDict()
    
    # Namespace e prefissi
    skos_data['@context'] = OrderedDict([
        ('skos', 'http://www.w3.org/2004/02/skos/core#'),
        ('dcterms', 'http://purl.org/dc/terms/'),
        ('rdf', 'http://www.w3.org/1999/02/22-rdf-syntax-ns#'),
        ('rdfs', 'http://www.w3.org/2000/01/rdf-schema#')
    ])
    
    # ConceptScheme principale
    concept_scheme_uri = "http://echoes-project.eu/skos/conceptScheme"
    skos_data['@graph'] = []
    
    # Crea il ConceptScheme
    concept_scheme = OrderedDict([
        ('@id', concept_scheme_uri),
        ('@type', 'skos:ConceptScheme'),
        ('dcterms:title', OrderedDict([
            ('@value', 'ECHOES Glossary'),
            ('@language', 'en')
        ])),
        ('dcterms:description', OrderedDict([
            ('@value', 'Glossary of terms for the ECHOES project'),
            ('@language', 'en')
        ])),
        ('skos:hasTopConcept', [])
    ])
    
    # Raccogli tutti i top concepts unici
    top_concepts = set()
    concepts = []
    
    # Salta l'header (riga 1)
    for row_idx, row in enumerate(ws.iter_rows(min_row=2, values_only=True), start=2):
        pref_label_en = row[0]
        definition_en = row[1]
        source_part1 = row[2] if row[2] else ""
        source_part2 = row[3] if row[3] else ""
        pref_label_it = row[4]
        definition_it = row[5]
        top_concept = row[6]
        
        # Salta righe vuote
        if not pref_label_en:
            continue
        
        # Crea URI per il concetto
        concept_uri = create_concept_uri(pref_label_en)
        
        # Crea il concetto SKOS
        concept = OrderedDict([
            ('@id', concept_uri),
            ('@type', 'skos:Concept'),
            ('skos:inScheme', concept_scheme_uri)
        ])
        
        # Aggiungi prefLabel in inglese
        if pref_label_en:
            concept['skos:prefLabel'] = []
            concept['skos:prefLabel'].append(OrderedDict([
                ('@value', pref_label_en.strip()),
                ('@language', 'en')
            ]))
        
        # Aggiungi prefLabel in italiano
        if pref_label_it:
            if 'skos:prefLabel' not in concept:
                concept['skos:prefLabel'] = []
            concept['skos:prefLabel'].append(OrderedDict([
                ('@value', pref_label_it.strip()),
                ('@language', 'it')
            ]))
        
        # Aggiungi definition in inglese
        if definition_en:
            concept['skos:definition'] = []
            concept['skos:definition'].append(OrderedDict([
                ('@value', definition_en.strip()),
                ('@language', 'en')
            ]))
        
        # Aggiungi definition in italiano
        if definition_it:
            if 'skos:definition' not in concept:
                concept['skos:definition'] = []
            concept['skos:definition'].append(OrderedDict([
                ('@value', definition_it.strip()),
                ('@language', 'it')
            ]))
        
        # Crea dcterms:source concatenando le colonne C e D
        if source_part1 or source_part2:
            source_text = f"Source of term: {source_part1.strip()}; source of definition: {source_part2.strip()}"
            concept['dcterms:source'] = source_text
        
        # Aggiungi il top concept
        if top_concept and top_concept.strip():
            top_concept_clean = top_concept.strip()
            top_concepts.add(top_concept_clean)
            top_concept_uri = create_top_concept_uri(top_concept_clean)
            concept['skos:broader'] = top_concept_uri
        
        concepts.append(concept)
    
    # Crea i top concepts come concetti SKOS
    top_concept_objects = []
    for tc in sorted(top_concepts):
        tc_uri = create_top_concept_uri(tc)
        top_concept_obj = OrderedDict([
            ('@id', tc_uri),
            ('@type', 'skos:Concept'),
            ('skos:inScheme', concept_scheme_uri),
            ('skos:topConceptOf', concept_scheme_uri),
            ('skos:prefLabel', OrderedDict([
                ('@value', tc),
                ('@language', 'en')
            ]))
        ])
        top_concept_objects.append(top_concept_obj)
        concept_scheme['skos:hasTopConcept'].append(tc_uri)
    
    # Aggiungi tutto al grafo
    skos_data['@graph'].append(concept_scheme)
    skos_data['@graph'].extend(top_concept_objects)
    skos_data['@graph'].extend(concepts)
    
    # Salva in YAML
    with open(output_yaml_path, 'w', encoding='utf-8') as f:
        yaml.dump(skos_data, f, default_flow_style=False, allow_unicode=True, 
                  sort_keys=False, width=1000, indent=2)
    
    print(f"✓ Conversione completata!")
    print(f"✓ File YAML generato: {output_yaml_path}")
    print(f"✓ Numero di concetti: {len(concepts)}")
    print(f"✓ Numero di top concepts: {len(top_concepts)}")
    print(f"\nTop Concepts identificati:")
    for tc in sorted(top_concepts):
        print(f"  - {tc}")


if __name__ == "__main__":
    excel_file = "/home/ubuntu/upload/ECHOESGlossary-CandidateTermsForWPvalidation(1).xlsx"
    output_file = "/home/ubuntu/echoes_glossary_skos.yaml"
    
    print("Conversione del glossario ECHOES in formato SKOS...")
    print(f"Input: {excel_file}")
    print(f"Output: {output_file}\n")
    
    process_excel_to_skos(excel_file, output_file)
