#!/usr/bin/env python3
"""
Script per convertire il file YAML SKOS in formato RDF/Turtle
"""

import yaml
import json


def yaml_to_turtle(yaml_path, turtle_path):
    """
    Converte un file YAML SKOS in formato RDF/Turtle
    """
    # Carica il file YAML
    with open(yaml_path, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
    
    # Apri il file Turtle per la scrittura
    with open(turtle_path, 'w', encoding='utf-8') as f:
        # Scrivi i prefissi
        f.write("@prefix skos: <http://www.w3.org/2004/02/skos/core#> .\n")
        f.write("@prefix dcterms: <http://purl.org/dc/terms/> .\n")
        f.write("@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .\n")
        f.write("@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .\n\n")
        
        # Processa ogni elemento del grafo
        for item in data['@graph']:
            item_id = item['@id']
            item_type = item['@type']
            
            f.write(f"<{item_id}>\n")
            f.write(f"    a {item_type} ;\n")
            
            # Processa le altre proprietà
            properties = []
            
            for key, value in item.items():
                if key in ['@id', '@type']:
                    continue
                
                # Gestisci diversi tipi di valori
                if isinstance(value, str):
                    # Valore semplice (URI)
                    properties.append(f"    {key} <{value}>")
                
                elif isinstance(value, dict):
                    # Valore con lingua
                    if '@value' in value and '@language' in value:
                        escaped_value = value['@value'].replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n')
                        properties.append(f'    {key} "{escaped_value}"@{value["@language"]}')
                    else:
                        escaped_value = str(value).replace('\\', '\\\\').replace('"', '\\"')
                        properties.append(f'    {key} "{escaped_value}"')
                
                elif isinstance(value, list):
                    # Lista di valori
                    for v in value:
                        if isinstance(v, str):
                            # URI
                            properties.append(f"    {key} <{v}>")
                        elif isinstance(v, dict):
                            # Valore con lingua
                            if '@value' in v and '@language' in v:
                                escaped_value = v['@value'].replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n')
                                properties.append(f'    {key} "{escaped_value}"@{v["@language"]}')
            
            # Scrivi tutte le proprietà
            if properties:
                f.write(" ;\n".join(properties))
                f.write(" .\n\n")
            else:
                # Rimuovi l'ultimo ";\n" e aggiungi ".\n"
                f.seek(f.tell() - 3)
                f.write(" .\n\n")
    
    print(f"✓ Conversione in Turtle completata!")
    print(f"✓ File Turtle generato: {turtle_path}")


if __name__ == "__main__":
    yaml_file = "/home/ubuntu/echoes_glossary_skos.yaml"
    turtle_file = "/home/ubuntu/echoes_glossary_skos.ttl"
    
    print("Conversione del file YAML SKOS in formato RDF/Turtle...")
    print(f"Input: {yaml_file}")
    print(f"Output: {turtle_file}\n")
    
    yaml_to_turtle(yaml_file, turtle_file)
