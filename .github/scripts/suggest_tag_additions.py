#!/usr/bin/env python3
"""
Tag Addition Suggester for Clinical Knowledge Base

This script:
1. Processes framework-mods files to identify suggested tag additions
2. Extracts potential new tags and their descriptions
3. Creates a proposed update to the tag-glossary.md file
4. Outputs suggestions in a structured format for review

Usage:
  python suggest_tag_additions.py

Output:
  - tag_suggestions.json - Contains suggested additions to the tag glossary
  - tag_glossary_additions.md - Contains formatted additions to append to the tag glossary
"""

import os
import re
import glob
import json
import yaml

# Configuration
TAG_GLOSSARY_FILE = 'tag-glossary.md'
FRAMEWORK_MODS_DIR = 'framework-mods'

def extract_yaml_front_matter(file_path):
    """Extract YAML front matter from a markdown file."""
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Check if file has YAML front matter (between --- markers)
    match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
    if match:
        try:
            # Parse YAML content
            front_matter = yaml.safe_load(match.group(1))
            return front_matter, content
        except Exception as e:
            print(f"Error parsing YAML in {file_path}: {e}")
    
    return None, content

def extract_tags_from_glossary():
    """Extract all existing tags from the tag glossary file."""
    if not os.path.exists(TAG_GLOSSARY_FILE):
        print(f"Warning: Tag glossary file '{TAG_GLOSSARY_FILE}' not found.")
        return set()
    
    existing_tags = set()
    tag_pattern = re.compile(r'\*\*([a-z0-9-]+)\*\*:')
    hierarchical_tag_pattern = re.compile(r'\*\*([a-z0-9-]+:[a-z0-9-]+)\*\*:')
    
    with open(TAG_GLOSSARY_FILE, 'r') as f:
        content = f.read()
        
        # Extract simple tags
        for match in tag_pattern.finditer(content):
            existing_tags.add(match.group(1))
            
        # Extract hierarchical tags
        for match in hierarchical_tag_pattern.finditer(content):
            existing_tags.add(match.group(1))
    
    return existing_tags

def extract_suggested_tags(file_path):
    """Extract suggested tags from a framework-mods file."""
    suggested_tags = []
    
    # Read file
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Look for patterns like:
    # - Add "tag-name" to Category
    # - Add "tag-with-multiple-words" as a new tag
    # - Expand the category to include "new-tag"
    tag_suggestion_patterns = [
        r'Add ["\']([a-z0-9-]+)["\']', 
        r'add ["\']([a-z0-9-]+)["\']',
        r'include ["\']([a-z0-9-]+)["\']',
        r'#([a-z0-9-]+)'  # Inline hashtags
    ]
    
    all_suggestions = []
    
    for pattern in tag_suggestion_patterns:
        matches = re.finditer(pattern, content)
        for match in matches:
            tag = match.group(1)
            # Find surrounding context for description
            start = max(0, match.start() - 100)
            end = min(len(content), match.end() + 200)
            context = content[start:end]
            
            all_suggestions.append((tag, context))
    
    return all_suggestions

def identify_new_tag_suggestions():
    """Identify new tags suggested in framework-mods files."""
    existing_tags = extract_tags_from_glossary()
    
    # Get all framework-mods files
    mod_files = glob.glob(f'{FRAMEWORK_MODS_DIR}/*.md')
    
    # Track suggestions
    tag_suggestions = {}
    
    for file_path in mod_files:
        try:
            # Extract front matter
            front_matter, _ = extract_yaml_front_matter(file_path)
            
            if not front_matter:
                print(f"Warning: No front matter found in {file_path}, skipping")
                continue
            
            # Get source file from front matter
            source_file = front_matter.get('source_file', '')
            
            # Extract suggested tags
            suggestions = extract_suggested_tags(file_path)
            
            # Filter out existing tags
            new_suggestions = []
            for tag, context in suggestions:
                if tag not in existing_tags and tag.lower() != 'new' and tag.lower() != 'tag':
                    new_suggestions.append((tag, context))
            
            if new_suggestions:
                tag_suggestions[file_path] = new_suggestions
                
        except Exception as e:
            print(f"Error processing {file_path}: {e}")
    
    return tag_suggestions

def generate_tag_glossary_additions(tag_suggestions):
    """Generate a formatted markdown file with suggested tag glossary additions."""
    if not tag_suggestions:
        return "No new tag suggestions found."
    
    content = "# Suggested Tag Glossary Additions\n\n"
    content += "The following tags have been suggested for addition to the tag glossary:\n\n"
    
    all_tags = {}
    
    for file_path, suggestions in tag_suggestions.items():
        for tag, context in suggestions:
            # Format tag with context
            if tag not in all_tags:
                all_tags[tag] = []
            all_tags[tag].append(context)
    
    # Sort tags alphabetically
    for tag in sorted(all_tags.keys()):
        content += f"## {tag}\n\n"
        content += "**Suggested definition:**\n\n"
        content += "_Define this tag based on the context below_\n\n"
        content += "**Context from framework modifications:**\n\n"
        
        for i, context in enumerate(all_tags[tag]):
            content += f"Context {i+1}:\n```\n{context.strip()}\n```\n\n"
    
    # Write to file
    with open('tag_glossary_additions.md', 'w') as f:
        f.write(content)
    
    return content

def main():
    # Identify new tag suggestions
    tag_suggestions = identify_new_tag_suggestions()
    
    # Print summary
    print(f"Found {sum(len(suggestions) for suggestions in tag_suggestions.values())} tag suggestions in {len(tag_suggestions)} files")
    
    # Write suggestions to JSON for programmatic use
    with open('tag_suggestions.json', 'w') as f:
        # Convert tuples to lists for JSON serialization
        serializable_suggestions = {
            file_path: [(tag, context) for tag, context in suggestions]
            for file_path, suggestions in tag_suggestions.items()
        }
        json.dump(serializable_suggestions, f, indent=2)
    
    # Generate formatted tag glossary additions
    generate_tag_glossary_additions(tag_suggestions)
    
    print("Generated tag_suggestions.json and tag_glossary_additions.md")

if __name__ == "__main__":
    main()