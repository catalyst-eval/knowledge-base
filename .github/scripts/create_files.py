#!/usr/bin/env python3
"""
Create new transcript analysis or framework mod file with current date

This script automatically generates new analysis and framework modification files
with the current date in both the filename and YAML front matter.

Usage:
  python create_files.py analysis concept-name
  python create_files.py framework-mod concept-name

Example:
  python create_files.py analysis healing-backlog-neurodivergent-couples
  python create_files.py framework-mod healing-backlog-neurodivergent-couples
"""

import os
import datetime
import argparse
import sys

def create_file(file_type, concept_name):
    # Get current date in different formats
    today = datetime.datetime.now()
    yaml_date = today.strftime("%Y-%m-%d")
    
    # Create filenames - always use YYYY-MM-DD format for consistency
    if file_type == "analysis":
        directory = "transcript-analyses"
        # Ensure consistent YYYY-MM-DD format for all files
        filename = f"{yaml_date}_{concept_name}.md"
        template = f"""---
title: "{concept_name.replace('-', ' ').title()}"
date: {yaml_date}
client_type: 
  - # Add client types
presenting_issue:
  - # Add presenting issues
neurotype:
  - # Add neurotypes
concepts:
  - # Add concepts
metaphors:
  - # Add metaphors
strategies:
  - # Add strategies
related_analyses:
  - # Add related analyses
version: 1
---

# {concept_name.replace('-', ' ').title()}

## Summary of Key Insights

[Add summary here]

## Novel Concepts Identified

### [First Novel Concept]

[Concept description and transcript quotes]

### [Second Novel Concept]

[Concept description and transcript quotes]

## Metaphors and Explanatory Tools Used

### [First Metaphor]

[Metaphor description and usage examples]

### [Second Metaphor]

[Metaphor description and usage examples]

## Client-Centered Applications

### [First Application Area]

[Application description and examples]

### [Second Application Area]

[Application description and examples]

## Practical Strategies Demonstrated

### [First Strategy]

[Strategy description and implementation examples]

### [Second Strategy]

[Strategy description and implementation examples]

## Research Validation and Connections to Existing Literature

[Connections to research literature and evidence-based practices]

## Related Analyses

- [Related Analysis 1](path/to/analysis1.md) - Brief description
- [Related Analysis 2](path/to/analysis2.md) - Brief description
"""
    elif file_type == "framework-mod":
        directory = "framework-mods"
        filename = f"{yaml_date}_{concept_name}_framework-mods.md"
        template = f"""---
title: "Framework Modifications for {concept_name.replace('-', ' ').title()}"
date: {yaml_date}
source_analyses:
  - "{yaml_date}_{concept_name}.md"
concepts:
  - # Add concepts
version: 1
---

# Framework Modifications for {concept_name.replace('-', ' ').title()}

Based on the transcript analysis focused on {concept_name.replace('-', ' ')}, the following additions and modifications to our clinical framework are recommended:

## New Tags to Add

### 1. [new-tag-name]
**Proposed Definition**: [definition]

**Justification**: [justification from transcript]

**Tag Category**: [category]

**Related Tags**: [related tags]

### 2. [new-tag-name]
**Proposed Definition**: [definition]

**Justification**: [justification from transcript]

**Tag Category**: [category]

**Related Tags**: [related tags]

## Expanded Conceptualizations

### 1. [existing-concept]
**Current Definition**: [current definition from tag glossary]

**Proposed Expansion**: [expanded definition]

**Justification**: [justification from transcript]

### 2. [existing-concept]
**Current Definition**: [current definition from tag glossary]

**Proposed Expansion**: [expanded definition]

**Justification**: [justification from transcript]

## Conceptual Relationships to Emphasize

### 1. [relationship-name]
[Description of how concepts relate to each other]

### 2. [relationship-name]
[Description of how concepts relate to each other]

## Conclusion

[Summary of proposed modifications and their significance]
"""
    else:
        print(f"Error: Unknown file type '{file_type}'")
        sys.exit(1)
    
    # Get full project path
    base_path = "/Users/Seabolt/Library/CloudStorage/GoogleDrive-tyler@bridgefamilytherapy.com/My Drive/Bridge Family Therapy/Concept_Dev"
    
    # Create file path
    file_path = os.path.join(base_path, directory, filename)
    
    # Check if file already exists
    if os.path.exists(file_path):
        print(f"Warning: File already exists: {file_path}")
        overwrite = input("Overwrite? (y/n): ").lower()
        if overwrite != 'y':
            print("Aborted.")
            sys.exit(0)
    
    # Ensure directory exists
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    
    # Write file
    with open(file_path, 'w') as f:
        f.write(template)
    
    print(f"Created {file_type} file: {file_path}")
    return file_path

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create new transcript analysis or framework mod file")
    parser.add_argument("file_type", choices=["analysis", "framework-mod"], help="Type of file to create")
    parser.add_argument("concept_name", help="Concept name for the file (used in filename)")
    
    args = parser.parse_args()
    create_file(args.file_type, args.concept_name)