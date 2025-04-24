# Code Tools for Neurodiversity-Affirming Clinical Knowledge Base

This directory contains scripts and utilities to help manage the clinical knowledge base.

## Script Overview

### `create_files.py`

Automatically creates new transcript analysis or framework modification files with the current date.

**Usage:**
```
python create_files.py analysis concept-name
python create_files.py framework-mod concept-name
```

**Example:**
```
python create_files.py analysis healing-backlog-neurodivergent-couples
python create_files.py framework-mod healing-backlog-neurodivergent-couples
```

This script:
- Automatically uses the current date in both filename and YAML front matter
- Creates files with consistent naming conventions
- Provides template structure for both analysis and framework mod files
- Places files in the correct directories

### `tag-validator-script.py`

Validates tags used in markdown files against the tag glossary and suggests additional tags.

### `index-updater-script.py`

Generates and updates index files that organize transcript analyses by different categories.

### `github-action-workflow.txt`

GitHub Actions workflow configuration for automating validation and index generation.

### `tag-implementation-guide.md`

Documentation on how to implement the tagging structure in the knowledge base.

## Using the File Creation Script

1. Run the script from the terminal with two parameters:
   - File type (`analysis` or `framework-mod`)
   - Concept name (used in the filename)

2. The script will:
   - Generate a file with today's date in the format YYYY-MM-DD
   - Create an appropriate YAML front matter
   - Include the template structure for the file type
   - Place the file in the correct directory

3. After running the script, edit the generated file to add your content

## Best Practices

- Always use the script to create new files to ensure consistent naming and dating
- Fill in all sections of the YAML front matter before committing
- Follow the tag glossary for consistent tagging
- Link related analyses to build connections in the knowledge base